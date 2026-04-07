# Digitising JIT Resource Planning & Routing Optimisation# - Detailed Case Study

**Role: Group Head - Logistics Planning Group**

Project Type: Micro-Logistics Optimisation & Resource Planning

## Project Overview
This project digitises the complex manual engineering planning process used for Just-In-Time (JIT) parts delivery in high-precision manufacturing. By translating Toyota-style Industrial Engineering (IE) logic into a Python-based optimisation engine, I developed a tool that determines the optimal fleet size and generates precise delivery schedules to maintain synchronised flow.

## Problem Statement: The Simulation Bottleneck
In high-volume JIT environments, designing synchronised routes that minimise operational cost is an iterative and time-intensive process. Because a planner must manually simulate the dynamic interactions between Takt Time, container volumes, and physical path constraints, even minor changes to production variables require a total recalculation. Without the speed of a digital tool, the planning lead time is significantly prolonged, especially as the logistics network grows in complexity.

## Methodology
### 1. Digital Geography & Pathing Logic
To digitise the physical environment, I translated the plant’s CAD layout into a structured coordinate system, forming the spatial foundation of the routing engine.
1.1 Spatial Node Mapping: Extracted $(x, y)$ coordinates from the plant layout to define critical nodes, including the Warehouse (Depot), Line-side Delivery Stations, and Transit Points.
  - Data Source: Nodes_coordinates.csv

1.2 Directed Edge Construction: Defined the logical connections between nodes to reflect the physical flow of the facility. This step is where one-way aisle constraints were mathematically enforced by creating directed paths that prevent illegal "backward" movements.
  - Data Source: From_To_Edges.csv
  
1.3 Graph Visualisation: Utilised the NetworkX library to build a Directed Graph (DiGraph) of the factory floor. This allowed for visual verification of edge weights (distances) and flow directionality.
  - Script: factory_floor_layout.py
  
1.4 Pathfinding & Distance Matrix Generation: Implemented Dijkstra’s Algorithm to calculate the absolute shortest legal path between every node pair. The result is an $N \times N$ Distance Matrix that serves as the primary input for the optimization solver.
  - Script: routing_distance_matrix.py
  - Output: From_To_distance_matrix.csv



1.1 Using the plant CAD layout, mapped the physical shop floor into nodes through their x,y coordinates: parts' delivery staging locations and delivery locations at the assembly line - filename: Nodes_coordinates.csv
1.2 Construct the node relationships or connections to ensure the digital model respects the physical flow of the plant and to enforce one-way aisle constraints - filename: From_To.csv
1.3 Plotted them into a graph visualisation using NetworkX (directed graphs with edge weights/distance). - script: factory_floor_layout.py
1.4 Used the 'Dijkstra' algorithm to find the shortest route between two nodes. script: routing_distance.py output: From_To_distnce_matrix.csv


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
