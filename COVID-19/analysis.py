import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json

df = pd.read_csv("data.txt", parse_dates=['timestamp'],skiprows=1,na_values=999999999)
df.set_index('timestamp',inplace=True)

# Daily graph
fig, ax = plt.subplots(1)
df.plot(drawstyle='steps-mid',y='delta_positive_from_yesterday',ax=ax)
ax.set_xlabel('')
ax.set_ylabel('persone/giorno (person/day)')
ax.legend(['nuovi positivi ogni giorno (new positive every day)'])
ax.figure.savefig('COVID-19-daily_delta_positive.png',bbox_inches='tight')



# Cumulative graph
df['positive'] = df['delta_positive_from_yesterday'].cumsum()
df['dead'] = df['delta_death_from_yesterday'].cumsum()

# can be interesting https://stackoverflow.com/a/13674286
fig, ax2 = plt.subplots(1)
df2 = df[['positive','dead','total_recovered']]
df2.plot(drawstyle='steps-mid',ax=ax2)
ax2.set_xlabel('')
ax2.set_ylabel('persone (person)')
# translation according to https://github.com/pomber/covid19
ax2.legend(['totale positivi (confirmed)','totale deceduti (deaths)','totale guariti (recovered)'])
ax2.figure.savefig('COVID-19-cumulative.png',bbox_inches='tight')

fig, ax3 = plt.subplots(1)
df3 = df[['positive','dead','total_recovered']]
df3 = df3.assign(positive_minus_dead_minus_recovered=df['positive']-df['dead']-df['total_recovered'])
df3.plot(drawstyle='steps-mid',ax=ax3)
ax3.set_xlabel('')
ax3.set_ylabel('persone (person)')
# translation according to https://github.com/pomber/covid19
ax3.legend(['$c=$totale positivi (confirmed)','$d$=totale deceduti (deaths)','$r$=totale guariti (recovered)','$c-d-r$'])
ax3.figure.savefig('COVID-19-cumulative-formula.png',bbox_inches='tight')



# Daily boxplot graph
df4 = pd.read_csv("data.txt", parse_dates=['timestamp'],skiprows=1,na_values=999999999)
delta_positive_from_yesterday_idx = 1
sz = len(df4.index)
cumulative_data = np.empty((sz,sz))
cumulative_data.fill(np.nan)
for r in range(0,sz):
    col = r
    for j in range(0,r+1):
        cumulative_data[j,col]=df4.iloc[j,delta_positive_from_yesterday_idx]

df5=pd.DataFrame(cumulative_data,columns=df4.iloc[:,0])

fig, ax5 = plt.subplots(1)
df5.boxplot(ax=ax5,rot=90,grid=False)
ax5.set_ylabel('persone/giorno (person/day)')
ax5.set_title('Boxplot per i nuovi positivi ogni giorno\n(boxplots for new positive every day)')
ax5.figure.savefig('COVID-19-daily_positive_boxplot.png',bbox_inches='tight')



# Print report "bollettino"-like
print(df2)



# Generate JSON data according to https://github.com/pomber/covid19
df_for_json = df2.copy()
df_for_json.reset_index(drop=False, inplace=True)
df_for_json.rename(columns={"timestamp": "date", "positive": "confirmed", "dead": "deaths", "total_recovered": "recovered"}, inplace=True)
df_for_json.fillna(method='ffill',inplace=True)
df_for_json['confirmed'] = df_for_json['confirmed'].astype(int)
df_for_json['deaths'] = df_for_json['deaths'].astype(int)
df_for_json['recovered'] = df_for_json['recovered'].astype(int)
df_for_json['date'] = df_for_json['date'].dt.strftime("%Y-%m-%d")

json_str = json.dumps(json.loads('{"Circondario Imolese": '+df_for_json.to_json(orient='records')+"}"),indent=2)
with open("data.json", "w") as text_file:
    text_file.write(json_str)

def min_max_normalization(df):
    return (df-df.min())/(df.max()-df.min())

pc = pd.read_csv("dpc-covid19-ita-regioni.csv", parse_dates=['data'])
pc.rename(columns={"data": "timestamp"},inplace=True)
pc['timestamp'] = pc['timestamp'].dt.floor('D')
pc.set_index('timestamp',inplace=True)
swabs = pc.loc[pc['denominazione_regione']=='Emilia-Romagna']['tamponi']
normalized_swabs = min_max_normalization(swabs)
print(normalized_swabs)

confirmed = df3[['positive']]
normalized_confirmed = min_max_normalization(confirmed)
print(normalized_confirmed)

usca = pd.read_csv('data-USCA.txt',parse_dates=['timestamp'])
usca.set_index('timestamp',inplace=True)
usca_swab = usca['swab']
normalized_usca_swabs = min_max_normalization(usca_swab)


result = pd.concat([normalized_swabs, normalized_confirmed,normalized_usca_swabs], axis=1)
print(result)
fig, ax6 = plt.subplots(1)
result.plot(drawstyle='steps-mid',ax=ax6,colormap='Accent')
ax6.set_xlabel('')
ax6.set_ylabel('Conteggi normalizzati (normalized counts) $min\\rightarrow 0$, $max\\rightarrow 1$')
ax6.legend(['Tamponi in Emilia Romagna (swabs)','Totale positivi (confirmed)','Tamponi USCA Circ. Imolese'])
ax6.figure.savefig('COVID-19-swabs.png',bbox_inches='tight')