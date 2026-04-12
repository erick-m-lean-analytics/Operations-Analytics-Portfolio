import pandas as pd
import networkx as nx
import numpy as np

# Load Data 
links_path = r"C:\Users\ericm\Documents\Digitising_JIT\From_To.csv"
coords_path = r"C:\Users\ericm\Documents\Digitising_JIT\Node_coordinates.csv"

df_links = pd.read_csv(links_path)
df_coords = pd.read_csv(coords_path)

# Clean headers
df_links.columns = df_links.columns.str.strip()
df_coords.columns = df_coords.columns.str.strip()

# Build Coordinate Map & Graph 
pos = {str(row['Node']).strip(): (row['X']/1000.0, row['Y']/1000.0) for _, row in df_coords.iterrows()}

G = nx.DiGraph()
for _, row in df_links.iterrows():
    u, v = str(row[df_links.columns[0]]).strip(), str(row[df_links.columns[1]]).strip()
    if u in pos and v in pos:
        dist = np.sqrt((pos[v][0]-pos[u][0])**2 + (pos[v][1]-pos[u][1])**2)
        G.add_edge(u, v, weight=round(dist, 2))

# Generate the All-Pairs Shortest Path Matrix
print("Calculating all-pairs shortest paths... (Dijkstra's Algorithm)")
# This returns a dictionary of dictionaries: {Source: {Target: Distance}}
all_dist_dict = dict(nx.all_pairs_dijkstra_path_length(G))

# Format into a Square Matrix
nodes = sorted(list(G.nodes()))
matrix_df = pd.DataFrame(index=nodes, columns=nodes)

# Fill the matrix
for start_node in nodes:
    for end_node in nodes:
        if start_node == end_node:
            matrix_df.at[start_node, end_node] = 0
        else:
            # Get distance from dictionary, default to 99999 if unreachable
            dist = all_dist_dict.get(start_node, {}).get(end_node, 99999)
            matrix_df.at[start_node, end_node] = round(dist, 2)

# Apply Toyota Standard speed (Optional but recommended)
# Create a second matrix for Travel Time (Seconds)
time_matrix_df = matrix_df.copy()
time_matrix_df = time_matrix_df.apply(lambda x: x * 1.6 if isinstance(x, (int, float)) else x)

# Export
matrix_df.to_csv('From_To_Distance_Matrix_Meters.csv')
time_matrix_df.to_csv('From_To_Time_Matrix_Seconds.csv')

print(f"Success! Generated a {len(nodes)}x{len(nodes)} matrix.")
print("Saved: 'From_To_Distance_Matrix_Meters.csv' and 'From_To_Time_Matrix_Seconds.csv'")
