# 输出说明

本项目用周期 Al 晶体的能量—体积曲线提取平衡晶格常数和体模量，并检验数值设置是否足以支撑这些材料性质。

## 应先读什么、回答什么

先读拟合的 a₀/B，再回到原始 E(V) 点、scenario 设置和 GPAW 日志，确认极小值在采样区间内。完成后应能说明曲线以什么单位、按多少原子归一化，以及下一笔计算应增加 k 点、截断能还是体积点。

## 用于理解这些结果的背景

孤立分子的坐标可以放在开放空间中；晶体则由晶胞沿晶格方向无限重复。周期边界让有限输入代表宏观材料，但电子态也必须满足相应的平移对称性。Bloch 描述把问题分成不同波矢 k 的电子态，实际计算用有限 k 点对布里渊区积分进行近似。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [gpaw-Al-a4.06.txt](gpaw-Al-a4.06.txt)
- [report.txt](report.txt)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

## 图与软件原始输出

![figure](figure.svg)

### native-cif-dft

- [native-cif-dft/eos.csv](native-cif-dft/eos.csv)
- [native-cif-dft/gpaw-a3.8.txt](native-cif-dft/gpaw-a3.8.txt)
- [native-cif-dft/gpaw-a3.9.txt](native-cif-dft/gpaw-a3.9.txt)
- [native-cif-dft/gpaw-a4.1.txt](native-cif-dft/gpaw-a4.1.txt)
- [native-cif-dft/gpaw-a4.2.txt](native-cif-dft/gpaw-a4.2.txt)
- [native-cif-dft/gpaw-a4.3.txt](native-cif-dft/gpaw-a4.3.txt)
- [native-cif-dft/gpaw-a4.txt](native-cif-dft/gpaw-a4.txt)
- [native-cif-dft/report.txt](native-cif-dft/report.txt)

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
