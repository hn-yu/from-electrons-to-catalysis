# 08 · 从一个势垒到催化观测量

吸附能、NEB 势垒、FES 和微观动力学输出放在同一报告里，并不自动组成一致机制。请检查它们之间的连接。

## 这个项目应该自己完成什么

本项目要求**手写推理、量纲检查和可否定的判断**。引用前面计算项目的成熟软件结果；不把讨论题包装成返回 true/false 的脚本。必要算术可以使用 NumPy，电子结构、采样与动力学仍由对应项目的软件完成。

## 输入案例

- [kinetics-report.txt](input/kinetics-report.txt)


$$\dot\theta=S r(\theta,T,p),\qquad \mathrm{TOF}=r_{product},$$
$$n_A=\frac{\partial\ln\mathrm{TOF}}{\partial\ln p_A},\quad E_{app}=-k_B\frac{\partial\ln\mathrm{TOF}}{\partial(1/T)}.$$

这些整体响应包含覆盖度和储库条件。它们一般不等于某一步显式压力幂或局部电子能垒。


## 作业步骤

1. 用 input/kinetics-report.txt 检查覆盖度归一化和各步净通量一致性。
2. 解释稳态与平衡的差别，给出非零 TOF 的持续驱动来源。
3. 在一个步骤更快但 TOF 反而更慢的假设例子中指出必须检查的热力学约束。
4. 针对隐藏慢变量、位点遗漏和厚度未收敛，各写一个后续检验。

将回答写入自己的 `runs/08_checkpoint/answer.md`，保留输入数据、公式、计算出的数值与结论范围。先完成回答，再查看 [参考分析](output/answer.md)。历史回答保存在 output/previous-answer.md；其中事前预测与事后测量不能互换身份。

## 提示

[逐步提示](hints/README.md) 给出三个具体推理环节。完整课程的 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md) 解释哪些工作应交给库。
