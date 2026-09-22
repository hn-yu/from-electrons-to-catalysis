# 01 · 从势能表组装薛定谔算符

本项目求一个粒子在一维外势中的定态能级和波函数。它把连续的薛定谔微分方程变成矩阵本征问题，为后面用基函数表示电子态做准备。

## 背景：为什么需要这一步

量子力学的定态满足 $\hat H\psi=E\psi$：当 Hamiltonian 作用于某些特殊的波函数时，结果只相差一个能量倍数。这样的 E 是允许能级，$|\psi(x)|^2$ 给出位置概率密度。波函数不是粒子的经典轨迹。

我们暂时只考虑一个粒子和给定外势，避开电子间相互作用带来的自洽问题。这样可以专注于三个可独立控制的因素：势函数是什么、边界放在哪里、连续导数如何离散。后面的 RHF 会保留本征求解，但势本身还会依赖电子密度。

程序不能存储每一个连续 x 上的函数值，因此选取有限网格点。差分把邻近点的波函数联系起来，形成三对角 Hamiltonian；边界条件则决定端点之外如何处理。得到一组数字后，仍需用解析解和网格收敛说明它们在逼近什么。

## 开始前需要理解的概念

- **定态与能级**：本征函数有确定能量；不同态按从低到高排列。
- **归一化**：总概率必须为 1，网格求和时要带积分权重 h。
- **Dirichlet 边界**：本例在计算盒两端令波函数为零，相当于额外的无限高墙。
- **节点**：一维波函数内部的变号零点；它能帮助识别不同低能态。
- **束缚态**：波函数在远离势阱处衰减；有限计算盒也会离散本来属于连续谱的态。

## 本次任务：从什么得到什么

分别读取 box、harmonic、finite_well、double_well 四份 x/V 表。用相同差分规则组装动能，再加上不同势能对角项，求最低四个态。方阱和谐振子提供解析能级；有限阱和双阱则练习根据波函数形状解释束缚与隧穿。

## 先用一个小例子走通思路

本例方阱盒长 L=12 bohr，最低解析能量为 $\pi^2/(2L^2)\approx0.03427$ Hartree。有限差分结果应随加密网格接近它。

谐振子 $V=x^2/2$ 的无限域能级为 0.5、1.5、2.5、3.5 Hartree。若加密网格后误差不再下降，可以进一步扩大盒长，检查波函数是否被边界挤压。两种改动处理的是不同误差。

## 实现边界

**手写**二阶导数离散、Hamiltonian 组装、归一化和收敛实验；**直接用 SciPy** 对称三对角本征求解器；**比对解析解**无限深方势阱与谐振子。数值线性代数不是本项目要重新实现的目标。

## 输入与物理模型

- [box.dat](input/box.dat)
- [control.toml](input/control.toml)
- [double_well.dat](input/double_well.dat)
- [finite_well.dat](input/finite_well.dat)
- [harmonic.dat](input/harmonic.dat)

四个 DAT 文件每行是 `x_bohr V_Hartree`，给出均匀内部网格。两端外侧各一个步长处施加 $\psi=0$。

原子单位下 $\hbar=m_e=1$：

```math
-\frac12\psi''(x)+V(x)\psi(x)=E\psi(x),
```

```math
H_{ii}=\frac1{h^2}+V_i,\qquad H_{i,i\pm1}=-\frac1{2h^2}.
```

求解器返回的向量满足 $\sum_i|c_i|^2=1$；连续概率要求 $h\sum_i|\psi_i|^2=1$，所以 $\psi_i=c_i/\sqrt h$。

盒长为 $L=(n+1)h$。无限深阱解析能级 $E_j=j^2\pi^2/(2L^2)$；$V=x^2/2$ 的无限域谐振子 $E_j=j+1/2$。

## 从公式到程序

1. 读 x 与 V，检验网格均匀。DAT 中的势是计算输入，改变文件必须改变 Hamiltonian。
2. 建立对角和次对角，交给 `eigh_tridiagonal`；只求所需低能态。
3. 输出波函数、归一化和解析误差。检查节点数是否随能级顺序增加。
4. 分别固定 L 加密网格、固定 h 扩大 L，解释两种收敛曲线。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 03_electronic_structure/01_schrodinger/run.py --output runs/01_schrodinger
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 将谐振子盒长减半，观察高激发态先受到边界影响。
- 对双阱逐渐提高中央势垒，预测最低两个态的能量劈裂变化；波函数奇偶性比仅看能量更有解释力。
- 有限阱里 E>0 的态仍被计算盒离散化，不能都叫“分子束缚态”。

## 分步提示与资料

[SciPy eigh_tridiagonal](https://docs.scipy.org/doc/scipy/reference/generated/scipy.linalg.eigh_tridiagonal.html)。

## 完成后应能解释什么

先看各体系 energies，再看对应 wavefunctions.csv 中的 x、V 和每列 ψ。解释概率归一化、节点数及边界行为；不要只交四个本征值。完成后应能辨认“网格不够细”和“盒子不够大”的不同现象。

## 与前后项目的关系

需要 [差分](../../02_bringup/03_finite_differences/README.md) 与矩阵本征值的基本概念。下一项 [LCAO](../02_lcao/README.md) 用少量基函数替代大量网格点，并引入非正交性。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
