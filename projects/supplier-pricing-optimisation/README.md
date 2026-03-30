# SaaS Supplier Pricing Optimisation – Detailed Case Study

**Role**: Business Process Excellence Engineer  
**Project Type**: Pricing Strategy & Revenue Optimisation

## Project Overview
This project focused on optimising the pricing model of a B2B SaaS platform that connects smash repairers with OEM and Aftermarket parts suppliers. The platform facilitates quote requests and part sourcing, with the business earning revenue primarily through a clip % (take-rate / commission) on the value of parts sold.

Suppliers operate under a tiered membership model (Gold vs Blue) that influences their effective take-rate. The goal was to move beyond a simple two-tier system and develop a more nuanced, data-driven pricing approach.

## Problem Statement
The existing Gold vs Blue tier structure and fixed take-rate logic were not optimally aligned with actual supplier behaviour. Leadership needed to understand:
- How different tiers and take-rates impact order volume, GMV, credits, and overall revenue
- Whether suppliers could be segmented more effectively based on real operational patterns
- What pricing adjustments could drive sustainable revenue growth while protecting supplier retention

## Methodology

### 1. Database Exploration & Mapping
- Conducted a thorough review of the normalised relational schema
- Identified key relationships between orders, invoices, payment engine data, membership tiers, and supplier attributes

### 2. Monthly Data Aggregation
- Built robust SQL queries to aggregate monthly metrics per supplier
- Calculated revenue contribution, GMV, order volume, credit ratios, and effective clip %
- Ensured time-series consistency across 24 months of data

### 3. Supplier Behavioural Segmentation
- **Why K-means?** Chosen for its simplicity, scalability, and ability to discover natural groupings in supplier behaviour without requiring labelled data.
- Features engineered: average GMV, order frequency, repairer preference strength, credit behaviour ratio, take-rate sensitivity, and part category diversity.
- Used the elbow method to determine the optimal number of clusters.
- Applied feature scaling and validated cluster quality using the index score and visual inspection.

**Determining Optimal Number of Clusters**
- Used the **elbow method** to identify the optimal number of clusters by plotting the within-cluster sum of squares (WCSS) against the number of clusters (K).
- The elbow point helped balance cluster compactness versus interpretability.

![Elbow Method for Optimal K](visuals/elbow_method.png)

**Feature Scaling Note**  
Prior to clustering, all features were normalised using StandardScaler to ensure equal contribution regardless of their original scale.

## Cluster Results (Supplier DNA)

After feature engineering and scaling, K-means clustering (validated with elbow method and silhouette score) revealed distinct behavioural segments among suppliers.

**Example of Resulting Behavioural Segments** (Synthetic illustration based on the applied methodology)

| Cluster | Description                        | Key Characteristics                          | Typical GMV Level | Take-rate Sensitivity | Recommended Pricing Strategy                          |
|---------|------------------------------------|----------------------------------------------|-------------------|-----------------------|-------------------------------------------------------|
| 0       | High-volume stable performers      | High GMV, strong loyalty & specialization    | Very High         | Low                   | Protective lower take-rate to maximise long-term retention |
| 1       | Growth-oriented consistent suppliers | Medium-high GMV, good efficiency             | High              | Medium                | Balanced dynamic take-rate bands with volume incentives   |
| 2       | Price-sensitive mid-tier           | Moderate GMV, higher credit usage            | Medium            | High                  | Conservative take-rate with targeted support programs     |
| 3       | Emerging or variable suppliers     | Lower GMV, mixed specialization              | Low-Medium        | Very High             | Growth-oriented entry rates with performance milestones    |

*(In the actual analysis, 6 meaningful clusters emerged with clear differences in profitability contribution and price elasticity. Full cluster profiles, centroids, and interactive visualisations are available in the Python notebook.)*

These behavioural segments ("supplier DNA") provided significantly richer insights than the existing Gold vs Blue tiers and formed the foundation for the pricing reclassification recommendations.

### 4. Comparative Analysis
- Analysed performance differences between the existing Gold/Blue tiers and the new behavioural clusters
- Quantified how take-rate levels affected different supplier segments

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
