# 01 · 从能级表到自由能

一个激发态能量高于基态，却仍可能在平衡时占据多数粒子。简并度如何与能量竞争？

## 实现边界

**手写**配分函数、占据、U/F/S 与谐振子求和的解析式；**直接用 SciPy logsumexp** 保证数值稳定；**比对**高低温解析极限和显式有限能级求和。这里没有必要调用整套电子结构软件。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [levels.csv](input/levels.csv)
- [temperatures.csv](input/temperatures.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`levels.csv` 每行给出 $E_i$（eV）和简并度 $g_i$；`temperatures.csv` 给出 K。概率 $p_i$ 指整个简并能级的概率，而不是其中单个微观态。

$$Z=\sum_i g_i e^{-\beta E_i},\quad p_i=\frac{g_ie^{-\beta E_i}}Z,\quad U=\sum_i p_iE_i,$$
$$F=-k_BT\ln Z,\qquad S=(U-F)/T,\qquad \beta=(k_BT)^{-1}.$$

单个谐振子 $E_n=\hbar\omega(n+1/2)$ 的和可以解析求出：

$$Z_{\rm vib}=\frac{e^{-\beta\hbar\omega/2}}{1-e^{-\beta\hbar\omega}},\quad U_{\rm vib}=\frac{\hbar\omega}2+\frac{\hbar\omega}{e^{\beta\hbar\omega}-1}.$$

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

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[SciPy logsumexp](https://docs.scipy.org/doc/scipy/reference/generated/scipy.special.logsumexp.html)。
