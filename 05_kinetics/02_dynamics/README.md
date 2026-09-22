# 02 · 用能量误差检验 Velocity Verlet

本项目手写 Velocity Verlet 积分器，从坐标、质量和动量生成经典轨迹，并用守恒量与 ASE 的独立积分器检验时间推进。

## 背景：为什么需要这一步

结构优化不断降低势能；无外界作用的经典动力学则让势能和动能互相转化，总能量守恒。给定势能面后，Newton 方程通过质量把力变成加速度，因此动力学输入还必须包含初始动量或速度。

连续时间方程需要用有限步长离散。Velocity Verlet 将位置更新与两端力的速度更新配合，具有良好的时间可逆性和长期能量性质。有限步长下通常仍有能量误差；有界振荡与不断累积的漂移需要区别对待。

真实轨迹与平衡采样也不是同一件事。这里检验无温控积分器和短轨迹，不据此证明体系已遍历所有状态，更不把加入温控器当成掩盖积分错误的方法。

## 开始前需要理解的概念

- **相空间初态**：位置和动量共同决定经典运动，只有 XYZ 坐标还不够。
- **动能 K**：与质量、速度有关，与势能 U 一起构成总能 E。
- **时间步长 Δt**：需解析最快相关运动，单位必须与力和质量配套。
- **稳定性与精度**：轨迹不发散只是最低要求，能量和相位误差还需检查。
- **NVE 图像**：粒子数、体积、总能量固定的孤立经典体系；本练习无恒温器。

## 本次任务：从什么得到什么

第一部分扫描约化单位谐振子的时间步长，观察稳定边界。第二部分读取 cluster.extxyz 的位置、质量、动量，自己推进 LJ 双粒子，再让 ASE VelocityVerlet 使用相同力接口和初态，逐帧比较轨迹。Ar 是标签，实际使用输入规定的教学质量和 LJ 参数。

## 先用一个小例子走通思路

约化谐振子取 m=k=1，所以 ω=1。Velocity Verlet 的线性稳定条件为 $\omega\Delta t\lt 2$；把步长调到超过 2 后，失稳来自离散推进，而不是弹簧突然变成了不稳定物理模型。

真实单位的双粒子案例另有时间换算：ASE 内部时间数值不能直接标为 fs。两个积分器使用同样错误的标签仍可能彼此一致，因此还要检查单位和守恒量。

## 实现边界

**手写后比对** Velocity Verlet 与 **ASE VelocityVerlet**。对照时双方使用同一能量/力接口以隔离积分器差异；这不构成 LJ 势本身的独立验证。真实大体系的温控、约束和轨迹管理直接用成熟 MD 软件。

## 输入与物理模型

- [cluster.extxyz](input/cluster.extxyz)
- [control.toml](input/control.toml)
- [timesteps.csv](input/timesteps.csv)

`cluster.extxyz` 含两个粒子的坐标、质量和动量。Ar 只是元素标签：本模型指定 $m=1$ u、$\epsilon=1$ eV、$\sigma=1$ Å，不代表真实氩参数。

```math
\mathbf r_{n+1}=\mathbf r_n+\Delta t\mathbf v_n+\frac{\Delta t^2}{2m}\mathbf F_n,
```

```math
\mathbf v_{n+1}=\mathbf v_n+\frac{\Delta t}{2m}(\mathbf F_n+\mathbf F_{n+1}).
```

```math
E_{tot}=\sum_i\frac12m_i v_i^2+\sum_{i\lt j}4\epsilon[(\sigma/r_{ij})^{12}-(\sigma/r_{ij})^6].
```

ASE 的内部时间单位与 fs 不同；传给其积分器的步长使用内部单位，报告中另输出 `dt_fs=dt/ase.units.fs`。谐振子扫描另使用 $m=k=1$ 的约化单位，不能混用。

## 从公式到程序

1. 对谐振子扫描 timesteps.csv，计算总能量偏差并观察稳定性边界。
2. 从 EXTXYZ 读取质量、位置与速度；手写循环保存每一步总能量和坐标。
3. 建立 ASE Calculator 适配器复用同一 LJ 势，用 ASE VelocityVerlet 推进相同步数。
4. 比较完整轨迹，不只看终点；保存 own-Verlet.csv 与 ASE-Verlet.csv。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 05_kinetics/02_dynamics/run.py --output runs/02_dynamics
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 相同初态下步长减半，预测能量振荡幅度如何变化；不要把有界振荡全叫“能量漂移”。
- 谐振子满足 ωΔt<2 的线性稳定条件，故意超过它并解释发散。
- 在一段轨迹终点反转速度，积分相同步数检查回到起始位置的误差。
- 换质量必须同时检查输入速度或动量保持了哪一个，否则初始动能也会变化。

## 分步提示与资料

[ASE Molecular Dynamics](https://ase-lib.org/ase/md.html)。

## 完成后应能解释什么

先读时间步长—能量误差表，再比较 own-Verlet.csv 与 ASE-Verlet.csv 的完整轨迹。完成后应能解释质量、动量和时间单位如何进入更新式，以及为什么同力接口的对照验证的是积分器而非势函数。

## 与前后项目的关系

与 [优化](../01_optimizer/README.md) 对照理解“沿力下降”和“按力加速”的区别；[Hessian](../03_hessian/README.md) 给出局部最快振动尺度，后面的 [伞形采样](../../06_catalysis/03_umbrella/README.md) 讨论轨迹覆盖不足。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
