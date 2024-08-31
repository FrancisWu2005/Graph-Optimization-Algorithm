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
    # Read the shapefile  GA_precincts16   New
    gdf = gpd.read_file('GA_precincts16   New.dbf')
    test = gdf.plot(column='CD', cmap='tab20', figsize=(10, 10))
    
    #districts = gdf['CD'].unique()
    #n_districts = len(districts)
    #colors = plt.cm.get_cmap('tab20', 14)  # Get a colormap that has enough unique colors

    plt.show()


if __name__ == "__main__":
    main()