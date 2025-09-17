# AeroBrief: Flight Brief + AI Delay Predictor (Day 1)

> **MVP (Day 1)** — A tiny, local script that generates a flight brief and outputs a *baseline* delay risk score (rule-based).  
> 后续会逐步替换为基于真实数据的 ML 模型。

## 🎯 Why this project / 项目意义
- 将**飞行运行简报**（航班信息、机场天气、时间窗口）与**延误风险预测**结合，形成可落地的飞行前辅助工具。
- 有清晰的技术栈（Python + 数据工程 + 机器学习），适合作为你的转学&实习作品集核心项目。

## ✅ Day 1 Deliverables / 当日交付
- 一个可运行的 `main.py`：输入航班信息 → 输出标准化「飞行简报」+ 基线延误风险分数。
- `brief_template.md`：飞行简报模板（后续可扩展为PDF/网页）。
- `requirements.txt`：依赖列表（尽量轻量）。

## 🧭 Roadmap / 路线图（简版）
- **Day 1**: 项目骨架 + 规则引擎 baseline（本仓库）
- **Day 2-3**: 数据源对接（历史航班 & METAR/TAF 天气 & 机场拥堵指标），清洗与特征工程
- **Day 4-5**: 训练第一个轻量模型（例如 XGBoost / LightGBM），对比规则baseline
- **Day 6-7**: CLI/小型Web页面（Streamlit/FastAPI）+ 可视化报告（特征重要性、混淆矩阵等）
- **Plus**: 航空业务 knowledge 注入（SID/STAR、枢纽时段、ATFM/slot、连接航班、机型变化）

## 📦 How to run / 运行方式
```bash
# 1) (可选) 创建虚拟环境
python3 -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) 安装依赖
pip install -r requirements.txt

# 3) 运行示例（可自定义参数）
python main.py \
  --flight_no CA123 \
  --dep ZBAA \
  --arr ZSPD \
  --dep_time 2025-09-20T08:30:00 \
  --arr_time 2025-09-20T10:45:00 \
  --dep_metar "ZBAA 200800Z 04005MPS 9999 FEW020 22/12 Q1015" \
  --arr_metar "ZSPD 200945Z 06010MPS 8000 RA BKN015 24/20 Q1009"
```

示例输出（示意）：
```
[BRIEF] CA123 ZBAA → ZSPD (2025-09-20 08:30 → 10:45)
[WEATHER] DEP(MVFR), ARR(IFR, RA)
[BASELINE DELAY RISK] 0.62  (medium-high)  — 主要受：降水、早高峰、到达机场拥堵影响
```

## 🗂️ Repo Layout / 目录
```
.
├── main.py               # CLI脚本：生成飞行简报 + 基线延误分
├── brief_template.md     # 简报模板（字符串变量）
├── requirements.txt      # 依赖（轻量）
└── README.md
```

## 📋 Day 1 Checklist / 今日清单
- [ ] 在 GitHub 创建新仓库：`aerobrief-delay`（或你喜欢的名字）
- [ ] 推送此 Day 1 骨架
- [ ] 本地运行 `python main.py ...`，确认输出
- [ ] 在 README 添加「数据源计划」与「建模计划」小节（已内置模板）
- [ ] 记录遇到的问题与明日目标

## 📊 Data Plan / 数据源计划（草案）
- **历史航班**：出发/到达时间、计划 vs 实际、延误标签（y）
- **天气**：METAR/TAF（可先离线样本 → 后续接入API）
- **机场负荷**：小时级出港/进港量（可从公开统计或自建估计）
- **时段/季节特征**：小时、工作日/周末、假日、月份
- **航线特征**：航距、枢纽-枢纽、历史准点率

## 🧠 Baseline Rules / 规则基线（可解释）
- 早晚高峰（06–09, 17–21）+0.10~0.20
- 降水/雷暴/低能见度 +0.15~0.45
- 大型枢纽到达 +0.05~0.15
- 近距离航段（周转紧凑） +0.05
- 最终分数限定在 [0, 1]，并划分阈值：low (<=0.33), medium (<=0.66), high (>0.66)

## 📝 Next Steps / 明日目标
- [ ] 设计`features.yaml`：统一特征字典与采样逻辑
- [ ] 准备5~10条「真实或仿真」航班样本CSV，做快速可视化
- [ ] 评估候选数据API（付费/免费/速率限制/许可）

---

MIT © 2025 David (owner) · Drafted with GPT-5 Thinking
