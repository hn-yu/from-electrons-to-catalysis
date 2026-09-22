# 输出说明

本项目用有限厚度的周期薄板代表 Cu(111) 表面，围绕 H 吸附能设计收敛实验，判断这个表面模型是否足够可靠。

## 应先读什么、回答什么

先从每个 case 的三个总能独立重算 Eads，再查看各轴变化和结构条件。完成后应能指出当前最大未解决差异及下一轮优先计算，并说明为什么其他轴变化小不能抵消厚度轴失败。

## 用于理解这些结果的背景

真实晶体表面在横向延伸，在垂直方向一侧是固体、另一侧是环境。周期电子结构程序通常在三个方向都重复晶胞，因此采用 slab：保留有限原子层，加入真空把相邻重复薄板分开。层数、真空和底部约束都会影响这个近似。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [baseline/fcc.extxyz](baseline/fcc.extxyz)
- [baseline-sites-0-final_H_position_A.dat](baseline-sites-0-final_H_position_A.dat)
- [baseline-sites.csv](baseline-sites.csv)
- [fixed_layers-0/fcc.extxyz](fixed_layers-0/fcc.extxyz)
- [fixed_layers-1/fcc.extxyz](fixed_layers-1/fcc.extxyz)
- [report.txt](report.txt)
- [size-0/fcc.extxyz](size-0/fcc.extxyz)
- [size-1/fcc.extxyz](size-1/fcc.extxyz)
- [sweep.csv](sweep.csv)
- [vacuum_A-0/fcc.extxyz](vacuum_A-0/fcc.extxyz)
- [vacuum_A-1/fcc.extxyz](vacuum_A-1/fcc.extxyz)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

## 图与软件原始输出

![figure](figure.svg)

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
