# 提示 2：在哪一种度量下归一化

AO 系数不同于正交基系数。把 $c=Xc'$ 代入：

$$c^TSc=c'^TX^TSXc'=c'^Tc'=1.$$

检查每一列的范数与不同列之间的重叠：

```python
metric_overlap = C.T @ S @ C
```

只检查 `np.linalg.norm(C[:,i])` 会误判正确结果。
