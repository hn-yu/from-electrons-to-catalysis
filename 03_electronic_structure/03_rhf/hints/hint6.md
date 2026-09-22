# 提示 6：DIIS 是约束残差最小化

令 $R(c)=\sum_i c_iR_i$，并要求 $\sum_i c_i=1$。最小化 $\|R(c)\|_F^2$，引入一个拉格朗日乘子：

$$
\begin{pmatrix}B&-\mathbf1\\-\mathbf1^T&0\end{pmatrix}
\begin{pmatrix}c\\\lambda\end{pmatrix}
=\begin{pmatrix}0\\-1\end{pmatrix},\qquad
B_{ij}=\langle R_i,R_j\rangle.
$$

$B$ 的维数是历史长度，不是 AO 数。比如保留 6 步历史，只需解一个 7×7 系统，然后用系数组合 Fock 矩阵。

几个容易混淆的点：

- 能量并不作为 B 的元素；B 是残差的内积。
- 所有残差必须在同一表示中；本项目用正交化 AO 表示。
- DIIS 能量不保证逐轮下降。收敛要靠最终条件，而不是每步单调性。
- 奇异矩阵往往意味着历史信息重复。删除旧历史或回退一次普通更新，比把异常吞掉并宣布收敛更合理。

先比较“不开 DIIS”和“开 DIIS”是否达到相同驻点。迭代次数不同是预期行为，能量与电子数不同则需要调查。DIIS 加速算法不能保证选到了物理上正确的 HF 解；下一项目的破缺自旋解正好展示这个区别。
