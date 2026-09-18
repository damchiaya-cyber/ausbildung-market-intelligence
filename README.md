# 📊 German Ausbildung Market Intelligence & Predictive Analytics Platform

An end-to-end Data Engineering, Machine Learning, and Business Intelligence platform engineered to analyze and forecast structural labor supply-and-demand imbalances across the German Dual Vocational Training System (*Duales Ausbildungssystem*).

---

## 🎯 Problem Statement
Germany faces a critical **Fachkräftemangel** (skilled labor shortage) driven by severe structural mismatches:
* **Regional Disparities:** High applicant surpluses in northern/western states vs. acute shortages in southern/eastern industrial hubs.
* **Sectoral Imbalance:** Over-saturation in popular administrative/IT trades alongside hundreds of thousands of unfilled vacancies in industrial, technical, and trade roles.

---

## 💡 Solution Architecture
This platform unifies federal datasets into an end-to-end analytical pipeline to give HR leaders and regional policymakers actionable insights:

1. **Data Warehouse (PostgreSQL):** Relational schema tracking supply (`Ausbildungsplatzangebot`), demand (`Ausbildungsplatznachfrage`), and regional metrics across all 16 *Bundesländer*.
2. **Predictive Modeling (Python & XGBoost):** Time-series forecasting to predict unfilled apprenticeship ratios and high-risk shortage clusters through 2028.
3. **Executive Analytics (Power BI):** Interactive regional heatmaps, DAX-driven KPI metrics, and trade sector breakdowns.

---

## 🛠️ Tech Stack
* **Database & ETL:** PostgreSQL, SQL (Window Functions, Aggregations)
* **Data Processing & ML:** Python (`pandas`, `scikit-learn`, `xgboost`, `statsmodels`)
* **Business Intelligence:** Power BI (DAX, Data Modeling, Star Schema)
* **Version Control:** Git, GitHub