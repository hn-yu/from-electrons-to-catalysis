# 输入说明

本项目从真实水分子坐标和二阶导数矩阵得到正常振动，解释曲率如何判断结构稳定性，以及质量如何把曲率变成频率。

## 这些输入用于哪项任务

读取 H2O_optimized.xyz、masses.dat 和 9×9 hessian.dat，核对原子顺序和 Hartree/bohr² 单位，构造质量加权矩阵并求完整九个模式。将同一矩阵和质量交给 ASE VibrationsData，核对频率；用 stationary_guesses.dat 继续练习最低点与鞍点分类。

## 阅读文件前先核对一个具体例子

单个质量 m 接弹簧 k 时，$\omega=\sqrt{k/m}$；质量变为四倍，频率减半而势能曲线不变。多原子体系的质量加权正是这个关系的矩阵形式。

水有九个笛卡尔自由度，其中六个是整体平移/转动，余下三个是内部振动。真实有限精度矩阵中的六个零模可能略带正负号；把所有负号直接取绝对值，会同时掩盖真正不稳定的模式。

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

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
