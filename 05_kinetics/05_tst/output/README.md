# 输出说明

本项目用过渡态理论把自由能势垒转换为单步速率和等待时间，量化能垒误差对动力学预测的影响。

## 应先读什么、回答什么

读 barrier-timescale.csv 时同时看势垒单位、温度和速率标签，检查 ln k 的斜率与时间倒数。完成后应能把一个能量误差翻译成速率倍率，并列出从电子 NEB 势垒到自由能 TST 势垒需要的补充。

## 用于理解这些结果的背景

反应热力学有利并不意味着反应很快。体系可能长时间留在反应物盆地中，只有少量热涨落能到达连接产物的分割面。过渡态理论（TST）用反应物与分割面附近的相对统计权重，乘以通过该面的频率尺度，估计净向外的反应事件。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [barrier-timescale.csv](barrier-timescale.csv)
- [report.txt](report.txt)
- [scan.csv](scan.csv)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
