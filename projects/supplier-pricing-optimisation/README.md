# SaaS Supplier Pricing Optimisation – Detailed Case Study

**Role**: Business Process Excellence Engineer  
**Project Type**: Pricing Strategy & Revenue Optimisation

## Project Overview
This project optimised the pricing model of a B2B SaaS platform connecting smash repairers with OEM and Aftermarket parts suppliers. The platform earns revenue primarily through a **clip % (take-rate / commission)** on parts sold. Suppliers operate under a tiered membership model (Gold vs Blue) that influences their effective take-rate.

## Problem Statement
The existing Gold vs Blue tier structure and fixed take-rate logic were not aligned with actual supplier behaviour. Leadership needed to understand how different tiers and take-rates impact order volume, GMV, credits, and overall revenue, and whether suppliers could be segmented more effectively based on real operational patterns.

## Methodology

### 1. Database Exploration & Mapping
Conducted a thorough review of a large normalised relational database schema. Mapped relationships across orders, invoices, payment data, membership tiers, and supplier attributes. Identified key metrics including GMV, order volume, quote win rate, fill rate, credit behaviour, part category concentration, and repairer preference.

**Key SQL files:**
- [`core_monthly_dataset.sql`](./sql_examples/core_monthly_dataset.sql) – main monthly aggregation
- [`supplier_credit_profile.sql`](./sql_examples/supplier_credit_profile.sql) – credit behaviour metrics

### 2. Monthly Data Aggregation
Designed and implemented SQL queries to build a consistent monthly supplier-level dataset. Calculated commercial and behavioural indicators including revenue contribution, GMV, order volume, credits, and effective take-rate.

### 3. Supplier Behavioural Segmentation (K-means Clustering)
Engineered features capturing scale, loyalty, risk, and pricing response (average GMV, order frequency, repairer preference strength, credit ratio, take-rate sensitivity, part category diversity).  
Applied StandardScaler, used the elbow method for cluster validation, and performed K-means clustering.

**Python script:**
- [`data_preparation_and_clustering.py`](./python_analysis/data_preparation_and_clustering.py)

**Visual:**
- [Elbow Method for Optimal K](./visuals/elbow_method.png)
  
### 4. Comparative Analysis & Recommendations
Compared performance across existing Gold/Blue tiers versus new behavioural clusters.  
Quantified differences in revenue contribution, GMV trajectories, credit patterns, and take-rate elasticity.  
Recommended moving from rigid tier rules to segment-informed dynamic take-rate adjustments.

**Output files:**
- [`Cluster_Uplift_Summary.csv`](./data/Cluster_Uplift_Summary.csv) – cluster-level summary

## Tech Stack
- **SQL**: Complex multi-table joins and time-series aggregation
- **Python**: Pandas, Scikit-learn (K-means + elbow method), Plotly

## Skills Demonstrated
- End-to-end relational database analysis
- Feature engineering and unsupervised machine learning for operational segmentation
- Translating analytical outputs into strategic pricing recommendations
- Balancing revenue growth with supplier sustainability

**Status**: Completed (synthetic version for public portfolio)  

**Confidentiality Note**:  
The queries and Python scripts closely reflect the logic and approach used in the real analysis. All table names, column names, and datasets have been generalised and replaced with synthetic examples for confidentiality. The original work was performed on a private production database.

← [Back to Main Portfolio](../../README.md)
