# 输出说明

本项目把状态与过渡态自由能转换成守恒、满足详细平衡的可逆反应网络，为后续覆盖度和催化速率计算建立一致输入。

## 应先读什么、回答什么

先读各步能垒、详细平衡残差和计量矩阵，再比较 Cantera 的稳态覆盖度与净通量。完成后应能从一条反应式写出对应矩阵列，并解释活度式与浓度式的单位换算为何影响 YAML 前因子。

## 用于理解这些结果的背景

实际催化反应通常经过吸附、表面转化和脱附等多个步骤。每一步的正向与逆向过程共享相同的过渡态，因此速率常数之比受到两端自由能差的约束。若任意指定两个方向的速率，可能得到在平衡条件下仍自行循环的矛盾模型。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [Cantera-coverages.dat](Cantera-coverages.dat)
- [Cantera-elementary_rates_s^-1.dat](Cantera-elementary_rates_s^-1.dat)
- [deltaG_eV.dat](deltaG_eV.dat)
- [detailed_balance_log_residual.dat](detailed_balance_log_residual.dat)
- [forward_s^-1.dat](forward_s^-1.dat)
- [own_steady_state-coverages.dat](own_steady_state-coverages.dat)
- [own_steady_state-elementary_rates_s^-1.dat](own_steady_state-elementary_rates_s^-1.dat)
- [own_steady_state-forward_s^-1.dat](own_steady_state-forward_s^-1.dat)
- [own_steady_state-reverse_s^-1.dat](own_steady_state-reverse_s^-1.dat)
- [report.txt](report.txt)
- [reverse_s^-1.dat](reverse_s^-1.dat)
- [stoichiometry.csv](stoichiometry.csv)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
