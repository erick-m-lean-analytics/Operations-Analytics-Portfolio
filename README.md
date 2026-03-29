# Operations-Analytics-Portfolio
**Erick Mortera**  
**Data-Driven Optimisation Engineer | Industrial Engineer | Lean & Toyota Production System Expert**

As a Data-Driven Optimisation Engineer with deep roots in Lean Manufacturing and Toyota Production System (TPS), I combine traditional industrial engineering expertise in resource planning, production forecasting, scheduling, and logistics with modern data analytics. 

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

The platform connects smash repairers (purchasers) with OEM and Aftermarket parts suppliers. Repairers use the platform to request quotes and source parts, while suppliers list parts and fulfil orders. The SaaS company earns revenue through a **clip % (take-rate / commission)** on the value of parts sold through the platform. Suppliers operate under a tiered membership model (Gold vs Blue) that influences their effective take-rate and platform benefits. 

**Stakeholder Request (CEO-level)**  
Review and optimise the current pricing model using **recent monthly transactional data**. Specifically requested:
- Monthly invoice amounts billed by the platform (full revenue roll-up)
- Supplier tier (Gold vs Blue) and Clip % (take-rate) each supplier is on
- Order volume, Gross Merchandise Value ($ order volume), credit values, part category classification and all other volume metrics captured in the system

**Key Deliverables**  
- Monthly supplier performance dashboard showing revenue contribution, tier behaviour, and take-rate effectiveness
- Segmentation of suppliers based on operational behaviour and profitability patterns
- Pricing tier reclassification options with estimated revenue uplift scenarios
- Actionable recommendations for adjusting clip % (take-rates) and tier logic to improve platform economics and supplier retention

**My Contribution as Data-Driven Optimisation Engineer**:
- Explored and mapped a large normalised relational database schema
- Designed and implemented monthly aggregation queries to surface pricing and performance trends
- **Applied K-means clustering to segment suppliers into behavioural groups ("supplier DNA") based on order patterns, GMV, credit behaviour, and take-rate response** — enabling targeted pricing strategies
- Quantified differences in behaviour and profitability between pricing tiers
- Delivered a clean, executive-ready dataset with clear recommendations for pricing adjustments

**Tech Used**  
- SQL: Time-based grouping, multi-table joins, and revenue calculations on normalised tables
- Python: Pandas for data transformation, Scikit-learn (K-means clustering with elbow method for optimal K), Plotly for visualisation and trend analysis
- Exploratory data analysis and feature scaling prior to clustering
  
**Status**: Completed – generalised queries, synthetic dataset, and insights available  
→ [View Project Details](./projects/supplier-pricing-optimisation)

**Confidentiality Note**: All data and visualisations shown are 100% synthetic. Real analysis was performed on a private production database.


1. Efficient Parts Delivery Routing for Assembly Lines  
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
