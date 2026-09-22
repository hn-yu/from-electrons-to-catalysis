# 07 · 用扰动代替“最高势垒就是决速步”的直觉

本项目通过单独扰动过渡态并重新求稳态，量化每一步对整体速率的控制程度，检验“最高局部势垒就是决速步”的直觉。

## 背景：为什么需要这一步

局部势垒决定从某个状态出发有多快，但整体通量还取决于该状态有多少人口、逆反应多强，以及其他步骤如何补充或消耗它。因此只把势垒排成一列，通常不足以确定提升哪个步骤最能加快催化。

速率控制度（degree of rate control，DRC）提出一个明确的反事实问题：保持所有中间体自由能和外界条件不变，只把某个过渡态略微降低，整体 TOF 会怎样变化？这同时改变该步正逆速率，保持平衡常数不变，然后让覆盖度重新调整。

改变中间体稳定性是另一种实验，它会改变相邻反应平衡与状态人口。本项目将两种扰动分开，并用 Cantera 的反应倍率提供独立对照，使“控制步骤”的判断建立在定义和响应上。

## 开始前需要理解的概念

- **局部正向势垒**：过渡态减去相邻反应物状态自由能，不包含该状态的实际人口。
- **过渡态 DRC Xi**：降低第 i 个过渡态后，lnTOF 对其变化的无量纲响应。
- **反应倍率 mi**：同时乘一条可逆反应的正逆速率，等效于在固定温度改变其过渡态。
- **中心差分**：使用正负微扰估计导数，需要寻找步长误差与求解误差之间的平台。
- **条件依赖**：控制度随温度、分压和模型变化，并非某一步永久的标签。

## 本次任务：从什么得到什么

本项目使用专门构造的 states.csv 与 transitions.csv，能量不同于上一项默认案例。先记录局部势垒排序，再手写 ±δ 过渡态扰动和稳态重算，得到 Xi；用 Cantera 的倍率扰动独立核对，并检查统一时间缩放给出的求和关系。

## 先用一个小例子走通思路

本例局部正向势垒约为 0.65、0.90、0.55 eV，最大的是第二步；但计算得到 Xi 约为 0.02558、0.00294、0.97148，第三步的控制度最大。

这并不表示第二步的势垒算错，而是表面人口和逆反应改变了局部速率对净通量的影响。把所有反应正逆速率统一乘 2，只会将稳态循环的时钟加快两倍，因此 TOF 也乘 2，给出本模型中 Xi 求和约为 1 的检查。

## 实现边界

**手写后比对**过渡态能量中心差分得到的 degree of rate control；**Cantera** 用反应倍率同时缩放正逆方向，独立重新求稳态。不能只比较基元势垒大小。

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

固定所有中间体自由能，对第 i 个过渡态定义

```math
X_i=-k_BT\frac{\partial\ln\mathrm{TOF}}{\partial G_i^\ddagger}=\frac{\partial\ln\mathrm{TOF}}{\partial\ln m_i},
```

$m_i$ 同时乘该反应正、逆速率。若所有速率常数统一乘 m，整个时间尺度缩放，TOF 也乘 m，因此这类模型满足 $\sum_iX_i\approx1$。

改变中间体能量会改变平衡常数和覆盖度，是另一个灵敏度问题，不应混称为同一种过渡态 DRC。

## 从公式到程序

1. 输出各步局部正向势垒 GTS−Gleft，并根据直觉先写预测。
2. 对每个 GTS 做 ±δ 扰动，每次重新求稳态，用中心差分计算 Xi。
3. Cantera 对第 i 反应分别乘 exp(±h)，比较独立得到的 Xi。
4. 再扰动中间体自由能，解释稳定中间体为什么可能降低反应速率。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 06_catalysis/07_rate_control/run.py --output runs/07_rate_control
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 示例 Xi 约 (0.02558,0.00294,0.97148)，第三步控制程度最大；将它与局部势垒排序并排展示。
- 将 δ 从 0.01 eV 逐步减小，检查中心差分平台；过小 δ 会放大稳态求解误差。
- 扫描温度与分压，观察控制分配是否转移；“决速步”不应被当成机制永恒不变的标签。
- 净 TOF 接近零或反向时，lnTOF 灵敏度不再适合直接使用，应重新定义响应量。

## 分步提示与资料

[Cantera 反应倍率接口](https://www.cantera.org/stable/python/kinetics.html)。

## 完成后应能解释什么

并排读局部势垒、DRC、Cantera 差值与扰动步长结果，再看中间体扰动引起的覆盖度变化。完成后应能准确说出“保持了什么、改变了什么、重新求了什么”，并识别净 TOF 接近零时对数响应的局限。

## 与前后项目的关系

需要 [微观动力学](../06_microkinetics/README.md)；[催化检查点](../08_checkpoint/README.md) 将把速率控制与电子能、采样和实验响应的证据连接起来。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
