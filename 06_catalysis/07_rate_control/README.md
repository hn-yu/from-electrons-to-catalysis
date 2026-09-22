# 07 · 用扰动代替“最高势垒就是决速步”的直觉

本项目故意构造一个反例：局部正向势垒最大的一步，并不是对整体速率影响最大的一步。你需要从覆盖度和扰动定义解释它。

## 实现边界

**手写后比对**过渡态能量中心差分得到的 degree of rate control；**Cantera** 用反应倍率同时缩放正逆方向，独立重新求稳态。不能只比较基元势垒大小。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [mechanism.yaml](input/mechanism.yaml)
- [states.csv](input/states.csv)
- [transitions.csv](input/transitions.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


模型是 $A(g)+*\rightleftharpoons A*\rightleftharpoons B*\rightleftharpoons B(g)+*$。A/B 是抽象异构态，YAML 用相同形式元素组成保证守恒，不代表实际氢反应。

`states.csv` 给出相对标准自由能，`transitions.csv` 给过渡态自由能，单位 eV。`mechanism.yaml` 是 Cantera 可直接读取的 ideal-gas + ideal-surface 机制，`X` 表示空位。

$$k_i^+=\frac{k_BT}{h}e^{-\beta(G_i^\ddagger-G_{left})},\quad k_i^-=\frac{k_BT}{h}e^{-\beta(G_i^\ddagger-G_{right})},$$
$$\frac{k_i^+}{k_i^-}=e^{-\beta\Delta G_i^\circ}.$$

手写模型气体活度为 $a=p/(1\ \mathrm{bar})$。Cantera 的气体浓度为 kmol/m³，$C^\circ=p^\circ/(RT)$。吸附的浓度速率系数应为 $k^+/C^\circ$，因此 YAML 的 Arrhenius 参数为 $A=(k_B/h)R/p^\circ,b=2$；其余单表面态转化为 $A=k_B/h,b=1$。

YAML 各占据态使用相同常热容，使反应中的热容项消去；参考熵取零，标准焓对应给定状态能量。这是为独立核对而构造的热力学模型，不能拿去预测真实气体的温度依赖。


固定所有中间体自由能，对第 i 个过渡态定义

$$X_i=-k_BT\frac{\partial\ln\mathrm{TOF}}{\partial G_i^\ddagger}=\frac{\partial\ln\mathrm{TOF}}{\partial\ln m_i},$$

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

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[Cantera 反应倍率接口](https://www.cantera.org/stable/python/kinetics.html)。
