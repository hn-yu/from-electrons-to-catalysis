# 输出说明

本项目从一张能级和简并度表计算平衡占据、内能、熵和自由能，理解电子能怎样进入有限温度的统计描述。

## 应先读什么、回答什么

先读占据随温度变化，再核对 U/F/S 以及谐振子截断误差。完成后应能从“一个态有多贵、同样能量有多少态”解释曲线，并说明为什么自由能零点能平移而平衡概率不变。

## 用于理解这些结果的背景

上一章计算的是指定几何下的电子态能量。温度非零时，体系可以访问多个状态；实验观测常对应这些状态的统计平均，而不是只取最低能态。与热浴交换能量、保持粒子数和体积固定的平衡描述称为正则系综。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [oscillator.csv](oscillator.csv)
- [report.txt](report.txt)
- [two_level-0-populations.dat](two_level-0-populations.dat)
- [two_level-1-populations.dat](two_level-1-populations.dat)
- [two_level-2-populations.dat](two_level-2-populations.dat)
- [two_level-3-populations.dat](two_level-3-populations.dat)
- [two_level-4-populations.dat](two_level-4-populations.dat)
- [two_level-5-populations.dat](two_level-5-populations.dat)
- [two_level-6-populations.dat](two_level-6-populations.dat)
- [two_level.csv](two_level.csv)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

## 图与软件原始输出

![figure](figure.svg)

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
