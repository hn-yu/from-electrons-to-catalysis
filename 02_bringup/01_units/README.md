# 01 · 让单位在公式两边闭合

为什么 1 eV 的误差对某些电子结构总能量很小，却足以把催化速率改变许多个数量级？本项目从量纲和热能标尺建立判断力。

## 实现边界

**手写**量纲换算链和热能、指数敏感性；**直接用库**读取物理常数；**做后比对**自己的换算与 ASE units。不要重写单位数据库，也不要把不同量纲都塞进同一个无标签浮点数。

完整课程的分工见 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md)。先根据下面的公式完成自己的版本，再打开 [参考实现](run.py)；共享数值核心位于 [src/catalysis](../../src/catalysis)。调用库时也要写出输入、输出与物理约定。

## 输入与物理模型

- [control.toml](input/control.toml)
- [conversions.csv](input/conversions.csv)
- [temperatures.csv](input/temperatures.csv)


`control.toml` 只放控制参数；几何、矩阵、能级、轨迹和反应机制分别保存在可检查的科学文件中。修改输入前复制整个 input 目录，保持原始案例可核对。


能量可以按每个粒子或每摩尔报告。设 $N_A$ 为阿伏伽德罗常数：

$$1\ {\rm eV/particle}=eN_A/1000\ {\rm kJ/mol}\simeq96.4853\ {\rm kJ/mol}.$$

振动波数 $\tilde\nu$ 是长度倒数，先乘光速得到频率，再乘普朗克常数：

$$E=hc\tilde\nu,\qquad k_BT=(8.617333262\times10^{-5}\ {\rm eV/K})T.$$

`conversions.csv` 的三列是数值、源单位、目标单位。`temperatures.csv` 是 K；不要将电子展宽参数当作这个热力学温度。

对同一个前因子，势垒误差 $\delta E$ 导致 $k(E+\delta E)/k(E)=\exp[-\delta E/(k_BT)]$。这是随后选择数值精度的物理依据。


## 从公式到程序

1. 给每种输入单位列出到所属量纲基准的比例；先验证源、目标属于同一量纲。
2. 每条换算同时打印自己的值、ASE 的值和差。常数版本不同可能产生末位差别。
3. 对 300 K 和 600 K 输出 kBT，再算 0.05、0.1 eV 势垒误差导致的速率比。

从仓库根目录运行，计算集群上提交 Slurm：

```bash
sbatch scripts/slurm.sh 02_bringup/01_units/run.py --output runs/01_units
```

个人电脑可在已安装环境中用 `python` 替代 `sbatch scripts/slurm.sh`。`--input` 接收输入目录。先看 [output/report.txt](output/report.txt)，再检查 [output/README.md](output/README.md) 所列中间量；JSON 只保留可追溯记录，读懂结果不需要解析它。

## 应当做的实验

- 把 `1 bar → Pa` 手算成 100000，检查程序。把 bar 转 eV 应当报错；常数表里都有这两个名称不代表允许相除。
- 300 K 的 kBT 约 0.02585 eV，600 K 约 0.05170 eV。预测温度翻倍时，固定势垒误差的影响如何改变。
- 分别解释“每摩尔吸附事件”和“每个表面原胞”对应的归一化，不能只把标签统一成 eV。

每次记录“改变的唯一因素→预期符号或量级→实际变化→仍不能得出的结论”。参考输出是已执行的示例，不是你尚未运行实验的盲预测。

## 分步提示与资料

先尝试后再依次打开 [提示](hints/README.md)。提示给出推导、局部代码和出错时的诊断，不代替解释自己的输出。

[ASE 单位体系](https://ase-lib.org/ase/units.html)；实际常数版本写入输出记录。
