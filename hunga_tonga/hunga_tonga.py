import pandas as pd
import matplotlib.pyplot as plt
from cycler import cycler

import seaborn as sns

lista=[]
s=[]
with open('dexter-d60a39d1-1b6d-4930-8f3d-9573724f1656.csv') as f:
    for line in f:
        if line in ['\n','\r\n']:
            lista.append(s)
            s = []
        else:
            s.append(line)


for i,c in enumerate(lista):
    f = open(str(i)+'.txt','w')
    if len(c)>2:
        f.write(c[1].strip()+',Stazione\n')
        for r in c[2:]:
            f.write(r.strip()+','+c[0])
        f.close()

dfs = []
cnt = 0
for i in range(1,27):
    try:
        df = pd.read_csv(str(i)+'.txt')
        df['p'] = df['Pressione atmosferica istantanea al livello della stazione a 2 m dal suolo (PA)']-df['Pressione atmosferica istantanea al livello della stazione a 2 m dal suolo (PA)'].mean()
        dfs.append(df)
        cnt=cnt+1
    except:
        pass

df=pd.concat(dfs)


colors = sns.color_palette('husl',n_colors=6)
plt.rc('axes', prop_cycle=(cycler('color', colors)*cycler('linestyle', ['solid', 'dashed', 'dashdot', 'dotted'])))

df['timestamp'] = pd.to_datetime(df['Inizio validità (UTC)'])
df.set_index('timestamp', inplace=True)
ax = df.groupby('Stazione')['p'].plot(legend=True,title='Fluctuations of atmospheric pressure around its local daily average at '+str(cnt)+' stations in Emilia Romagna, Italy\nData source: DEXT3R https://simc.arpae.it/dext3r/',xlabel='15th Jan 2022, UTC times',ylabel='Pascal',grid=True)
ax[0].xaxis.grid(True, which='both')
ax[0].annotate("Hunga Tonga-Hunga Ha'apai eruption?", xy=(pd.to_datetime('2022-01-15 20:00:00+00:00'), 175),  xycoords='data',
            xytext=(0.8, 0.95), textcoords='axes fraction',
            arrowprops=dict(facecolor='black', shrink=0.05),
            horizontalalignment='right', verticalalignment='top',
            )

plt.show()