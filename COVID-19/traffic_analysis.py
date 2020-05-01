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

dtype={
"Transiti - Totale": 'Int64',
"Transiti - Non Classificato": 'Int64',
"Transiti - Leggeri": 'Int64',
"Transiti - Pesanti": 'Int64',
"Transiti - Diurno": 'Int64',
"Transiti - Notturno": 'Int64',
"Transiti - Feriali": 'Int64',
"Transiti - Festivi": 'Int64'}

dtype={
"Transiti - Festivi": 'Int64'}

tmp = []
for f in lanes:
    tmp.append(pd.read_csv(f,sep=';',thousands='.'))
    
df = pd.concat(tmp)

#df = pd.read_csv('RilevazioniPerPostazione-2020-02-29.csv',sep=';',thousands='.')

df['Giorno'] = pd.to_datetime(df['Giorno'],format="%d/%m/%Y")
df1 = df[df['Giorno']>='2020-02-01']

df1 = df1.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values=['Transiti - Totale'])
df1 = 100*df1/df1.max()
df1.plot(legend=False)

#c1 = (df['Postazione']==251) | (df['Postazione']==255) | (df['Postazione']==505) | (df['Postazione']==651)
c1 = (df['Postazione']==156) | (df['Postazione']==252) | (df['Postazione']==600) | (df['Postazione']==52)
#c1 = df['Postazione']==255
c2 = df['Giorno']>='2020-02-01'
df2 = df[c1&c2]

#df.set_index(['Giorno','Postazione','Corsia'],inplace=True)

df3 = df2.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values=['Transiti - Totale'])
df3 = 100*df3/df3.max()
df3.plot(legend=True)




#c2 = df['Corsia']=='0 - DA INNESTO SS16 (SAN BIAGIO - ARGENTA) A CONFINE REGIONALE TOSCANA'

#df = df[c2]

# c3 = c1 & c2

#df = df[df['Giorno']>='2020-02-01']
#print(df['Giorno'].describe())
# Miseria.set_index('Giorno',inplace=True)
# print(Miseria)
# Miseria.plot()
plt.show()


