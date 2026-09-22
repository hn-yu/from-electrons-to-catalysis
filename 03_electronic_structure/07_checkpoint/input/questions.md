# 案例与问题

现在给你一个收敛的 RHF 能量和一条拉伸曲线。你能区分输入错误、数值错误和方法失效吗？


RHF 的关键不变量是

$$\mathrm{Tr}(DS)=N_e,\quad X^TSX=I,\quad FDS-SDF\rightarrow0,$$
$$E_{tot}=\tfrac12\mathrm{Tr}[D(H+F)]+E_{NN}.$$

这些关系检验算法的一致性；UHF 的 $\langle S^2\rangle$、有限基组 FCI 与周期收敛趋势检验的是其他层次。


1. 用 input/scf-report.txt 的 H₂O 案例核对电子数、核排斥和最终总能。
2. 解释若能量看似收敛但 Tr(DS)=5 而不是 10，最可能混用了哪种密度约定。
3. 给“RHF 收敛，所以 H₂ 解离正确”的结论写反例。
4. 为周期晶格常数建立 k 点与截断的分开收敛计划，说明分子 SCF 测试不能覆盖什么。
