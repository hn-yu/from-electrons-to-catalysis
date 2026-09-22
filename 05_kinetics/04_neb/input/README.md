# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [endpoints.dat](endpoints.dat)

两行 x y，二维 NEB 起止初猜；先分别优化。

## [fcc.extxyz](fcc.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [hcp.extxyz](hcp.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。
