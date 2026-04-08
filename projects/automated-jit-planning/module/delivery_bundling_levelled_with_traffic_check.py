import pandas as pd
import math
import os

# --- 0. DYNAMIC SENSITIVITY & CONGESTION INPUTS ---
TOTAL_SHIFT_MIN = 450 
CAPACITY_LIMIT = 0.95 
MAX_WORK_MIN = TOTAL_SHIFT_MIN * CAPACITY_LIMIT # 427.5 mins

# Hardcoded Aisle Sharing Logic
aisle_conflict_map = {
    'Final RH': 'AISLE_A', 'Trimline LH': 'AISLE_A',
    'Trimline RH': 'AISLE_B', 'Engine RH': 'AISLE_B', 'Chassis RH': 'AISLE_B',
    'Engine LH': 'INDEPENDENT', 'Chassis LH': 'INDEPENDENT',
    'Final LH': 'INDEPENDENT',
    'AC_Bldg': 'INDEPENDENT',
    'Trim Zero': 'INDEPENDENT'
}

# --- 1. Load Data ---
base_p = r"C:\Users\ErickMortera\OneDrive - PartsCheck Pty Ltd\Documents\Portfolio\Digitising_JIT\Module_2_Capacity"
input_p = os.path.join(base_p, "Exploded_Tasks_Verification.csv")
output_p = os.path.join(base_p, "Milk_Run_Delivery_Groups_levelled.csv")

df = pd.read_csv(input_p)

# --- 2. Step: Bundle & Level ---
all_trips = []
trip_counter = 1

for group_name, group_data in df.groupby('Lineside_Group', observed=False):
    pending = group_data.sort_values('Task_ID').to_dict('records')
    part_counts = group_data['Part_Name'].value_counts()
    
    # Calculate intervals per SKU (Consumption Heartbeat)
    part_intervals = {part: (TOTAL_SHIFT_MIN / count) for part, count in part_counts.items()}

    while pending:
        bundle, parts, to_remove, qty = [], set(), [], 0
        for i, task in enumerate(pending):
            if task['Part_Name'] not in parts:
                bundle.append(task)
                parts.add(task['Part_Name'])
                qty += task['DEL_QTY']
                to_remove.append(i)
            if len(bundle) == 3: break
        for index in sorted(to_remove, reverse=True): pending.pop(index)
            
        furthest = max(bundle, key=lambda x: x['Travel_Time_Secs'])
        
        # IE Logic: Sum individual service times (Decant vs Swap) + Travel
        total_service_secs = sum(t['Service_Time_Secs'] for t in bundle)
        trip_duration_min = (furthest['Travel_Time_Secs'] + total_service_secs) / 60
        
        p_part = list(parts)[0]
        
        all_trips.append({
            'Trip_ID': f"TRIP_{trip_counter:03d}",
            'Lineside_Group': group_name,
            'Primary_Part': p_part,
            'Part_Interval_Min': part_intervals[p_part],
            'DEL_QTY': qty,
            'Duration_Min': round(trip_duration_min, 2),
            'Parts_Delivered': ", ".join(parts),
            'Outbound_Path': furthest['Outbound_Path'],
            'Return_Path': furthest['Return_Path']
        })
        trip_counter += 1

temp_df = pd.DataFrame(all_trips)

# --- 3. Step: DYNAMIC TAKT CALCULATION ---
# Total Warehouse Heartbeat = Available Time / Total Trips Needed
total_trips_needed = len(temp_df)
# We floor the takt to ensure we are always ahead of the line consumption
calc_takt = math.floor(TOTAL_SHIFT_MIN / total_trips_needed) if total_trips_needed > 0 else 10
TAKT_MIN = max(2, min(15, calc_takt)) # Safety buffer: No faster than 2m, no slower than 15m

# --- 4. Step: DETERMINISTIC TRIP-LEVEL BALANCING ---
zone_order = temp_df.groupby('Lineside_Group', observed=False)['Duration_Min'].sum().sort_values(ascending=False).index
temp_df['Lineside_Group'] = pd.Categorical(temp_df['Lineside_Group'], categories=zone_order, ordered=True)
temp_df = temp_df.sort_values(['Lineside_Group', 'Trip_ID'])

assigned_drivers = []
current_driver = 1
current_driver_load = 0

for mins in temp_df['Duration_Min']:
    if (current_driver_load + mins) > MAX_WORK_MIN:
        current_driver += 1
        current_driver_load = 0
    assigned_drivers.append(current_driver)
    current_driver_load += mins

temp_df['Assigned_Driver'] = assigned_drivers

# --- 5. Step: CONGESTION-AWARE DE-CONFLICTION ---
temp_df['Aisle_ID'] = temp_df['Lineside_Group'].map(aisle_conflict_map).fillna('INDEPENDENT')
temp_df['Raw_Offset'] = temp_df.groupby(['Lineside_Group', 'Primary_Part'], observed=False).cumcount() * temp_df['Part_Interval_Min']
# Snap delivery to the nearest calculated Takt Pulse
temp_df['Start_Offset_Min'] = temp_df['Raw_Offset'].apply(lambda x: math.ceil(x / TAKT_MIN) * TAKT_MIN)

temp_df = temp_df.sort_values('Start_Offset_Min').reset_index(drop=True)

def resolve_all_conflicts(df, takt):
    for i in range(len(df)):
        conflict = True
        while conflict:
            conflict = False
            cur_start = df.at[i, 'Start_Offset_Min']
            cur_driver = df.at[i, 'Assigned_Driver']
            cur_aisle = df.at[i, 'Aisle_ID']
            
            for j in range(i):
                if df.at[j, 'Start_Offset_Min'] == cur_start:
                    # Logic: Cannot have same driver busy OR two drivers in shared aisle
                    if cur_driver == df.at[j, 'Assigned_Driver']:
                        conflict = True
                    elif cur_aisle != 'INDEPENDENT' and cur_aisle == df.at[j, 'Aisle_ID']:
                        conflict = True
                
                if conflict:
                    df.at[i, 'Start_Offset_Min'] += takt
                    break
    return df

temp_df = resolve_all_conflicts(temp_df, TAKT_MIN)

# --- 6. Export & Summary ---
cols = ['Trip_ID', 'Assigned_Driver', 'Lineside_Group', 'Aisle_ID', 'Primary_Part', 'DEL_QTY', 
        'Start_Offset_Min', 'Duration_Min', 'Parts_Delivered', 'Outbound_Path', 'Return_Path']

temp_df = temp_df.sort_values(['Assigned_Driver', 'Start_Offset_Min'])
temp_df[cols].to_csv(output_p, index=False)

print(f"✅ Dynamic Leveling Complete (Takt: {TAKT_MIN}m based on {total_trips_needed} trips).")
print("-" * 50)
for d in sorted(temp_df['Assigned_Driver'].unique()):
    workload = temp_df[temp_df['Assigned_Driver']==d]['Duration_Min'].sum()
    print(f"🚛 Driver {int(d)}: {workload:.1f} mins work ({ (workload/TOTAL_SHIFT_MIN)*100 :.1f}% Utilized)")