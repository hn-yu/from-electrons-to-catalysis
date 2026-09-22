# 07 · 电子结构结果的四层核对

现在给你一个收敛的 RHF 能量和一条拉伸曲线。你能区分输入错误、数值错误和方法失效吗？

## 这个项目应该自己完成什么

本项目要求**手写推理、量纲检查和可否定的判断**。引用前面计算项目的成熟软件结果；不把讨论题包装成返回 true/false 的脚本。必要算术可以使用 NumPy，电子结构、采样与动力学仍由对应项目的软件完成。

## 输入案例

- [scf-report.txt](input/scf-report.txt)


RHF 的关键不变量是

$$\mathrm{Tr}(DS)=N_e,\quad X^TSX=I,\quad FDS-SDF\rightarrow0,$$
$$E_{tot}=\tfrac12\mathrm{Tr}[D(H+F)]+E_{NN}.$$

这些关系检验算法的一致性；UHF 的 $\langle S^2\rangle$、有限基组 FCI 与周期收敛趋势检验的是其他层次。


## 作业步骤

1. 用 input/scf-report.txt 的 H₂O 案例核对电子数、核排斥和最终总能。
2. 解释若能量看似收敛但 Tr(DS)=5 而不是 10，最可能混用了哪种密度约定。
3. 给“RHF 收敛，所以 H₂ 解离正确”的结论写反例。
4. 为周期晶格常数建立 k 点与截断的分开收敛计划，说明分子 SCF 测试不能覆盖什么。

将回答写入自己的 `runs/07_checkpoint/answer.md`，保留输入数据、公式、计算出的数值与结论范围。先完成回答，再查看 [参考分析](output/answer.md)。历史回答保存在 output/previous-answer.md；其中事前预测与事后测量不能互换身份。

## 提示

[逐步提示](hints/README.md) 给出三个具体推理环节。完整课程的 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md) 解释哪些工作应交给库。
