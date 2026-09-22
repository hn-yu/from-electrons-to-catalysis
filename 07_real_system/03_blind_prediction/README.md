# 03 · 保留真正的事前与事后记录

这个案例的结果已经公开。任务是审查历史预测的价值，并为尚未执行的下一轮计算制定新的预测。

## 这个项目应该自己完成什么

本项目要求**手写推理、量纲检查和可否定的判断**。引用前面计算项目的成熟软件结果；不把讨论题包装成返回 true/false 的脚本。必要算术可以使用 NumPy，电子结构、采样与动力学仍由对应项目的软件完成。

## 输入案例

- [prediction-template.md](input/prediction-template.md)

- [historical-prediction.md](input/historical-prediction.md)


历史区间：$E_{ads}\in[-0.8,+0.3]$ eV，低置信度。容限：0.05 eV。区间覆盖度与数值收敛是两个不同命题。

$$\Delta_{layers}=E_{ads}^{4L}-E_{ads}^{3L}.$$

不要用已知的 Δlayers 来伪造一条声称更早写下的精确预测。


## 作业步骤

1. 阅读 input/historical-prediction.md，分别识别原始预测与追加的 postmortem。
2. 评价这个区间能回答“吸附符号是否可靠”吗？
3. 为 5/6 层的未执行实验填 prediction-template.md，给出物理理由、容限和失败标准。
4. 说明如何保留原条目，再追加实际测量；没有计算时不得填写测量值。

将回答写入自己的 `runs/03_blind_prediction/answer.md`，保留输入数据、公式、计算出的数值与结论范围。先完成回答，再查看 [参考分析](output/answer.md)。历史回答保存在 output/previous-answer.md；其中事前预测与事后测量不能互换身份。

## 提示

[逐步提示](hints/README.md) 给出三个具体推理环节。完整课程的 [实现边界表](../../docs/IMPLEMENTATION_BOUNDARIES.md) 解释哪些工作应交给库。
