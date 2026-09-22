# 输出说明

本项目求一个粒子在一维外势中的定态能级和波函数。它把连续的薛定谔微分方程变成矩阵本征问题，为后面用基函数表示电子态做准备。

## 应先读什么、回答什么

先看各体系 energies，再看对应 wavefunctions.csv 中的 x、V 和每列 ψ。解释概率归一化、节点数及边界行为；不要只交四个本征值。完成后应能辨认“网格不够细”和“盒子不够大”的不同现象。

## 用于理解这些结果的背景

量子力学的定态满足 $\hat H\psi=E\psi$：当 Hamiltonian 作用于某些特殊的波函数时，结果只相差一个能量倍数。这样的 E 是允许能级，$|\psi(x)|^2$ 给出位置概率密度。波函数不是粒子的经典轨迹。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [box-analytic_error_Hartree.dat](box-analytic_error_Hartree.dat)
- [box-energies_Hartree.dat](box-energies_Hartree.dat)
- [box-normalization.dat](box-normalization.dat)
- [box-wavefunctions.csv](box-wavefunctions.csv)
- [double_well-energies_Hartree.dat](double_well-energies_Hartree.dat)
- [double_well-normalization.dat](double_well-normalization.dat)
- [double_well-wavefunctions.csv](double_well-wavefunctions.csv)
- [finite_well-energies_Hartree.dat](finite_well-energies_Hartree.dat)
- [finite_well-normalization.dat](finite_well-normalization.dat)
- [finite_well-wavefunctions.csv](finite_well-wavefunctions.csv)
- [harmonic-analytic_error_Hartree.dat](harmonic-analytic_error_Hartree.dat)
- [harmonic-energies_Hartree.dat](harmonic-energies_Hartree.dat)
- [harmonic-normalization.dat](harmonic-normalization.dat)
- [harmonic-wavefunctions.csv](harmonic-wavefunctions.csv)
- [report.txt](report.txt)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
