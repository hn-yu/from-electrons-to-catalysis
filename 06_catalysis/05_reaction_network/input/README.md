# 输入说明

本项目把状态与过渡态自由能转换成守恒、满足详细平衡的可逆反应网络，为后续覆盖度和催化速率计算建立一致输入。

## 这些输入用于哪项任务

从 states.csv 与 transitions.csv 手写两方向 TST 常数和计量矩阵，检查详细平衡与位点守恒。Cantera 直接读取独立的原生 mechanism.yaml 并求稳态，核对覆盖度和各步通量；修改能量表时显式更新 YAML，保证比较的是同一个模型。

## 阅读文件前先核对一个具体例子

设一步反应两端自由能为 0 和 −0.3 eV，过渡态为 +0.15 eV。正向势垒为 0.15 eV，逆向为 0.45 eV，所以速率常数比为 $e^{0.3/(k_BT)}$。

把过渡态升高 0.1 eV，两方向速率都减慢，但比值不变。若只减慢正向，则相当于改变了平衡常数，不能再声称两端热力学完全不变。

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [mechanism.yaml](mechanism.yaml)

Cantera 原生 gas+surface 机制；SI m、kmol、s，能垒 J/kmol，参考压力 1 bar。

## [states.csv](states.csv)

状态及能量；动力学 G0_eV 为相对标准自由能，相图 energy_eV 为明确合成教学数据。

```csv
state,G0_eV
vacancy,0.0
A_ads,-0.3
```

## [transitions.csv](transitions.csv)

逗号分隔表；第一行为字段与单位，数值不可脱离列名解释。

```csv
step,TS_eV
1,0.15
2,0.45
```

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
