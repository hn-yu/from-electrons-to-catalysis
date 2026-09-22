# 02 · 从分子坐标到气相 Gibbs 自由能

本项目从 H₂、CO、CO₂ 和 H₂O 的原子坐标出发，将电子能与分子运动的统计贡献组合为指定温压下的气相 Gibbs 自由能。

## 背景：为什么需要这一步

一个气体分子不仅有电子态，还能整体平移、转动和内部振动。电子结构基态能量没有包含这些自由度在有限温度下的占据，也没有包含气体可访问空间带来的熵。讨论气相反应或气体吸附时，需要把这些贡献放回同一个热力学表达式。

刚性转子—谐振子近似（RRHO）把转动看作固定几何的刚体运动，把平衡结构附近的振动看作独立谐振子，再假定这些运动近似可分离。相应配分函数相乘，logq 和自由能贡献相加。理想气体近似则忽略分子之间的相互作用。

频率必须围绕适当的平衡结构得到，整体平移和整体转动不能再当作内部振动重复计数。Gibbs 自由能 G=H−TS 适合指定温度和压力的比较；与上一项的 F 相比，H 中还包含理想气体 pV 项。

## 开始前需要理解的概念

- **ZPE**：振动零点能，即谐振子最低能级的能量；温度趋零时仍存在。
- **惯性矩 I**：质量相对转轴的分布，决定转动能级尺度。
- **旋转对称数 σ**：扣除因相同原子不可区分而重复计入的转动构型。
- **内部振动数**：线性分子 3N−5，非线性分子 3N−6；余下自由度是刚体运动。
- **标准压力**：定义气相熵和化学势的参考；与计算程序的压力单位需同时说明。

## 本次任务：从什么得到什么

ASE 读取四种 XYZ 和惯性矩，PySCF 提供 RHF/STO-3G 优化所需能量/梯度与 Hessian。你手写平移、转动、振动的 RRHO 分项，生成 H/S/G；把同一组优化几何、频率和标准态交给 ASE IdealGasThermo 独立核对。

## 先用一个小例子走通思路

水和 CO₂ 都有三个原子、九个笛卡尔自由度。水非线性，减去三个平移和三个转动后剩三个振动；CO₂ 线性，独立转动只有两个，因此有四个振动。不能只按原子数选相同数量的频率。

把水的 σ 从 2 错写为 1，会把转动配分函数扩大两倍，熵增加 $k_B\ln2$，G 降低 $k_BT\ln2$。这个差异即使电子能完全相同也会出现，说明热化学元数据本身是物理输入。

## 实现边界

**直接用 PySCF** 优化所需梯度与解析 Hessian，ASE 处理结构和惯性矩；**手写 RRHO** 各配分函数与 H/S/G；再用 **ASE IdealGasThermo 独立比对**。不手写分子积分和电子结构 Hessian。

## 输入与物理模型

- [CO.xyz](input/CO.xyz)
- [CO2.xyz](input/CO2.xyz)
- [H2.xyz](input/H2.xyz)
- [H2O.xyz](input/H2O.xyz)
- [control.toml](input/control.toml)
- [molecules.csv](input/molecules.csv)

H₂、CO、CO₂、H₂O 坐标来自 XYZ；`molecules.csv` 明确线性分类、旋转对称数和电子自旋。计算先用 RHF/STO-3G 优化几何，再取内部振动频率；这组数据是方法练习而非高精度实验热化学。

```math
q_{\rm trans}=\left(\frac{2\pi mk_BT}{h^2}\right)^{3/2}\frac{k_BT}{p},
```

```math
q_{\rm rot}^{\rm linear}=\frac{8\pi^2Ik_BT}{\sigma h^2},\quad q_{\rm rot}^{\rm nonlinear}=\frac{\sqrt\pi}{\sigma}\prod_{a=1}^3\left(\frac{8\pi^2I_ak_BT}{h^2}\right)^{1/2}.
```

$\sigma$ 防止将不可区分的转动构型重复计数。H₂ 为 2、CO 为 1、CO₂ 为 2、水为 2。

```math
H=E_{\rm elec}+U_{\rm vib}+(5/2+d_{\rm rot})k_BT,\quad G=H-TS,
```

线性分子 $d_{\rm rot}=1$，非线性为 $3/2$；$5/2$ 包括平移内能 $3/2$ 与理想气体的 pV 项 1。振动项含 ZPE。

## 从公式到程序

1. 从 XYZ 读几何，检查能量和梯度的单位：PySCF 梯度为 Hartree/bohr，优化坐标为 Å。
2. 优化后分析 Hessian，去掉刚体自由度；线性分子有 3N−5 个内部振动，非线性有 3N−6 个。
3. 计算质量、惯性矩、各配分函数，输出 electronic/ZPE/thermal H/S/G 分项。
4. 将相同几何、频率、温度、压力和对称数传给 ASE；输出 G_error，并保存优化后的 XYZ。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 04_thermodynamics/02_molecular_thermochemistry/run.py --output runs/02_molecular_thermochemistry
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 把水的对称数从 2 改为 1，预测 ΔG=−kBT ln2；不要将它当能量计算误差。
- 将压力提高 10 倍，G 增加 kBT ln10，H 在此理想模型下不变。
- 故意把很小的刚体频率当振动加入，观察熵异常增大；“频率都是实数”仍不足以证明模式分类正确。

## 分步提示与资料

[ASE thermochemistry](https://ase-lib.org/ase/thermochemistry/thermochemistry.html)；[PySCF Hessian](https://pyscf.org/user/grad.html)。

## 完成后应能解释什么

先核对优化后 XYZ 和内部模式数，再读 electronic/ZPE/thermal H/S/G 分项，最后看与 ASE 的差值。完成后应能解释每项来自哪种运动、哪些近似允许它们相加，以及为何 RHF/STO-3G 的软件一致性不等于实验热化学精度。

## 与前后项目的关系

前置是 [配分函数](../01_partition/README.md)。频率的矩阵来源可先读 [Hessian](../../05_kinetics/03_hessian/README.md) 的背景；下一项 [化学势](../03_chemical_potential/README.md) 使用气体 G 来描述储库。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
