# 输入说明

本项目比较 H 在 Cu(111) 上的 atop、bridge、fcc 和 hcp 起始位点，把吸附能排序与优化后的真实结构、受力和数值误差联系起来。

## 这些输入用于哪项任务

读取基准 2×2×3、0.25 ML 的四个 POSCAR 与真实 PBE 能量表，自己重新计算吸附能和相对位点差，检查输出的最终 H 坐标与最大力。新增计算由 ASE/GPAW 完成，并保存 relaxed.extxyz 与原始日志供结构核对。

## 阅读文件前先核对一个具体例子

已有 fcc 与 hcp 吸附能约 −0.0898 和 −0.0827 eV，fcc 低约 0.0071 eV。这是当前设置中的排序；还需要在相同覆盖度下加厚 slab 等，判断这 7 meV 是否稳定。

若只更换同组共同 H₂ 参考，四个吸附能一起平移，位点差保持不变。若某个结构优化后从 bridge 移到了 hollow，则它的最终能量应按最终结构解释，而不能仅按输入文件名分类。

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

[返回完整背景与公式](../README.md) · [查看结果怎样解释](../output/README.md)
