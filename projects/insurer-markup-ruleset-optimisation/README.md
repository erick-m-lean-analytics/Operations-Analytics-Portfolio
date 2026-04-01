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
Identified how many smash repair workshops were performing manual edits. Compared those configured with the legacy “Standard” ruleset against those using custom rulesets. Discovered that repairers do not use a single ruleset exclusively, they interchange between them. This revealed four distinct behavioural groups: purely custom, purely standard, mix-more-custom, and mix-more-standard.

Key SQL file: [repairer_override_groups.sql](./sql/repairer_override_groups.sql)

### 2. Custom Markup Rules Identification  
Analysed the specific markup rules being used by repairers in the custom-ruleset group to understand real-world pricing behaviour versus the configured defaults.

Key SQL file: [custom_markup_rules.sql](./sql/custom_markup_rules.sql)

### 3. Top 5 Insurer Candidate Selection  
Because the custom rules showed many variations even for the same insurer, identified and recommended the Top 5 insurers (based on reach and quote volume) that would be the strongest candidates for a new standardised baseline ruleset.

Key SQL file: `top5_insurer_baseline_candidates.sql`

### 4. Pilot Repairer Identification  
Selected a targeted list of smash repairers who would be ideal participants for a pilot program to test the new baseline ruleset.

Key SQL file: `pilot_repairer_selection.sql`

## Results & Recommendations

- Quantified the high-potential impact of the new baseline ruleset: smash repair workshops and their owners will retain more take-away profit while significantly reducing the lead time spent manually configuring markups  
- Created clear visibility into standard/default markups versus actual effective markups across the four behavioural groups  
- Identified and proposed the Top 5 insurers and their specific ruleset baselines (based on reach and quote volumes) that could serve as new default baselines for the platform  
- Recommended a targeted list of smash repairers for the pilot program to test the new baseline ruleset

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


