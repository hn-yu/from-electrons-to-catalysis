"""GET documentation URLs and validate HTML fragment targets; stdlib only.

Run separately from scientific tests: remote documentation can move even when
the repository has not changed. The JSON report retains every source location,
HTTP status, final URL, page title, and missing fragment for review.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import subprocess
import time
from urllib.error import HTTPError, URLError
from urllib.parse import unquote, urldefrag
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
# Repository docs use inline Markdown links, autolinks, or bare URLs. Literal
# parentheses in a destination should be percent-encoded, as should spaces.
URL_PATTERN = re.compile(r"https?://[^\s<>\[\]()\"'`，。；、]+")
ERROR_TITLE = re.compile(r"\b(?:404|page not found|access denied)\b", re.I)


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.anchors = set()
        self.title = ""
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.anchors.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.anchors.add(attrs["name"])
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def collect_links():
    paths = subprocess.check_output(
        ["git", "ls-files", "-z", "--cached", "--others", "--exclude-standard",
         "--", "*.md", "*.rst", "*.html"], cwd=ROOT,
    ).decode().split("\0")
    links = {}
    for name in sorted(set(paths) - {""}):
        path = ROOT / name
        if not path.is_file():
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            for match in URL_PATTERN.finditer(line):
                url = unescape(match[0].rstrip(".,;:"))
                links.setdefault(url, []).append({"file": name, "line": number})
    return links


def check_url(url, timeout, retries):
    base, fragment = urldefrag(url)
    result = {"url": url, "status": None, "final_url": None, "title": "",
              "anchor_ok": None, "ok": False, "error": None}
    for attempt in range(retries + 1):
        try:
            request = Request(base, headers={
                "User-Agent": "Mozilla/5.0 (compatible; CourseDocumentationLinkCheck/1.0)",
            })
            with urlopen(request, timeout=timeout) as response:
                result.update(status=response.status, final_url=response.url)
                content_type = response.headers.get_content_type()
                charset = response.headers.get_content_charset() or "utf-8"
                body = response.read()
            if not 200 <= result["status"] < 300:
                result["error"] = f"Unexpected HTTP {result['status']}"
                return result
            if content_type in ("text/html", "application/xhtml+xml"):
                page = Page()
                page.feed(body.decode(charset, errors="replace"))
                result["title"] = " ".join(page.title.split())
                if ERROR_TITLE.search(result["title"]):
                    result["error"] = "Error page returned with successful HTTP status"
                    return result
                if fragment:
                    anchor = unquote(fragment)
                    result["anchor_ok"] = bool(
                        {anchor, "user-content-" + anchor} & page.anchors
                    )
                    if not result["anchor_ok"]:
                        result["error"] = f"Missing HTML anchor: {anchor}"
                        return result
            elif fragment:
                result["error"] = f"Cannot validate fragment in {content_type}"
                return result
            result.update(ok=True, error=None)
            return result
        except HTTPError as exc:
            result.update(status=exc.code, final_url=exc.url, error=str(exc))
            if exc.code not in (408, 429, 500, 502, 503, 504):
                return result
        except (URLError, TimeoutError, OSError) as exc:
            result["error"] = str(exc)
        if attempt < retries:
            time.sleep(2 ** attempt)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, default=ROOT / "runs/external-links.json")
    parser.add_argument("--timeout", type=float, default=20)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.timeout <= 0 or args.retries < 0 or args.workers < 1:
        parser.error("timeout/workers must be positive and retries nonnegative")
    links = collect_links()
    if not links:
        parser.error("No external documentation links found")
    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check_url, url, args.timeout, args.retries): url for url in links}
        for future in as_completed(futures):
            result = future.result()
            result["locations"] = links[result["url"]]
            results.append(result)
            label = "OK" if result["ok"] else "FAIL"
            detail = result["title"] if result["ok"] else result["error"]
            print(f"{label} {result['status']} {result['url']} — {detail}", flush=True)
            if not result["ok"]:
                for location in result["locations"]:
                    print(f"  {location['file']}:{location['line']}", flush=True)
    failures = sum(not result["ok"] for result in results)
    report = {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
              "unique_urls": len(links), "occurrences": sum(map(len, links.values())),
              "failures": failures, "results": sorted(results, key=lambda r: r["url"])}
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(links)} URLs / {report['occurrences']} references; {failures} failures.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
