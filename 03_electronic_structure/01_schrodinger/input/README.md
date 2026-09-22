# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

## [box.dat](box.dat)

均匀内部网格 x_bohr V_Hartree；Dirichlet 墙在首尾外侧一个网格步长。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [double_well.dat](double_well.dat)

均匀内部网格 x_bohr V_Hartree，双阱势。

## [finite_well.dat](finite_well.dat)

均匀内部网格 x_bohr V_Hartree，有限阱势。

## [harmonic.dat](harmonic.dat)

均匀内部网格 x_bohr V_Hartree，谐振子势。
