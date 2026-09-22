# 02 · 用模拟器调通流程，再明确换模型

相同的 ASE 接口可以挂接 Morse、EMT 或 GPAW。接口相同究竟保证了什么，又没有保证什么？

## 这个项目应该自己完成什么

本项目要求**手写推理、量纲检查和可否定的判断**。引用前面计算项目的成熟软件结果；不把讨论题包装成返回 true/false 的脚本。必要算术可以使用 NumPy，电子结构、采样与动力学仍由对应项目的软件完成。

## 输入案例

- [contracts.csv](input/contracts.csv)




统一接口提供 $E(\mathbf R)$ 和 $\mathbf F=-\nabla E$。数值优化、Verlet 和 NEB 可以复用，但换 calculator 会换势能面。

$$\delta E_{obs}=\delta E_{implementation}+\delta E_{numerical}+\delta E_{model}$$

这里只是误差来源的记账框架，不假定三项统计独立，也不意味着可直接加绝对值当置信区间。


## 作业步骤

1. 根据 input/contracts.csv，指定每个练习的手写部分、库部分与对照对象。
2. 列出能在 Morse/EMT 上发现的三种实现错误，以及必须在 GPAW 上检查的两种数值误差。
3. 写一个从模型势迁移到 DFT 的验收顺序，每一步说明检查的可观测量。
4. 解释为什么 EMT 与 PBE 吸附能接近不能自动校准整个势能面。

将回答写入自己的 `runs/02_emulation/answer.md`，保留输入数据、公式、计算出的数值与结论范围。先完成回答，再查看 [参考分析](output/answer.md)。历史回答保存在 output/previous-answer.md；其中事前预测与事后测量不能互换身份。

## 提示

[逐步提示](hints/README.md) 给出三个具体推理环节。完整课程的 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md) 解释哪些工作应交给库。
