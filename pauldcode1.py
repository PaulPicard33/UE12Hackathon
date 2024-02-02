import requests
import json
import numpy as np 
Destinataires =  {'SOGARIS' : (2.36815, 48.74991),
                  'Mines Paris' : (2.33969, 48.84563),
'Observatoire de Paris' : (2.33650, 48.83730),
'Marie du 14e' : (2.32698, 48.83320),
'Gare Montparnasse TGV' : (2.32159, 48.84117),
'Mairie du 15e' : (2.29991, 48.84126)}
(lng_origine, lat_origine) = (2.34017, 48.84635)
(lng_destination, lat_destination) = (2.35036, 48.8413)
try:
    r =requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={lng_origine},{lat_origine}&end={lng_destination},{lat_destination}").json()  
    print(f"Distance : {r['distance']} mètres, Durée :{r['duration']} minutes")
    
except Exception:
    print(f'erreur requete !')
durée = 0
distance = 0

cles=[Destinataires.keys()]
M = np.shape(len(cles))
for i in range(len(cles)):
    for j in range(len(cles)):
        M[i][j]=requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={Destinataires[cles[i]][0]},{Destinataires[cles[i]][1]}&end={Destinataires[cles[j]][0]},{Destinataires[cles[j]][1]}").json()['distance']
print(M)


