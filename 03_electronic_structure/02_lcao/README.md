# 02 · 非正交基组中的本征问题

本项目用两个可以重叠的基函数表示量子态，解释为什么分子轨道计算会得到广义本征方程 Hc=εSc，以及怎样可靠地求解它。

## 背景：为什么需要这一步

上一项目在网格上存储波函数。另一种办法是预先选一些已知形状的函数，再寻找它们的线性组合。量子化学常选择以原子为中心的基函数，称为原子轨道基函数（AO）；形成的整个分子轨道称为 MO。LCAO 即“原子轨道的线性组合”。

基函数是表示空间，系数才是本次求解的未知量。相邻原子上的基函数会在空间重叠，因此它们不一定像直角坐标轴那样互相正交。系数向量的普通长度就不再等于波函数的概率范数，重叠矩阵 S 负责记录这种几何关系。

把 $\psi=\sum_\mu c_\mu\chi_\mu$ 代入方程，再分别投影到每个基函数，左边得到 Hamiltonian 矩阵，右边出现 S。因此 S 不是额外的相互作用，也不是需要随便消掉的误差；它来自你选择的表示方法。

## 开始前需要理解的概念

- **基函数 χ 与系数 c**：χ 是已知函数，c 决定当前轨道如何组合它们。
- **矩阵元 Hμν**：Hamiltonian 在两个基函数之间的积分，单位为能量。
- **重叠 Sμν**：两个基函数的内积，无量纲；正定性保证非零系数组合具有正范数。
- **正交化 X**：改变基的表示，使内积变成单位矩阵，再使用普通对称本征求解器。
- **残差**：把求出的 c、ε 代回原方程后的差，是对求解结果的直接检查。

## 本次任务：从什么得到什么

读取给定的两个 2×2 矩阵。这是为代数练习设计的模型，不是声称来自某个真实分子的积分。你先手写 S 的谱正交化，在变换后的 H′ 中求解，再把系数变回原基；最后独立调用 SciPy 的广义本征求解器。

## 先用一个小例子走通思路

输入为 $H_{11}=H_{22}=-1$、$H_{12}=-0.3$ Hartree，$S_{11}=S_{22}=1$、$S_{12}=0.2$。对称组合的能量是 $(-1-0.3)/(1+0.2)\approx-1.08333$；反对称组合为 $(-1+0.3)/(1-0.2)=-0.875$ Hartree。

分母是重叠造成的归一化。如果把 S 当作 I，就会得到 −1.3 和 −0.7。两组都可能由某个矩阵对角化程序正常输出，但它们求解的是不同的问题。

## 实现边界

**手写后比对**对称正交化、变换与残差；NumPy 提供普通对称本征求解器；SciPy `eigh(H,S)` 走独立广义本征路径。不要手写通用本征算法。

## 输入与物理模型

- [control.toml](input/control.toml)
- [hamiltonian.dat](input/hamiltonian.dat)
- [overlap.dat](input/overlap.dat)

`hamiltonian.dat` 为 Hartree，`overlap.dat` 无量纲，均是完整方阵。基函数重叠 $S_{\mu\nu}=\langle\chi_\mu|\chi_\nu\rangle$。

```math
Hc=\varepsilon Sc,\quad c^TSc=1.
```

对称正交化为

```math
S=UsU^T,\quad X=Us^{-1/2}U^T,\quad X^TSX=I,
```

```math
H'=X^THX,\quad H'c'=\varepsilon c',\quad c=Xc'.
```

Rayleigh 商是 $c^THc/(c^TSc)$，不是 $c^THc/(c^Tc)$。若 S 含极小本征值，$s^{-1/2}$ 会放大误差；这对应近线性相关的基函数。

## 从公式到程序

1. 检查 H、S 对称，S 正定，输出其最小本征值。
2. 构造 X 并输出 XᵀSX；在正交基中对角化 H′ 后变换回原 AO 基。
3. 同时运行 SciPy 的广义求解器，比较能量及 `H C - S C diag(e)` 残差。
4. 保存 X、C 和 CᵀSC 三个矩阵，使下一项目可以逐项核对。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/02_lcao/run.py --output runs/02_lcao
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 把 S 错当单位矩阵，定量比较能量变化；矩阵形状不报错不表示物理正确。
- 逐渐使两个基函数接近线性相关，观察 X 的元素和残差。
- 对基函数做可逆线性组合，同时变换 H 和 S。能级应保持不变，系数会变。

## 分步提示与资料

[SciPy 广义对称本征问题](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh.html)。

## 完成后应能解释什么

检查 energies、CᵀSC 和 H C−S C ε，而不只看普通向量长度。完成时应能从基函数展开推导出 S 的位置，并说明为什么相同能级的轨道可以整体变号而不改变物理。

## 与前后项目的关系

前置是 [网格薛定谔方程](../01_schrodinger/README.md) 的本征问题。下一项 [RHF](../03_rhf/README.md) 将复用 X 与 S，但 Hamiltonian 的有效单电子部分会随密度迭代。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
