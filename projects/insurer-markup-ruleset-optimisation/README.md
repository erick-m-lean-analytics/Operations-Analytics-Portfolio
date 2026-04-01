# Insurer Markup Ruleset Optimisation – Detailed Case Study
**Role:** Business Process Excellence Engineer

**Project Type:** Pricing Ruleset & Operational Efficiency Optimisation

## Project Overview
Data-driven optimisation project for a B2B SaaS platform serving the Australian smash repair industry.

The platform enables smash repair workshops to apply configurable markup rulesets that determine the final sell price to insurers or walk-in customers. These rules flow from client-level defaults and insurer-specific overrides all the way through quoting, purchase orders, and automated invoice posting.

## Problem Statement
Active smash repair workshops were frequently manually editing markup rules in the platform. This caused undercharging or overcharging of insurers and customers, friction and approval delays, higher rework rates, longer lead times for repairs, and increased dependency on support team training.
Root Causes

New repairers were automatically assigned a legacy “Standard” ruleset during onboarding
Estimators regularly performed manual overrides on sell prices instead of using configured rules

## Methodology

### 1. Repairer Override Behaviour Analysis  
Identified how many smash repair workshops were performing manual edits. Compared those configured with the legacy “Standard” ruleset against those using custom rulesets. Discovered that repairers do not use a single ruleset exclusively; they alternate between them. This revealed four distinct behavioural groups: purely custom, purely standard, mix-more-custom, and mix-more-standard.

Key SQL file: [repairer_override_groups.sql](./sql/repairer_override_groups.sql)

### 2. Custom Markup Rules Identification  
Analysed the specific markup rules being used by repairers in the custom-ruleset group to understand real-world pricing behaviour versus the configured defaults.

Key SQL file: [custom_markup_rules.sql](./sql/custom_markup_rules.sql)

### 3. Top 5 Insurer Candidate Selection  
Because the custom rules showed many variations even for the same insurer, I identified and recommended the Top 5 insurers (based on reach and quote volume) that would be the strongest candidates for a new standardised baseline ruleset.

Key SQL file: [top5_insurer_baseline_candidates.sql](./sql/top5_insurer_baseline_candidates.sql)

### 4. Pilot Repairer Identification  
Selected a targeted list of smash repairers who would be ideal participants for a pilot program to test the new baseline ruleset.

Key SQL file: [pilot_repairer_selection.sql](./sql/pilot_repairer_selection.sql)

## Results & Recommendations
- Identified four distinct repairer behavioural groups based on custom-rule adoption (last 90 days):
  - Purely Custom (100% of drafts): ~20% of active repairers
  - High Custom Adoption (>75% of drafts): ~6% of repairers
  - Hybrid User (25%-75%): ~3% of repairers
  - Low Custom Adoption (<25%): ~71% of repairers

- Magnitude of manual edits across all line items was consistently low (under 2% per draft on average), meaning the configured rules (standard or custom) were applied without tweaks in the vast majority of drafts. However, there is still a strong business rationale for establishing a new baseline ruleset and running targeted pilots before these rates potentially increase.

- Additional insight from custom-ruleset analysis: Even among repairers using custom rules, a portion of the configurations were incorrect or set in a way that would cause the repairer to lose profit (under-charging)

- Quantified the high-potential impact of the new baseline ruleset: smash repair workshops and their owners will retain more take-home profit while significantly reducing the lead time spent manually configuring markups  

- Benefits of implementing the new baseline ruleset:
  - Increased take-home profit for repairers by reducing incorrect or suboptimal markup configurations
  - Efficiency Gains: Reducing even a small percentage of manual edits frees up time for higher-value work (e.g., more repairs or better customer service)
  - Scalability and Futureproofing: Creates a more consistent, supportable platform for long-term growth

- Proposed two options for the Top 5 insurers as candidates for the new standardised baseline ruleset:
  - Option 1 (Market Reach): The five insurers with the broadest shop adoption – ideal for widespread efficiency gains across the most repairers
  - Option 2 (Quote Volume): The five insurers with the highest quote throughput – ideal for high-throughput scenarios where even small optimisations yield big savings

- Recommended a targeted list of smash repairers for the pilot program (high-volume shops aligned with the top insurers) to test the new baseline ruleset and validate the efficiency and profit-protection gains.
**Sample Outputs**  
- [Top 5 Insurer Candidates](./results/top5_insurer_candidates.csv)  
- [Pilot Repairer Candidates](./results/pilot_repairer_candidates.csv)

**Tech Stack**
MySQL: Multi-table joins across normalised schema, conditional aggregation, and time-based analysis
Excel Power Pivot for reporting and visualisation

**Skills Demonstrated**
End-to-end relational database analysis in a complex normalised schema
Quantifying real-world pricing behaviour versus configured rules
Translating analytical findings into actionable product and operational recommendations
Balancing pricing accuracy with user experience and repairer retention

**Status:** Completed (synthetic version for public portfolio)

**Confidentiality Note:**
The SQL queries in this project closely reflect the logic and approach I used in the real analysis. Table names, column names, and all data have been generalised and replaced with synthetic examples to protect confidentiality. The original work was performed on a private production database.

← [Back to Main Portfolio](../../README.md)


