import pandas as pd
import math 
from sklearn.neighbors import NearestNeighbors

nga = pd.read_csv('it.txt',sep='\t',encoding='utf-8',dtype={'ADM1':str,'TRANSL_CD':str,'F_TERM_DT':str})
X = math.pi*nga[['LAT','LONG']]/180

nbrs = NearestNeighbors(n_neighbors=1, metric='haversine').fit(X)

def query_nn(lat,lon):
    distance,index = nbrs.kneighbors([[math.pi*lat/180,math.pi*lon/180]])
    # print(distance[0][0],nga.iloc[index[0][0]].FULL_NAME_RO,nga.iloc[index[0][0]].LAT,nga.iloc[index[0][0]].LONG)
    return nga.iloc[index[0][0]].FULL_NAME_RO

print(query_nn(45.874722,13.514444))
print(query_nn(45.915556,13.499722))

print(query_nn(44.313611,11.583889))
print(query_nn(44.329444,11.587778))

