# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

## [H2O.xyz](H2O.xyz)

电子结构优化的起始水坐标，Å。

## [H2O_optimized.xyz](H2O_optimized.xyz)

RHF/STO-3G 优化后的水坐标，Å，与 hessian.dat 对应。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [hessian.dat](hessian.dat)

3N×3N 笛卡尔二阶导数，Hartree/bohr²；顺序 atom1-x,y,z,atom2-x,y,z…

## [masses.dat](masses.dat)

每个原子一个质量，u；按 XYZ 顺序，质量加权时每个质量重复三个方向。

## [stationary_guesses.dat](stationary_guesses.dat)

二维最小值/鞍点初猜，模型坐标。
