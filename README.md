# 📦 End-to-End Supply Chain Analytics & Operations Suite

Welcome to the Supply Chain Analytics repository. This portfolio brings together data-driven operational solutions across **Inventory Health Optimization** and **Demand Planning & Forecast Accuracy**, bridging technical analytics with strategic financial decision-making.

---

## 🗺️ Repository Structure

```text
.
├── assets/                  # Visualizations, charts, and dashboard exports
│   ├── dsi_distribution.png
│   └── forecast_vs_actual.png
├── data/                    # Operational datasets
│   ├── demand_forecast_raw.csv
│   └── raw_inventory.csv
├── notebooks/               # Python analytical scripts
│   ├── 01_inventory_health_analysis.py
│   └── 02_demand_planning_analysis.py
├── sql/                     # SQL queries and metrics logic
│   ├── 01_inventory_analysis.sql
│   └── 02_forecast_accuracy.sql
└── README.md                # Project documentation
```
📊 Module 1: Inventory Health Analysis & Capital Recovery Strategy
Executive Summary
This project addresses a critical operational challenge: an organization holding $83.7M USD in total inventory, where global averages masked severe operational inefficiencies. Through a custom data analytics pipeline, we identified that 99.7% of the capital was tied up in overstock, with $44.2M USD in high-risk perishable items (Food & Beverages) exceeding 45 days of supply (DSI).

A 30-60-90 day remediation strategy was designed to release +$40M USD in cash flow and elevate inventory turnover from 3.68 to 6.0 turns/year.
### 📊 Key Operational Metrics & Findings

| Metric | Baseline (Day 0) | Target (Day 90) | Impact / Status |
| :--- | :--- | :--- | :--- |
| **Total Capital Tied Up** | $83.7M USD | ~$35.0M USD | -$48.7M USD |
| **Perishable Risk Stock (>45d)** | $44.2M USD | $0.0M USD | FEFO Clearance & Bundling |
| **Inventory Turnover** | 3.68 turns/yr | 6.00 turns/yr | +63% Efficiency |
| **Average Days of Supply (DSI)** | 99.1 days | 60.0 days | -39.1 Days Reduction |

---
🎯 Module 2: Demand Planning & Forecast Accuracy
Executive Summary
To prevent future inventory imbalances, this module evaluates the accuracy of baseline demand forecasts against actual historical sales. By measuring forecast errors and bias across product categories, we establish a data-backed foundation to optimize safety stock levels and mitigate both stockout risks and over-purchasing costs.

🛠️ Framework & Analytical Metrics
MAPE (Mean Absolute Percentage Error):
Calculates the average magnitude of error in percentage terms, regardless of direction.

Forecast Bias (%):
Identifies systematic over-forecasting (risk of excess stock) or under-forecasting (risk of stockouts).

Forecast Accuracy (%):
Measures total model accuracy (100% - MAPE).

💻 Tech Stack & Execution Guide
SQL: PostgreSQL / ANSI SQL for data aggregation, DSI calculation, and accuracy window queries (sql/).

Python: pandas, numpy, matplotlib, seaborn for statistical modeling and visualization (notebooks/).
How to Run
Database Queries: Execute scripts in sql/01_inventory_analysis.sql and sql/02_forecast_accuracy.sql directly on your database environment.

Python Scripts: Run the data processing pipelines:
python notebooks/01_inventory_health_analysis.py
python notebooks/02_demand_planning_analysis.py
