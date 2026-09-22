# 输入说明

本项目从 H₂、CO、CO₂ 和 H₂O 的原子坐标出发，将电子能与分子运动的统计贡献组合为指定温压下的气相 Gibbs 自由能。

## 这些输入用于哪项任务

ASE 读取四种 XYZ 和惯性矩，PySCF 提供 RHF/STO-3G 优化所需能量/梯度与 Hessian。你手写平移、转动、振动的 RRHO 分项，生成 H/S/G；把同一组优化几何、频率和标准态交给 ASE IdealGasThermo 独立核对。

## 阅读文件前先核对一个具体例子

水和 CO₂ 都有三个原子、九个笛卡尔自由度。水非线性，减去三个平移和三个转动后剩三个振动；CO₂ 线性，独立转动只有两个，因此有四个振动。不能只按原子数选相同数量的频率。

把水的 σ 从 2 错写为 1，会把转动配分函数扩大两倍，熵增加 $k_B\ln2$，G 降低 $k_BT\ln2$。这个差异即使电子能完全相同也会出现，说明热化学元数据本身是物理输入。

## [CO.xyz](CO.xyz)

分子原子坐标，Å；第一行原子数、第二行注释，之后元素与 x y z。

## [CO2.xyz](CO2.xyz)

分子原子坐标，Å；第一行原子数、第二行注释，之后元素与 x y z。

## [H2.xyz](H2.xyz)

分子原子坐标，Å；第一行原子数、第二行注释，之后元素与 x y z。

## [H2O.xyz](H2O.xyz)

电子结构优化的起始水坐标，Å。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [molecules.csv](molecules.csv)

XYZ、线性/非线性、旋转对称数、电子自旋 S；各字段进入热化学。

```csv
molecule,geometry,symmetry,linear,spin
H2,H2.xyz,2,true,0
CO,CO.xyz,1,true,0
```

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
