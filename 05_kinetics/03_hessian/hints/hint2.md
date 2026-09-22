# 提示 2：为什么是两个平方根

$H\mathbf a=\omega^2M\mathbf a$ 左乘 $M^{-1/2}$，再代入 $\mathbf q=M^{1/2}\mathbf a$，才得到普通对称本征问题。只把 H 的每一行除以质量，会得到 $M^{-1}H$；它与质量加权矩阵本征值相同但通常不对称，不应交给假定对称的 `eigh`。

```python
m = np.repeat(masses, 3)  # mO,mO,mO,mH,mH,mH,mH,mH,mH
Hmw = H / np.sqrt(m[:, None] * m[None, :])
lambda_, Q = np.linalg.eigh(Hmw)
cartesian_modes = Q / np.sqrt(m[:, None])
```

检查正规化约定：$Q^TQ=I$，而 Cartesian 位移矩阵 A 满足 $A^TMA=I$。若要绘制位移箭头，可另行缩放箭头长度；这种绘图缩放不改变频率。

同位素实验先保持 H 不变，只改 masses。若把质量乘 4 后频率没有变成原来的一半，错误就在质量或单位转换，和电子结构方法无关。
