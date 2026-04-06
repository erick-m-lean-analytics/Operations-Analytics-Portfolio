# Digitising JIT Resource Planning & Routing Optimisation#

**Role: Industrial Engineer / Logistics Operations Architect**

Project Type: Micro-Logistics Optimization & Resource Planning

## Project Overview##
This project digitises the complex manual engineering planning process used for Just-In-Time (JIT) parts delivery in high-precision manufacturing. By translating Toyota-style Industrial Engineering (IE) logic into a Python-based optimisation engine, I developed a tool that determines the optimal fleet size and generates precise delivery schedules to maintain synchronised flow.

## Problem Statement: The Simulation Bottleneck
In high-volume JIT environments, designing synchronised routes that minimise operational cost is an iterative and time-intensive process. Because a planner must manually simulate the dynamic interactions between Takt Time, container volumes, and physical path constraints, even minor changes to production variables require a total recalculation. Without the speed of a digital tool, the planning lead time is significantly prolonged, especially as the logistics network grows in complexity.

## Methodology
### 1. Digital Geography & Pathing Logic
Mapped the physical shop floor into a mathematical Distance Matrix. Applied a constant speed of 1.6s/m to convert spatial distance into travel time. Implemented a "Big M" Penalty logic to strictly enforce one-way aisle constraints, ensuring the digital model respects the physical flow of the plant.

Key Python script:

step1_geography.py – matrix generation & one-way logic

### 2. Workload & Service Standards Mapping
Designed a systematic approach to define the "Work Content" of each delivery. Mapped SKU container types (Crates, Dollies, Single-piece) to their respective Standard Unloading Times. Used Pandas to aggregate these standards into a station-level workload dataset.

Key Data files:

parts_demand.csv – SKU frequencies (10, 50, 100-min cycles)

service_standards.json – Standard times per container type

### 3. Constraint-Based Routing Optimization (CVRP)
Applied the Capacitated Vehicle Routing Problem (CVRP) model using Google OR-Tools. The "Capacity" was defined as Time; the solver was constrained to ensure the sum of Travel Time and Service Time never exceeded the Takt Time (600s). This automatically determined the minimum number of vehicles required for the loop.

Python script:

step3_optimizer.py – OR-Tools implementation

### 4. Verification & Sensitivity Analysis
Consolidated the modular steps into an integrated pipeline to perform "What-If" simulations. Tested the impact of Takt Time fluctuations and speed variability on fleet requirements. Generated Gantt charts to verify Synchronised Release, ensuring no two vehicles occupy the same one-way aisle simultaneously.

**Visuals:**

Route Gantt Chart – Conflict-free dispatching visualization

Takt Sensitivity Plot – Fleet size vs. production beat

## Tech Stack
- Python: Core logic and automation
- Google OR-Tools: Combinatorial optimization (Routing)
- Pandas/NumPy: Data manipulation and matrix mathematics
- Matplotlib/Plotly: Logistics visualization and Gantt charts

## Skills Demonstrated
- Translation of Industrial Engineering (TPS) principles into algorithmic constraints
- Optimization of high-frequency micro-logistics and "Point-of-Use" delivery
- Resource capacity planning and fleet size determination
- Designing industry-agnostic logic applicable to Mining, Warehousing, and Manufacturing
- Status: Completed (Synthetic version for public portfolio)

**Confidentiality Note:**
This project utilises the actual planning methodologies and operational flow logic used in Toyota manufacturing facilities. To ensure data privacy, the plant location and specific production models have been anonymised; however, the distances, aisle constraints, and service-time variables represent a verified, functional shop-floor environment.

← [Back to Main Portfolio](../../README.md)
