# 提示 2：中心差分的能量步长与对数倍率

手写路径使用能量 δ：

$$X_i\approx-k_BT[\ln r(G_i^\ddagger+\delta)-\ln r(G_i^\ddagger-\delta)]/(2\delta).$$

Cantera 路径使用 h=δ/kBT 的对数倍率，方向相反。两种表达经负号后应一致。

若两边步长不同，只能要求在差分误差容限内一致，而非末位完全相同。
