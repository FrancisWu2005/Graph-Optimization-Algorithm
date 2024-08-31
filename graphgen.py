# pylint: disable=locally-disabled, bare-except, multiple-statements, bad-indentation, attribute-defined-outside-init, pointless-string-statement, broad-exception-caught, C  
import geopandas as gpd
import networkx as nx
from shapely.geometry import Polygon
import pandas as pd
import matplotlib.pyplot as plt


# # Read the shapefile
# gdf = gpd.read_file('C:\\Users\\MD_Admin\\Documents\\GA_precincts16.shp')

# # Create a graph from the shapefile
# graph = nx.Graph()

# # Add nodes and edges based on the shapefile's geometry
# for index, row in gdf.iterrows():
#     # Assuming 'geometry' is the column containing geometry information
#     geometry = row['ID']
    
#     # Use some logic to extract nodes and edges from the geometry
#     # For example, you might extract nodes from the coordinates of a LineString or Polygon
    
#     # gdf[gdf.geometry.touches(geom)]['ID'].tolist()

#     # # Add nodes to the graph
#     # graph.add_nodes_from(nodes)
    
#     # # Add edges to the graph
#     # graph.add_edges_from(edges)

# # Write the graph to a METIS graph file
# #nx.write_gpickle(graph, 'your_graph.gpickle')


def main():
    # Read the shapefile
    gdf = gpd.read_file('GA_precincts16.shp')

    # Custom Dictionary to map values to index
    tIndexer1 = 1
    dictTrueIndex = {}
    for row in gdf.iterrows():
        # Assuming 'geometry' is the column containing geometry information
        dictTrueIndex[row[1]['ID']] = tIndexer1
        tIndexer1 += 1

    # Create a GeoDataFrame for edges (this would be based on your adjacency logic)
    # For this example, we'll create an empty DataFrame
    edges = pd.DataFrame(columns=['node1', 'node2'])

    # Assume gdf has a column 'ID' which is a unique identifier for each precinct
    for index, geom in enumerate(gdf.geometry):
        # Find neighbors
        try:
            neighbors = gdf[gdf.geometry.touches(geom)]['ID'].tolist()
            for neighbor in neighbors:
                if dictTrueIndex.get(neighbor) != index + 1:
                    # Assuming 'index' is the ID for the precinct
                    edges = edges._append({'node1': index + 1, 'node2': dictTrueIndex.get(neighbor)}, ignore_index=True)
        except:
            print(f"Error with precinct {index}")

    # Create the graph
    G = nx.Graph()

    # Assuming 'CD' column contains district numbers starting from 1 and up to n
    districts = gdf['CD'].unique()
    n_districts = len(districts)
    colors = plt.cm.get_cmap('tab20', 14)  # Get a colormap that has enough unique colors

    # Modified by Moses
    color_map = []
    for ab in range (0, 14):
        color_map.append('gray') # Set default color to gray

    for idx, district in enumerate(districts):
        color_map[int(district) - 1] = colors(idx - 1)  # Map each district to a unique color

    node_colors = [color_map[int(row['CD'])-1] for index, row in gdf.iterrows()]

    color_map = []
    # Add nodes
    for index, row in gdf.iterrows():
        G.add_node(dictTrueIndex.get(row['ID']))
        color_map.append(node_colors[index-1])
        
    # Add edges
    #print(len(edges))
    for index, row in edges.iterrows():
        G.add_edge(row['node1'], row['node2'])

    # Now you can write the graph to a file in a format that gpmetis understands
    # METIS expects a simple format where the first line contains the number of nodes and edges
    # and each subsequent line contains the nodes that are adjacent to that node.

    num_nodes = G.number_of_nodes()
    num_edges = G.number_of_edges()

    # You need to prepare the METIS input file
    with open('graph_file.graph', 'w') as file:
        file.write(f"{num_nodes} {len(edges)}\n")
        index = 1

        # Dysfunctional seperate lines
        # for node in G.nodes():
        #     neighbors = G.neighbors(node)
        #     for neighbor in neighbors:
        #         if neighbor != node:
        #             # Write the line for this node
        #             file.write(str(index) + " " + str(neighbor+1) + " 1\n")
        #     index += 1
        
        # Functional single line
        for node in G.nodes():
            # Get all neighbors of the node as a list of strings
            neighbors = [str(neighbor) for neighbor in G.neighbors(node)]

            #Write the line for this node
            file.write(str(node) + " " + " ".join(neighbors) + "\n")

        # Functional seperate lines
        #for n2 in G.edges():
            #file.write(str(n2[0]) + " " + str(n2[1]) + "\n")
        
    nx.draw(G, node_size = 25, with_labels=False, node_color=color_map, edge_color='gray')
    plt.show()

if __name__ == "__main__":
    main()