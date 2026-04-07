import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

# Load Data 
links_path = r"C:\Users\ericm\OneDrive\Documents\Digitising_JIT\From_To.csv"
coords_path = r"C:\Users\ericm\OneDrive\Documents\Digitising_JIT\Node_coordinates.csv"

df_links = pd.read_csv(links_path)
df_coords = pd.read_csv(coords_path)

df_links.columns = df_links.columns.str.strip()
df_coords.columns = df_coords.columns.str.strip()

# Coordinate Map (millimetres to meters) 
pos = {
    str(row['Node']).strip(): (row['X'] / 1000.0, row['Y'] / 1000.0) 
    for _, row in df_coords.iterrows()
}

# Create Graph & Weights
G = nx.DiGraph()
for _, row in df_links.iterrows():
    u = str(row[df_links.columns[0]]).strip()
    v = str(row[df_links.columns[1]]).strip()
    
    if u in pos and v in pos:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        distance = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        G.add_edge(u, v, weight=round(distance, 2))

# Optimisation for Single Screen Display
# Use a standard wide-screen ratio
fig, ax = plt.subplots(figsize=(16, 9)) 

# Draw Nodes - Smaller size to prevent overlapping on one screen
nx.draw_networkx_nodes(G, pos, node_size=400, node_color='#E0E0E0', edgecolors='black', ax=ax)

# Draw Labels - Smaller font for screen fitting
nx.draw_networkx_labels(G, pos, font_size=6, font_weight='bold', ax=ax)

# Draw Edges - Thinner lines for a cleaner look
nx.draw_networkx_edges(G, pos, arrowstyle='-|>', arrowsize=10, 
                       edge_color='darkred', connectionstyle='arc3,rad=0.15', 
                       alpha=0.5, width=1, ax=ax)

# Draw Edge Labels (Distances)
# 'label_pos=0.4' moves the label slightly away from the centre to avoid overlap
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                             font_size=5, font_color='blue', 
                             label_pos=0.4, rotate=True, ax=ax)

plt.title("Digitized JIT Factory Floor Layout (Meters)", fontsize=16)
plt.xlabel("X (Meters)")
plt.ylabel("Y (Meters)")

# Fit to one screen
plt.tight_layout()
ax.set_aspect('equal') # Keeps the 5.7m horizontal looking like 5.7m vertical
plt.grid(True, linestyle=':', alpha=0.3)


plt.savefig('factory_floor_layout_cartesian.png', dpi=200, bbox_inches='tight')
print("Graph optimized for screen view. Saved as 'factory_floor_layout_cartesian.png'")
plt.show()
