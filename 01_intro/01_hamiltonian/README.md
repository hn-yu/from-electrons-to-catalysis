# 01 · 从坐标写出电子—核 Hamiltonian

给出 H₂ 的核坐标后，哪些项已经是确定的数，哪些项仍是待求的电子算符？这一问题贯穿整个课程。

## 这个项目应该自己完成什么

本项目要求**手写推理、量纲检查和可否定的判断**。引用前面计算项目的成熟软件结果；不把讨论题包装成返回 true/false 的脚本。必要算术可以使用 NumPy，电子结构、采样与动力学仍由对应项目的软件完成。

## 输入案例

- [H2.xyz](input/H2.xyz)


非相对论、无外场的原子单位 Hamiltonian：

$$\hat H=-\sum_i\frac12\nabla_i^2-\sum_A\frac1{2M_A}\nabla_A^2-\sum_{iA}\frac{Z_A}{r_{iA}}+\sum_{i<j}\frac1{r_{ij}}+\sum_{A<B}\frac{Z_AZ_B}{R_{AB}}.$$

电子索引用 i,j，核索引用 A,B；$M_A$ 以电子质量为单位。输入 H2.xyz 的坐标是 Å，代入原子单位核排斥项前必须换成 bohr。


## 作业步骤

1. 给五项分别命名、判断符号，并说明两体项为何不能重复计数。
2. 对 0.74 Å 的 H₂ 手算核排斥能；说明总分子能不可能只由这一项决定。
3. 写出 Born–Oppenheimer 固定核电子方程及核在势能面上的运动方程。
4. 从该方程指出 RHF、DFT、经典核、RRHO、TST 分别在何处增加近似。

将回答写入自己的 `runs/01_hamiltonian/answer.md`，保留输入数据、公式、计算出的数值与结论范围。先完成回答，再查看 [参考分析](output/answer.md)。历史回答保存在 output/previous-answer.md；其中事前预测与事后测量不能互换身份。

## 提示

[逐步提示](hints/README.md) 给出三个具体推理环节。完整课程的 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md) 解释哪些工作应交给库。
