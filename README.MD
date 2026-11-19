# 💰 Financial Reporting & Anomaly Detection System

![CI](https://github.com/https://github.com/meeeed23-maker//financial-reporting-system/actions/workflows/ci.yml/badge.svg)

## 🎯 Business Context
Automated monthly financial reporting system with **Actual vs Budget variance analysis**,
**data quality controls**, and **AI-based anomaly detection** — built on the Superstore dataset.

## 📊 Power BI Dashboard

Interactive report built with **Power BI Desktop** and **Power Query** from `financial_data_scored.csv` (Budget vs. Actual tracking and **Isolation Forest** anomaly detection).

### 1. Financial Overview (`Overview`)
![Overview Dashboard](dashboard/Screenshots/overview_dashboard.png)

### 2. Detected Anomalies (`Anomalies`)
![Anomalies Dashboard](dashboard/Screenshots/anomalies_dashboard.png)

## 🛠️ Tech Stack (matching job requirements)
| Requirement | Implementation |
|---|---|
| **Python** | Pandas, NumPy, Scikit-learn |
| **SQL** | `sql/schema.sql` + analytical queries |
| **Power BI** | `dashboard/powerbi/financial_dashboard.pbix` |
| **Excel Automation** | `src/report_generator.py` (openpyxl) |
| **AI / ML** | `src/anomaly_detector.py` (Isolation Forest) |
| **Data Quality** | `src/data_quality.py` (6 automated checks) |
| **CI/CD** | GitHub Actions (auto-run on push) |

## 🚀 Quick Start
```bash
pip install -r requirements.txt
python src/prepare_data.py       # Generate budget vs actual dataset
python src/data_quality.py       # Run data quality checks
python src/anomaly_detector.py   # Detect anomalies with ML
python src/report_generator.py   # Generate Excel report
streamlit run dashboard/streamlit/app.py  # Launch dashboard