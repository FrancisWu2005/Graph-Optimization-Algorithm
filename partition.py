import geopandas as gpd
import networkx as nx
from shapely.geometry import Polygon
import pandas as pd
import matplotlib.pyplot as plt

# Read the shapefile
gdf = gpd.read_file('/Users/franciswu/gerrymandering/GA_precincts/GA_precincts16.shp')

# Create a GeoDataFrame for edges (this would be based on your adjacency logic)
# For this example, we'll create an empty DataFrame
edges = pd.DataFrame(columns=['node1', 'node2'])

# Assume gdf has a column 'ID' which is a unique identifier for each precinct
for index, geom in enumerate(gdf.geometry):
    # Find neighbors
    neighbors = gdf[gdf.geometry.touches(geom)]['ID'].tolist()
    for neighbor in neighbors:
        if neighbor['CD'] == index['CD']:
            if neighbor != index:
                # Assuming 'index' is the ID for the precinct
                edges = edges._append({'node1': index, 'node2': neighbor}, ignore_index=True)

# Create the graph
G = nx.Graph()

node_sizes = []

# Add nodes
for index, row in gdf.iterrows():
    G.add_node(row['ID'])

# Add edges
for index, row in edges.iterrows():
    G.add_edge(row['node1'], row['node2'])

# Now you can write the graph to a file in a format that gpmetis understands
# METIS expects a simple format where the first line contains the number of nodes and edges
# and each subsequent line contains the nodes that are adjacent to that node.

num_nodes = G.number_of_nodes()
num_edges = G.number_of_edges()

# You need to prepare the METIS input file
with open('graph_file.graph', 'w') as file:
    file.write(f"{num_nodes} {num_edges}\n")
    for node in G.nodes():
        # Get all neighbors of the node as a list of strings
        neighbors = [str(neighbor) for neighbor in G.neighbors(node)]
        # Write the line for this node
        file.write(" ".join(neighbors) + "\n")

(edgecuts, parts) = metis.part_graph(G, 3)
colors = ['red','blue','green']
for i, p in enumerate(parts):
    G.node[i]['color'] = colors[p]
nx.write_dot(G, 'example.dot')

plt.show()
