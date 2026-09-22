# 01 · 优化的是驻点，还是你希望的结构

更快地找到一个极小值不等于找到正确的物理状态。用 Morse 和多盆地势面，区分步长、收敛判据与初始构型的作用。

## 实现边界

**手写后比对**最速下降与 Armijo 回溯；**直接用 SciPy BFGS** 作为成熟优化器。比较终点、能量与梯度，不要求不同算法的迭代次数一致。真实原子结构优化直接用 ASE 优化器。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [mb_starts.dat](input/mb_starts.dat)
- [morse_starts.dat](input/morse_starts.dat)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`morse_starts.dat` 给出初始键长 Å，`mb_starts.dat` 给出二维 Müller–Brown 模型坐标。两种势能均以教学 eV 表示；二维坐标不是原子坐标。

令 $\mathbf g=\nabla E=-\mathbf F$，最速下降为

$$\mathbf x_{n+1}=\mathbf x_n-\alpha\mathbf g_n.$$

Armijo 条件要求实际能量下降至少达到线性预测的一部分：

$$E(\mathbf x-\alpha\mathbf g)\le E(\mathbf x)-c\alpha\|\mathbf g\|^2,\quad 0<c<1.$$

BFGS 从相邻步的位移与梯度变化近似逆 Hessian，因而可以修正各方向曲率尺度，但仍然是局部算法。


## 从公式到程序

1. 在每一步输出 E、力范数和位置；失败时明确报告未达到收敛。
2. 从 α=0.1 开始不断折半，直到满足 Armijo 条件。
3. 对每一个相同初始点调用 SciPy BFGS，用相同解析梯度。
4. 若终点不同，先确定是不是落入不同盆地，再判断算法是否错误。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 05_kinetics/01_optimizer/run.py --output runs/01_optimizer
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 把 Morse 初态推到强排斥区，固定大步长会发生什么？回溯为何能改善？
- 从 Müller–Brown 不同盆地出发，记录各极小值能量；“所有运行都收敛”仍不证明全局极小。
- 同时缩放某个坐标与相应势参数，观察最速下降的条件数问题，再看 BFGS 的改善。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[SciPy BFGS](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-bfgs.html)。
