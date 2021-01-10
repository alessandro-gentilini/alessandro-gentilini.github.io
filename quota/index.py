import geopandas as gpd
import unicodedata
com = gpd.read_file('/home/ag/Downloads/Limiti01012020/Limiti01012020/Com01012020/',encoding='utf-8')

cnt = 0
for c in com.COMUNE:
    print(str(cnt)+' '+unicodedata.normalize('NFKD', c).encode('ASCII', 'ignore'))
    cnt = cnt+1