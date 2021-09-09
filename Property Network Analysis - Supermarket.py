
#===================================================================================
#=================================== Load Packages =================================
#===================================================================================

import pandas as pd  # provides interface for interacting with tabular data
from shapely.geometry import Point, Polygon, MultiPolygon, box, LineString  # for manipulating text data into geospatial shapes
from shapely import wkt  # stands for "well known text," allows for interchange across GIS programs
import rtree  # supports geospatial join
import osmnx as ox # retrieve OpenStreetMap (OSM) data 
import networkx as nx
import geopandas as gpd  # combines the capabilities of pandas and shapely for geospatial operations
import matplotlib.pyplot as plt


#===================================================================================
#=================================== Import Data ===================================
#===================================================================================

#import Hamilton Road network and Plot
place_name = "Hamilton, New Zealand"
graph = ox.graph_from_place(place_name, network_type='drive')
G_projected = ox.project_graph(graph)
ox.plot_graph(G_projected)
plt.show()

#import Hamilton Boundary
city = ox.geocode_to_gdf(place_name)
ax = ox.project_gdf(city).plot()
plt.show()


#Get supermarkets
query = {'shop':'supermarket'}
restaurants_gdf = ox.geometries_from_place(place_name, tags=query,which_result=1 )
restaurants_gdf.head(5)

#Get residential properties
query = {'building':True}
addr_gdf = ox.geometries_from_place(place_name, tags=query,which_result=1 )
addr_gdf.head(20)

# Set up a plot axis
fig, ax = plt.subplots(figsize = (15,10))


# Visualise both on the plot
city.plot(ax = ax, alpha = 0.5)
restaurants_gdf.plot(ax = ax, markersize = 1, color = 'red', alpha = 0.8, label = 'supermarket Locations')
addr_gdf.plot(ax = ax, markersize = 1, color = 'blue', alpha = 0.8, label = 'residential properties')
plt.legend()
plt.show()

#===================================================================================
#============================= Convert Polygons into Points =======================
#===================================================================================

restaurants_gdf['geometry'] = restaurants_gdf['geometry'].apply(
  lambda x: x.centroid if type(x) == Polygon else (
  x.centroid if type(x) == MultiPolygon else x)
)

addr_gdf['geometry'] = addr_gdf['geometry'].apply(
  lambda x: x.centroid if type(x) == Polygon else (
  x.centroid if type(x) == MultiPolygon else x)
)




addr_gdf['geometry'].to_file("scratch\\addr_gdf.geojson", driver='GeoJSON')