# 02 · 吸附位点竞争与参考态

结构文件里写着 fcc，优化后它就一定还是 fcc 吗？本项目要求把起始位点、最终几何与相对能量对应起来。

## 实现边界

**直接用 ASE/GPAW** 求四个位点与气体/清洁表面的能量和力；**手写**化学计量、位点排序及可靠性分析。EMT 只保留为历史流程示例，当前主数据是 PBE。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [baseline/H2.extxyz](input/baseline/H2.extxyz)
- [baseline/bridge.POSCAR](input/baseline/bridge.POSCAR)
- [baseline/calculator.toml](input/baseline/calculator.toml)
- [baseline/clean.POSCAR](input/baseline/clean.POSCAR)
- [baseline/fcc.POSCAR](input/baseline/fcc.POSCAR)
- [baseline/hcp.POSCAR](input/baseline/hcp.POSCAR)
- [baseline/ontop.POSCAR](input/baseline/ontop.POSCAR)
- [cases.csv](input/cases.csv)
- [control.toml](input/control.toml)
- [energies.csv](input/energies.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


基准目录提供 2×2×3 Cu(111)、一个 H，覆盖度 0.25 ML。ontop/bridge/fcc/hcp 的 POSCAR 是起始构型；输出 H 的最终坐标和残余力用于检验位点身份。

$$E_{ads}^{(i)}=E_{slab+H}^{(i)}-E_{slab}-\tfrac12E_{H_2},$$
$$\Delta E_{ij}=E_{ads}^{(i)}-E_{ads}^{(j)}.$$

共同气体与清洁参考在位点能量差中消去。但不同覆盖度、胞大小或计算设置下不能如此消去。

fcc/hcp 的区别在于下方堆垛层位置，不是只由 H 的高度决定。优化时关闭点群对称，避免初始对称强迫后续轨迹保留不应有的限制。


## 从公式到程序

1. 从 input/cases.csv 定位所有四个位点结构及计算参数。
2. 默认从 energies.csv 重算四个吸附能，并输出最终坐标与最大力。
3. 用 ASE 查看最终结构是否发生位点迁移；初始名称只作为轨迹标签。
4. 需要新 DFT 时用 `run.py --calculate`，计算会保存 GPAW 原始日志和 relaxed.extxyz。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 06_catalysis/02_adsorption/run.py --output runs/02_adsorption
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 既有 PBE 给 atop≈+0.5311、bridge≈+0.0481、fcc≈−0.0898、hcp≈−0.0827 eV。fcc/hcp 差仅约 0.007 eV。
- 将这个差与层数误差比较，解释为什么目前不能据此可靠宣布位点排序已经收敛。
- 在固定覆盖度下加厚 slab，并给每个位点加微小横向扰动，检查是否存在对称性保持的假驻点。
- 改气体参考只会统一平移同组吸附能；预测位点排序是否改变。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[ASE 表面构造工具](https://ase-lib.org/ase/build/surface.html) 与 [GPAW](https://gpaw.readthedocs.io/)。
