# 输出说明

本项目从 H₂、CO、CO₂ 和 H₂O 的原子坐标出发，将电子能与分子运动的统计贡献组合为指定温压下的气相 Gibbs 自由能。

## 应先读什么、回答什么

先核对优化后 XYZ 和内部模式数，再读 electronic/ZPE/thermal H/S/G 分项，最后看与 ASE 的差值。完成后应能解释每项来自哪种运动、哪些近似允许它们相加，以及为何 RHF/STO-3G 的软件一致性不等于实验热化学精度。

## 用于理解这些结果的背景

一个气体分子不仅有电子态，还能整体平移、转动和内部振动。电子结构基态能量没有包含这些自由度在有限温度下的占据，也没有包含气体可访问空间带来的熵。讨论气相反应或气体吸附时，需要把这些贡献放回同一个热力学表达式。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [CO-optimized.xyz](CO-optimized.xyz)
- [CO2-optimized.xyz](CO2-optimized.xyz)
- [H2-optimized.xyz](H2-optimized.xyz)
- [H2O-optimized.xyz](H2O-optimized.xyz)
- [report.txt](report.txt)
- [results-0-frequencies_cm^-1.dat](results-0-frequencies_cm^-1.dat)
- [results-0-positions_A.csv](results-0-positions_A.csv)
- [results-1-frequencies_cm^-1.dat](results-1-frequencies_cm^-1.dat)
- [results-1-positions_A.csv](results-1-positions_A.csv)
- [results-2-frequencies_cm^-1.dat](results-2-frequencies_cm^-1.dat)
- [results-2-positions_A.csv](results-2-positions_A.csv)
- [results-3-frequencies_cm^-1.dat](results-3-frequencies_cm^-1.dat)
- [results-3-positions_A.csv](results-3-positions_A.csv)
- [results.csv](results.csv)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
