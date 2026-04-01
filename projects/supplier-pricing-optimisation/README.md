# SaaS Supplier Pricing Optimisation – Detailed Case Study

**Role**: Business Process Excellence Engineer  
**Project Type**: Pricing Strategy & Revenue Optimisation

## Project Overview
This project optimised the pricing model of a B2B SaaS platform connecting smash repairers with OEM and Aftermarket parts suppliers. The platform earns revenue through a **clip % (take-rate / commission)** on parts sold. Suppliers operate under a tiered membership model (Gold vs Blue) that affects their effective take-rate.

## Problem Statement
The existing Gold vs Blue tier structure and fixed take-rate logic were not aligned with actual supplier behaviour. Leadership needed to understand:
- How tiers and take-rates impact order volume, GMV, credits, and overall revenue
- Whether suppliers could be segmented more effectively based on real operational patterns
- What pricing adjustments could drive sustainable revenue growth while protecting supplier retention

## Methodology

### 1. Database Exploration & Mapping
- Conducted a thorough review of a large normalised relational database schema
- Mapped relationships across orders, invoices, payment engine data, membership tiers, and supplier attributes
- Identified and validated key performance and behavioural metrics, including:
    - Order volume and Gross Merchandise Value (GMV)
    - Quote win rate and order fill rate
    - Repairer preference strength
    - Order cancellations attributable to supplier fault
    - Part type concentration and vehicle make dominance

### 2. Monthly Data Aggregation
- Designed and implemented robust SQL aggregation queries to build a consistent monthly supplier-level dataset
- Calculated and derived commercial and behavioural indicators, including revenue contribution, GMV, order volume, credit utilisation ratios, and effective clip (take‑rate) percentages
- Aggregated data over a 24-month window while handling missing periods and structural changes

**Key SQL files:**
- [`core_monthly_dataset.sql`](../sql_examples/core_monthly_dataset.sql) – main monthly aggregation
- [`supplier_credit_profile.sql`](../sql_examples/supplier_credit_profile.sql) – credit behaviour metrics

  
### 3. Supplier Behavioural Segmentation (K-means Clustering)
- Engineered features capturing scale, loyalty, risk, and pricing response:
   - Average GMV, Order frequency, Repairer preference strength, Credit utilisation ratio, Take‑rate sensitivity, Part category diversity
- Applied StandardScaler for normalisation
- Used the elbow method and silhouette score to determine the optimal number of clusters

  
 
- Applied K-means clustering (illustrated with 4 clusters in this repository)

## Cluster Results (Supplier DNA)

After feature engineering and scaling, K-means clustering (validated with the elbow method and silhouette score) revealed clearly differentiated supplier behavioural segments.
Note: The table below is a synthetic illustration aligned to the observed behavioural patterns. In the real analysis, six statistically distinct and economically meaningful clusters emerged.

**Example of Resulting Behavioural Segments** 

| Cluster | Description                          | Key Characteristics                                | Typical GMV Level | Take-rate Sensitivity |      Recommended Pricing Strategy                          |
|---------|--------------------------------------|----------------------------------------------------|-------------------|-----------------------|------------------------------------------------------------|
| 0       | High-volume stable performers        | Very High GMV, strong loyalty, high specialization | Very High         | Low                   | Protective lower take-rate to maximise long-term retention |
| 1       | Growth-oriented consistent suppliers | Medium-high GMV, good efficiency                   | High              | Medium                | Balanced dynamic take-rate bands with volume incentives    |
| 2       | Price-sensitive mid-tier             | Moderate GMV, higher credit usage                  | Medium            | High                  | Conservative take-rate with targeted support programs      |
| 3       | Emerging or variable suppliers       | Lower GMV, mixed specialization                    | Low-Medium        | Very High             | Growth-oriented entry rates with performance milestones    |

These behavioural segments ("supplier DNA") provided significantly richer insights than the existing Gold vs Blue tiers and formed the foundation for the pricing reclassification recommendations.

### 4. Comparative Analysis
- Compared performance across existing Gold/Blue tiers versus the new behavioural clusters
- Quantified differences in GMV contribution, credit patterns, and take-rate elasticity
- Highlighted mismatches between rigid tier-based pricing and actual supplier economics

## Tech Stack
- **MySQL**: Complex multi-table joins, window functions, and time-series aggregation on normalised tables
- **Python**: Pandas for data merging and transformation, Scikit-learn (K-means clustering + elbow method), Plotly for visualisation
- Feature engineering, scaling, and cluster validation

## Results & Recommendations
**Key Findings**
- Supplier behaviour naturally formed more distinct segments than the binary Gold/Blue tiers
- Different segments showed markedly different responses to take-rate changes
- Clear opportunities to move from one-size-fits-all tier rules to segment-informed pricing logic

**Pricing Optimisation Recommendations**
- Replace rigid tier rules with behavioural-segment-based take-rate adjustments
- Introduce dynamic take-rate bands based on GMV and order patterns
- Develop targeted strategies for high-potential segments to improve retention while protecting overall revenue

## Lessons Learned
- Behavioural clustering using K-means provided significantly richer insights than relying solely on the existing Gold/Blue tiers.
- Combining domain knowledge with unsupervised learning creates more actionable pricing strategies
- Clear communication of technical results (especially clustering) to non-technical stakeholders is critical for driving real business change.

## Skills Demonstrated
- End-to-end relational database analysis and metric design
- Feature engineering and unsupervised machine learning for operational segmentation
- Translating complex analytics into strategic pricing recommendations
- Optimisation thinking that balances revenue growth with supplier sustainability

**Status**: Completed (synthetic version for public portfolio)  
**Confidentiality Note**: The queries and Python scripts closely reflect the logic and approach used in the real analysis. All table names, column names, and datasets have been generalised and replaced with synthetic examples for confidentiality. The original work was performed on a private production database.
---

← [Back to Main Portfolio](../../README.md)
