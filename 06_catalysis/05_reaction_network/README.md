# 05 · 从状态能量构造满足详细平衡的网络

本项目把状态与过渡态自由能转换成守恒、满足详细平衡的可逆反应网络，为后续覆盖度和催化速率计算建立一致输入。

## 背景：为什么需要这一步

实际催化反应通常经过吸附、表面转化和脱附等多个步骤。每一步的正向与逆向过程共享相同的过渡态，因此速率常数之比受到两端自由能差的约束。若任意指定两个方向的速率，可能得到在平衡条件下仍自行循环的矛盾模型。

反应网络需要两类信息：有哪些状态、如何通过基元反应连接，以及每种连接的热力学和动力学参数。计量矩阵将每步的净反应事件转为各物种数量变化，让守恒关系成为可直接检查的代数性质。

本例只有空位、A* 和 B* 三种单占位点状态，气相 A/B 维持给定分压。它是抽象异构化模型，用来学习一致的网络构造；Cantera YAML 使用相同形式元素组成保持守恒，不对应实际氢化学。

## 开始前需要理解的概念

- **基元反应**：网络中显式建模的单步转换，具有一对正逆速率。
- **星号与覆盖度**：* 表示空位，A* 表示被 A 占据的位点；YAML 中空位名为 X。
- **详细平衡**：热力学平衡时每步正逆通量相等，速率常数比与平衡常数一致。
- **计量矩阵 S**：每列对应一条反应，每行对应一个表面物种的净增减。
- **活度与浓度**：手写模型用 p/p°，Cantera 用浓度型质量作用式，参数必须换算。

## 本次任务：从什么得到什么

从 states.csv 与 transitions.csv 手写两方向 TST 常数和计量矩阵，检查详细平衡与位点守恒。Cantera 直接读取独立的原生 mechanism.yaml 并求稳态，核对覆盖度和各步通量；修改能量表时显式更新 YAML，保证比较的是同一个模型。

## 先用一个小例子走通思路

设一步反应两端自由能为 0 和 −0.3 eV，过渡态为 +0.15 eV。正向势垒为 0.15 eV，逆向为 0.45 eV，所以速率常数比为 $e^{0.3/(k_BT)}$。

把过渡态升高 0.1 eV，两方向速率都减慢，但比值不变。若只减慢正向，则相当于改变了平衡常数，不能再声称两端热力学完全不变。

## 实现边界

**手写后比对**计量矩阵、正逆 TST 常数和详细平衡；**Cantera 原生 YAML** 独立定义热力学与反应并求表面稳态。通用刚性求解器直接用库，不重写。

## 输入与物理模型

- [control.toml](input/control.toml)
- [mechanism.yaml](input/mechanism.yaml)
- [states.csv](input/states.csv)
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

计量矩阵作用在基元净速率上，物种顺序为 $(*,A*,B*)$：

```math
S=\begin{pmatrix}-1&0&1\\1&-1&0\\0&1&-1\end{pmatrix},\quad\dot{\boldsymbol\theta}=S\mathbf r.
```

每列和为零体现单占位点守恒；这与气相元素守恒是不同的核对。

## 从公式到程序

1. 从 CSV 能量计算所有正逆速率；打印 ln(k+/k−)+ΔG°/kBT，应接近零。
2. 写计量矩阵并验证列和；手算每一步反应改变哪些覆盖度。
3. Cantera 仅从 mechanism.yaml 读取机制，独立推进覆盖度；比较稳态覆盖度和每步净通量。
4. 若修改状态表，用 make_mechanism.py 显式更新 YAML 并检查 diff，不能让两套输入无声失配。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 06_catalysis/05_reaction_network/run.py --output runs/05_reaction_network
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 只改变某步正向速率，看看详细平衡残差如何暴露不一致。
- 同时平移所有状态与过渡态的能量零点，应保持相应能垒不变；储库能也必须一致处理。
- 调整气体分压使循环总自由能为零，验证平衡时所有净通量为零，但正向和逆向通量通常不为零。

## 分步提示与资料

[Cantera 原生 YAML 机制](https://www.cantera.org/3.2/userguide/creating-mechanisms.html)。

## 完成后应能解释什么

先读各步能垒、详细平衡残差和计量矩阵，再比较 Cantera 的稳态覆盖度与净通量。完成后应能从一条反应式写出对应矩阵列，并解释活度式与浓度式的单位换算为何影响 YAML 前因子。

## 与前后项目的关系

需要 [化学势](../../04_thermodynamics/03_chemical_potential/README.md) 与 [TST](../../05_kinetics/05_tst/README.md)；下一项 [微观动力学](../06_microkinetics/README.md) 用这个网络求随条件变化的观测量。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
