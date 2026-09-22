# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

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
