# 🤖 AI-Powered E-Commerce Operations Intelligence System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Prophet](https://img.shields.io/badge/Prophet-Forecasting-0467DF?style=for-the-badge)
![Scikit--learn](https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-LLM%20AI-00A67E?style=for-the-badge)
![GitHub](https://img.shields.io/badge/Status-Complete-10B981?style=for-the-badge)

**A real, working, AI-powered operations intelligence platform for e-commerce businesses.**  
Built on 99,441 real orders from the Olist Brazilian E-Commerce dataset.

[📊 View Dashboard](#dashboard) • [🚀 Quick Start](#quick-start) • [📁 Project Structure](#project-structure) • [📈 Results](#results)

</div>

---

## 📌 Why This System?

Most e-commerce businesses drown in data but starve for decisions.

This system changes that. It takes raw transactional data and automatically delivers:
- **What will customers demand next?** — 90-day demand forecast
- **Which customers are about to leave?** — RFM segmentation + churn prediction  
- **Which sellers are behaving unusually?** — Automated anomaly detection
- **What should we tell management?** — AI-generated weekly ops report

All connected through a single interactive Streamlit dashboard.

---

## 🏗️ System Architecture

```
Raw Data (9 CSV files)
        ↓
   Data Pipeline
   (EDA + Cleaning + Feature Engineering)
        ↓
┌───────────────────────────────────────────┐
│           4 ML/AI Modules                 │
│                                           │
│  Module 1    │  Module 2    │  Module 3   │
│  Demand      │  Customer    │  Anomaly    │
│  Forecasting │  Analytics   │  Detection  │
│  (Prophet)   │  (RFM+XGB)   │  (IsoForest)│
│              │              │             │
│         Module 4 — AI Reports             │
│         (Groq LLM Integration)            │
└───────────────────────────────────────────┘
        ↓
  Streamlit Dashboard
  (5 Pages, Interactive, Live)
```

---

## 📦 Modules

### Module 1 — Demand Forecasting Engine
> *How much stock do we need for the next 90 days?*

- Algorithm: **Facebook Prophet** (time-series forecasting)
- Input: Daily order counts aggregated from 99,441 orders
- Output: 90-day forecast with upper/lower confidence bounds
- Key finding: Black Friday spike detected in November 2017

### Module 2 — Customer Behavior Analytics
> *Which customers are loyal, which are leaving, which are lost?*

- Framework: **RFM Analysis** (Recency, Frequency, Monetary)
- Algorithm: **Gradient Boosting Classifier** for churn prediction
- Input: 96,478 unique customer purchase histories
- Output: 5 customer segments + individual churn probability scores

### Module 3 — Operations Anomaly Detector
> *Which sellers are behaving unusually and why?*

- Algorithm: **Isolation Forest** (unsupervised ML)
- Input: Seller-level aggregates across 4 operational features
- Output: 149 anomalous sellers flagged from 2,970 total
- No labeled data required — fully unsupervised

### Module 4 — AI Report & Email Generator
> *What should operations management know this week?*

- Integration: **Groq API** + **llama-3.3-70b-versatile**
- Output 1: Weekly executive operations summary report
- Output 2: Supplier reorder email (triggered by forecast)
- Fully automated — zero manual writing required
- **Email Dispatch: Automated via Brevo SMTP** — report 
  sent directly to recipient email automatically
- Fully automated — zero manual writing or sending required
---

## 📊 Results

| Metric | Value |
|--------|-------|
| Total Orders Analyzed | 99,441 |
| Total Revenue Tracked | R$20,470,727 |
| Delivery Rate | 97.1% |
| Avg Delivery (vs estimated) | 12 days early |
| Anomalous Sellers Detected | 149 / 2,970 |
| At-Risk Customers Identified | 39,867 (41.3%) |
| Champion Customers | 7,815 (8.1%) |
| Forecast Horizon | 90 days |
| Forecast MAE | 81.48 orders/day |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.12 |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, XGBoost |
| Time Series | Facebook Prophet |
| AI Integration | Groq API (llama-3.3-70b) |
| Visualization | Plotly, Matplotlib, Seaborn |
| Dashboard | Streamlit |
| Version Control | Git + GitHub |
| Dataset | Olist Brazilian E-Commerce (Kaggle) |

---

## 📁 Project Structure

```
Smart Ops/
│
├── data/
│   ├── raw/                    ← 9 Olist CSV files (not tracked by Git)
│   └── processed/              ← Cleaned outputs
│       ├── master_data.csv
│       ├── demand_forecast.csv
│       ├── rfm_segments.csv
│       └── seller_anomalies.csv
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_module1_demand.ipynb
│   ├── 03_module2_customer.ipynb
│   ├── 04_module3_anomaly.ipynb
│   └── 05_module4_ai_report.ipynb
│
├── dashboard/
│   └── app.py                  ← Streamlit application
│
├── outputs/
│   ├── monthly_orders.png
│   ├── top_categories.png
│   ├── demand_forecast.png
│   ├── customer_segments.png
│   ├── anomaly_detection.png
│   ├── weekly_report.txt
│   └── supplier_email.txt
│
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/vinayuser102/AI-Powered-E-Commerce-Operations-Intelligence-System.git
cd AI-Powered-E-Commerce-Operations-Intelligence-System
```

### 2. Install Dependencies
```bash
pip install pandas numpy matplotlib seaborn plotly jupyter scikit-learn streamlit prophet xgboost groq
```

### 3. Download Dataset
Download the [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) from Kaggle and place all 9 CSV files in `data/raw/`

### 4. Run the Notebooks (in order)
```bash
jupyter notebook
```
Run notebooks in sequence: 01 → 02 → 03 → 04 → 05

### 5. Launch Dashboard
```bash
cd dashboard
python -m streamlit run app.py
```

### 6. Add Your Groq API Key
In `notebooks/05_module4_ai_report.ipynb`, replace:
```python
GROQ_API_KEY = "your_groq_api_key_here"
```
Get a free key at [console.groq.com](https://console.groq.com)



### 7. Configure Email (Optional)
Create a `.env` file in the project root:
GROQ_API_KEY=your_groq_api_key
BREVO_SMTP_KEY=your_brevo_smtp_key
SENDER_EMAIL=your_email@gmail.com
BREVO_LOGIN=your_brevo_login@smtp-brevo.com
RECIPIENT_EMAIL=recipient@gmail.com


Get a free Brevo account at [brevo.com](https://brevo.com)

---

## 🖥️ Dashboard

The Streamlit dashboard has 5 pages:

| Page | Content |
|------|---------|
| Overview | KPI cards + Monthly order volume chart |
| Demand Forecast | Interactive 90-day Prophet forecast |
| Customer Segments | RFM pie chart + segment table + churn metric |
| Anomaly Detection | Scatter plot with flagged sellers highlighted |
| AI Reports | Generated weekly report + supplier email |

---

## 📚 Dataset

**Olist Brazilian E-Commerce Public Dataset**  
Source: [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)  
License: CC BY-NC-SA 4.0

| File | Records |
|------|---------|
| olist_orders_dataset.csv | 99,441 |
| olist_order_items_dataset.csv | 112,650 |
| olist_customers_dataset.csv | 99,441 |
| olist_products_dataset.csv | 32,951 |
| olist_order_reviews_dataset.csv | 99,224 |
| olist_order_payments_dataset.csv | 103,886 |
| olist_sellers_dataset.csv | 3,095 |

---

## 🔑 Key Findings

- **97.1% delivery rate** — Olist maintains strong fulfillment performance
- **41.3% of customers are At Risk** — major retention opportunity identified
- **Only 8.1% are Champions** — loyalty program urgently needed
- **149 sellers flagged as anomalous** — including one with 165-day avg delay
- **Black Friday pattern confirmed** — November 2017 shows clear demand spike
- **R$20.4M revenue** tracked across 25 months of operations



---


**Vinay Sharma**  
Data analyst | Operations Analytics | AI/ML
GitHub: [@vinayuser102](https://github.com/vinayuser102)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">



⭐ Star this repo if you found it useful

</div>
