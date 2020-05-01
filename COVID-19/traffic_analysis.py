import zipfile
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

lanes = []
stations = []

zips = glob.glob("./flussi_MTS/*.zip")
for z in zips:
    bn = os.path.basename(z)
    n = os.path.splitext(bn)[0]
    with zipfile.ZipFile(z, 'r') as zip_ref:
        zip_ref.extractall('.')
        new_name = 'RilevazioniPerCorsia-'+n+'.csv'
        os.rename('RilevazioniPerCorsia.csv',new_name)
        lanes.append(new_name)
        new_name = 'RilevazioniPerPostazione-'+n+'.csv'
        os.rename('RilevazioniPerPostazione.csv',new_name)
        stations.append(new_name)

tmp = []
for f in lanes:
    tmp.append(pd.read_csv(f,sep=';',thousands='.'))
    
df = pd.concat(tmp)
df['Giorno'] = pd.to_datetime(df['Giorno'],format="%d/%m/%Y")

df1 = df[df['Giorno']>='2020-02-01']
df1 = df1.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values=['Transiti - Totale'])
df1 = 100*df1/df1.max()
df1.plot(legend=False)

c1 = (df['Postazione']==251) | (df['Postazione']==255) | (df['Postazione']==505) | (df['Postazione']==651)
#c1 = (df['Postazione']==156) | (df['Postazione']==252) | (df['Postazione']==600) | (df['Postazione']==52)
#c1 = df['Postazione']==255
c2 = df['Giorno']>='2020-02-01'
df2 = df[c1&c2]

df3 = df2.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values=['Transiti - Totale'])
df3 = 100*df3/df3.max()
df3.plot(legend=True)

plt.show()


