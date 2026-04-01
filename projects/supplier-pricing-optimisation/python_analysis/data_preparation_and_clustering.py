# =============================================================================
# Supplier Pricing Consolidation & Clustering Script
# This script merges multiple datasets exported from SQL queries. Most files were already aggregated to supplier-month level.
# The resulting dataset is then used for index calculation, K-means clustering, and pricing uplift analysis.
# =============================================================================

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import os
import warnings

# ====================== 1. PATH CONFIGURATION ======================
working_path = r"C:\Users\ErickMortera\Documents\SQL_projects\Supplier Pricing"
summary_output = os.path.join(working_path, "Cluster_Uplift_Summary.csv")
master_output = os.path.join(working_path, "Supplier_Master_Clustering_Analysis.csv")

# ====================== 2. PART SPECIALISATION INDEX ======================
# The specialisation data ("Top_part_types_&_make_dominated.csv") was still at a more granular level (per item type / make). Therefore, I calculated the 
# category concentration ratio (Specialisation Index) before merging it with the other supplier-level metrics.

try:
    spec_path = os.path.join(working_path, "Top_part_types_&_make_dominated.csv")
    spec_raw = pd.read_csv(spec_path)
    
    potential_cols = ['estimated_gmv_requested_qty', 'gmv_this_category', 'gmv', 'estimated_gmv']
    gmv_col = next((c for c in spec_raw.columns if c in potential_cols or 'gmv' in c.lower()), None)
    
    if gmv_col:
        total_gmv_per_supp = spec_raw.groupby('supplier_id')[gmv_col].sum()
        cat_totals = spec_raw.groupby(['supplier_id', 'item_type_id'])[gmv_col].sum().reset_index()
        top_cat_gmv = cat_totals.groupby('supplier_id')[gmv_col].max()
        spec_df = (top_cat_gmv / total_gmv_per_supp.replace(0, 1)).reset_index()
        spec_df.columns = ['supplier_id', 'category_concentration_ratio']
    else:
        spec_df = pd.DataFrame(columns=['supplier_id', 'category_concentration_ratio'])
        
except Exception as e:
    spec_df = pd.DataFrame(columns=['supplier_id', 'category_concentration_ratio'])

# ====================== 3. DATA MERGE & GHOST REMOVAL ======================
df = pd.read_csv(os.path.join(working_path, "Supplier_profile_with_metrics_final_supplier_level.csv"))
df = df.merge(spec_df, on='supplier_id', how='left')

med_val = df['category_concentration_ratio'].median()
df['category_concentration_ratio'] = df['category_concentration_ratio'].fillna(med_val if pd.notna(med_val) else 0.5)

df = df.merge(pd.read_csv(os.path.join(working_path, "Supplier_quotewin_rate_and_avg_fill_rate.csv")), on='supplier_id', how='left', suffixes=('', '_dup'))
df = df.merge(pd.read_csv(os.path.join(working_path, "Preferred_supplier_relationship_aggregated_to_supplier_level.csv")), left_on='supplier_id', right_on='supplierID', how='left', suffixes=('', '_dup'))

credit_df = pd.read_csv(os.path.join(working_path, "Supplier_credit_profile.csv"))
credit_agg = credit_df.groupby('supplier_id').agg({'pct_preventable_of_credited_lines': 'mean', 'credited_line_count': 'sum', 'order_volume': 'sum'}).reset_index()
credit_agg['credit_frequency_rate'] = (credit_agg['credited_line_count'] / credit_agg['order_volume'].replace(0, 1))
df = df.merge(credit_agg, on='supplier_id', how='left', suffixes=('', '_dup'))

# Standard cleanup
df = df.loc[:, ~df.columns.str.contains('_dup')].fillna(0)

# Quality filter - remove low-activity or anomalous suppliers
initial_count = len(df)
df = df[
    (df['months_with_data'] > 1) & 
    (df['total_gmv_gross'] >= 1000) & 
    (df['value_weighted_fill_rate_pct'] > 0) &
    (df['category_concentration_ratio'] > 0)
].copy()

print(f"Data Cleansed. Removed {initial_count - len(df)} rows. {len(df)} High-Quality Suppliers remaining.")


# ====================== 4. INDEX CALCULATION & CLUSTERING ======================
scaler = MinMaxScaler()

# Scale individual components
df['INDEX_Scale'] = scaler.fit_transform(df[['total_gmv_gross']])
df['INDEX_Efficiency'] = scaler.fit_transform(df[['value_weighted_fill_rate_pct']])

# INDEX_Loyalty: Weighted combination of repairer relationship strength, consistency, and tenure 
# Weights chosen based on business intuition: 
#   - 45% on weighted supplier share with repairers (strongest signal of loyalty)
#   - 35% on activity consistency
#   - 20% on tenure on platform
tenure = (df['months_on_platform'] / df['months_with_data'].replace(0, 1))
loyalty_raw = (0.45 * (df['avg_unique_repairers_per_month'] * df['avg_weighted_supplier_share']) + 0.35 * df['activity_consistency_pct'] + 0.20 * tenure)
df['INDEX_Loyalty'] = scaler.fit_transform(loyalty_raw.values.reshape(-1, 1))
df['INDEX_Specialization'] = scaler.fit_transform(df[['category_concentration_ratio']])

