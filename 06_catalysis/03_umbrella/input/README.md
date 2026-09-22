# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [windows.csv](windows.csv)

umbrella 中心为无量纲模型坐标；弹簧常数 K 为 eV。

```csv
center,kappa_eV
-1.5,2.0
-1.25,2.0
```
