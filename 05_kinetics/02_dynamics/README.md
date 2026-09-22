# 02 · 用能量误差检验 Velocity Verlet

一个轨迹看起来在振动，并不能证明积分器正确。长期能量行为、时间步长和独立实现才是更可靠的检查。

## 实现边界

**手写后比对** Velocity Verlet 与 **ASE VelocityVerlet**。对照时双方使用同一能量/力接口以隔离积分器差异；这不构成 LJ 势本身的独立验证。真实大体系的温控、约束和轨迹管理直接用成熟 MD 软件。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [cluster.extxyz](input/cluster.extxyz)
- [control.toml](input/control.toml)
- [timesteps.csv](input/timesteps.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`cluster.extxyz` 含两个粒子的坐标、质量和动量。Ar 只是元素标签：本模型指定 $m=1$ u、$\epsilon=1$ eV、$\sigma=1$ Å，不代表真实氩参数。

$$\mathbf r_{n+1}=\mathbf r_n+\Delta t\mathbf v_n+\frac{\Delta t^2}{2m}\mathbf F_n,$$
$$\mathbf v_{n+1}=\mathbf v_n+\frac{\Delta t}{2m}(\mathbf F_n+\mathbf F_{n+1}).$$

$$E_{tot}=\sum_i\frac12m_i v_i^2+\sum_{i<j}4\epsilon[(\sigma/r_{ij})^{12}-(\sigma/r_{ij})^6].$$

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

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[ASE Molecular Dynamics](https://ase-lib.org/ase/md.html)。
