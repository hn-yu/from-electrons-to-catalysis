# 01 · 从能级表到自由能

本项目从一张能级和简并度表计算平衡占据、内能、熵和自由能，理解电子能怎样进入有限温度的统计描述。

## 背景：为什么需要这一步

上一章计算的是指定几何下的电子态能量。温度非零时，体系可以访问多个状态；实验观测常对应这些状态的统计平均，而不是只取最低能态。与热浴交换能量、保持粒子数和体积固定的平衡描述称为正则系综。

Boltzmann 因子让高能微观态受到指数抑制，但同一能量可能对应许多微观态。这种数量称为简并度，它会提高整个能级出现的概率。配分函数 Z 把所有权重加起来，既用于概率归一化，也连接能级信息与宏观热力学量。

自由能 F=U−TS 同时考虑平均能量与可访问状态数量。因此“低能态最有利”只在特定低温极限才足够。这个最小模型先隔离能量和熵的竞争，再进入真实分子的平移、转动与振动。

## 开始前需要理解的概念

- **微观态与能级**：多个不同微观态可以具有同一能量；本表每行代表一个能级。
- **简并度 gi**：该能级的微观态数量；能级概率包含这个倍数。
- **热能 kBT**：衡量温度相对于能级间隔的能量尺度，本项目统一用 eV。
- **配分函数 Z**：统计权重之和，无量纲；计算时优先保留 logZ 以避免指数溢出。
- **U、F、S**：平均内能、Helmholtz 自由能和熵；不是三个可以随意互换的能量名称。

## 本次任务：从什么得到什么

读取 levels.csv 和 temperatures.csv，自己实现概率与 U/F/S；用 SciPy logsumexp 稳定求和。第二部分把谐振子的无限等间隔能级截断求和，与解析表达式比较，找出高温时截断需要怎样增加。

## 先用一个小例子走通思路

两个能级为 0 和 0.1 eV，简并度为 1 和 3，则激发能级与基态的概率比是 $3e^{-0.1/(k_BT)}$。低温时指数压制激发；无限高温时能级概率趋于 1/4 和 3/4，而不是各一半。

给两个能级同时加 10 eV，概率不变，因为公共指数在归一化时消掉；U 和 F 都增加 10 eV，S 不变。这是无需参考答案就能检验实现的受控实验。

## 实现边界

**手写**配分函数、占据、U/F/S 与谐振子求和的解析式；**直接用 SciPy logsumexp** 保证数值稳定；**比对**高低温解析极限和显式有限能级求和。这里没有必要调用整套电子结构软件。

## 输入与物理模型

- [control.toml](input/control.toml)
- [levels.csv](input/levels.csv)
- [temperatures.csv](input/temperatures.csv)

`levels.csv` 每行给出 $E_i$（eV）和简并度 $g_i$；`temperatures.csv` 给出 K。概率 $p_i$ 指整个简并能级的概率，而不是其中单个微观态。

```math
Z=\sum_i g_i e^{-\beta E_i},\quad p_i=\frac{g_ie^{-\beta E_i}}Z,\quad U=\sum_i p_iE_i,
```

```math
F=-k_BT\ln Z,\qquad S=(U-F)/T,\qquad \beta=(k_BT)^{-1}.
```

单个谐振子 $E_n=\hbar\omega(n+1/2)$ 的和可以解析求出：

```math
Z_{\rm vib}=\frac{e^{-\beta\hbar\omega/2}}{1-e^{-\beta\hbar\omega}},\quad U_{\rm vib}=\frac{\hbar\omega}2+\frac{\hbar\omega}{e^{\beta\hbar\omega}-1}.
```

零点能在低温仍存在；不能在自由能中无声删除，又在能量中保留。

## 从公式到程序

1. 用 log(g)−βE 计算 logweights，通过 logsumexp 得到 logZ，随后求 p。
2. 输出各温度的 U、F、S 和占据，检查概率和为 1。
3. 将谐振子截断到 n_max 个能级，增大 n_max 与解析 U/F 比较。
4. 保留 logZ，即使 Z 本身超出浮点表示范围。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 04_thermodynamics/01_partition/run.py --output runs/01_partition
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 高温时两能级的概率趋于简并度之比，而不一定为 1:1。
- 给所有能级加同一常数 C：U、F 应加 C，S 和占据不变。
- 令低激发能远小于 kBT，比较量子谐振子的热激发能与经典 kBT；不要把 ZPE 当成热激发。

## 分步提示与资料

[SciPy logsumexp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html)。

## 完成后应能解释什么

先读占据随温度变化，再核对 U/F/S 以及谐振子截断误差。完成后应能从“一个态有多贵、同样能量有多少态”解释曲线，并说明为什么自由能零点能平移而平衡概率不变。

## 与前后项目的关系

需要 [单位与能量尺度](../../02_bringup/01_units/README.md)；下一项 [分子热化学](../02_molecular_thermochemistry/README.md) 将把这些求和应用于不同分子自由度。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
