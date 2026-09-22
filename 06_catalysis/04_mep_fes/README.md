# 04 · 最低能量路径为什么不是自由能路径

两个位置的最低势能相同，但一个位置允许更多横向涨落，它们在有限温度下还等价吗？

## 实现边界

**手写**横向高斯积分与熵项；**用 SciPy quad 独立积分比对**。这个解析模型服务于理解 NEB 与采样的区别，真实自由能不应由最低能量路径直接冒充。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [temperatures.csv](input/temperatures.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


模型与上一项目一致：$U(x,y)=V(x)+(1+x^2)y^2$，$V(x)=0.15(x^2-1)^2$。

沿 y 最小化给出 MEP：$y=0,E_{MEP}(x)=V(x)$。而边缘自由能是积分：

$$e^{-\beta F(x)}\propto\int_{-\infty}^{\infty}e^{-\beta U(x,y)}dy=e^{-\beta V(x)}\sqrt{\frac{\pi k_BT}{1+x^2}},$$
$$F(x)=V(x)+\frac{k_BT}{2}\ln(1+x^2)+C(T).$$

$C(T)$ 与 x 无关，可在同一温度比较势垒时消去。不同温度下不能任意比较被分别平移后的绝对自由能。


## 从公式到程序

1. 读温度表，计算 V(x) 和解析 F(x)。
2. 对每个 x 用 SciPy quad 对 y 从负无穷到正无穷积分，独立恢复 F。
3. 每个温度分别减去实际最低 F；不要把 0 K 的 x=±1 固定当成有限温最低点。
4. 输出每温度的 MEP、解析 F、积分 F 与最大误差。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 06_catalysis/04_mep_fes/run.py --output runs/04_mep_fes
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 提高温度，预测中央区域更宽的横向分布如何降低自由能势垒。
- 将横向曲率改为常数，F 与 MEP 应只相差一个与 x 无关的常数。
- 通过求导推算自由能极小值的移动，再与离散网格最小值比较。
- 解释 NEB 收敛和 FES 采样收敛各自回答了哪一个数学问题。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[SciPy quad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html)。
