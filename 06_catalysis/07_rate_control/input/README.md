# 输入说明

本项目通过单独扰动过渡态并重新求稳态，量化每一步对整体速率的控制程度，检验“最高局部势垒就是决速步”的直觉。

## 这些输入用于哪项任务

本项目使用专门构造的 states.csv 与 transitions.csv，能量不同于上一项默认案例。先记录局部势垒排序，再手写 ±δ 过渡态扰动和稳态重算，得到 Xi；用 Cantera 的倍率扰动独立核对，并检查统一时间缩放给出的求和关系。

## 阅读文件前先核对一个具体例子

本例局部正向势垒约为 0.65、0.90、0.55 eV，最大的是第二步；但计算得到 Xi 约为 0.02558、0.00294、0.97148，第三步的控制度最大。

这并不表示第二步的势垒算错，而是表面人口和逆反应改变了局部速率对净通量的影响。把所有反应正逆速率统一乘 2，只会将稳态循环的时钟加快两倍，因此 TOF 也乘 2，给出本模型中 Xi 求和约为 1 的检查。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [mechanism.yaml](mechanism.yaml)

Cantera 原生 gas+surface 机制；SI m、kmol、s，能垒 J/kmol，参考压力 1 bar。

## [states.csv](states.csv)

状态及能量；动力学 G0_eV 为相对标准自由能，相图 energy_eV 为明确合成教学数据。

```csv
state,G0_eV
vacancy,0.0
A_ads,-0.7
```

## [transitions.csv](transitions.csv)

逗号分隔表；第一行为字段与单位，数值不可脱离列名解释。

```csv
step,TS_eV
1,0.65
2,0.2
```

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
