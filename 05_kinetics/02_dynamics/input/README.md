# 输入说明

本项目手写 Velocity Verlet 积分器，从坐标、质量和动量生成经典轨迹，并用守恒量与 ASE 的独立积分器检验时间推进。

## 这些输入用于哪项任务

第一部分扫描约化单位谐振子的时间步长，观察稳定边界。第二部分读取 cluster.extxyz 的位置、质量、动量，自己推进 LJ 双粒子，再让 ASE VelocityVerlet 使用相同力接口和初态，逐帧比较轨迹。Ar 是标签，实际使用输入规定的教学质量和 LJ 参数。

## 阅读文件前先核对一个具体例子

约化谐振子取 m=k=1，所以 ω=1。Velocity Verlet 的线性稳定条件为 $\omega\Delta t\lt 2$；把步长调到超过 2 后，失稳来自离散推进，而不是弹簧突然变成了不稳定物理模型。

真实单位的双粒子案例另有时间换算：ASE 内部时间数值不能直接标为 fs。两个积分器使用同样错误的标签仍可能彼此一致，因此还要检查单位和守恒量。

## [cluster.extxyz](cluster.extxyz)

坐标 Å、显式质量 u、动量/速度遵循 ASE 内部单位；模型参数不代表真实 Ar。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [timesteps.csv](timesteps.csv)

逗号分隔表；第一行为字段与单位，数值不可脱离列名解释。

```csv
dt_reduced
0.01
0.05
```

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
