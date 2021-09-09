import pandas as pd  # provides interface for interacting with tabular data
import geopandas as gpd  # combines the capabilities of pandas and shapely for geospatial operations
from shapely.geometry import Point, Polygon, MultiPolygon  # for manipulating text data into geospatial shapes
from shapely import wkt  # stands for "well known text," allows for interchange across GIS programs
import rtree  # supports geospatial join
import osmnx as ox # retrieve OpenStreetMap (OSM) data 
import matplotlib.pyplot as plt


df = gpd.read_file("C:\\Users\\natda\\Source\\Repos\\GIS Work\\scratch\\Shortest Path.geojson")
network = gpd.read_file("C:\\Users\\natda\\Source\\Repos\\GIS Work\\scratch\\Hamilton Roads.geojson")

network.plot()
plt.show()

place_name = "Hamilton, New Zealand"
graph = ox.graph_from_place(place_name)
area = ox.geometries_from_place(place_name, tags = {'gdf': True})
buildings = ox.geometries_from_place(place_name, tags = {'building': True})

fig, ax = ox.plot_graph(graph)

nodes, edges = ox.graph_to_gdfs(graph)
nodes.head()
edges.head()

fig, ax = plt.subplots()

edges.plot(ax=ax, linewidth=1, edgecolor='#BC8F8F')
buildings.plot(ax=ax, facecolor='khaki', alpha=0.7)
plt.tight_layout()
plt.show()