import pandas as pd  # provides interface for interacting with tabular data
from shapely.geometry import Point, Polygon, MultiPolygon, box, LineString  # for manipulating text data into geospatial shapes
from shapely import wkt  # stands for "well known text," allows for interchange across GIS programs
import rtree  # supports geospatial join

import osmnx as ox # retrieve OpenStreetMap (OSM) data 
import networkx as nx
import geopandas as gpd  # combines the capabilities of pandas and shapely for geospatial operations

import matplotlib.pyplot as plt

#import Hamilton Road network and Plot
place_name = "Hamilton, New Zealand"
graph = ox.graph_from_place(place_name, network_type='drive')
fig, ax = ox.plot_graph(graph)


#Extract Road edges to Geopandas df
nodes, edges = ox.graph_to_gdfs(graph, nodes=True, edges=True)

#create bounding box
bbox = box(*edges.unary_union.bounds)

#extract the centroid of our bounding box as the source location.
orig_point = bbox.centroid

#find the easternmost node in our street network. 
#We can do this by calculating the x coordinates and finding out which node has the largest x-coordinate value. Let’s ensure that the values are floats.
nodes['x'] = nodes.x.astype(float)
maxx = nodes['x'].max()

#retrieve the target Point having the largest x-coordinate.
target_loc = nodes.loc[nodes['x']==maxx, :]

#extract the Point geometry from the data.
target_point = target_loc.geometry.values[0]

#now find the nearest graph nodes (and their node-ids) to these points. 
#For osmnx we need to parse the coordinates of the Point as coordinate-tuple with Latitude, Longitude coordinates.
orig_xy = (orig_point.y, orig_point.x)
target_xy = (target_point.y, target_point.x)

orig_node = ox.get_nearest_node(graph, orig_xy)
target_node = ox.get_nearest_node(graph, target_xy)

o_closest = nodes.loc[orig_node]
t_closest = nodes.loc[target_node]

#make a GeoDataFrame out of these series
od_nodes = gpd.GeoDataFrame([o_closest, t_closest], geometry='geometry', crs=nodes.crs)

#we are ready to do the routing and find the shortest path between the origin and target locations
route = nx.shortest_path(G=graph, source=orig_node, target=target_node, weight='length')
print(route)

#plot route
fig, ax = ox.plot_graph_route(graph, route)

#get rout nodes
route_nodes = nodes.loc[route]

#create a LineString out of the Point geometries of the nodes
route_line = LineString(list(route_nodes.geometry.values))
print(route_line)

#turn into Geo df
route_geom = gpd.GeoDataFrame(crs=edges.crs)
route_geom['geometry'] = None
route_geom.loc[0, 'geometry'] = route_line

route_geom.to_timestamp()


route_geom.to_file("scratch\\route_geom.geojson", driver='GeoJSON')

