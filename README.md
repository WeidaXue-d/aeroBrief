# AeroBrief: Flight Brief + AI Delay Predictor (Day 1)

> **MVP (Day 1)** — A tiny, local script that generates a flight brief and outputs a *baseline* delay risk score (rule-based).  
> 后续会逐步替换为基于真实数据的 ML 模型。

##  Why this project / 项目意义
- 将**飞行运行简报**（航班信息、机场天气、时间窗口）与**延误风险预测**结合，形成可落地的飞行前辅助工具。



示例输出（示意）：
```
[BRIEF] CA123 ZBAA → ZSPD (2025-09-20 08:30 → 10:45)
[WEATHER] DEP(MVFR), ARR(IFR, RA)
[BASELINE DELAY RISK] 0.62  (medium-high)  — 主要受：降水、早高峰、到达机场拥堵影响
```

## Repo Layout / 目录
```
.
├── main.py               # CLI脚本：生成飞行简报 + 基线延误分
├── brief_template.md     # 简报模板（字符串变量）
├── requirements.txt      # 依赖（轻量）
└── README.md
```



## Data Plan / 数据源计划（草案）
- **历史航班**：出发/到达时间、计划 vs 实际、延误标签（y）
- **天气**：METAR/TAF（可先离线样本 → 后续接入API）
- **机场负荷**：小时级出港/进港量（可从公开统计或自建估计）
- **时段/季节特征**：小时、工作日/周末、假日、月份
- **航线特征**：航距、枢纽-枢纽、历史准点率

##  Baseline Rules / 规则基线（可解释）
- 早晚高峰（06–09, 17–21）+0.10~0.20
- 降水/雷暴/低能见度 +0.15~0.45
- 大型枢纽到达 +0.05~0.15
- 近距离航段（周转紧凑） +0.05
- 最终分数限定在 [0, 1]，并划分阈值：low (<=0.33), medium (<=0.66), high (>0.66)

## Day 1 Run Log
Example run saved in [runs/demo_2025-09-20.txt](runs/demo_2025-09-20.txt)



---

APACHE-2.0 © 2025 David Xue (owner) · Drafted with GPT
