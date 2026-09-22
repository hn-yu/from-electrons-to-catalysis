# 02 · 吸附位点竞争与参考态

本项目比较 H 在 Cu(111) 上的 atop、bridge、fcc 和 hcp 起始位点，把吸附能排序与优化后的真实结构、受力和数值误差联系起来。

## 背景：为什么需要这一步

一个表面可提供多个局部成键环境：原子正上方、两原子之间、三重空位等。不同环境改变电子结构和几何松弛，形成不同的候选吸附态。比较位点是构建表面反应网络的前提，因为网络节点首先需要对应可辨认的物理状态。

起始结构的文件名只标记如何放置吸附物。优化后原子可能迁移到另一位点，也可能因严格对称而留在不稳定驻点。判断位点身份要看最终坐标、邻近原子和残余力，必要时再做扰动或 Hessian 检查。

本例共享清洁表面与 H₂ 参考，因此同组位点差中这些项消去。然而，几个 meV 的位点差只有在相关数值误差更小时才有可信排序；许多有效数字不能代替收敛证据。

## 开始前需要理解的概念

- **atop / ontop**：吸附物位于一个表面原子上方。
- **bridge**：吸附物位于两个相邻表面原子之间。
- **fcc 与 hcp hollow**：都为三重空位，但下方原子层的堆垛位置不同。
- **结构松弛**：允许未固定原子移动到局部驻点。
- **共同参考抵消**：只适用于相同组成、同一参考和可比计算条件的能量差。

## 本次任务：从什么得到什么

读取基准 2×2×3、0.25 ML 的四个 POSCAR 与真实 PBE 能量表，自己重新计算吸附能和相对位点差，检查输出的最终 H 坐标与最大力。新增计算由 ASE/GPAW 完成，并保存 relaxed.extxyz 与原始日志供结构核对。

## 先用一个小例子走通思路

已有 fcc 与 hcp 吸附能约 −0.0898 和 −0.0827 eV，fcc 低约 0.0071 eV。这是当前设置中的排序；还需要在相同覆盖度下加厚 slab 等，判断这 7 meV 是否稳定。

若只更换同组共同 H₂ 参考，四个吸附能一起平移，位点差保持不变。若某个结构优化后从 bridge 移到了 hollow，则它的最终能量应按最终结构解释，而不能仅按输入文件名分类。

## 实现边界

**直接用 ASE/GPAW** 求四个位点与气体/清洁表面的能量和力；**手写**化学计量、位点排序及可靠性分析。EMT 只保留为历史流程示例，当前主数据是 PBE。

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

基准目录提供 2×2×3 Cu(111)、一个 H，覆盖度 0.25 ML。ontop/bridge/fcc/hcp 的 POSCAR 是起始构型；输出 H 的最终坐标和残余力用于检验位点身份。

```math
E_{ads}^{(i)}=E_{slab+H}^{(i)}-E_{slab}-\tfrac12E_{H_2},
```

```math
\Delta E_{ij}=E_{ads}^{(i)}-E_{ads}^{(j)}.
```

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

## 分步提示与资料

[ASE 表面构造工具](https://ase-lib.org/ase/build/surface.html) 与 [GPAW](https://gpaw.readthedocs.io/)。

## 完成后应能解释什么

把能量表与最终结构对应起来读，再检查位点差相对于未解决误差的大小。完成后应能说明“哪个起点能量最低”和“哪个稳定吸附态最可靠”之间还需要哪些结构与收敛证据。

## 与前后项目的关系

承接 [slab 收敛](../01_slab/README.md)；[NEB](../../05_kinetics/04_neb/README.md) 可连接已核实的位点，[反应网络](../05_reaction_network/README.md) 需要这样的状态定义。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
