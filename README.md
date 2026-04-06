# Operations-Analytics-Portfolio
## Featured Projects
### Project 1. Digitising JIT Resource Planning & Routing Optimisation

**Project Overview**

This project digitises the complex manual planning process used for parts delivery in high-precision manufacturing. By translating Industrial Engineering logic into Python code, I built a tool that calculates the exact number of delivery resources needed and generates a precise schedule to maintain Just-In-Time (JIT) flow. 

The tool is designed to automate the standard planning steps for designing a parts delivery system in a car manufacturing plant: ensuring parts arrive exactly when needed while managing physical floor constraints such as one-way aisles and limited lineside space.

Although it was designed for high-volume manufacturing, the logic is industry-agnostic and can be applied to any operation that requires synchronised logistics, such as mining supply chains, large-scale warehousing, or regional land logistics.

**Problem Statement (Operational Planning)**
In a high-volume environment, planning delivery routes manually is prone to error. If deliveries are unsynchronised, two major issues occur:

- Traffic Congestion: Too many vehicles are hitting the same one-way aisles at once, causing delays.
- Inventory Imbalance: Too much stock at the assembly line (overflow) or too much at the warehouse (blocking flow).

**Key Objectives**
- Synchronised Release: Time the departure of each delivery to prevent "traffic jams" in unidirectional paths.
- Inventory Minimisation: Maintain the minimum stock at both the warehouse and the lineside to support continuous flow.
- Resource Optimisation: Determine the fewest number of drivers/vehicles required to meet the production beat (Takt Time).
- Path Constraints: If delivering in a unidirectional path, strictly follow one-way traffic rules.

**Methodology**
- Network Mapping (NetworkX): I mapped the facility as a "Directed Graph." This allowed the program to recognise that moving from Point A to B might be a short distance, but the return from B to A must follow a specific one-way loop.
- Automated Logic (OR-Tools): I translated manual "expert" rules into mathematical constraints:

  Capacity: How much can one vehicle carry?
  Parts unloading cycle times: How long does it take to unload the parts onto lineside flow racks

  Timing: When must the vehicle leave to arrive at the exact moment stock runs low? - 

  Spacing: How many seconds must be between vehicle releases to avoid congestion in the aisles? - This is used to set a timetable of delivery to follow

Schedule Generation: The tool outputs a "Logistics Timetable" that tells operators exactly what to load, when to leave, and which path to take.

   - [View Project](./projects/assembly-line-delivery-routing/README.md)


### Project 2. SaaS Supplier Pricing Optimisation 
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
- Designed and implemented efficient monthly aggregation queries to surface key operational attributes of the supplier. 
- Constructed a composite index and normalised individual metrics to enable consistent cross-supplier comparison
- Applied K-means clustering using the elbow method to determine the optimal number of clusters to segment suppliers into distinct behavioural groups ("supplier DNA") based on order patterns, GMV, credit behaviour, and take-rate response
- Quantified key differences in supplier behaviour, performance, and profitability across pricing tiers and take-rates

**Tech Used**  
- MySQL: Time-based grouping, multi-table joins, and revenue calculations on normalised tables
- Python: Pandas for data transformation, Scikit-learn (K-means clustering with elbow method), Plotly for visualisation and trend analysis

**Results & Recommendations**  
- Developed multiple pricing reclassification options and uplift strategies, including:
  - Tier-specific clip % adjustments based on supplier behavioural segments
  - Dynamic take-rate bands instead of a single fixed rate per tier
  - Targeted pricing logic to improve supplier retention while protecting overall platform revenue
- Delivered a clean, executive-ready monthly dataset with clear, data-backed recommendations for pricing adjustments and estimated potential revenue uplift scenarios
- Translated complex database outputs into stakeholder-friendly insights and visualisations to support strategic decision-making

**Status**: Completed – generalised queries, synthetic dataset, and insights available  

**Confidentiality Note**  
The SQL queries and Python scripts in this project closely reflect the logic and approach I used in the real analysis. Table names, column names, and all data have been generalised and replaced with synthetic examples to protect confidentiality. The original work was performed on a private production database.

→ [View Full Project Details](./projects/supplier-pricing-optimisation)

### Project 3. Insurer Markup Ruleset Optimisation

**Project Overview**

Data-driven optimisation project for a B2B SaaS platform serving the Australian smash repair industry.

The platform enables smash repair workshops (purchasers) to source automotive parts from OEM, parallel, aftermarket, recycled, and reconditioned suppliers. Workshops apply configurable markup rulesets to determine the final sell price to insurers or walk-in customers. These rules operate at both the client level (standard/default markups with custom overrides) and the insurer level (specific markups by part type). The effective markup flows through quoting, supplier pricing selection, purchase orders, and automated invoice posting.

**Problem Statement (Product Manager-level)**
Active smash repair workshops were frequently manually editing markup rules in the platform. This caused undercharging or overcharging of insurers and customers, friction and approval delays, higher rework rates, longer lead times for repairs, and increased dependency on support team training.

**Root Causes**
- New repairers were automatically assigned a legacy “Standard” ruleset during onboarding
- Estimators regularly performed manual overrides on sell prices instead of using configured rules

**Key Objectives** 
- Identify which smash repair shops were performing frequent manual edits/overrides
- Understand how often custom overrides were actually occurring in practice
- Identify gaps in pricing method rulesets when used with different insurers
  
**Methodology Used**
- Explored and mapped the complex normalised relational database schema linking repairer's price method configurations, insurer mappings, and invoice posting tables
- Performed exploratory data analysis and data preparation (cleaning and shaping dataframes)
- Designed and implemented robust aggregation queries to calculate real-world effective markups and quantify override impact

**Tech Used**
- MySQL: Multi-table joins across normalised schema, conditional aggregation, and time-based analysis
- Excel Power Pivot for reporting and visualisation

**Results & Recommendations**
- Created clear visibility into standard/default markups versus actual effective markups
- Identified and proposed Top 5 insurers and specific ruleset baselines based on reach and quote volumes that could serve as new default baselines
- Recommended a targeted list of smash repairers for the pilot program to test the new baseline ruleset

**Status:** Completed – generalised queries, synthetic dataset, and insights available
→ View Full Project Details

**Confidentiality Note**  
The SQL queries in this project closely reflect the logic and approach I used in the real analysis. Table names, column names, and all data have been generalised and replaced with synthetic examples to protect confidentiality. The original work was performed on a private production database.

→ [View Full Project Details](./projects/insurer-markup-ruleset-optimisation)






