# Automated JIT Logistics & Routing Optimisation - Detailed Case Study

**Role: Group Head - Logistics Planning Group**

Project Type: Micro-Logistics Optimisation & Resource Planning

## Project Overview
This project digitises the complex manual engineering planning process used for Just-In-Time (JIT) parts delivery in high-precision manufacturing. By translating Toyota-style Industrial Engineering (IE) logic into a Python-based optimisation engine, I developed a tool that determines minimum lead times, optimises fleet size, and generates precise delivery schedules to maintain a synchronised flow while preventing traffic congestion.

## Problem Statement: The Operational Planning Bottleneck
In high-volume JIT environments, designing synchronised routes that minimise operational cost is an iterative and time-intensive process. Because a planner must manually simulate the dynamic interactions between Takt Time, container volumes, and physical path constraints, even minor changes to production variables require a total recalculation. Without the speed of a digital tool, the planning lead time is significantly prolonged, especially as the logistics network grows in complexity.

## Methodology
### 1. Digital Geography & Pathing Logic
To digitise the physical environment, I translated the plant’s CAD layout into a structured coordinate system, forming the spatial foundation of the routing engine.

  **1.1  Spatial Node Mapping:** Extracted (x, y) coordinates from the plant layout to define critical nodes, including the Warehouse (Depot), Line-side Delivery Stations, and Transit Points.

  To maintain high-fidelity with the physical shop floor, the following Node Classification was used:

  Code - Description: 

  TR/TL - TrimLine Station (Right/Left Handside),  C - Chassis Line Station,  F - Final Line Station,  EG - Engine Line Station,  AC_B - Aircon Building,  T0 - Trim zero (Start of Assembly Line),  SML_Dr - Small parts drop off point,  SML_St - Small parts delivery staging area,  
Bulky_1 - Bulky parts staging area No.1/No.2,  I_17 - Intersection No.17

  - Source Visual: [`Plant CAD layout.png`](./data/Factory_CAD_layout.png) 
  - Output: [`Node_coordinates.csv`](./data/Node_coordinates.csv)
 

  **1.2  Directed Edge (path) Construction - routing logic:** 
Defined the logical "From-To" connections between nodes to mathematically enforce the physical flow of the facility. By utilising Directed Edges, I ensured the routing engine strictly respects one-way aisle constraints and prevents illegal "backward" movements.

  - Output: [`From_To.csv`](./data/From_To.csv) 
  
  **1.3  Graph Visualisation of the shop-floor layout:** Utilised the NetworkX library to build a Directed Graph (DiGraph) of the factory floor. This allowed for visual verification of edge weights (distances) and flow directionality.
  - Script: [`factory_floor_layout.py`](./module/factory_floor_layout.py) 
  - Output: [`Factory graph visualisation`](./output/factory_floor_layout_cartesian.png) 
  
  **1.4 Distance Matrix Generation & Finding the shortest path between nodes:** Implemented Dijkstra’s Algorithm to **calculate the absolute shortest legal path** between every node pair. The result is an N x N Distance Matrix that serves as the primary input for the optimisation solver.
  - Script: [`master_distance_matrix.py`](./module/master_distance_matrix.py) 
  - Output: [`Distance_Matrix.csv`](./output/From_To_Distance_Matrix_Meters.csv) 


  ### 2. Workload Modelling & Service Standards (Gentan-i)

  To determine the optimal fleet size (drivers and tow-tractors) for any given demand, I calculated the precise Work Content for every delivery cycle. This phase translated physical handling constraints into high-fidelity time standards.
> [!IMPORTANT]
> This is the step where the input (production demand) can be adjusted for sensitivity analysis before running the subsequent scripts
>

  **2.1 Service Time Standardisation:** 
Mapped SKU-specific container types (Dunnage, Regular Dollies, and Custom Dollies) to their respective Standard Unloading/Loading Times. 
  - Logic Applied: Integrated the Gentan-i (standard time per unit of work) for vehicle travel speed, calibrated at 1.6s/m.
  - Scope: Focused on a specific vehicle-model segment within a Mixed-Model Production System to simulate high-complexity delivery requirements.
  - Output: [`Demand.csv`](./data/Demand.csv) 

  **2.2 Workload Explosion:** 
Generated a comprehensive task list by intersecting the delivery frequencies (i.e. 10, 50, 100-min cycles for the current Takt time) with standardised service times and required trip counts. This "exploded" the data into individual work elements, including travel times, service durations, and specific routes, to calculate the total required man-seconds.
  - Script: [`delivery_tasks_list.py`](./module/delivery_tasks_list.py) 
  - Output: [`Exploded_Task_List.csv`](./output/Exploded_Tasks_Verification.csv) 

  **2.3 Spatial Validation:** Cross-referenced all generated delivery routes and calculated travel times against the digital graph to ensure 100% alignment with physical aisle constraints.
  - Compare: [`Factory graph visualisation`](./output/factory_floor_layout_cartesian.png)  vs [`Exploded_Task_List.csv`](./output/EXploded_Tasks_Verification.csv) 
    
### 3. Constraint-Based Routing Optimisation (CVRP)
Utilised a Standardised 3-Slot Batch Constraint to aggregate the exploded task list into synchronised Milk Run trips. This stage focused on maximising tow tractor utilisation while respecting physical line-side space and equipment payload limits.

  **3.1 Intelligent Trip Bundling and Levelled deliveries (Heijunka):**
Developed a grouping algorithm that aggregates individual deliveries into unified trips based on:
  - Geographical Clustering: Grouping tasks by shared Lineside_Group to eliminate redundant travel "Muda."
  - Unified Path Physics: Identifying the furthest node within a bundle to calculate a single, accurate round-trip duration, preventing the "double-counting" of distances common in manual planning.
  - Pull-System (Levelled production): Enforcing a "No Duplicate Parts" constraint per trip to respect limited rack footprints at workstations and avoid inventory waste.
  - Traffic Congestion Prevention: Ensuring no simultaneous deliveries occur on the same aisle
    
  - Script: [`delivery_bundling_levveled_with_traffic_checkpy`](./module/delivery_bundling_levelled_with_traffic_check.py) 
  - Output: [`MIlk_Run_Delivery_Groups.csv`](./output/Milk_Run_Delivery_Groups_levelled.csv)

  **3.2 Quantified Resource Reduction:**
By aggregating the total required man-seconds (Travel + Service) across the 450-minute shift, the engine mathematically determined the minimum required fleet size.

> [!IMPORTANT]
> **Key Result: 40% Efficiency Gain**

The optimisation engine proved that the plant's production demand could be met with 3 drivers/tuggers instead of the 5 previously required by manual planning.
  - Total Work Content: 70,079.86 Seconds
  - Theoretical Headcount: 2.60 Drivers
  - Actual Requirement: 3 Drivers (Operating at 86% utilization)

## Tech Stack
- Python: Core logic and automation
- NetworkX: Logistics visualisation
- Pandas/NumPy: Data manipulation and matrix mathematics

## Skills Demonstrated
- Translation of Industrial Engineering (TPS) principles into algorithmic constraints
- Optimisation of high-frequency micro-logistics and "Point-of-Use" delivery
- Resource capacity planning and fleet size determination
- Designing industry-agnostic logic applicable to Mining, Warehousing, and Manufacturing

Status: Completed 

**Confidentiality Note:**
This project utilises the actual planning methodologies and operational flow logic used in Toyota manufacturing facilities. To ensure data privacy, the plant location and specific production models have been anonymised; however, the distances, aisle constraints, and service-time variables represent a verified, functional shop-floor environment.

← [Back to Main Portfolio](../../README.md)
