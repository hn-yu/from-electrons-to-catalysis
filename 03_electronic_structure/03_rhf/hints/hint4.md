# 提示 4：给每个求和指标一个明确位置

先写出一个元素：

$$
F_{pq}=h_{pq}+\sum_{rs}D_{rs}[(pq|rs)-\tfrac12(pr|qs)].
$$

p、q 是自由指标，决定输出元素；r、s 是被求和的指标。最直接的四重循环虽然慢，但很适合先排除指标错误。

```python
F = h.copy()
for p in range(n):
    for q in range(n):
        for r in range(n):
            for s in range(n):
                F[p, q] += D[r, s] * (eri[p, q, r, s]
                                     - 0.5 * eri[p, r, q, s])
```

确认后可以写成：

```python
J = np.einsum('pqrs,rs->pq', eri, D)
K = np.einsum('prqs,rs->pq', eri, D)
F = h + J - 0.5 * K
```

不要从记忆随意更换字符串，先把每个位置与上面的式子对应。检查 J、K、F 都是对称矩阵；再用同一个任意对称 D 比较四循环与张量收缩。这样不依赖最终 SCF 是否收敛，就能验证 Fock build。
