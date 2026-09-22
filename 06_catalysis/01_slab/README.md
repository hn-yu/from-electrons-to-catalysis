# 01 · 收敛一个可解释的表面观测量

清洁 slab 的总能量稳定，并不能保证吸附能稳定。数值设置应围绕最终观测量设计。

## 实现边界

**直接用 GPAW/PBE 与 ASE** 做电子结构、结构读写和优化；**手写**能量差、单因素收敛与覆盖度核对。默认分析真实计算表；`--calculate` 对 cases.csv 中每套 POSCAR 重新计算。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [baseline/H2.extxyz](input/baseline/H2.extxyz)
- [baseline/calculator.toml](input/baseline/calculator.toml)
- [baseline/clean.POSCAR](input/baseline/clean.POSCAR)
- [baseline/fcc.POSCAR](input/baseline/fcc.POSCAR)
- [cases.csv](input/cases.csv)
- [control.toml](input/control.toml)
- [cutoff_eV-0/H2.extxyz](input/cutoff_eV-0/H2.extxyz)
- [cutoff_eV-0/calculator.toml](input/cutoff_eV-0/calculator.toml)
- [cutoff_eV-0/clean.POSCAR](input/cutoff_eV-0/clean.POSCAR)
- [cutoff_eV-0/fcc.POSCAR](input/cutoff_eV-0/fcc.POSCAR)
- [energies.csv](input/energies.csv)
- [fixed_layers-0/H2.extxyz](input/fixed_layers-0/H2.extxyz)

完整清单与单位见 [input/README.md](input/README.md)。

`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


输入 `cases.csv` 的每行指向一个独立目录，包含 clean.POSCAR、fcc.POSCAR、H2.extxyz 和 calculator.toml。数据源见 DATA_SOURCE.md。

$$E_{ads}=E_{slab+H}-E_{slab}-\frac12E_{H_2},$$
$$\delta_j=E_{ads}(q_j)-E_{ads}(q_0).$$

$q_j$ 是只改变一项的计算设置。截断能、k 点、真空、层数、固定层和电子展宽分别扫描，不能拿不同设置的 clean 与 adsorbed 能量相减。

1×1 表面胞中一个 H 是 1 ML；2×2 中一个 H 是 0.25 ML。横向扩胞同时改变覆盖度，因此该轴不单是数值收敛。


## 从公式到程序

1. 读每个 case 的总能量三元组，自己重新计算 Eads。
2. 输出相对基准变化，并与事先指定的 0.05 eV 阈值比较。
3. 对变化大的轴解释可能物理来源；继续增加该轴，而不是用其他轴的小差异抵消它。
4. 新计算命令为 `sbatch scripts/slurm.sh 06_catalysis/01_slab/run.py --calculate --output runs/new-slab`，会执行输入表全部 case。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 06_catalysis/01_slab/run.py --output runs/01_slab
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 已有 1×1×3 基准 Eads 约 +0.0456 eV；增加到四层变为约 −0.3018 eV，厚度差约 0.35 eV，远超阈值。
- 将每个 case 的三个参考能都打印，检查总能量是否虽然变化很大，但差值发生抵消。
- 下一轮保持覆盖度固定增加层数，事前指定何种平台趋势足以改变当前“未收敛”的判断。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[GPAW 表面计算](https://gpaw.readthedocs.io/tutorialsexercises/structureoptimization/surface/surface.html)；[ASE 约束](https://ase-lib.org/ase/constraints.html)。
