# 提示 1：换算链而不是魔法数字

先写单位消去过程：

$$E[\mathrm{kJ/mol}]=E[\mathrm{eV}]\times e[\mathrm{J/eV}]\times N_A[\mathrm{mol^{-1}}]/1000.$$

```python
energy_kj_mol = energy_ev * electron_charge * avogadro / 1000
```

如果忘了 $N_A$，得到的是单粒子的 kJ。反向换算再换回来只能检查可逆性；两个方向都错同一个常数时仍然通过，因此还必须与独立常数表比对。

检查点：1 Hartree 约等于 27.2114 eV，1000 cm⁻¹ 约等于 0.123984 eV。
