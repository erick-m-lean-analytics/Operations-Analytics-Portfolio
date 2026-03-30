# SaaS Supplier Pricing Optimisation – Detailed Case Study

**Role**: Business Process Excellence Engineer  
**Project Type**: Pricing Strategy & Revenue Optimisation

## Project Overview
This project focused on optimising the pricing model of a B2B SaaS platform that connects smash repairers with OEM (Original Equipment Manufacturer) and Aftermarket parts suppliers. 

The platform connects smash repairers (purchasers) with OEM and Aftermarket parts suppliers. Repairers request quotes and source parts, while suppliers list parts and fulfil orders. The SaaS company earns revenue primarily through a **clip % (take-rate / commission)** on the value of parts sold. Suppliers operate under a tiered membership model (Gold vs Blue) that influences their effective take-rate and platform benefits.

## Problem Statement
The existing Gold vs Blue tier structure and fixed take-rate logic were not optimally aligned with actual supplier behaviour. Leadership needed to understand:
- How different tiers and take-rates impact order volume, GMV, credits, and overall revenue
- Whether suppliers could be segmented more effectively based on real operational patterns
- What pricing adjustments could drive sustainable revenue growth while protecting supplier retention

## Methodology

### 1. Database Exploration & Mapping
- Performed a comprehensive review of a large, fully normalised relational database schema to understand the end‑to‑end supplier lifecycle
- Mapped core entities and relationships across orders, invoices, payment engine data, membership tiers, and supplier attributes
- Identified and validated key supplier performance and behavioural metrics, including:
  - Order volume and Gross Merchandise Value (GMV)
  - Quote win rate and order fill rate
  - Repairer preference strength
  - Order cancellations attributable to supplier fault
  - Part type concentration and vehicle make dominance
- Documented metric definitions and lineage to ensure analytical consistency and reproducibility

### 2. Monthly Data Aggregation
- Designed and implemented robust SQL aggregation pipelines to extract metric‑level data at the supplier level
- Calculated and derived commercial and behavioural indicators, including revenue contribution, GMV, order volume, credit utilisation ratios, and effective clip (take‑rate) percentages
- Aggregated all measures into a consistent monthly grain per supplier to support longitudinal analysis
- Ensured time‑series integrity and completeness across a 24‑month analysis window, handling missing periods and structural changes explicitly

### 3. Supplier Behavioural Segmentation (K-means Clustering)
- Engineered a behavioural feature set capturing both commercial scale and operational behaviour, including:
 - Average Gross Merchandise Value (GMV)
 - Order frequency
 - Repairer preference strength
 - Credit utilisation ratio
 - Take‑rate sensitivity
 - Part category diversity
- Features were deliberately selected to balance volume, loyalty, risk, and pricing response, rather than relying purely on revenue-based metrics.
- Applied StandardScaler to normalise all features, ensuring no single variable dominated cluster assignment due to scale effects.
- Used the elbow method to evaluate within-cluster sum of squares (WCSS) across candidate cluster counts.
- Selected the optimal cluster count and evaluated clustering quality using silhouette score and centroid stability.
- Applied K-means clustering with n_clusters=4 for illustration purposes in this repository.

Why K-means?
K-means was selected for its interpretability, scalability to large populations of suppliers, and effectiveness in identifying natural, unlabeled behavioural groupings. Its centroid-based structure also enabled a straightforward translation of cluster definitions into pricing-strategy logic.

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
- Compared supplier performance across existing Gold/Blue tiers and the new behavioural clusters
- Analysed differences in:
  - Revenue contribution
  - GMV growth trajectories
  - Credit utilisation patterns
  - Take‑rate elasticity by segment
- Quantified how identical take‑rate levels produced materially different outcomes depending on supplier behavioural profile

This analysis highlighted structural mismatches between tier-based pricing and actual supplier economics.
## Tech Stack
- **SQL**: Complex multi-table joins, window functions, and time-series aggregation on normalised tables
- **Python**: Pandas for data preparation, Scikit-learn (K-means clustering + elbow method), Plotly for interactive visualisations
- Exploratory data analysis, feature scaling, and cluster validation techniques

## Results & Recommendations

**Key Findings**
- Supplier behaviour naturally fell into more than two distinct segments, revealing limitations in the current binary tier system.
- Certain segments showed high sensitivity to take-rate changes, while others were more tolerant.
- Clear opportunities existed to move from rigid tier rules to segment-informed pricing logic.

**Pricing Optimisation Recommendations**
- Implement tier-specific clip % adjustments based on behavioural segments rather than a one-size-fits-all approach per tier
- Introduce dynamic take-rate bands that adapt to supplier GMV and order patterns
- Develop targeted pricing strategies for high-potential segments to improve retention and revenue balance
- Provided multiple reclassification scenarios with estimated potential revenue uplift ranges

**Deliverables**
- Behavioural segmentation model ("supplier DNA")
- Executive summary with visual insights and recommended pricing adjustments

## Lessons Learned
- Behavioural clustering using K-means provided significantly richer insights than relying solely on the existing Gold/Blue tiers.
- Combining domain knowledge (Lean/TPS principles of waste reduction and flow) with unsupervised machine learning created more practical and actionable pricing strategies.
- Clear communication of technical results (especially clustering) to non-technical stakeholders is critical for driving real business change.

## Skills Demonstrated
- End-to-end relational database analysis
- Unsupervised machine learning for operational segmentation
- Translating complex analytical outputs into strategic pricing recommendations
- Optimisation thinking that balances revenue growth with supplier sustainability

**Status**: Completed (synthetic version for public portfolio)  
**Confidentiality Note**: All code, data, and visualisations in this repository are 100% synthetic and generalised. The real analysis was performed on a private production database.

---

← [Back to Main Portfolio](../../README.md)
