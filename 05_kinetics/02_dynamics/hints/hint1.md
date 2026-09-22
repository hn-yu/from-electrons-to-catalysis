# 提示 1：两次力对应两个不同位置

新力必须在已经更新的位置上计算：

```python
x += dt * v + 0.5 * dt**2 * force / mass
new_force = potential.force(x)
v += 0.5 * dt * (force + new_force) / mass
force = new_force
```

如果两次都用旧力，就不是 Velocity Verlet。多原子质量数组应扩展为 `(N,1)`，使三个笛卡尔方向使用同一原子质量。
