# 案例与问题

吸附能、NEB 势垒、FES 和微观动力学输出放在同一报告里，并不自动组成一致机制。请检查它们之间的连接。


$$\dot\theta=S r(\theta,T,p),\qquad \mathrm{TOF}=r_{product},$$
$$n_A=\frac{\partial\ln\mathrm{TOF}}{\partial\ln p_A},\quad E_{app}=-k_B\frac{\partial\ln\mathrm{TOF}}{\partial(1/T)}.$$

这些整体响应包含覆盖度和储库条件。它们一般不等于某一步显式压力幂或局部电子能垒。


1. 用 input/kinetics-report.txt 检查覆盖度归一化和各步净通量一致性。
2. 解释稳态与平衡的差别，给出非零 TOF 的持续驱动来源。
3. 在一个步骤更快但 TOF 反而更慢的假设例子中指出必须检查的热力学约束。
4. 针对隐藏慢变量、位点遗漏和厚度未收敛，各写一个后续检验。
