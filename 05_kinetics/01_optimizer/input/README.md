# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [mb_starts.dat](mb_starts.dat)

每行 x y，二维模型坐标，无量纲。

## [morse_starts.dat](morse_starts.dat)

每行一个初始键长，Å。
