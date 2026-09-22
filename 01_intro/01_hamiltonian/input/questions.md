# 案例与问题

给出 H₂ 的核坐标后，哪些项已经是确定的数，哪些项仍是待求的电子算符？这一问题贯穿整个课程。


非相对论、无外场的原子单位 Hamiltonian：

$$\hat H=-\sum_i\frac12\nabla_i^2-\sum_A\frac1{2M_A}\nabla_A^2-\sum_{iA}\frac{Z_A}{r_{iA}}+\sum_{i<j}\frac1{r_{ij}}+\sum_{A<B}\frac{Z_AZ_B}{R_{AB}}.$$

电子索引用 i,j，核索引用 A,B；$M_A$ 以电子质量为单位。输入 H2.xyz 的坐标是 Å，代入原子单位核排斥项前必须换成 bohr。


1. 给五项分别命名、判断符号，并说明两体项为何不能重复计数。
2. 对 0.74 Å 的 H₂ 手算核排斥能；说明总分子能不可能只由这一项决定。
3. 写出 Born–Oppenheimer 固定核电子方程及核在势能面上的运动方程。
4. 从该方程指出 RHF、DFT、经典核、RRHO、TST 分别在何处增加近似。
