# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

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
