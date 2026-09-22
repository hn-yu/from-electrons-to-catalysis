# 提示 1：先检查原胞归一化

ASE 读取的 CIF 可能是原胞，也可能是常规胞。可靠的每原子量是

```python
volume_per_atom = atoms.get_volume() / len(atoms)
energy_per_atom = atoms.get_potential_energy() / len(atoms)
a = (4 * volume_per_atom)**(1/3)
```

若只把体积除以原子数，却不处理能量，体模量会带入错误因子。比较不同胞之前先统一这两个归一化。
