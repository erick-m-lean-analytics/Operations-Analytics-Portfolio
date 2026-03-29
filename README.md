# Operations-Analytics-Portfolio
**Erick Mortera**  
**Data-Driven Optimisation Engineer | Industrial Engineer | Lean & Toyota Production System Expert**

As a Data-Driven Optimisation Engineer with deep roots in Lean Manufacturing and Toyota Production System (TPS), I combine traditional industrial engineering expertise in resource planning, production forecasting, scheduling, and logistics with modern **data analytics**. 

I use SQL, Python, and OR-Tools to uncover inefficiencies, improve supply chain performance, and deliver measurable gains in productivity, revenue, and operational efficiency across manufacturing and SaaS environments. 

## About Me
- **Name**: Erick Mortera
- **Specialisation**: Data-Driven Operational Optimisation using Lean/TPS principles
- **Focus Areas**: Routing optimisation, demand forecasting, workforce modelling, and predictive analytics.
- **Tools & Skills**: SQL, Python (Pandas, NumPy, OR-Tools), Excel/Power BI, data visualisation.
- **Contact**:erick.s.mortera@gmail.com

## Featured Projects
### 1. SaaS Supplier Pricing Optimisation 
**Project Overview**  
Data-driven optimisation project for a B2B SaaS platform in the automotive parts industry.  

The platform connects smash repairers (purchasers) with OEM and Aftermarket parts suppliers. Repairers use the platform to request quotes and source parts, while suppliers list parts and fulfil orders. The SaaS company earns revenue primarily through a **clip % (take-rate / commission)** on the value of parts sold through the platform. Suppliers operate under a tiered membership model (Gold vs Blue) that influences their effective take-rate and platform benefits.

**Problem Statement (CEO-level)**  
The business needed to review and optimise its pricing model to improve revenue while maintaining supplier retention. Using recent monthly transactional data, the key challenge was to understand how different supplier tiers and clip % (take-rates) affect order volume, GMV, credits, and overall platform economics.

**Key Objectives**  
- Analyse monthly invoice revenue (full commission roll-up)
- Understand supplier tier (Gold vs Blue) performance and effective clip % (take-rate)
- Measure order volume, Gross Merchandise Value (GMV), credit values, and other volume metrics
- Identify opportunities for pricing adjustments and tier reclassification

**Methodology Used**  
- Explored and mapped a large normalised relational database schema to understand relationships across orders, invoices, payments, and supplier tiers
- Designed and implemented efficient monthly aggregation queries to surface pricing trends, revenue contribution, and performance metrics
- Applied K-means clustering (with elbow method for optimal cluster selection) to segment suppliers into distinct behavioural groups ("supplier DNA") based on order patterns, GMV, credit behaviour, and take-rate response
- Quantified key differences in supplier behaviour and profitability across pricing tiers and take-rates

**Tech Used**  
- SQL: Time-based grouping, multi-table joins, and revenue calculations on normalised tables
- Python: Pandas for data transformation, Scikit-learn (K-means clustering with elbow method), Plotly for visualisation and trend analysis
- Exploratory data analysis and feature scaling prior to clustering

**Results & Recommendations**  
- Developed multiple pricing reclassification options and uplift strategies, including:
  - Tier-specific clip % adjustments based on supplier behavioural segments
  - Dynamic take-rate bands instead of a single fixed rate per tier
  - Targeted pricing logic to improve supplier retention while protecting overall platform revenue
- Delivered a clean, executive-ready monthly dataset with clear, data-backed recommendations for pricing adjustments and estimated potential revenue uplift scenarios
- Translated complex database outputs into stakeholder-friendly insights and visualisations to support strategic decision-making

**Status**: Completed – generalised queries, synthetic dataset, and insights available  
→ [View Full Project Details](./projects/supplier-pricing-optimisation)

**Confidentiality Note**: All data, queries, and visualisations shown here are 100% synthetic. Real analysis was performed on a private production database.


### 2. Markup Ruleset Optimisation & Revenue Leakage Analysis
**Project Overview**
Data-driven optimisation project for a B2B SaaS platform serving the Australian smash repair industry.
The platform enables smash repair workshops (purchasers) to source automotive parts from OEM, parallel, aftermarket, recycled, and reconditioned suppliers. Workshops apply configurable markup rulesets to determine the final sell price to insurers or customers. These rules operate at two main levels:

