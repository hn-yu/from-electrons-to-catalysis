# 06 · 覆盖度与基元速率共同决定 TOF

最容易发生的基元反应为什么未必贡献最大的催化通量？先求出体系大部分时间待在哪个状态。

## 实现边界

**手写后比对**质量作用 RHS、稳态线性方程与 SciPy BDF 积分；**Cantera** 独立读取 YAML 并求同一温度/分压的稳态。网络扩大后的刚性求解和相管理直接用成熟库。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [mechanism.yaml](input/mechanism.yaml)
- [pressures.csv](input/pressures.csv)
- [states.csv](input/states.csv)
- [temperatures.csv](input/temperatures.csv)
- [transitions.csv](input/transitions.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


模型是 $A(g)+*\rightleftharpoons A*\rightleftharpoons B*\rightleftharpoons B(g)+*$。A/B 是抽象异构态，YAML 用相同形式元素组成保证守恒，不代表实际氢反应。

`states.csv` 给出相对标准自由能，`transitions.csv` 给过渡态自由能，单位 eV。`mechanism.yaml` 是 Cantera 可直接读取的 ideal-gas + ideal-surface 机制，`X` 表示空位。

$$k_i^+=\frac{k_BT}{h}e^{-\beta(G_i^\ddagger-G_{left})},\quad k_i^-=\frac{k_BT}{h}e^{-\beta(G_i^\ddagger-G_{right})},$$
$$\frac{k_i^+}{k_i^-}=e^{-\beta\Delta G_i^\circ}.$$

手写模型气体活度为 $a=p/(1\ \mathrm{bar})$。Cantera 的气体浓度为 kmol/m³，$C^\circ=p^\circ/(RT)$。吸附的浓度速率系数应为 $k^+/C^\circ$，因此 YAML 的 Arrhenius 参数为 $A=(k_B/h)R/p^\circ,b=2$；其余单表面态转化为 $A=k_B/h,b=1$。

YAML 各占据态使用相同常热容，使反应中的热容项消去；参考熵取零，标准焓对应给定状态能量。这是为独立核对而构造的热力学模型，不能拿去预测真实气体的温度依赖。


三个净速率为

$$r_1=k_1^+a_A\theta_*-k_1^-\theta_A,\quad r_2=k_2^+\theta_A-k_2^-\theta_B,$$
$$r_3=k_3^+\theta_B-k_3^-a_B\theta_*.$$

固定储库时 $\dot\theta=Q\theta$。稳态满足 $Q\theta=0$ 和 $\sum\theta=1$；因 Q 奇异，替换一行守恒方程后求解。循环稳态要求 $r_1=r_2=r_3=\mathrm{TOF}$。


## 从公式到程序

1. 写出 generator 的每个非对角转移率，验证每列和为零。
2. 用归一化替换一个冗余方程求稳态；另从空表面用 BDF 积分到稳态。
3. 将相同 T、pA、pB 交给 Cantera，比较三个覆盖度和净通量。
4. 扫描温度与反应物分压，对每个点都重新求覆盖度，再估算反应级数和表观活化能。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 06_catalysis/06_microkinetics/run.py --output runs/06_microkinetics
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 600 K、pA=1 bar、pB=0.01 bar 时，θ≈(0.0028751,0.9514282,0.0456967)，TOF≈752320.86 s⁻¹；这是抽象模型结果。
- 增加 pA 可能使表面更饱和，速率未必保持一阶。用 d lnTOF/d ln pA 验证。
- 改变初始覆盖度，稳定的唯一稳态应保持相同；短时间轨迹可以不同。
- 比较最大残差与最大基元通量的相对尺度，巨大速率相消时不能只要求一个固定绝对容差。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[Cantera 表面热力学与覆盖度接口](https://www.cantera.org/stable/python/thermo.html)；[SciPy BDF](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.BDF.html)。
