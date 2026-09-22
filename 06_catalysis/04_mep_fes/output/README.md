# 输出说明

本项目对同一个二维势分别做最小化和统计积分，直接展示最低能量路径与有限温自由能剖面为何不同。

## 应先读什么、回答什么

把 MEP、解析自由能和数值积分曲线放在同温度同零点下阅读。完成后应能从横向积分推导熵项，并说明 NEB 力收敛与自由能采样收敛为何不能互相替代。

## 用于理解这些结果的背景

将高维体系投影到一个反应坐标 x 时，可以问两个不同问题：固定 x 后最低能构型有多高，或者固定 x 后所有可访问构型的总统计权重有多大。前者是最小化，后者是积分，通常不产生相同函数。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [F-1000K.csv](F-1000K.csv)
- [F-300K.csv](F-300K.csv)
- [F-600K.csv](F-600K.csv)
- [MEP_eV.dat](MEP_eV.dat)
- [finite_temperature-0-F_eV.dat](finite_temperature-0-F_eV.dat)
- [finite_temperature-1-F_eV.dat](finite_temperature-1-F_eV.dat)
- [finite_temperature-2-F_eV.dat](finite_temperature-2-F_eV.dat)
- [finite_temperature.csv](finite_temperature.csv)
- [report.txt](report.txt)
- [x.dat](x.dat)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
