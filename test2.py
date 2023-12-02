import geopandas as gpd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import math
from shapely.ops import unary_union

def is_valid_district(subgraph, G):
    if not nx.is_connected(subgraph):
        return False
    population = 0
    for node in G.nodes():
        population += G.nodes[node]['pop']
    
    pop_balance = 0
    for node in subgraph.nodes:
        pop_balance += subgraph.nodes[node]['pop']
    pop_balance = pop_balance / (population/14)
    if pop_balance > 1.005 or pop_balance < .995:
        return False

    return True
    

def recombination_proposal(G, subgraphs, j=2):
    try:
        attempts = 0
        
        district1 = random.randint(1,14)
        R = list(subgraphs[district1].nodes)
        random.shuffle(R)
        for node in R:
            for neighbor in G.neighbors(node):
                if G.nodes[neighbor]['district'] != G.nodes[node]['district']:
                    
                    district2 = int(G.nodes[neighbor]['district'])
                    R.append(subgraphs[district2].nodes)
                    break
            else:
                continue
            break
        R_graph = nx.compose(subgraphs[district1], subgraphs[district2])
        while attempts < 10:    
            # Create a spanning tree from R
            T = nx.minimum_spanning_tree(R_graph)
            edges = list(T.edges)
            random.shuffle(edges)

            # Iterate over edges
            for e in edges:
                T.remove_edge(*e)
                components = list(nx.connected_components(T))
                for i in range(len(components)):
                    subgraph = G.subgraph(components[i])
                    if is_valid_district(subgraph, G):
                        # Make it a new district, remove these nodes from R
                        try:
                            subgraphs[district1] = subgraph
                            subgraphs[district2] = G.subgraph(components[i+1])
                            for i in range(len(G.nodes())):
                                if G.nodes[i] in subgraph:
                                    G.nodes[i]['district'] = district1
                                if G.nodes[i] in G.subgraph(components[i+1]):
                                    G.nodes[i]['district'] = district2
                        except:
                            pass
                        return subgraphs
                else:
                        # No valid district, add edge back and try next edge
                    T.add_edge(*e)
                    continue


            attempts += 1
        

        return subgraphs
    except:
        return subgraphs
    
def polsby_popper(area, perimeter):
    return 4 * math.pi * area / perimeter**2

def energy(subgraphs, G, gdf):
    energy = 0
    for subgraph in subgraphs:
        nodes = []
        for node in G.nodes():
            if int(G.nodes[node]['district']) == int(subgraph):
                nodes.append(node)
        precincts = gdf[gdf['ID'].isin(nodes)]
        district_whole = unary_union(precincts.geometry)
        area = district_whole.area
        perimeter = district_whole.length
        if perimeter != 0:
            energy += polsby_popper(area, perimeter)
    
    return energy

def temp(s):
    return 1000 * 0.99^s

def sim_anneal(G, subgraphs):
    for i in range(10):
        sol_proposed = recombination_proposal(G, subgraphs)
        if energy(sol_proposed, G, gdf) >= energy(subgraphs, G, gdf):
            subgraphs = sol_proposed
        else:
            energy_change = energy(subgraphs, G, gdf) - energy(sol_proposed, G, gdf)
            if (energy_change/temp(i)) >= random.random():
                subgraphs = sol_proposed
    return subgraphs, G
        


# Load the shapefile
gdf = gpd.read_file('/Users/franciswu/gerrymandering/GA_precincts/GA_precincts16.shp')


# Create an empty graph
G = nx.Graph()

# Add nodes with district attribute
# Assuming 'ID' is a unique identifier for each precinct and 'District' is the congressional district
for index, row in gdf.iterrows():
    G.add_node(row['ID'], district = row['CD'], pop = row['TOTPOP'])



# Add edges based on adjacency
for index, precinct in gdf.iterrows():
    neighbors = list(gdf[gdf.geometry.touches(precinct.geometry)]['ID'])
    for neighbor_id in neighbors:
        if neighbor_id != precinct['ID']:
            G.add_edge(precinct['ID'], neighbor_id)


# Create subgraphs for each congressional district
districts = gdf['CD'].unique()
subgraphs = {int(district): G.subgraph([n for n, attr in G.nodes(data=True) if attr['district'] == district]) for district in districts}

# Example usage of subgraphs
#for district, subgraph in subgraphs.items():
    #print(f"District {district} has {subgraph.number_of_nodes()} precincts")

#plt.figure(figsize=(12, 8))
#pos = nx.spring_layout(G)  # Layout for the nodes

#for district, subgraph in subgraphs.items():
    #nx.draw(subgraph, pos, with_labels=False, node_size=30, node_color=np.random.rand(3,))

#plt.title("Congressional Districts")
#plt.show()



subgraphs, G = sim_anneal(G, subgraphs)

compactness = energy(subgraphs, G, gdf)

plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G)  # Layout for the nodes
for district, subgraph in subgraphs.items():
    nx.draw(subgraph, pos, with_labels=False, node_size=30, node_color=np.random.rand(3,))

plt.title("Congressional Districts")
plt.show()

print("Final compactness score:", compactness )


f = open('precincts.txt', 'a')
for node in G.nodes():
    f.write(G.nodes[node]['district'] + "\n")
f.close()




