import zipfile
import glob
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
from matplotlib.lines import Line2D

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
df1 = df1.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values='Transiti - Totale')
df1 = 100*df1/df1.max()
fig, ax = plt.subplots(1)
df1.plot(legend=False,ax=ax,color='#084286', alpha=.1)
ax.set_title('Flussi di traffico Emilia Romagna\n(Traffic in Emilia Romagna)\nData source: https://servizissiir.regione.emilia-romagna.it/FlussiMTS/')
ax.set_ylabel('Numero transiti giornalieri normalizzato\n(Normalized number of daily transits)\n100=max')
ax.set_xlabel('Data (date)')
ax.figure.savefig('Emilia_Romagna_all_stations.png',bbox_inches='tight')

#c1 = (df['Postazione']==251) | (df['Postazione']==255) | (df['Postazione']==505) | (df['Postazione']==651)
#c1 = (df['Postazione']==156) | (df['Postazione']==252) | (df['Postazione']==600) | (df['Postazione']==52)
c1 = df['Postazione']==255
c2 = df['Giorno']>='2020-02-01'
df2 = df[c1&c2]

df3 = df2.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values='Transiti - Totale')
fig, ax = plt.subplots(1)
df3.plot(legend=True,ax=ax)
ax.set_title('Strada: SS 9 tra Castel San Pietro e Imola\n(Traffic along road Via Emilia)\nData source: https://servizissiir.regione.emilia-romagna.it/FlussiMTS/')
ax.set_ylabel('Numero transiti giornalieri (number of daily transits)')
ax.set_xlabel('Data (date)')
ax.figure.savefig('station_255_Via_Emilia.png',bbox_inches='tight')

df3 = 100*df3/df3.max()
fig, ax = plt.subplots(1)
df3.plot(legend=True,ax=ax)
ax.set_title('Strada: SS 9 tra Castel San Pietro e Imola\n(Traffic along road Via Emilia)\nData source: https://servizissiir.regione.emilia-romagna.it/FlussiMTS/')
ax.set_ylabel('Numero transiti giornalieri normalizzato\n(Normalized number of daily transits)\n100=max')
ax.set_xlabel('Data (date)')
ax.figure.savefig('station_255_Via_Emilia_normalized.png',bbox_inches='tight')


df4 = df[df['Giorno']>='2020-02-01']
df4 = df4.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values=['Transiti - Leggeri','Transiti - Pesanti'])
df4 = 100*df4/df4.max()
fig, ax = plt.subplots(1)
colors={'Transiti - Leggeri':'blue','Transiti - Pesanti':'red'}
for i in df4:
    df4[i].plot(ax=ax,color=colors[i[0]], alpha=.1,lw=.2)

lines = [Line2D([0], [0], color=c) for c in ('blue','red')]
labels = ['Leggeri (light)', 'Pesanti (heavy)']
ax.legend(lines, labels)    

ax.set_title('Flussi di traffico Emilia Romagna\n(Traffic in Emilia Romagna)\nData source: https://servizissiir.regione.emilia-romagna.it/FlussiMTS/')
ax.set_ylabel('Numero transiti giornalieri normalizzato\n(Normalized number of daily transits)\n100=max')
ax.set_xlabel('Data (date)')
ax.figure.savefig('Emilia_Romagna_all_stations_light_vs_heavy.png',bbox_inches='tight')



df5 = df[df['Giorno']>='2020-02-01']
df5 = df5.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values=['Transiti - Diurno','Transiti - Notturno'])
df5 = 100*df5/df5.max()
fig, ax = plt.subplots(1)
colors={'Transiti - Diurno':'yellow','Transiti - Notturno':'black'}
for i in df5:
    df5[i].plot(ax=ax,color=colors[i[0]], alpha=.1,lw=.2)

lines = [Line2D([0], [0], color=c) for c in ('yellow','black')]
labels = ['Diurno (Daytime)', 'Notturno (Night-time)']
ax.legend(lines, labels)    

ax.set_title('Flussi di traffico Emilia Romagna\n(Traffic in Emilia Romagna)\nData source: https://servizissiir.regione.emilia-romagna.it/FlussiMTS/')
ax.set_ylabel('Numero transiti giornalieri normalizzato\n(Normalized number of daily transits)\n100=max')
ax.set_xlabel('Data (date)')
ax.figure.savefig('Emilia_Romagna_all_stations_daytime_vs_night.png',bbox_inches='tight')



df6 = df[df['Giorno']>='2020-02-01']
df6 = df6.pivot_table(index='Giorno', columns=['Postazione','Corsia'],values=['Transiti - Feriali','Transiti - Festivi'])
df6 = 100*df6/df6.max()
fig, ax = plt.subplots(1)
colors={'Transiti - Feriali':'red','Transiti - Festivi':'green'}
for i in df6:
    df6[i].plot(ax=ax,color=colors[i[0]], alpha=.1,lw=.2)

lines = [Line2D([0], [0], color=c) for c in ('red','green')]
labels = ['Feriali (mon-fri)', 'Festivi (sat-sun)']
ax.legend(lines, labels)    

ax.set_title('Flussi di traffico Emilia Romagna\n(Traffic in Emilia Romagna)\nData source: https://servizissiir.regione.emilia-romagna.it/FlussiMTS/')
ax.set_ylabel('Numero transiti giornalieri normalizzato\n(Normalized number of daily transits)\n100=max')
ax.set_xlabel('Data (date)')
ax.figure.savefig('Emilia_Romagna_all_stations_workday_vs_holiday.png',bbox_inches='tight')

