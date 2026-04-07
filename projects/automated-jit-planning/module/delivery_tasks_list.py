import pandas as pd
import math
import os

# --- 1. Load Data with Corrected Subfolder Paths ---
base_p = r"C:\Users\ericm\OneDrive\Documents\Portfolio\Digitising_JIT"

dist_matrix_p = os.path.join(base_p, "Module_1_Map", "From_To_Distance_Matrix_Meters.csv")
route_matrix_p = os.path.join(base_p, "Module_1_Map", "From_To_Routing_Matrix_Sequence.csv")

demand_p = os.path.join(base_p, "Module_2_Capacity", "Demand.csv")
output_p = os.path.join(base_p, "Module_2_Capacity", "Exploded_Tasks_Verification.csv")

demand_df = pd.read_csv(demand_p)
dist_matrix = pd.read_csv(dist_matrix_p, index_col=0)
route_matrix = pd.read_csv(route_matrix_p, index_col=0)

# --- 2. Lineside_Group Mapping Logic ---
def map_lineside_group(address):
    addr = str(address).strip().upper()
    if addr.startswith('TR'): return 'Trimline RH'
    if addr.startswith('TL'): return 'Trimline LH'
    if addr.startswith('CL'): return 'Chassis LH'
    if addr.startswith('CR'): return 'Chassis RH'
    if addr.startswith('FR'): return 'Final RH'
    if addr.startswith('FL'): return 'Final LH'
    if addr.startswith('EG_R'): return 'Engine RH'
    if addr.startswith('EG_L'): return 'Engine LH'
    if addr.startswith('T0'): return 'Trim Zero'
    if addr.startswith('AC_B'): return 'AC_Bldg'
    return 'Other'

# --- 3. Explode tasks ---
exploded_tasks = []

for index, row in demand_df.iterrows():
    num_deliveries = math.ceil(row['NO_OF_TRIP_REQD'])
    start_node = str(row['NODE_ID']).strip()
    end_node = str(row['LINESIDE_ADDRESS']).strip()
    p_name = str(row['Part_Name']).strip()
    
    # Verified lookups
    one_way_dist = dist_matrix.loc[start_node, end_node]
    node_chain = route_matrix.loc[start_node, end_node]
    
    # Distance and Travel Time Calculations
    round_trip_dist = one_way_dist * 2
    travel_time_secs = round_trip_dist * 1.6
    
    # Service Time Logic: CUS_DOLLEY = 24s, Others = 80s
    container = str(row['LEVEL3_CONTAINER_TYPE']).strip()
    service_time = 24 if container == 'CUS_DOLLEY' else 80

    for i in range(num_deliveries):
        exploded_tasks.append({
            'Task_ID': f"{p_name}_{i+1}",
            'Part_Name': p_name,
            'DEL_QTY': row['DEL_QTY'],
            'Node_ID Source': start_node,
            'Lineside_Address': end_node,
            'Lineside_Group': map_lineside_group(end_node),
            'Routing_Path': node_chain,
            'Round_Trip_Meters': round(round_trip_dist, 2),
            'Travel_Time_Secs': round(travel_time_secs, 2),
            'Service_Time_Secs': service_time,
            'Total_Cycle_Secs': round(travel_time_secs + service_time, 2)
        })

# --- 4. Create and Save ---
tasks_df = pd.DataFrame(exploded_tasks)
tasks_df.to_csv(output_p, index=False)

print(f"✅ Clean Manifest Created: {len(tasks_df)} rows.")
print(f"Removed redundant 'TOTAL_TIME' column.")
print(f"File saved: {output_p}")