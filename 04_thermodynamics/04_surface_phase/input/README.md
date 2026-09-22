# 输入说明

本项目比较能与气体交换 H 原子的三种表面状态，学习用巨势而不是裸总能确定给定化学势下最稳定的覆盖度。

## 这些输入用于哪项任务

ASE 读取三个 POSCAR，核对 H 原子数与 states.csv。你手写 Ω 直线、解析交点和全局稳定性筛选，再和离散扫描比较。states.csv 的 0、−0.5、−0.7 eV 是人为指定的模型能量；结构负责明确组成，不代表这些能量来自 DFT。

## 阅读文件前先核对一个具体例子

在 $\mu=-0.35$ eV 时，clean 的 Ω 为 0，half 的 Ω 为 $-0.7-2(-0.35)=0$。但 quarter 的 Ω 为 $-0.5-(-0.35)=-0.15$ eV，更低。

所以 clean/half 的交点不是相界。实际相界在 −0.5 和 −0.2 eV，中间有 quarter 稳定区间。把所有交点直接画成相界，会得到一个代数求解正确、物理选择错误的相图。

## [clean.POSCAR](clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [half.POSCAR](half.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [quarter.POSCAR](quarter.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [states.csv](states.csv)

状态及能量；动力学 G0_eV 为相对标准自由能，相图 energy_eV 为明确合成教学数据。

```csv
name,energy_eV,adsorbates
clean,0.0,0
quarter,-0.5,1
```

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
