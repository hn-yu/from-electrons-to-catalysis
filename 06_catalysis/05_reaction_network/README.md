# 05 · 从状态能量构造满足详细平衡的网络

正逆速率不能分别凭直觉指定。给定状态和过渡态，怎样让动力学与热力学讲述同一个故事？

## 实现边界

**手写后比对**计量矩阵、正逆 TST 常数和详细平衡；**Cantera 原生 YAML** 独立定义热力学与反应并求表面稳态。通用刚性求解器直接用库，不重写。

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


计量矩阵作用在基元净速率上，物种顺序为 $(*,A*,B*)$：

$$S=\begin{pmatrix}-1&0&1\\1&-1&0\\0&1&-1\end{pmatrix},\quad\dot{\boldsymbol\theta}=S\mathbf r.$$

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

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[Cantera 原生 YAML 机制](https://www.cantera.org/3.2/userguide/creating-mechanisms.html)。
