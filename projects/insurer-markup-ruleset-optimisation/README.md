# Insurer Markup Ruleset Optimisation – Detailed Case Study
**Role:** Business Process Excellence Engineer

**Project Type:** Pricing Ruleset & Operational Efficiency Optimisation

## Project Overview
Data-driven optimisation project for a B2B SaaS platform serving the Australian smash repair industry.
The platform enables smash repair workshops (purchasers) to source automotive parts from OEM, parallel, aftermarket, recycled, and reconditioned suppliers. Workshops apply configurable markup rulesets to determine the final sell price to insurers or walk-in customers. These rules operate at the client level (standard/default markups with custom overrides) and at the insurer level (specific markups by part type). The effective markup flows through quoting, supplier pricing selection, purchase orders, and automated invoice posting.


## Problem Statement
Active smash repair workshops were frequently manually editing markup rules in the platform. This caused undercharging or overcharging of insurers and customers, friction and approval delays, higher rework rates, longer lead times for repairs, and increased dependency on support team training.
Root Causes

New repairers were automatically assigned a legacy “Standard” ruleset during onboarding
Estimators regularly performed manual overrides on sell prices instead of using configured rules

## Methodology

### 1. Database Exploration & Mapping
Conducted a thorough review of the large normalised relational database schema. Mapped relationships across client pricing configurations, insurer mappings, quote drafts, purchase orders, and invoice posting tables to understand how markup rules actually flow from configuration to final invoiced price.

**Key SQL files:**
markup_ruleset_effective_calc.sql – core aggregation of standard vs actual markups
override_frequency_analysis.sql – quantification of manual edits


### 2. Real-World Markup & Override Analysis
Designed and implemented robust aggregation queries to calculate effective markups (standard/default vs actual) and measure the frequency and impact of manual overrides across repairers and insurers.
Gap Analysis & Baseline Identification
Performed exploratory data analysis to identify the most common insurer-specific rulesets in use and quantify the business impact of overrides on revenue leakage and operational friction.

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


