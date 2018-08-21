import requests
import pandas as pd
from pyproj import Proj, transform

# script for returning elevation from lat, long, based on open elevation data
# which in turn is based on SRTM
def get_elevation(lat, long):
    query = ('https://api.open-elevation.com/api/v1/lookup'
             f'?locations={lat},{long}')
    r = requests.get(query).json()  # json object, various ways you can extract value
    # one approach is to use pandas json functionality:
    elevation = pd.io.json.json_normalize(r, 'results')['elevation'].values[0]
    return elevation

x = 563407
y = 5023034

inProj = Proj('+init=EPSG:32632')
outProj = Proj('+init=EPSG:4326')#lat/long

x2,y2 = transform(inProj,outProj,x,y)

print(x2, y2)

print(get_elevation(y2,x2))