"""Run this project; install the repository with pip install -e . first."""
from pathlib import Path
from catalysis.cli import run_project

if __name__ == "__main__":
    run_project(Path(__file__).parent)
