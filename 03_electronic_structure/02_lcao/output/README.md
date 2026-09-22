# 输出说明

本项目用两个可以重叠的基函数表示量子态，解释为什么分子轨道计算会得到广义本征方程 Hc=εSc，以及怎样可靠地求解它。

## 应先读什么、回答什么

检查 energies、CᵀSC 和 H C−S C ε，而不只看普通向量长度。完成时应能从基函数展开推导出 S 的位置，并说明为什么相同能级的轨道可以整体变号而不改变物理。

## 用于理解这些结果的背景

上一项目在网格上存储波函数。另一种办法是预先选一些已知形状的函数，再寻找它们的线性组合。量子化学常选择以原子为中心的基函数，称为原子轨道基函数（AO）；形成的整个分子轨道称为 MO。LCAO 即“原子轨道的线性组合”。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [C_transpose_S_C.dat](C_transpose_S_C.dat)
- [SciPy_energies_Hartree.dat](SciPy_energies_Hartree.dat)
- [X.dat](X.dat)
- [coefficients.dat](coefficients.dat)
- [energies_Hartree.dat](energies_Hartree.dat)
- [report.txt](report.txt)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
