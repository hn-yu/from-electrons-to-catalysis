# 04 · 用巨势比较不同覆盖度

含有不同吸附原子数的两个 slab，为什么不能只比较总能量大小？本项目构造一个可以逐条求交点的表面相图。

## 实现边界

**手写**组成核对、巨势直线、交点与下包络；**直接用 ASE** 读 POSCAR。输入状态能量是人为指定的可解模型，不宣称来自这些结构的 DFT。真实材料的电子能应由 GPAW 提供。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [clean.POSCAR](input/clean.POSCAR)
- [control.toml](input/control.toml)
- [half.POSCAR](input/half.POSCAR)
- [quarter.POSCAR](input/quarter.POSCAR)
- [states.csv](input/states.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


三个 POSCAR 是相同面积的 Cu slab，含 0、1、2 个 H。`states.csv` 给出的相对能量为 0、−0.5、−0.7 eV，供本模型练习。

$$\Omega_i(\mu)=E_i-N_i\mu,\qquad i_{stable}=\arg\min_i\Omega_i.$$

若要转为表面自由能，所有相同面积 A 的结果同时除以 A；这里的差值只涉及一侧吸附，不能机械除以 2A。

两态交点满足

$$\mu_{ij}=(E_i-E_j)/(N_i-N_j).$$

0/1 吸附原子交点为 −0.5 eV，1/2 为 −0.2 eV。0/2 的直接交点 −0.35 eV 不在下包络上，因为中间覆盖度更稳定。


## 从公式到程序

1. 从 POSCAR 数 H 原子，与 states.csv 的 adsorbates 列核对。
2. 对每个 μ 计算所有巨势，输出每条直线而不只输出胜者。
3. 解析求所有两两交点，再判断交点是否属于全局下包络。
4. 用 phase.csv 检查扫描的离散转变点与解析交点相差是否小于一个网格步长。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 04_thermodynamics/04_surface_phase/run.py --output runs/04_surface_phase
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 提高单吸附态能量，使它离开下包络，观察相图怎样跳过一个覆盖度。
- 对所有状态能量加常数，不改变相界；若给每个吸附原子加同一能量，则相界整体平移。
- 增加构型熵前先解释当前图代表零温离散有序态比较，不能把突变线当作完整有限温相变。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[ASE VASP/POSCAR 读写](https://ase-lib.org/ase/io/formatoptions.html#vasp)。
