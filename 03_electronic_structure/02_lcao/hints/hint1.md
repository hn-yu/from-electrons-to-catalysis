# 提示 1：为什么逆矩阵乘 H 不是首选

形式上 $S^{-1}Hc=\varepsilon c$，但 $S^{-1}H$ 一般不是普通欧氏度量下的对称矩阵。

若把它交给只读取半边矩阵的 `eigh`，可能得到完全错误的答案。

通过 $X^THX$ 得到真正对称的矩阵，避免显式求逆。

```python
w, u = np.linalg.eigh(S)
X = (u / np.sqrt(w)) @ u.T
```
