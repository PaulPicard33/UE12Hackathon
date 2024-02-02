import requests
import json
import numpy as np
import itertools
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

## Définition des constantes et des données

acceleration = 1.85 #m/s**2
vitesse = 40/3.6
Area=4.56
k1=2.15e-3
Cx=0.46e-3
rhoair = 1
M = 3.5e3
g=9.81
PW=vitesse*(0.5*rhoair*vitesse**2*Cx*Area)

Destinataires =  {'SOGARIS' : (2.36815, 48.74991),
                  'Mines Paris' : (2.33969, 48.84563),
'Observatoire de Paris' : (2.33650, 48.83730),
'Marie du 14e' : (2.32698, 48.83320),
'Gare Montparnasse TGV' : (2.32159, 48.84117),
'Mairie du 15e' : (2.29991, 48.84126)}

cles = list(Destinataires.keys())
num_destinataires = len(cles)
M = np.zeros((num_destinataires, num_destinataires))  # Créez une matrice remplie de zéros

for i in range(num_destinataires):
    for j in range(num_destinataires):
        if i != j:  # Évitez de calculer la distance entre un point et lui-même
            start_coords = Destinataires[cles[i]]
            end_coords = Destinataires[cles[j]]
            
            # Utilisez requests.get pour obtenir les informations de l'itinéraire et extrayez la distance
            distance = requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={start_coords[0]},{start_coords[1]}&end={end_coords[0]},{end_coords[1]}").json()['distance']
            duree = requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={start_coords[0]},{start_coords[1]}&end={end_coords[0]},{end_coords[1]}").json()['duration']
            M[i][j] = distance

## Calcul du plus court chemin

def plus_court_chemin_glouton(matrice_distance):
    nombre_points = len(matrice_distance)
    point_de_livraison = list(range(1, nombre_points))  # Commence à partir de 1 pour exclure le point de départ (0)
    meilleur_chemin = None
    meilleure_distance = float('inf')

    # Générer toutes les permutations possibles des points de livraison 
    permutations = itertools.permutations(point_de_livraison)

    for permutation in permutations:
        chemin_actuel = [0] + list(permutation) + [0]  # Ajoute le point de départ à la fin du chemin pour fermer la boucle
        distance_totale = calculer_distance_totale(chemin_actuel, matrice_distance)

        if distance_totale < meilleure_distance:
            meilleure_distance = distance_totale
            meilleur_chemin = chemin_actuel

    return meilleur_chemin, meilleure_distance

def calculer_distance_totale(chemin, matrice_distance):
    distance_totale = 0
    for i in range(len(chemin) - 1):
        distance_totale += matrice_distance[chemin[i]][chemin[i + 1]]
    return distance_totale


opti, opti2 = plus_court_chemin_glouton(M)
print("Le plus court chemin est ", opti," et sa distance totale est ", opti2,"mètres")

## Présentation graphique des résultats

def plot_graphe_chemin(matrice_distance, chemin):
    nombre_points = len(matrice_distance)
    G = nx.DiGraph()

    for i in range(nombre_points):
        G.add_node(i)

    for i in range(len(chemin) - 1):
        G.add_edge(chemin[i], chemin[i + 1], weight=matrice_distance[chemin[i]][chemin[i + 1]])

    pos = nx.circular_layout(G)
    edge_labels = nx.get_edge_attributes(G, 'weight')

    nx.draw(G, pos, with_labels=True, node_size=800, node_color="skyblue", font_size=8, font_color="black")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

    plt.title('Plus court chemin trouvé')
    plt.show()

plot_graphe_chemin(M, opti)