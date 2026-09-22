# 案例与问题

一张吸附电子能表能否直接变成温压相图？你需要补足哪些项，哪些项能够抵消？


$$\Delta G(T,p)=\Delta E_{elec}+\Delta ZPE+\Delta H_{thermal}-T\Delta S,$$
$$\mu(T,p)=\mu^\circ(T)+k_BT\ln(p/p^\circ).$$

若 μ° 已经包含气体 ZPE 与热修正，反应式中不能再重复加入这些气体项。


1. 读取 input/thermochemistry.csv，解释每一列进入 H、S、G 的位置。
2. 对 600 K、压力增加十倍，手算气体 μ 变化与吸附 ΔG 的变化方向。
3. 写出线性 CO₂ 和非线性 H₂O 应有的内部模式数及旋转对称数。
4. 给出一种电子吸附能负、自由吸附能正的温压条件，并声明使用的近似。
