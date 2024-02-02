import networkx as nx

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
            elif j in route and i not in route and route[-1] == 0:
                idx_j = route.index(j)
                route.insert(idx_j, i)
                break

    return routes

# Exemple d'utilisation
distance_matrix = [[0, 10, 15, 20],
                   [10, 0, 35, 25],
                   [15, 35, 0, 30],
                   [20, 25, 30, 0]]

capacity = float('inf')  # Capacité infinie pour cet exemple

result = clarke_and_wright(distance_matrix, capacity)
print(result)

