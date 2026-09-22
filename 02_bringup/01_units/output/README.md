# 输出说明

本项目把电子结构、光谱和动力学中常见的单位放到同一个可检查的换算链上，并用热能尺度判断某个能量误差是否会影响结论。

## 应先读什么、回答什么

先读 conversions.csv 中 own 与 ASE 两列，区分常数末位差和明显量纲错误；再读 thermal_scales.csv。完成时应能不用程序说出 300/600 K 的 kBT 量级，并从允许的速率倍率反推出能量容限。

## 用于理解这些结果的背景

电子结构软件常报告 Hartree，表面科学常用 eV，热化学表常用 kJ/mol，振动光谱则用 cm⁻¹。这些数值不能只换标签：有的按单粒子计，有的按一摩尔计，波数还需要通过光子能量关系才转换为能量。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [conversions.csv](conversions.csv)
- [report.txt](report.txt)
- [thermal_scales.csv](thermal_scales.csv)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
