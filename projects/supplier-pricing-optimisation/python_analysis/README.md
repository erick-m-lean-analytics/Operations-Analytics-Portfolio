# Python Analysis – Supplier Pricing Optimisation

This folder contains the Python scripts used to process the aggregated SQL data and perform behavioural segmentation.

## Main Script
**`data_preparation_and_clustering.py`**

**What it does:**
- Loads the four CSV files produced by the SQL queries
- Merges them into a single supplier-level dataset
- Calculates composite indices (Scale, Efficiency, Loyalty, Specialisation, Credit Health)
- Performs feature scaling
- Runs K-means clustering (using elbow method for validation)
- Produces two output files:
  - `Cluster_Uplift_Summary.csv` – high-level cluster profiles and metrics
  - `Supplier_Master_Clustering_Analysis.csv` – detailed per-supplier view

## How to run
1. Place the output CSVs from the SQL queries in the `data/` folder
2. Run `python data_preparation_and_clustering.py`

## Output Files
- `Cluster_Uplift_Summary.csv` – Cluster-level summary (recommended for review)
- `Supplier_Master_Clustering_Analysis.csv` – Full per-supplier dataset with indices and proposed logic

This script demonstrates end-to-end data preparation, feature engineering, and unsupervised learning for operational decision-making.
