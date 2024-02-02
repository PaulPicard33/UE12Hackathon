import requests
import json

(lng_origine, lat_origine) = (2.36815, 48.74991)
(lng_destination, lat_destination) = (2.33650, 48.83730)
r=requests.get(f"https://wxs.ign.fr/essentiels/geoportail/itineraire/rest/1.0.0/route?resource=bdtopo-osrm&start={lng_origine},{lat_origine}&end={lng_destination},{lat_destination}").json()
print(f"Distance : {r['distance']} mètres, Durée :{r['duration']} minutes")
