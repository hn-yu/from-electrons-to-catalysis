# 04 · 把真实力与弹簧力放在正确方向

直接连接两个极小值通常不是反应路径。NEB 为什么既需要弹簧，又必须去掉弹簧在垂直方向的分量？

## 实现边界

**手写后比对**二维势上的 NEB 切线、力投影和松弛，与 **ASE NEB/FIRE** 对照。原子扩展直接读 EXTXYZ 并用 ASE climbing-image NEB；示例 EMT 只演示流程，不能当作真实 H/Cu 扩散预测。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [endpoints.dat](input/endpoints.dat)
- [fcc.extxyz](input/fcc.extxyz)
- [hcp.extxyz](input/hcp.extxyz)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`endpoints.dat` 给出二维模型的两个初始点；先各自优化。`fcc.extxyz`、`hcp.extxyz` 给出 Cu/H 原子路径的两端，底层模型固定整个 Cu 衬底。

对于中间 image i，切线单位向量 $\hat\tau_i$ 沿当前路径。NEB 力为

$$\mathbf F_i^{NEB}=\mathbf F_i-(\mathbf F_i\cdot\hat\tau_i)\hat\tau_i+k(|\mathbf R_{i+1}-\mathbf R_i|-|\mathbf R_i-\mathbf R_{i-1}|)\hat\tau_i.$$

第一项让路径在垂直方向靠近 MEP，第二项维持 image 间距。沿路径最高能 image 给出离散势垒；climbing image 则反转真实力的切向分量以靠近鞍点。

二维 Müller–Brown 势缩放为教学 eV，坐标不是 Å。原子部分的 Å/eV 则由 ASE 处理，二者不能混成同一个物理势垒。


## 从公式到程序

1. 优化端点并冻结；线性插值内部 image。
2. 依据局部能量排序构造改进切线；分别计算真力垂直分量和弹簧平行分量。
3. 自写 NEB 与 ASE 使用相同端点、image 数、弹簧与停止阈值，输出路径和势垒差。
4. 原子扩展直接读取 fcc/hcp EXTXYZ，先优化端点，再运行 ASE climbing-image NEB 并保存所有 image。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 05_kinetics/04_neb/run.py --output runs/04_neb
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 二维基准势垒约 1.056 eV，当前自写/ASE 差约 0.00032 eV。加倍 image 数，分开观察离散峰值误差与力收敛误差。
- 若错误地保留真实力的切向分量，images 会往极小值聚集；画 image 间距比看一个势垒数更容易诊断。
- 原子 EMT 示例势垒约 0.0095 eV。解释为什么这个数不能用于发表 H/Cu 的实际扩散率。
- 用 Hessian 验证候选鞍点是否恰有一个相关负曲率方向；NEB 收敛本身不是完整过渡态验证。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[ASE NEB](https://ase-lib.org/ase/neb.html)。
