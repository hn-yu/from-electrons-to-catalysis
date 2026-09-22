# 输入说明

本项目求一个粒子在一维外势中的定态能级和波函数。它把连续的薛定谔微分方程变成矩阵本征问题，为后面用基函数表示电子态做准备。

## 这些输入用于哪项任务

分别读取 box、harmonic、finite_well、double_well 四份 x/V 表。用相同差分规则组装动能，再加上不同势能对角项，求最低四个态。方阱和谐振子提供解析能级；有限阱和双阱则练习根据波函数形状解释束缚与隧穿。

## 阅读文件前先核对一个具体例子

本例方阱盒长 L=12 bohr，最低解析能量为 $\pi^2/(2L^2)\approx0.03427$ Hartree。有限差分结果应随加密网格接近它。

谐振子 $V=x^2/2$ 的无限域能级为 0.5、1.5、2.5、3.5 Hartree。若加密网格后误差不再下降，可以进一步扩大盒长，检查波函数是否被边界挤压。两种改动处理的是不同误差。

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

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
