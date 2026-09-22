# 02 · 从两原子坐标到一致的能量和力

优化器和分子动力学真正使用的是力。一个看起来平滑的能量曲线，为什么仍可能把原子推向错误方向？

## 实现边界

**手写后比对** Morse 能量、解析导数和中心差分；用 **ASE MorsePotential** 独立验证。XYZ 读写、原子容器和后续优化器直接用 ASE。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [bonds.xyz](input/bonds.xyz)
- [control.toml](input/control.toml)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`bonds.xyz` 是多帧两原子坐标，Å 为长度单位；每帧独立计算距离 $r=|\mathbf R_2-\mathbf R_1|$。

$$E(r)=D[(1-z)^2-1],\quad z=e^{-a(r-r_e)},\quad F_r=-\frac{dE}{dr}=-2Daz(1-z).$$

$D$ 的单位为 eV，$a$ 为 Å⁻¹，$r_e$ 为 Å。这里无穷远能量为零，平衡点能量为 $-D$。

$$\mathbf F_2=F_r\frac{\mathbf R_2-\mathbf R_1}{r},\qquad\mathbf F_1=-\mathbf F_2.$$

径向力不是某一个原子的固定 z 分量。ASE 的参数对应关系为 `epsilon=D, r0=re, rho0=a*re`；比较时将截断放到所有测试距离之外。


## 从公式到程序

1. 从每帧 XYZ 计算距离和单位方向，写自己的能量与两原子力。
2. 用中心差分估算同一距离处的径向力。不能把数值梯度和力混为一谈。
3. 给同一 ASE Atoms 挂上 MorsePotential；比较能量、第二个原子力在键方向的投影。
4. 输出 scan.csv 的六列，说明解析值、差分值和库值各来自哪条路径。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 02_bringup/02_forces/run.py --output runs/02_forces
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 在平衡距离两侧选点：短键应排斥，长键应吸引。平衡点 F=0 只能检查一个特殊位置。
- 将整个分子平移并旋转 37°；能量不变，力随坐标旋转。固定 z 方向的错误代码会在这里暴露。
- 给能量统一加常数 10 eV，预测力、振动频率和优化终点是否改变。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[ASE MorsePotential 源码](https://ase-lib.org/_modules/ase/calculators/morse.html)。
