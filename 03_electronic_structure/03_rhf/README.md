# 从 AO 积分到 restricted Hartree–Fock：自己完成一次 SCF

给定一组核坐标与基函数，为什么电子能量需要“迭代”，而不是对角化一次矩阵？因为一个电子感受到的平均场由其余电子的分布决定，而电子分布又由这个平均场的轨道决定。本项目把这个闭环逐项展开。

完成后，你应能用一张纸解释 `SCF converged` 究竟检查了什么，并能在一个最终能量错误的程序中定位：积分文件、正交化、密度的因子 2、交换项指标、能量计数还是收敛判据出了错。

## 本项目的实现边界

| 自己实现 | 直接用成熟工具 | 独立比对 |
|---|---|---|
| 积分文件重建、对称正交化、D/J/K/F、SCF 能量、迭代及 DIIS | PySCF 生成 AO 积分；NumPy/SciPy 做矩阵运算与对称对角化 | 从同一 XYZ 和基组运行 PySCF RHF；比较积分、电子数、残差及能量 |

`prepare_integrals.py` 只负责生成数据及独立参照。`run.py` 从文本积分开始，SCF 循环在 [rhf_from_integrals](../../src/catalysis/electronic.py)；循环内不调用 PySCF 的 SCF。读过步骤后，建议先自行实现一个不含 DIIS 的版本，再参考给出的解。

## 输入：坐标和积分就是计算对象

[案例清单](input/cases.csv) 指定 H₂、HeH⁺、LiH、H₂O 的坐标、基组、电荷与自旋。以 [H2/molecule.xyz](input/H2/molecule.xyz) 为例：

```text
2

H  0.000000  0.000000  0.000000
H  0.000000  0.000000  0.740000
```

XYZ 坐标单位为 Å。积分文件采用原子单位：能量为 Hartree，电子质量、电荷绝对值和 ℏ 为 1。不要因为积分用原子单位而把 XYZ 的 0.74 误当成 bohr。

| 文件 | 内容 | 怎么读 |
|---|---|---|
| `system.dat` | nAO、电子数、核排斥能 | 一行三个数；前两个为整数 |
| `s.dat` | 重叠矩阵 S | `i j value`，只给下三角，指标从 1 开始 |
| `t.dat`、`v.dat` | 动能、核吸引积分 | 同上；单位 Hartree |
| `eri.dat` | 非零、置换唯一的电子排斥积分 | `i j k l value`，chemists' notation |
| `pyscf_reference.dat` | 独立 PySCF 总能量 | 仅用来验证，不能进入 SCF 更新 |

改坐标或基组后必须重新生成积分。只改 XYZ、继续使用旧积分，会得到另一个 Hamiltonian 的正确答案。[compare.py](compare.py) 会检查这种不一致。

## 第一步：明确体系和能量零点

对固定的核位置，核排斥能为

$$
E_{NN}=\sum_{A<B}\frac{Z_AZ_B}{R_{AB}}.
$$

这里的 $R_{AB}$ 必须用 bohr。它不参与电子密度更新，但必须加进总能量。H₂ 的核距变短时，$E_{NN}$ 增大；电子–核吸引同时变化，不能单独用核排斥判断成键。

先读取 nAO、$N_e$ 与 $E_{NN}$，检查 $N_e$ 为偶数且 $N_e\le2n_{AO}$。本项目为闭壳层 RHF，每个占据空间轨道容纳两个反自旋电子，$n_{occ}=N_e/2$。

## 第二步：重建一电子与二电子积分

$$
S_{\mu\nu}=\langle\chi_\mu|\chi_\nu\rangle,\qquad
h_{\mu\nu}=T_{\mu\nu}+V_{\mu\nu},
$$

$$
(\mu\nu|\lambda\sigma)=\iint
\chi_\mu(\mathbf r_1)\chi_\nu(\mathbf r_1)
\frac{1}{r_{12}}
\chi_\lambda(\mathbf r_2)\chi_\sigma(\mathbf r_2)
\,d\mathbf r_1d\mathbf r_2.
$$

希腊指标遍历 AO；这里使用实基函数。先把数组初始化为零，再读数据。一电子矩阵满足 $S_{\mu\nu}=S_{\nu\mu}$。ERI 有八重置换对称：每对内部交换，以及两对整体交换，都不改变积分。

不要把 $(\mu\nu|\lambda\sigma)$ 与 $(\mu\lambda|\nu\sigma)$ 当成同一个元素，后者正是交换项所需的不同排列。先用四重循环写出正确实现，再决定是否压缩存储。见 [提示 1：指标与对称性](hints/hint1.md)。

## 第三步：在非正交 AO 上建立正交化变换

AO 之间重叠，所以方程是 $FC=SC\varepsilon$，不是普通的 $FC=C\varepsilon$。对角化

$$
S=UsU^T,\qquad X=Us^{-1/2}U^T,
\qquad X^TSX=I.
$$

$s$ 是重叠矩阵的本征值对角矩阵。$s^{-1/2}$ 表示对**本征值**取平方根倒数，不是对 S 的每个矩阵元操作。

