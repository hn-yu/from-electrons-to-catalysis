# 05 · 电子能、自由能与储库的检查点

一张吸附电子能表能否直接变成温压相图？你需要补足哪些项，哪些项能够抵消？

## 这个项目应该自己完成什么

本项目要求**手写推理、量纲检查和可否定的判断**。引用前面计算项目的成熟软件结果；不把讨论题包装成返回 true/false 的脚本。必要算术可以使用 NumPy，电子结构、采样与动力学仍由对应项目的软件完成。

## 输入案例

- [thermochemistry.csv](input/thermochemistry.csv)


$$\Delta G(T,p)=\Delta E_{elec}+\Delta ZPE+\Delta H_{thermal}-T\Delta S,$$
$$\mu(T,p)=\mu^\circ(T)+k_BT\ln(p/p^\circ).$$

若 μ° 已经包含气体 ZPE 与热修正，反应式中不能再重复加入这些气体项。


## 作业步骤

1. 读取 input/thermochemistry.csv，解释每一列进入 H、S、G 的位置。
2. 对 600 K、压力增加十倍，手算气体 μ 变化与吸附 ΔG 的变化方向。
3. 写出线性 CO₂ 和非线性 H₂O 应有的内部模式数及旋转对称数。
4. 给出一种电子吸附能负、自由吸附能正的温压条件，并声明使用的近似。

将回答写入自己的 `runs/05_checkpoint/answer.md`，保留输入数据、公式、计算出的数值与结论范围。先完成回答，再查看 [参考分析](output/answer.md)。历史回答保存在 output/previous-answer.md；其中事前预测与事后测量不能互换身份。

## 提示

[逐步提示](hints/README.md) 给出三个具体推理环节。完整课程的 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md) 解释哪些工作应交给库。
