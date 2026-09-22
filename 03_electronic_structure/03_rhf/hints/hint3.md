# 提示 3：电子数是第一个物理检查

对正交归一的占据 MO，$C_{occ}^TSC_{occ}=I$，所以

$$
\mathrm{Tr}(DS)=2\mathrm{Tr}(C_{occ}^TSC_{occ})=2n_{occ}=N_e.
$$

这里使用 trace 的循环性质。AO 自身不正交，所以 `trace(D)` 缺少了重叠度量 S。

```python
Cocc = C[:, :nelectron // 2]
D = 2.0 * Cocc @ Cocc.T
ne_check = np.trace(D @ S)
```

H₂ 与 HeH⁺ 都有两个电子，但不具有相同的核吸引 Hamiltonian。相同占据数不意味着相同能量。

把这个检查放在每轮更新之后。如果电子数从第一轮就错，优先检查占据列、factor 2 和正交化；不要通过调整收敛阈值“修复”电子数。对已收敛 RHF，还可检查 $DSD\approx2D$，它来自双占据投影密度的幂等性质。
