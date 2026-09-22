# 03 · 从有偏轨迹恢复自由能

每个窗口都采到了数据，为什么拼起来仍可能得到错误自由能？本项目同时考察重加权算法和隐藏慢变量。

## 实现边界

**手写后比对** Metropolis 与直方图 WHAM；对同一批轨迹用 **PyMBAR FES** 独立重加权。实际原子轨迹应由成熟 MD/偏置软件产生，本例解析二维势用来知道正确边缘自由能。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [windows.csv](input/windows.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


`windows.csv` 每行给出中心 $c_k$ 和弹簧 $K_k$，模型坐标无量纲，K 的单位为 eV。窗口偏置 $W_k(x)=K_k(x-c_k)^2/2$。

$$U(x,y)=0.15(x^2-1)^2+(1+x^2)y^2.$$

积分掉 y 得到（差一个任意常数）

$$F(x)=0.15(x^2-1)^2+\frac{k_BT}{2}\ln(1+x^2)+C.$$

WHAM 的分箱概率自洽方程为

$$p_b=\frac{\sum_kn_{kb}}{\sum_kN_k\exp[\beta(f_k-W_{kb})]},\quad e^{-\beta f_k}=\sum_bp_be^{-\beta W_{kb}}.$$

零计数箱没有自由能信息，不能用零填充。PyMBAR 使用各真实样本位置处的偏置，WHAM 使用箱中心偏置，因此两者在有限箱宽下不要求逐位相等。


## 从公式到程序

1. 每个窗口做有偏 Metropolis，丢弃 burn 步后保存 window-XX.csv 轨迹。
2. 对同一组 bins 统计 counts，用对数域 WHAM 求 p 与 F。
3. 构造每个样本在全部窗口下的 reduced potential u_kn，交给 PyMBAR FES。
4. 保存 F-comparison.csv、窗口接受率和隐藏坐标均值；只在采样充分区域对齐常数后比较曲线形状。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 06_catalysis/03_umbrella/run.py --output runs/03_umbrella
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 当前同样本 WHAM/PyMBAR 的形状 RMS 差约为 0.00005 eV（一维）与 0.00015 eV（二维）；缩小箱宽会改变离散偏差和统计噪声。
- 将相邻窗口间距加大，观察重叠消失；求解器停止迭代并不能保证所有自由能盆地有可靠连接。
- bad_coordinate 示例从 y=−1 和 +1 出发，x 可以重叠但 y 不跨越。解释为什么漂亮的一维直方图无法证明整体平衡。
- 增加独立随机种子、分析相关时间，再讨论误差条；当前示例不把每个相邻轨迹点当独立样本。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[PyMBAR FES 官方接口](https://pymbar.readthedocs.io/en/4.0.2/fes_with_pymbar.html)。
