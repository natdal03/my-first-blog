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

place_name = "Kamppi, Helsinki, Finland"
graph = ox.graph_from_place(place_name)