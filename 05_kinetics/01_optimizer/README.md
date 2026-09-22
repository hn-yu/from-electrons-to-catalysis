# 01 · 优化的是驻点，还是你希望的结构

本项目从给定初始结构寻找附近的低能驻点，学习梯度、步长选择和局部能量盆地怎样共同决定结构优化的结果。

## 背景：为什么需要这一步

电子结构计算提供 E(R)，力提供它对原子位置的下降方向。结构优化利用这些信息找到受力接近零的几何。它是一种数值搜索：每一步的位置更新服务于降低能量，并不代表原子经过了真实的物理时间。

最速下降沿负梯度移动，但势面各方向可能有很不相同的曲率。固定大步长可能越过谷底，小步长又可能进展很慢。Armijo 回溯在每一步检查实际能量是否充分下降；BFGS 则利用位移和梯度变化估计局部曲率，改善搜索方向。

这些都是局部方法。多盆地势面上，不同初始位置可能通向不同极小值；“已收敛”必须连同起点、停止条件和所得状态一起解释。先用可视化的低维模型理解这些现象，再将成熟优化器用于真实原子结构。

## 开始前需要理解的概念

- **梯度与力**：梯度指向能量上升，力为负梯度。
- **驻点**：一阶导数为零，可能是极小值、极大值或鞍点。
- **吸引盆地**：给定算法下会流向同一终点的一组初始位置。
- **线搜索**：沿已选方向决定移动多远，避免只凭固定步长猜测。
- **BFGS**：通过历史梯度变化更新曲率近似的局部优化方法。

## 本次任务：从什么得到什么

读取 Morse 初始键长和 Müller–Brown 二维初始点，手写最速下降与 Armijo 回溯，保存每一步位置、能量和梯度。对同一起点与同一解析势调用 SciPy BFGS，比较终点和残余力，并说明差异是否来自不同盆地。

## 先用一个小例子走通思路

对 $E(x)=kx^2/2$，固定步长最速下降给出 $x_{n+1}=(1-\alpha k)x_n$。只有 $0\lt \alpha k\lt 2$ 才会收敛；同一步长在软方向可用，在硬方向可能发散。

这解释了为何“步长 0.1 在一个模型有效”不能作为通用设置，也说明回溯为何要重新计算试探位置的能量。Morse 强排斥一侧正是观察这个问题的具体输入。

## 实现边界

**手写后比对**最速下降与 Armijo 回溯；**直接用 SciPy BFGS** 作为成熟优化器。比较终点、能量与梯度，不要求不同算法的迭代次数一致。真实原子结构优化直接用 ASE 优化器。

## 输入与物理模型

- [control.toml](input/control.toml)
- [mb_starts.dat](input/mb_starts.dat)
- [morse_starts.dat](input/morse_starts.dat)

`morse_starts.dat` 给出初始键长 Å，`mb_starts.dat` 给出二维 Müller–Brown 模型坐标。两种势能均以教学 eV 表示；二维坐标不是原子坐标。

令 $\mathbf g=\nabla E=-\mathbf F$，最速下降为

```math
\mathbf x_{n+1}=\mathbf x_n-\alpha\mathbf g_n.
```

Armijo 条件要求实际能量下降至少达到线性预测的一部分：

```math
E(\mathbf x-\alpha\mathbf g)\le E(\mathbf x)-c\alpha\|\mathbf g\|^2,\quad 0\lt c\lt 1.
```

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

## 分步提示与资料

[SciPy BFGS](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-bfgs.html)。

## 完成后应能解释什么

先读每条优化轨迹的能量和梯度，再比较不同起点的终点。完成后应能区分步长导致的失败、梯度实现错误与正常的多盆地行为，并解释为什么局部优化不保证全局最低能。

## 与前后项目的关系

需要 [能量/力接口](../../02_bringup/02_forces/README.md)；下一项 [动力学](../02_dynamics/README.md) 使用同样的力但遵循真实运动方程，[Hessian](../03_hessian/README.md) 则判断驻点类型。

[输入文件说明](input/README.md) · [输出阅读指南](output/README.md) · [分步提示](hints/README.md) · [全课程实现边界](../../docs/IMPLEMENTATION_BOUNDARIES.md)
