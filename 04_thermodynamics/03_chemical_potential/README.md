# 03 · 压力通过化学势改变吸附方向

本项目用一个可手算的吸附模型，解释温度和气体压力如何通过化学势改变吸附自由能的方向。

## 背景：为什么需要这一步

表面与周围气体接触时，吸附原子数可以改变。表面获得一个粒子的同时，气体储库失去一个粒子；比较反应前后不能只算表面的能量变化，还要计入储库的自由能代价。

化学势 μ 表示在指定条件下增加一个粒子的 Gibbs 自由能变化。理想气体的压力依赖是 kBT ln(p/p°)：压缩气体减少其可访问空间，提高粒子留在气相的自由能。于是把粒子从高压气相移到表面，通常比从低压气相移过去更有利。

为单独看清这个效应，本项目用固定气体熵近似标准化学势，暂时忽略吸附态振动和覆盖度熵。它不是某个真实气体的完整热化学预测，而是将电子吸附能、气相熵和压力三者拆开的练习。

## 开始前需要理解的概念

- **储库**：足够大、能交换粒子且维持指定 T/p 的环境。
- **化学势 μ**：每粒子的自由能，单位可为 eV；摩尔形式应配套使用 R。
- **标准态 p°**：对数中压力比的参考，本例为 1 bar。
- **吸附自由能 ΔGads**：吸附后减去吸附前的自由能，负值表示该转移方向在本模型下有利。
- **参考电子能 Egas**：用于与电子吸附能对齐零点，不能在 μ 中算过后再次减去。

## 本次任务：从什么得到什么

读取温度表、压力表和控制文件中的 Eads、气体熵，手写 μ−Egas 与 ΔGads 的二维扫描。输出每个条件的数值和 ΔG=0 边界，用解析斜率检验压力扫描的符号与单位。

## 先用一个小例子走通思路

输入 $E_{ads}=-0.6$ eV、$s_{gas}=0.0015$ eV/K。在 600 K、1 bar，气相热修正为 −0.9 eV，所以 $\Delta G_{ads}=-0.6-(-0.9)=+0.3$ eV。负电子吸附能仍可对应正吸附自由能。

同温度下压力增加十倍，μ 增加约 0.11905 eV，ΔGads 因而降低相同数值。两处符号相反，是因为气体出现在吸附反应的反应物一侧。

## 实现边界

**手写**化学势与反应自由能的符号、标准态和压力扫描；直接用 NumPy 的 log。上一项目可提供成熟软件算出的标准热化学，本例使用明确标注的常熵模型以隔离压力效应。

## 输入与物理模型

- [control.toml](input/control.toml)
- [pressures.csv](input/pressures.csv)
- [temperatures.csv](input/temperatures.csv)

输入温度为 K、压力为 bar，标准压力 $p^\circ=1$ bar。控制文件给出相对于气体电子能的常熵近似 $\mu^\circ-E_{gas}=-Ts_{gas}$。

```math
\mu(T,p)=\mu^\circ(T)+k_BT\ln(p/p^\circ),
```

```math
\Delta G_{ads}=E_{ads}-[\mu(T,p)-E_{gas}].
```

因此降低压力会降低气相化学势，让吸附更不利；提高压力则相反。本模型忽略吸附态振动、侧向相互作用与覆盖度熵，不能用于定量相界预测。

平衡条件 $\Delta G_{ads}=0$ 给出

```math
\ln(p_{eq}/p^\circ)=\frac{E_{ads}+Ts_{gas}}{k_BT}.
```

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

## 分步提示与资料

标准气相热化学的实现可对照 [ASE IdealGasThermo](https://ase-lib.org/ase/thermochemistry/thermochemistry.html)。

## 完成后应能解释什么

先读 scan.csv 中固定温度的压力序列，确认对 ln p 的斜率，再看温度变化。完成后应能写出储库项在反应式中的位置，并说明换成真实 RRHO 标准化学势后保留哪些关系、改变哪些数值。

## 与前后项目的关系

承接 [分子热化学](../02_molecular_thermochemistry/README.md)；下一项 [表面相图](../04_surface_phase/README.md) 用同一储库比较多个不同组成的表面。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
