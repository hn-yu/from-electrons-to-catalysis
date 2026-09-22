# 02 · 用真实 PBE 计算回答一个有限问题

最终项目不是“调用成功就完成”。任务是为 H/Cu(111) 的吸附能给出可追溯输入、软件输出和目前证据允许的结论。

## 实现边界

**直接用 ASE/GPAW** 的周期 PAW/PBE、优化器和结构文件；**手写**反应参考、误差预算和下一轮计算设计。默认分析已执行数据；新计算用 `--calculate`，绝不静默退回 EMT。

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


`cases.csv` 指向基准与七个单因素变体，每个目录给出完整坐标和 calculator.toml；`energies.csv` 保存每套独立计算的 clean/H₂/adsorbed 总能量。

$$\Delta E_{ads}=E[H/Cu(111)]-E[Cu(111)]-\frac12E[H_2].$$

基准是 1×1×3、一个 H、1 ML、250 eV、3×3×1 k 点。它是一套 bringup 起点，不是已收敛表面模型。

$$\epsilon_q=|\Delta E_{ads}(q_{refined})-\Delta E_{ads}(q_{base})|.$$

既定容限是 0.05 eV；对已执行变体检验这个声明，不把失败的容限在结果出现后悄悄放宽。


## 从公式到程序

1. 先读本节 calculation memo 和 blind prediction，区分历史事前记录与现在已经知道的数值。
2. 检查每个 POSCAR 的原子数、层数、晶胞、真空与 Selective dynamics；H₂ 参考使用独立分子盒。
3. 默认运行完成表格分析；执行 `sbatch scripts/slurm.sh 07_real_system/02_real_dft/run.py --calculate --output runs/new-real-dft` 则真正运行全部案例。
4. 新运行保存 GPAW 原始 txt、优化日志和 relaxed.extxyz，停止条件失败会报错。
5. 写出数据支持的有限结论，并优先补计算厚度失败的轴。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 07_real_system/02_real_dft/run.py --output runs/02_real_dft
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 基准吸附能 +0.04560 eV；四层约 −0.30182 eV，说明当前吸附符号对 slab 厚度不稳定。
- 2×2×3、单 H 变成 0.25 ML，结果约 −0.08851 eV。将其同时标为覆盖度变化，不能仅称为“超胞误差”。
- 提出保持覆盖度与底部约束一致的 4/5/6 层后续计划，并事前定义平台判据。
- 当前数据不能支持可靠位点排序、有限温 TOF 或实验活性结论；列出每个推断还缺哪种信息。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[GPAW 安装与文档](https://gpaw.readthedocs.io/)；本仓库 [安装说明](../../INSTALL.md)。

## 原生结构接口检查

[output/native-poscar-check](output/native-poscar-check) 是直接从当前 fcc.POSCAR 新执行的 PBE 单点，保留软件原始日志与带能量/力的 EXTXYZ。最大力约 1.67 eV/Å，未作几何优化，因此仅验证输入和软件接口，不能充当吸附驻点或收敛证据。
