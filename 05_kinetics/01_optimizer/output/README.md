# 输出说明

本项目从给定初始结构寻找附近的低能驻点，学习梯度、步长选择和局部能量盆地怎样共同决定结构优化的结果。

## 应先读什么、回答什么

先读每条优化轨迹的能量和梯度，再比较不同起点的终点。完成后应能区分步长导致的失败、梯度实现错误与正常的多盆地行为，并解释为什么局部优化不保证全局最低能。

## 用于理解这些结果的背景

电子结构计算提供 E(R)，力提供它对原子位置的下降方向。结构优化利用这些信息找到受力接近零的几何。它是一种数值搜索：每一步的位置更新服务于降低能量，并不代表原子经过了真实的物理时间。

[report.txt](report.txt) 给出运行模式、关键量及独立对照。以下文件保留可复算的中间数据：

- [minima-0-SciPy_x.dat](minima-0-SciPy_x.dat)
- [minima-0-own-x.dat](minima-0-own-x.dat)
- [minima-0-start.dat](minima-0-start.dat)
- [minima-1-SciPy_x.dat](minima-1-SciPy_x.dat)
- [minima-1-own-x.dat](minima-1-own-x.dat)
- [minima-1-start.dat](minima-1-start.dat)
- [minima-2-SciPy_x.dat](minima-2-SciPy_x.dat)
- [minima-2-own-x.dat](minima-2-own-x.dat)
- [minima-2-start.dat](minima-2-start.dat)
- [minima-3-SciPy_x.dat](minima-3-SciPy_x.dat)
- [minima-3-own-x.dat](minima-3-own-x.dat)
- [minima-3-start.dat](minima-3-start.dat)
- [minima-4-SciPy_x.dat](minima-4-SciPy_x.dat)
- [minima-4-own-x.dat](minima-4-own-x.dat)
- [minima-4-start.dat](minima-4-start.dat)
- [minima-5-SciPy_x.dat](minima-5-SciPy_x.dat)
- [minima-5-own-x.dat](minima-5-own-x.dat)
- [minima-5-start.dat](minima-5-start.dat)
- [minima.csv](minima.csv)
- [report.txt](report.txt)

CSV 的首行和 DAT 的首部注释给出列名、矩阵约定或单位；解释数值时请同时核对对应输入。

`result.json` 是附属审计记录：逐输入文件 SHA-256、实际源文件 SHA-256、启动版本、软件版本与 Slurm 作业号。若计算时工作树尚未提交，源文件哈希比 HEAD 更精确。

`legacy-result.json`、`legacy-inputs/` 和 previous-analysis.md 保留上一版记录。旧图若位于 legacy-figures/，只对应旧输入，不能当成当前主数据的图。

软件之间的一致性检验算法；它不自动验证模型适用、采样遍历性或 DFT 数值收敛。请按项目正文中的受控实验解释结论。

[返回推导与受控实验](../README.md) · [核对输入](../input/README.md)
