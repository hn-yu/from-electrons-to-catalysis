# 06 · 从力到速率，哪一步证明了什么

优化、Hessian、NEB 和 TST 连在一起后很容易给人“机制已经证明”的错觉。请逐个审查推断。

## 这个项目应该自己完成什么

本项目要求**手写推理、量纲检查和可否定的判断**。引用前面计算项目的成熟软件结果；不把讨论题包装成返回 true/false 的脚本。必要算术可以使用 NumPy，电子结构、采样与动力学仍由对应项目的软件完成。

## 输入案例

- [normal_modes.csv](input/normal_modes.csv)


驻点满足 $\nabla E=0$；局部极小值要求相关自由度的 Hessian 无负曲率；一阶鞍点应有一个相关负曲率方向。

$$k\approx\frac{k_BT}{h}e^{-\Delta G^\ddagger/(k_BT)},\qquad \tau=1/k.$$

NEB 通常给势能势垒 ΔE‡，TST 需要指定状态和分割面的自由能势垒 ΔG‡。


## 作业步骤

1. 查看 input/normal_modes.csv，解释水的六个近零模式为什么会有很小负号。
2. 给“最大力很小所以是极小值”找一个反例，并提出最便宜的检查。
3. 用 600 K、0.1 eV 势垒变化估算速率倍率。
4. 列出把二维 NEB 势垒迁移为真实表面扩散系数所缺的输入。

将回答写入自己的 `runs/06_checkpoint/answer.md`，保留输入数据、公式、计算出的数值与结论范围。先完成回答，再查看 [参考分析](output/answer.md)。历史回答保存在 output/previous-answer.md；其中事前预测与事后测量不能互换身份。

## 提示

[逐步提示](hints/README.md) 给出三个具体推理环节。完整课程的 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md) 解释哪些工作应交给库。
