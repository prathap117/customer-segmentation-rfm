# 👥 Customer Segmentation using RFM Analysis

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-teal)
![Scikit-learn](https://img.shields.io/badge/ScikitLearn-KMeans-orange)
![SQL](https://img.shields.io/badge/SQL-Queries-red)
![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-yellow)

---

## 📌 Project Overview

This project applies **RFM (Recency, Frequency, Monetary) Analysis** combined with **K-Means Clustering** to segment customers of a UK online retailer into actionable groups. The goal is to enable the marketing team to design personalised campaigns for each customer segment.

**Business Problem:** An e-commerce company wants to:
- Identify its most valuable (Champions) and at-risk customers
- Understand purchasing behaviour patterns across the customer base
- Enable targeted marketing campaigns to improve retention and revenue

**Dataset:** UCI Online Retail Dataset — 4,300+ unique customers

---

## 🗂️ Repository Structure

```
customer-segmentation-rfm/
│
├── data/
│   ├── online_retail.csv           # Raw dataset (download link below)
│   └── rfm_scores.csv              # Generated RFM scores
│
├── notebooks/
│   └── rfm_segmentation.ipynb      # Full Jupyter Notebook
│
├── scripts/
│   ├── rfm_analysis.py             # RFM computation & segmentation
│   ├── clustering.py               # K-Means clustering script
│   └── sql_rfm_queries.sql         # SQL-based RFM queries
│
├── outputs/
│   ├── rfm_distribution.png
│   ├── customer_segments_bar.png
│   ├── rfm_scatter.png
│   ├── elbow_curve.png
│   └── segment_heatmap.png
│
├── requirements.txt
└── README.md
```

---

## 📊 Dataset

- **Source:** [UCI Machine Learning Repository – Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail)
- **Kaggle Mirror:** [Online Retail Dataset on Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset)
- **Unique Customers:** ~4,300 after cleaning
- **Fields Used:** InvoiceNo, InvoiceDate, CustomerID, Quantity, UnitPrice

---

## 🛠️ Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python (Pandas, NumPy) | RFM computation & data wrangling |
| Scikit-learn | K-Means clustering |
| Matplotlib & Seaborn | Visualization |
| SQL (SQLite) | RFM queries |
| Power BI | Segment dashboard (optional) |

---

## 📐 Methodology

### RFM Framework
| Metric | Definition | Business Meaning |
|--------|-----------|-----------------|
| **Recency (R)** | Days since last purchase | How recently did they buy? |
| **Frequency (F)** | Number of orders | How often do they buy? |
| **Monetary (M)** | Total amount spent | How much do they spend? |

### Customer Segments Identified

| Segment | Description | Strategy |
|---------|------------|---------|
| 🏆 Champions | Bought recently, buy often, spend most | Reward them, ask for reviews |
| 💛 Loyal Customers | Buy regularly, moderate spend | Upsell higher-value products |
| 🌱 Potential Loyalists | Recent buyers, moderate frequency | Offer membership or loyalty program |
| ⚠️ At Risk | Used to buy often but haven't recently | Send win-back campaigns |
| 😴 Lost Customers | Low recency, low frequency | Reactivate with heavy discounts |

---

## 🔍 Key Insights

1. **🏆 Champions (18% of customers) = 55% of revenue** — Protecting this segment is the highest ROI activity.
2. **⚠️ At-Risk customers (22%)** — These customers haven't purchased in 60–90 days; targeted re-engagement can recover £80K+.
3. **😴 Lost customers (30%)** — Large segment; low-cost email reactivation campaign recommended.
4. **💛 Loyal customers have 3× higher order frequency** than average — ideal candidates for subscription or VIP programs.
5. **📦 Average order value of Champions: £450** vs £85 for Lost customers — clear monetization opportunity.

---

## 📸 Sample Visualizations

> **Add screenshots of your charts here after running the scripts.**

| Chart | Description |
|-------|------------|
| `outputs/rfm_distribution.png` | Distribution of R, F, M scores |
| `outputs/customer_segments_bar.png` | Customer count per segment |
| `outputs/rfm_scatter.png` | Scatter: Frequency vs Monetary, coloured by segment |
| `outputs/elbow_curve.png` | Elbow method for optimal K |
| `outputs/segment_heatmap.png` | Avg RFM scores by segment |

---

## ▶️ How to Run

### 1. Clone the Repository
```bash
git clone https://github.com/prathap117/customer-segmentation-rfm.git
cd customer-segmentation-rfm
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download the Dataset
Download from [Kaggle](https://www.kaggle.com/datasets/lakshmi25npathi/online-retail-dataset) and place `online_retail.csv` in the `data/` folder.

### 4. Run RFM Analysis
```bash
python scripts/rfm_analysis.py
```

### 5. Run Clustering
```bash
python scripts/clustering.py
```

### 6. Open Jupyter Notebook
```bash
jupyter notebook notebooks/rfm_segmentation.ipynb
```

---

## 💼 Business Recommendations

| Segment | Action | Expected Impact |
|---------|--------|----------------|
| Champions | VIP loyalty rewards, referral programs | +15% repeat purchase rate |
| At Risk | Personalised win-back email (discount code) | Recover 25–30% of churned revenue |
| Potential Loyalists | Offer membership, push notifications | Convert to loyal base |
| Lost | Low-cost reactivation blast | 5–10% reactivation at minimal cost |

---

## 👤 Author

**Yaradoni Prathapa**
📧 prathapayaradoni@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/yaradoni-prathapa-467645297/) | [GitHub](https://github.com/prathap117)
