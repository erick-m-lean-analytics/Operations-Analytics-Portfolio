import pandas as pd
import os

# --- 1. Load the Manifest ---
base_p = r"C:\Users\ericm\OneDrive\Documents\Portfolio\Digitising_JIT\Module_2_Capacity"
input_p = os.path.join(base_p, "Exploded_Tasks_Verification.csv")
output_p = os.path.join(base_p, "Milk_Run_Delivery_Groups.csv")

df = pd.read_csv(input_p)

# --- 2. Process Groupings by Lineside_Group ---
final_trips = []
trip_counter = 1

# Group by the production zone (e.g., Trimline RH)
for group_name, tasks in df.groupby('Lineside_Group'):
    # Sort tasks by Task_ID (which includes the sequence number) to maintain order
    pending_tasks = tasks.sort_values('Task_ID').to_dict('records')
    
    while pending_tasks:
        current_trip_bundle = []
        parts_in_trip = set()
        
        # --- RULE: Bundle up to 3 dollies, NO DUPLICATE PARTS ---
        indices_to_remove = []
        for i, task in enumerate(pending_tasks):
            if task['Part_Name'] not in parts_in_trip:
                current_trip_bundle.append(task)
                parts_in_trip.add(task['Part_Name'])
                indices_to_remove.append(i)
            
            # Stop if we hit 3 dollies (Full Tugger)
            if len(current_trip_bundle) == 3:
                break
        
        # Remove selected tasks from the pending list
        for index in sorted(indices_to_remove, reverse=True):
            pending_tasks.pop(index)
            
        # --- 3. Travel Time Logic (Furthest Path Only) ---
        # Get the task in this bundle with the maximum travel time
        furthest_task = max(current_trip_bundle, key=lambda x: x['Travel_Time_Secs'])
        
        # Sum the service times of all dollies in the trip
        total_service_time = sum(t['Service_Time_Secs'] for t in current_trip_bundle)
        
        # --- 4. Build the Trip Row ---
        final_trips.append({
            'Trip_ID': f"TRIP_{trip_counter:03d}",
            'Lineside_Group': group_name,
            'Dolly_Count': len(current_trip_bundle),
            'Parts_Delivered': ", ".join(parts_in_trip),
            'Task_IDs': ", ".join([t['Task_ID'] for t in current_trip_bundle]),
            'Furthest_Address': furthest_task['Lineside_Address'],
            'Routing_Path': furthest_task['Routing_Path'],
            'Unified_Travel_Secs': furthest_task['Travel_Time_Secs'], # Max of the 3
            'Total_Service_Secs': total_service_time,
            'Total_Cycle_Secs': round(furthest_task['Travel_Time_Secs'] + total_service_time, 2)
        })
        trip_counter += 1

# --- 5. Export & Analysis ---
final_df = pd.DataFrame(final_trips)
final_df.to_csv(output_p, index=False)

# --- Resource Calculation ---
SHIFT_SECONDS = 450 * 60  # 27,000 seconds
total_workload_secs = final_df['Total_Cycle_Secs'].sum()
resource_requirement = total_workload_secs / SHIFT_SECONDS

print(f"✅ Milk Run Grouping Complete: {len(final_df)} Trips created.")
print(f"Constraint: Same parts are never in the same trip.")
print(f"Logic: Travel time based on furthest node in each bundle.")
print("-" * 30)
print(f"📊 TOTAL WORKLOAD: {total_workload_secs:,.2f} seconds")
print(f"🚛 RESOURCE REQUIREMENT: {resource_requirement:.2f} Tuggers/Drivers")
print("-" * 30)