Client-level (standard/default ruleset): Default markup percentages set by each smash repair workshop, with the ability to apply custom overrides.
Insurer-level ruleset: Specific markup percentages negotiated or mandated by insurers, broken down by part type (OEM, parallel, aftermarket, recycled, reconditioned).

The effective markup is calculated by combining the standard/default rules with any overrides or insurer-specific rates. This flows through draft quoting, supplier pricing selection, purchase orders, and automated invoice posting — including complex handling for credits, cancellations, No Longer Available (NLA) items, non-active month adjustments, and paid vs unpaid invoices. The SaaS platform earns revenue via a clip % (take-rate / commission) applied to the final marked-up value.

**Business Problem Statement**
The platform was experiencing inconsistent and suboptimal markup application across its client base. Many smash repair workshops frequently overrode the standard/default markup rules, while insurer-specific rules were not always correctly mapped or enforced. This created several issues:

- Revenue leakage for the platform (lower clip % revenue due to lower effective markups)
- Difficulty in predicting and controlling platform fee income
- Potential margin erosion for repair workshops or disputes with insurers
- Lack of visibility into which rules were actually driving revenue versus which were being bypassed

**Objectives**
The Head of Product needed a clear understanding of how the current standard/default + insurer + override rules were performing in the real world and actionable recommendations to optimise the entire ruleset for better platform economics without harming client relationships.
Stakeholder Request (Product Manager-level)
Analyse and optimise the current markup ruleset using recent transactional data from quoting, supplier pricing, and posted invoices. Specifically requested:

**Key Deliverables**

Markup performance dashboard showing standard/default vs effective markups, override frequency, variance analysis, fee revenue contribution, and period-over-period trends
Segmentation of clients and insurers based on markup behaviour, override patterns, part-type usage, and profitability impact
Ruleset optimisation scenarios with estimated revenue uplift, client margin effects, and retention risk
Prioritised, actionable recommendations for refining standard/default markups, insurer-specific rules, override controls, and automated posting logic

**My Contribution as Data-Driven Optimisation Engineer:**

Explored and mapped the complex normalised relational database schema linking client configurations, insurer mappings, draft/supplier pricing, purchase orders, and invoice posting tables
Designed and implemented robust aggregation queries to calculate real-world effective markups, override impact, credit/NLA/cancellation adjustments, and variance metrics
Applied K-means clustering to segment clients and insurers into behavioural groups (“markup DNA”) based on override frequency, part-type markup usage, fee contribution, credit behaviour, and compliance patterns — enabling targeted ruleset adjustments and personalised recommendations
Quantified revenue leakage from current standard/default + override logic versus optimised scenarios and simulated business impact
Delivered a clean, executive-ready dataset with visualised insights and prioritised change roadmap

**Tech Used**

SQL: Multi-table joins across normalised schema, conditional aggregation for credits/NLA/cancellations/non-active adjustments, time-based grouping, and window functions for trend analysis
Python: Pandas for data transformation and feature engineering, Scikit-learn (K-means clustering with elbow method for optimal K), Plotly for interactive dashboards and scenario visualisations
Exploratory data analysis, feature scaling, and business-rule simulation prior to clustering

Status: Completed – generalised queries, synthetic dataset, and insights available
→ View Project Details
Confidentiality Note: All data and visualisations shown are 100% synthetic. Real analysis was performed on a private production database.









2. Efficient Parts Delivery Routing for Assembly Lines  
   - Description: Algorithm to optimize delivery routes for automotive parts, considering constraints like one-way paths, capacities, and just-in-time delivery based on takt time.  
   - Tech: Python with OR-Tools for vehicle routing.  
   - [View Project](./projects/assembly-line-delivery-routing/README.md)

2. Workforce Management Calculator 
   - (Coming soon) Based on cycle times and demand to forecast required team members.

3. Cohort Analysis for Retention  
   - (Coming soon) Analyzing patterns in manufacturing data.

## Why This Portfolio?
These projects highlight skills in analytical problem-solving, stakeholder-friendly insights, and operational efficiency—directly relevant to roles in supply chain, mining/oil & gas, and remote operations.

Feel free to star this repo or reach out if you'd like to collaborate!
