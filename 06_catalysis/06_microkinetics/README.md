# 06 · 覆盖度与基元速率共同决定 TOF

本项目将基元反应速率与表面覆盖度耦合，求稳态周转频率，并解释温度和压力响应为什么不能仅由某个单步势垒判断。

## 背景：为什么需要这一步

一个反应步骤即使速率常数很大，也需要相应反应物真的存在。例如表面转化的事件率与 A* 覆盖度相乘；吸附则需要气体和空位同时存在。网络中每一步都在改变下一步可用的状态人口，所以必须一起求解。

微观动力学用质量作用式构造各步净速率，再用计量关系推进覆盖度。固定气体储库时，本例的三状态单占位模型给出线性方程；更一般的多位点、相互作用或多粒子反应常产生非线性方程。

稳态表示各状态人口不再随时间变化，仍可以持续有物质流过网络。只有平衡时每步净通量才为零。维持反应物和产物分压的储库提供驱动力，表面催化循环把这种驱动转化为持续周转。

## 开始前需要理解的概念

- **质量作用式**：速率常数乘参与物种的活度或覆盖度，再减逆反应贡献。
- **覆盖度 θ**：单个位点处于某状态的分数，本例三者非负且和为 1。
- **稳态**：dθ/dt=0；允许正逆不相等但各步净通量彼此平衡。
- **TOF**：单位位点单位时间的净产物生成数，本例为 s⁻¹。
- **反应级数与表观活化能**：整体 TOF 对压力和温度的导数，包含人口重新分配。
- **刚性方程**：多个时间尺度相差很大，时间积分直接用 SciPy BDF 等成熟方法。

## 本次任务：从什么得到什么

读取同一三状态机制与温压扫描表，手写质量作用 RHS 和稳态矩阵，用归一化条件替换一个冗余方程。分别通过直接稳态解、SciPy BDF 积分和 Cantera 原生 YAML 得到覆盖度与 TOF；每次改变 T/p 都重新求稳态，再计算整体响应。

## 先用一个小例子走通思路

600 K、pA=1 bar、pB=0.01 bar 时，示例覆盖度约为 $(0.002875,0.951428,0.045697)$。表面约 95% 时间处于 A*，空位只有约 0.29%；这会直接限制需要空位的吸附事件。

若忽略逆反应写 r≈k₁pAθ*，只有 θ* 随压力几乎不变时才近似一阶。升压同时压低空位比例时，速率增长可能趋于饱和，必须由重新求解后的覆盖度来判断。

## 实现边界

**手写后比对**质量作用 RHS、稳态线性方程与 SciPy BDF 积分；**Cantera** 独立读取 YAML 并求同一温度/分压的稳态。网络扩大后的刚性求解和相管理直接用成熟库。

## 输入与物理模型

- [control.toml](input/control.toml)
- [mechanism.yaml](input/mechanism.yaml)
- [pressures.csv](input/pressures.csv)
- [states.csv](input/states.csv)
- [temperatures.csv](input/temperatures.csv)
- [transitions.csv](input/transitions.csv)

模型是 $A(g)+*\rightleftharpoons A*\rightleftharpoons B*\rightleftharpoons B(g)+*$。A/B 是抽象异构态，YAML 用相同形式元素组成保证守恒，不代表实际氢反应。

`states.csv` 给出相对标准自由能，`transitions.csv` 给过渡态自由能，单位 eV。`mechanism.yaml` 是 Cantera 可直接读取的 ideal-gas + ideal-surface 机制，`X` 表示空位。

```math
k_i^+=\frac{k_BT}{h}e^{-\beta(G_i^\ddagger-G_{left})},\quad k_i^-=\frac{k_BT}{h}e^{-\beta(G_i^\ddagger-G_{right})},
```

```math
\frac{k_i^+}{k_i^-}=e^{-\beta\Delta G_i^\circ}.
```

手写模型气体活度为 $a=p/(1\ \mathrm{bar})$。Cantera 的气体浓度为 kmol/m³，$C^\circ=p^\circ/(RT)$。吸附的浓度速率系数应为 $k^+/C^\circ$，因此 YAML 的 Arrhenius 参数为 $A=(k_B/h)R/p^\circ,b=2$；其余单表面态转化为 $A=k_B/h,b=1$。

YAML 各占据态使用相同常热容，使反应中的热容项消去；参考熵取零，标准焓对应给定状态能量。这是为独立核对而构造的热力学模型，不能拿去预测真实气体的温度依赖。

三个净速率为

```math
r_1=k_1^+a_A\theta_*-k_1^-\theta_A,\quad r_2=k_2^+\theta_A-k_2^-\theta_B,
```

```math
r_3=k_3^+\theta_B-k_3^-a_B\theta_*.
```

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

## 分步提示与资料

[Cantera 表面热力学与覆盖度接口](https://www.cantera.org/stable/python/thermo.html)；[SciPy BDF](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.BDF.html)。

## 完成后应能解释什么

先核对覆盖度和为 1、各步净通量相等，再读温压扫描中的 TOF、反应级数和表观活化能。完成后应能用人口变化解释曲线，并区分初态影响的暂态与固定储库下的最终稳态。

## 与前后项目的关系

前置是 [反应网络](../05_reaction_network/README.md)；下一项 [速率控制](../07_rate_control/README.md) 通过受控扰动判断哪些过渡态最影响整体 TOF。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
