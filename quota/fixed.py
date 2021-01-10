
import json

with open('italy_geo.json') as f:
   data = json.load(f)

for x in data:
    if x[u'comune'] == u'Imola':
        lat = float(x[u'lat'])
        lon = float(x[u'lng'])
        print(lat,lon)
        break
else:
    x = None