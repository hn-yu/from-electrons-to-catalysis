# 提示 2：向量范数与概率积分

求解器不知道 bohr，也不知道积分权重。直接画它给出的系数，网格加密时振幅会改变。

$$\int |\psi|^2dx\approx h\sum_i|\psi_i|^2.$$

```python
psi = eigenvectors / np.sqrt(h)
assert np.allclose(h * np.sum(psi**2, axis=0), 1)
```

波函数整体乘 −1 不改变物理。比对两次本征向量前可先按重叠调整符号，简并子空间则要比较投影算符。
