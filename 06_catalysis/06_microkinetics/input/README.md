# 输入说明

本项目将基元反应速率与表面覆盖度耦合，求稳态周转频率，并解释温度和压力响应为什么不能仅由某个单步势垒判断。

## 这些输入用于哪项任务

读取同一三状态机制与温压扫描表，手写质量作用 RHS 和稳态矩阵，用归一化条件替换一个冗余方程。分别通过直接稳态解、SciPy BDF 积分和 Cantera 原生 YAML 得到覆盖度与 TOF；每次改变 T/p 都重新求稳态，再计算整体响应。

## 阅读文件前先核对一个具体例子

600 K、pA=1 bar、pB=0.01 bar 时，示例覆盖度约为 $(0.002875,0.951428,0.045697)$。表面约 95% 时间处于 A*，空位只有约 0.29%；这会直接限制需要空位的吸附事件。

若忽略逆反应写 r≈k₁pAθ*，只有 θ* 随压力几乎不变时才近似一阶。升压同时压低空位比例时，速率增长可能趋于饱和，必须由重新求解后的覆盖度来判断。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [mechanism.yaml](mechanism.yaml)

Cantera 原生 gas+surface 机制；SI m、kmol、s，能垒 J/kmol，参考压力 1 bar。

## [pressures.csv](pressures.csv)

逗号分隔表；第一行为字段与单位，数值不可脱离列名解释。

```csv
p_bar
0.01
0.1
```

## [states.csv](states.csv)

状态及能量；动力学 G0_eV 为相对标准自由能，相图 energy_eV 为明确合成教学数据。

```csv
state,G0_eV
vacancy,0.0
A_ads,-0.3
```

## [temperatures.csv](temperatures.csv)

逗号分隔表；第一行为字段与单位，数值不可脱离列名解释。

```csv
T_K
400
600
```

## [transitions.csv](transitions.csv)

逗号分隔表；第一行为字段与单位，数值不可脱离列名解释。

```csv
step,TS_eV
1,0.15
2,0.45
```

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
