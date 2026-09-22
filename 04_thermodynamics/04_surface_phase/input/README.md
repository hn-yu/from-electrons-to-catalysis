# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

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
