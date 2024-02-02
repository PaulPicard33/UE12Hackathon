import requests
import json
import numpy as np 
import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd

Destinataires =  {'SOGARIS' : (2.36815, 48.74991),
                  'Mines Paris' : (2.33969, 48.84563),
'Observatoire de Paris' : (2.33650, 48.83730),
'Marie du 14e' : (2.32698, 48.83320),
'Gare Montparnasse TGV' : (2.32159, 48.84117),
'Mairie du 15e' : (2.29991, 48.84126)}


def clarke_and_wright(distance_matrix, capacity):
    num_customers = len(distance_matrix) - 1  # Nombre de clients
    G = nx.complete_graph(num_customers + 1)  # Graphe complet avec le dépôt et les clients

    # Attribution des distances aux arêtes du graphe
    for i in range(num_customers + 1):
        for j in range(i + 1, num_customers + 1):
            G[i][j]['distance'] = distance_matrix[i][j]

    # Tri des arêtes par distance décroissante
    edges_sorted = sorted(G.edges(data=True), key=lambda x: x[2]['distance'], reverse=True)

    # Initialisation des itinéraires
    routes = [[0, i, 0] for i in range(1, num_customers + 1)]
    # Construction des itinéraires
    for edge in edges_sorted:
        i, j, distance = edge
        for route in routes:
            if i in route and j not in route and route[-1] == 0:
                idx_i = route.index(i)
                route.insert(idx_i + 1, j)
                break
            elif j in route and i not in route and route[1] == 0:
                idx_j = route.index(j)
                route.insert(idx_j, i)
                break

    return routes


cles = list(Destinataires.keys())
num_destinataires = len(cles)
DISTANCE = np.zeros((num_destinataires, num_destinataires))  # Créez une matrice remplie de zéros
DUREE= np.zeros((num_destinataires, num_destinataires)) 
Energy = 0
for i in range(num_destinataires):
    for j in range(num_destinataires):
        if i != j:  # Évitez de calculer la distance entre un point et lui-même
            start_coords = Destinataires[cles[i]]
            end_coords = Destinataires[cles[j]]
            
            # Utilisez requests.get pour obtenir les informations de l'itinéraire et extrayez la distance
            distance = requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={start_coords[0]},{start_coords[1]}&end={end_coords[0]},{end_coords[1]}").json()['distance']
            duree = requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={start_coords[0]},{start_coords[1]}&end={end_coords[0]},{end_coords[1]}").json()['duration']
            DISTANCE[i][j] = distance
            DUREE[i][j] = duree



capacity=float(8)

acceleration = 1.85 #m/s**2
vitesse = 40/3.6 #m/s
Area=4.56
k1=2.15e-3
Cx=0.46e-3
rhoair = 1
M = 3.5e3
g=9.81
PW=vitesse*(0.5*rhoair*vitesse**2*Cx*Area+M*g*(k1+k1*vitesse**2))*(1/0.3)
PWa=(vitesse/2)*(0.5*rhoair*(vitesse/2)**2*Cx*Area+M*g*(k1+k1*(vitesse/2)**2)+M*acceleration)*(1/0.3)
result = clarke_and_wright(DISTANCE,capacity)
print(result)
dureetot = 0
for i in range(len(result[0])-1):
    dureetot+=requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={Destinataires[cles[result[0][i]]][0]},{Destinataires[cles[result[0][i]]][1]}&end={Destinataires[cles[result[0][i+1]]][0]},{Destinataires[cles[result[0][i+1]]][1]}").json()['duration']

Energyconsumed = 0.3*dureetot*PWa + 0.7*dureetot*PW
print(Energyconsumed)

plt.figure()
G=nx.DiGraph(DISTANCE)

nx.draw(G)

plt.show()
