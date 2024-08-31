import geopandas as gpd
import matplotlib.pyplot as plt

# Load the shapefile
gdf = gpd.read_file('/Users/franciswu/gerrymandering/tl_2022_13_scsd/tl_2022_13_scsd.shp')

gdf['CD'] = gdf['CD'].astype('category')

# Plot the GeoDataFrame, coloring by the 'CD' column
gdf.plot(column='CD', legend=True)

# Add title and axis labels
plt.title('Precincts by CD')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Remove the axis for a cleaner look
plt.axis('off')


# Show the plot
plt.show()