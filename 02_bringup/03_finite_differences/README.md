# 03 · 为什么更小的差分步长反而更差

本项目主动破坏一个正确的力计算：从截断误差主导区走到浮点消减主导区，建立选择步长的方法。

## 实现边界

**手写**中心差分和误差扫描；解析 Morse 力作为独立公式基准。NumPy 提供数组和浮点运算，画图可直接用 Matplotlib；不需要调用另一套差分包装器来掩盖误差来源。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [bonds.xyz](input/bonds.xyz)
- [control.toml](input/control.toml)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


对 XYZ 给出的距离 $r$，中心差分为

$$F_h=-\frac{E(r+h)-E(r-h)}{2h}=F(r)-\frac{E′′′(r)}{6}h^2+O(h^4).$$

上式三阶导数项解释了理想的二阶收敛。浮点相减则引入约 $\epsilon_{\rm mach}|E|/h$ 的误差，因此总误差的模型为

$$\varepsilon(h)\approx Ah^2+B\epsilon_{\rm mach}/h.$$

`control.toml` 指定对数步长范围与采样点数。几何距离由 `bonds.xyz` 读取，不能继续使用硬编码位置。


## 从公式到程序

1. 对每个 h 重新求两侧能量，用解析力算绝对误差。
2. 在 log–log 坐标画误差对 h；在大 h 区估计斜率是否接近 2。
3. 查最优 h 所在量级，再检查极小 h 时两个能量是否已被舍入成同一个数。
4. 保留每一个采样点，不要只输出“最佳步长”。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 02_bringup/03_finite_differences/run.py --output runs/03_finite_differences
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 在平衡点与非平衡点各扫描一次；近零导数的相对误差会失去意义，改看绝对误差。
- 对能量加一个很大的常数再差分：解析力不变，差分舍入误差却可能变大。
- 模拟电子结构能量噪声，并预测最优步长向哪边移动；梯度验证必须考虑 SCF 精度。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

本项目的基准公式来自上一项目 Morse 势；浮点工具见 [NumPy spacing](https://numpy.org/doc/stable/reference/generated/numpy.spacing.html)。
