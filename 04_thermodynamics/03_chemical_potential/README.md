# 03 · 压力通过化学势改变吸附方向

相同的负吸附电子能，为什么在低压高温下仍可能不吸附？本项目把气体熵和压力放回反应自由能。

## 实现边界

**手写**化学势与反应自由能的符号、标准态和压力扫描；直接用 NumPy 的 log。上一项目可提供成熟软件算出的标准热化学，本例使用明确标注的常熵模型以隔离压力效应。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [pressures.csv](input/pressures.csv)
- [temperatures.csv](input/temperatures.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


输入温度为 K、压力为 bar，标准压力 $p^\circ=1$ bar。控制文件给出相对于气体电子能的常熵近似 $\mu^\circ-E_{gas}=-Ts_{gas}$。

$$\mu(T,p)=\mu^\circ(T)+k_BT\ln(p/p^\circ),$$
$$\Delta G_{ads}=E_{ads}-[\mu(T,p)-E_{gas}].$$

因此降低压力会降低气相化学势，让吸附更不利；提高压力则相反。本模型忽略吸附态振动、侧向相互作用与覆盖度熵，不能用于定量相界预测。

平衡条件 $\Delta G_{ads}=0$ 给出

$$\ln(p_{eq}/p^\circ)=\frac{E_{ads}+Ts_{gas}}{k_BT}.$$


## 从公式到程序

1. 分别读温度表和压力表，构造二维扫描，不把 bar 数值直接当 Pa 使用。
2. 计算 μ−Egas 和 ΔGads，输出 scan.csv。
3. 从公式预测 ΔG 对 ln p 的斜率，再用表格有限差分核对。
4. 标出 ΔG=0 的压力，检查扫描范围是否真正覆盖它。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 04_thermodynamics/03_chemical_potential/run.py --output runs/03_chemical_potential
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 在 600 K 提高压力十倍，ΔG 应降低约 0.11905 eV。
- 分别在固定压力、固定化学势下改变温度，说明为什么这不是同一个实验。
- 用上一项目的真实 RRHO μ°(T) 替换常熵模型，比较低温与高温的偏差来源。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

标准气相热化学的实现可对照 [ASE IdealGasThermo](https://ase-lib.org/ase/thermochemistry/thermochemistry.html)。