计算 $F'=X^TFX$，解普通对称本征问题 $F'C'=C'\varepsilon$，再变回 $C=XC'$。如果最小的 $s_i$ 接近零，基组近线性相关，盲目取倒数会放大噪声。本作业直接拒绝该输入。见 [提示 2](hints/hint2.md)。

## 第四步：初始轨道和密度——先固定因子 2 的约定

先令 $F=h$，得到初始轨道。占据最低的 $n_{occ}$ 列，构造**自旋求和密度**

$$
D_{\mu\nu}=2\sum_{i=1}^{n_{occ}}C_{\mu i}C_{\nu i},
\qquad N_e=\operatorname{Tr}(DS).
$$

在非正交基中，$\operatorname{Tr}(D)$ 通常不等于电子数。参考课程有些项目使用单自旋密度 $P=D/2$，对应 $2J-K$；本项目使用 D，对应 $J-K/2$。两种约定都正确，混用就会错。见 [提示 3](hints/hint3.md)。

## 第五步：从旧密度构造新的 Fock 矩阵

$$
J_{\mu\nu}=\sum_{\lambda\sigma}D_{\lambda\sigma}
(\mu\nu|\lambda\sigma),\qquad
K_{\mu\nu}=\sum_{\lambda\sigma}D_{\lambda\sigma}
(\mu\lambda|\nu\sigma),
$$

$$
F=h+J-\frac12K.
$$

J 是经典库仑平均场；K 来自同自旋电子波函数的反对称性。两者均依赖 D，因此对角化 F 后产生的新 D 一般会改变 F，这就是自洽迭代的来源。

对新的 F 重复正交化、对角化、占据、密度构造。每轮保存 D 和 F，先验证矩阵对称性及电子数，再看最终能量。见 [提示 4](hints/hint4.md)。

## 第六步：计算能量并检查一个自洽状态

$$
E_{elec}=\frac12\sum_{\mu\nu}D_{\mu\nu}(h_{\mu\nu}+F_{\mu\nu}),
\qquad E_{tot}=E_{elec}+E_{NN}.
$$

因子 $1/2$ 防止电子间相互作用重复计数。若刚构造了新 D，应使用由这个新 D 重建的 F 来评价其能量，不能把新 D 与旧 F 随意搭配。

同时观察 $|\Delta E|$、$\|\Delta D\|_F$ 和正交基中的驻点残差

$$
R=X^T(FDS-SDF)X.
$$

能量差很小但 R 很大，意味着“能量变化不大”，不意味着已满足 HF 方程。见 [提示 5](hints/hint5.md)。

## 第七步：先让固定点迭代工作，再加入 DIIS

DIIS 用几步历史 Fock 矩阵的线性组合减小残差：

$$
F^{DIIS}=\sum_i c_iF_i,\qquad \sum_i c_i=1,
\qquad B_{ij}=\operatorname{Tr}(R_i^TR_j).
$$

求带约束的小线性系统，不是“把历史能量平均”。历史残差几乎线性相关时，DIIS 方程会病态；丢弃部分历史或回退到普通更新。见 [提示 6](hints/hint6.md)。

## 运行与逐项核对

从仓库根目录，先安装量子化学依赖 `pip install -e '.[quantum,test]'`。

```bash
# 课程附带积分；仅当你修改坐标、基组或电荷时重新生成：
sbatch scripts/slurm.sh 03_electronic_structure/03_rhf/prepare_integrals.py
# 学生算法从文本积分出发：
sbatch scripts/slurm.sh 03_electronic_structure/03_rhf/run.py
# 独立从 XYZ 运行 PySCF，并检查积分是否仍对应这些坐标：
sbatch scripts/slurm.sh 03_electronic_structure/03_rhf/compare.py
```

[参考输出](output/report.txt) 包含每轮能量、密度变化、残差和矩阵。各体系输出目录还含 `S.dat`、`X.dat`、`D_initial.dat`、`F_final.dat` 与 `iterations.csv`。H₂/STO-3G、0.74 Å 的总能量应约为 −1.117 Hartree；最后以实际表格的精确值核对。

验收顺序：① 积分与 PySCF 相符；② $X^TSX=I$；③ $\operatorname{Tr}(DS)=N_e$；④ 最终残差小；⑤ 同模型总能量误差小于 $10^{-8}$ Hartree。不要逐元素要求 MO 系数同号，本征矢可以整体乘 −1；简并轨道还可在简并子空间内旋转。

## 思考与下一项实验

1. 只把 D 中的 2 去掉，其他式子不改。最早失败的检查是什么？为什么可能仍输出一个看似合理的负能量？
2. 将 H₂ 拉长到 3 Å，RHF 与 PySCF 仍相符。这能证明 RHF 描述解离正确吗？下一项目用 UHF 和自旋污染回答。
3. 在相同几何上扩大基组，最低能量降低是数值改进还是方法改进？应保持哪些条件才能使用变分原则？
4. 同一 SCF 最终能量、不同轨道相位，是程序错误吗？你应比较什么物理量？

资料：[PySCF SCF 文档](https://pyscf.org/user/scf.html)、Szabo & Ostlund 第 3 章。项目拆分方式参考 [ProgrammingProjects 的 SCF 项目](https://github.com/hn-yu/ProgrammingProjects/tree/master/Project%2303)，本项目明确使用自旋求和密度约定。