# INDEX_Credit_Health: Inverse of credit risk (higher = better)
# Weights: 60% on preventable credits, 40% on credit frequency
credit_risk_raw = (0.60 * df['pct_preventable_of_credited_lines'] + 0.40 * df['credit_frequency_rate'])
df['INDEX_Credit_Health'] = 1 - scaler.fit_transform(credit_risk_raw.values.reshape(-1, 1))

# Final feature set for clustering
features = ['INDEX_Scale', 'INDEX_Efficiency', 'INDEX_Loyalty', 'INDEX_Specialization', 'INDEX_Credit_Health']

# Clustering: Elbow method initially showed a bend around K=6. After testing multiple values, I used n_clusters=6 for the final model.
df['AI_Cluster'] = KMeans(n_clusters=6, random_state=42, n_init=10).fit_predict(df[features])

# ====================== 5. SUMMARY: PROPOSE RATE & UPLIFT CALCULATION ======================
# Calculate current clip rate
df['Current_Clip_Rate'] = (df['total_fees_billed'] / df['total_gmv_gross'].replace(0, 1))

# Calculate average GMV per month
if 'avg_gmv_per_month' not in df.columns:
    df['avg_gmv_per_month'] = df['total_gmv_gross'] / df['months_with_data'].replace(0, 1)

# 75th percentile threshold (data-driven)
gmv_75th_per_month = 56782   # Rounded from your calculation: 1,192,422.17 / 21

def get_target_rate_and_tier(row):
    """
    Proposed re-classification and take-rate logic using 75th percentile of avg GMV:
    - Suppliers with avg GMV below ~$56,782 per month lose Gold classification (move to Blue).
    - Blue suppliers with avg GMV above ~$56,782 per month get a lower take-rate (0.013).
    """
    current_tier = row['dominant_tier']
    avg_gmv = row['avg_gmv_per_month']
   
    # Step 1: Re-classification
    if current_tier == 'Gold' and avg_gmv < gmv_75th_per_month:
        new_tier = 'Blue'
    else:
        new_tier = current_tier
   
    # Step 2: Apply take-rate based on new tier
    if new_tier == 'Blue':
        if avg_gmv >= gmv_75th_per_month:
            return 0.013, new_tier           # Lower rate for high-volume Blue suppliers
        else:
            return 0.015, new_tier           # Standard Blue rate (1.5%)
    else:  # Gold
        return 0.0115, new_tier              # Standard Gold rate



# Apply the new target rate to every supplier
df['AI_Target_Rate'] = df.apply(get_target_rate_and_tier, axis=1)

# Calculate new target revenue excluding GST
df['AI_Target_Revenue_ExGST'] = (df['total_gmv_gross'] * df['AI_Target_Rate']) / 1.1

# Calculate net uplift (positive = expected revenue gain)
df['AI_Net_Uplift_ExGST'] = df['AI_Target_Revenue_ExGST'] - df['total_fees_billed']

# Shows how the old Blue/Gold tiers are distributed across the new clusters
tier_stats = df.groupby(['AI_Cluster', 'dominant_tier']).agg({'supplier_id': 'count', 'Current_Clip_Rate': 'mean'}).unstack(fill_value=0)
tier_stats.columns = [f'{col[0]}_{col[1]}' for col in tier_stats.columns]

# Shows detailed profile for each new AI cluster 
cluster_stats = df.groupby('AI_Cluster').agg({
    'INDEX_Scale': 'mean', 'INDEX_Efficiency': 'mean', 'INDEX_Loyalty': 'mean', 'INDEX_Specialisation': 'mean', 'INDEX_Credit_Health': 'mean',
    'value_weighted_fill_rate_pct': 'mean', 'category_concentration_ratio': 'mean', 'pct_preventable_of_credited_lines': 'mean',
    'total_gmv_gross': 'sum', 'total_fees_billed': 'sum', 'AI_Target_Revenue_ExGST': 'sum', 'AI_Net_Uplift_ExGST': 'sum'
}).rename(columns={'value_weighted_fill_rate_pct': 'ACTUAL_Avg_Fill_Rate', 'category_concentration_ratio': 'ACTUAL_Avg_Specialisation', 'pct_preventable_of_credited_lines': 'ACTUAL_Avg_Credit_Risk'})

# Create proposed rates per cluster + tier (using the same logic as apply_rate)
target_rates = df.groupby(['AI_Cluster', 'dominant_tier'])['AI_Target_Rate'].mean().unstack(fill_value=0)
target_rates.columns = [f'Proposed_Rate_{col}' for col in target_rates.columns]

summary = pd.concat([tier_stats, cluster_stats, target_rates], axis=1)
final_cols = ['supplier_id_Blue', 'supplier_id_Gold', 'INDEX_Scale', 'INDEX_Efficiency', 'INDEX_Loyalty', 'INDEX_Specialization', 'INDEX_Credit_Health', 'ACTUAL_Avg_Fill_Rate', 'ACTUAL_Avg_Specialization', 'ACTUAL_Avg_Credit_Risk', 'Current_Clip_Rate_Blue', 'Proposed_Rate_Blue', 'Current_Clip_Rate_Gold', 'Proposed_Rate_Gold', 'total_gmv_gross', 'total_fees_billed', 'AI_Target_Revenue_ExGST', 'AI_Net_Uplift_ExGST']

summary[final_cols].round(4).to_csv(summary_output)
df.round(4).to_csv(master_output, index=False)

print(f"\n MASTER CLEANSED: All indices are now relative to the active population.")
