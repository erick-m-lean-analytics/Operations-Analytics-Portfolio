import pandas as pd
import plotly.express as px
import os
from datetime import datetime, timedelta

# --- 1. Load the Grouped Trips ---
base_p = r"C:\Users\ericm\OneDrive\Documents\Portfolio\Digitising_JIT\Module_2_Capacity"
input_p = os.path.join(base_p, "Milk_Run_Delivery_Groups.csv")
df = pd.read_csv(input_p)

# --- 2. Sequence Logic: Staggering to Prevent Congestion ---
# We assume T0 is the start of the shift (0 mins)
# We process by Lineside_Group to ensure no overlap in the same aisle
scheduled_trips = []

for group_name, trips in df.groupby('Lineside_Group'):
    current_time_secs = 0  # Start of shift for this group
    
    for _, trip in trips.iterrows():
        start_time = current_time_secs
        duration = trip['Total_Cycle_Secs']
        end_time = start_time + duration
        
        # Convert seconds to "Minutes from Start" for the Gantt X-Axis
        scheduled_trips.append({
            'Trip_ID': trip['Trip_ID'],
            'Lineside_Group': group_name,
            'Parts': trip['Parts_Delivered'],
            'Start_Min': round(start_time / 60, 2),
            'End_Min': round(end_time / 60, 2),
            'Duration_Min': round(duration / 60, 2),
            # Formatting for Plotly (using a dummy date to create a time axis)
            'Start_Date': datetime(2026, 1, 1) + timedelta(seconds=start_time),
            'End_Date': datetime(2026, 1, 1) + timedelta(seconds=end_time)
        })
        
        # KEY LOGIC: The next trip in THIS group can only start after the previous one finishes
        # (Preventing two drivers in the same aisle/Lineside_Group at once)
        current_time_secs = end_time + 60  # Adding a 1-minute safety buffer

# --- 3. Create the Gantt Dataframe ---
gantt_df = pd.DataFrame(scheduled_trips)

# --- 4. Generate the Visualization ---
fig = px.timeline(
    gantt_df, 
    x_start="Start_Date", 
    x_end="End_Date", 
    y="Lineside_Group", 
    color="Lineside_Group",
    hover_data=["Trip_ID", "Parts", "Duration_Min"],
    title="JIT Milk Run Sequence: 450-Minute Shift Schedule"
)

# Format the X-Axis to show 0 to 450 minutes instead of clock time
fig.update_layout(
    xaxis=dict(
        title="Shift Time (Minutes)",
        tickformat="%H:%M", # This will show as relative time from 00:00
    ),
    yaxis_title="Production Zones (Lineside Groups)",
    showlegend=False
)

# --- 5. Export ---
gantt_df.to_csv(os.path.join(base_p, "Shift_Gantt_Schedule.csv"), index=False)
fig.write_html(os.path.join(base_p, "Milk_Run_Gantt_Chart.html"))

print("✅ Congestion Control Applied.")
print(f"Total Workload across 450 mins: {round(gantt_df['Duration_Min'].sum() / 450, 2)} Drivers.")
print("Saved: 'Shift_Gantt_Schedule.csv' and 'Milk_Run_Gantt_Chart.html'")