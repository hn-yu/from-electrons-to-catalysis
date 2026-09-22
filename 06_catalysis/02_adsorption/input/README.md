# 输入文件、格式与单位

从 [项目正文](../README.md) 的物理模型开始。`run.py --input` 接收本目录的副本，而不是一个 JSON 文件。

## [DATA_SOURCE.md](DATA_SOURCE.md)

模型、来源或输入约定说明。

## [baseline/H2.extxyz](baseline/H2.extxyz)

ASE 扩展 XYZ，包含坐标、晶胞及约束/额外原子属性；详见首部 Properties。

## [baseline/bridge.POSCAR](baseline/bridge.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [baseline/calculator.toml](baseline/calculator.toml)

GPAW/PBE backend、cutoff_eV、kpts、smearing_eV、fmax；长度 Å，力 eV/Å。

## [baseline/clean.POSCAR](baseline/clean.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [baseline/fcc.POSCAR](baseline/fcc.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [baseline/hcp.POSCAR](baseline/hcp.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [baseline/ontop.POSCAR](baseline/ontop.POSCAR)

VASP POSCAR；晶胞 Å、元素与原子数、Selective dynamics 约束、标明 Direct/Cartesian 的坐标。

## [cases.csv](cases.csv)

逐案例目录及模型身份；结构文件必须与该行的设置、覆盖度/电荷对应。

```csv
scenario,parameter,value,directory,coverage_ML
baseline,baseline,baseline,baseline,0.25
```

## [control.toml](control.toml)

控制参数；字段中的 eV、A、K、bar 明确单位，数组仅表示扫描或软件设置。

## [energies.csv](energies.csv)

已执行 PBE 总能量三元组；每行属于独立 scenario，eV。不可混用不同 scenario 的参考。

```csv
scenario,site,clean_eV,H2_eV,total_eV,force_max_eV_A,Hx_A,Hy_A,Hz_A
baseline,ontop,-36.842150445181304,-6.5923090093646906,-39.607194000190844,0.03319100046610585,-7.267431589112657e-20,2.448636292354312e-20,13.691902634303924
baseline,bridge,-36.842150445181304,-6.5923090093646906,-40.09024201123972,0.03947402080376796,1.2763114620834413,0.007814039663266006,13.24892898471376
```
