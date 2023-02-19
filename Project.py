from platform import java_ver
from urllib import response
from urllib.request import urlopen
import osmnx as ox
import networkx as nx
import math
import csv
from urllib.request import urlopen
import json
#Helper functions
def addnodes(G, nodes):
    for i in nodes:
        G[i] = []
    return G

def addedges(G, edges, directed=False):
    for i in edges:
        G[i[0]].append(tuple((i[1], i[2])))
        if directed == False:
            G[i[1]].append(tuple((i[0], i[2])))
    return G

def getOutNeighboursweighted(G,node):
    lst = G[node]
    lst1 = []
    for i in lst:
        lst1.append(i)
    return lst1
def getshortestpath(G,a):
    dist={}
    dic={}
    for i in G.keys():
        if i==a:
            dist[a] = [0,'']
            dic[a] = 0
        else:
            dist[i] = [math.inf,'']
            dic[i] = math.inf

    while dic:
        x=min(dic,key=dic.get)

        y=getOutNeighboursweighted(G,x)
        for i in y:
            if dist[x][0] + i[1] < dist[i[0]][0]:
                dist[i[0]][0] = dist[x][0] + i[1]
                dic[i[0]] = dist[x][0] + i[1]
                dist[i[0]][1] = x
        del dic[x]
    return dist

def finduserlocation():
    url = 'https://ipinfo.io/'
    response = urlopen(url)
    data = json.load(response)
    loc = data['loc'].split(',')
    loc[0] = float(loc[0])
    loc[1] = float(loc[1])
    return tuple(loc)

def convertedges(graph):
    edges = []
    for i in graph.edges():
        x=i[0]
        y=i[1]
        z=graph.get_edge_data(x, y)
        j=z[0]
        dist=j['length']
        tup=(x,y,dist)
        edges.append(tup)
    return edges

def locateamenities(graph, point, amenity):
    amenities = ox.geometries_from_point(point, tags = {'amenity': amenity}) #Data for hospitals, similar to a csv file. returns stuff like name and osm_id

    centroids = amenities.centroid  #returns center of hospital
    X = centroids.x
    Y = centroids.y

    nn = ox.get_nearest_nodes(graph, X, Y, method='balltree')
    return nn, amenities

def mergeSortDistances(data):
  if len(data) > 1:
    mid = len(data)//2
    l1 = data[:mid]
    l2 = data[mid:]

    mergeSortDistances(l1)
    mergeSortDistances(l2)

    i = 0   #merging begins here
    j = 0
    k = 0
    while i < len(l1) and j < len(l2):
      if l1[i][1][0] < l2[j][1][0]:
        data[k] = l1[i]
        i = i+1
      else:
        data[k] = l2[j]
        j = j+1
      k = k+1

    while i < len(l1):
      data[k] = l1[i]
      i = i+1
      k = k+1

    while j < len(l2):
      data[k] = l2[j]
      j = j+1
      k = k+1

    return data

def main(amenity='hospital',radius=2000):
    point = finduserlocation()
    graph = ox.graph_from_point(point, network_type="drive",dist=radius, simplify=True)
    userlocation = ox.get_nearest_node(graph,point)
    ####preparing the street level graph
    G={}
    nodes=graph.nodes
    edges = convertedges(graph)
    addnodes(G,nodes)
    addedges(G,edges,True)
    ##Street level done
    u = []
    v = []
    key = []
    data = []
    for uu, vv, kkey, ddata in graph.edges(keys=True, data=True):
        u.append(uu)
        v.append(vv)
        key.append(kkey)
        data.append(ddata)    

    roadColors = []
    roadWidths = []

    for item in data:   #for appearance of the map, the streets and so on
        if "length" in item.keys():
            if item["length"] <= 100:
                linewidth = 0.2
                color = "#a6a6a6" 
                
            elif item["length"] > 100 and item["length"] <= 200:
                linewidth = 0.3
                color = "#676767"
                
            elif item["length"] > 200 and item["length"] <= 400:
                linewidth = 0.5
                color = "#454545"
                
            elif item["length"] > 400 and item["length"] <= 800:
                color = "#bdbdbd"
                linewidth = 0.6
            else:
                color = "#d5d5d5"
                linewidth = 0.9

            if "primary" in item["highway"]:
                linewidth = 1.2
                color = "#ffff"
        else:
            color = "#a6a6a6"
            linewidth = 0.10
                
        roadColors.append(color)
        roadWidths.append(linewidth)


    #Nearest Node to the Hospitals. returns nearest street
    nn, amenities = locateamenities(graph, point, amenity)

    nearest_hospital=[]

    for i in range(0, len(nn)):
        #print(hospitals['name'][i], nn[i])
        nearest_hospital.append((amenities['name'][i], nn[i])) #creating tuples of hospital names and their corresponding nodes

    j=getshortestpath(G,userlocation) #shortest distances of all nodes from user location

    j=mergeSortDistances(list(j.items())) #sorting via merge sort the distances of all nodes from user location
    final=dict(j)

    for i in final.keys():
        if i in nn:
            save=i  #saving first amenity found as that has the shortest distance
            break

    for j in nearest_hospital:
        if save == j[1]:
            amenityname=j[0] #saving name of amenity
            break


    route = ox.shortest_path(graph, userlocation, save, weight="length")

    bgcolor = "#061529"
    fig, ax = ox.plot_graph_route(graph, route,dpi = 300,node_size=0,bgcolor = bgcolor,
    save = False, edge_color=roadColors,edge_linewidth=roadWidths, edge_alpha=1)  

    fig.tight_layout(pad=0)
    fig.savefig("Hospital Route.png", dpi=300, bbox_inches='tight', format="png", 
                facecolor=fig.get_facecolor(), transparent=False)

    print("Nearest", amenity, "is:",amenityname)
    return ("Nearest", amenity, "is:",amenityname)


