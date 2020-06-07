import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from matplotlib.ticker import ScalarFormatter
from datetime import date

# Population size is from http://dati.istat.it/Index.aspx?QueryId=18964
emilia_romagna_end_november_2019 = 4469568
# According to http://www.nuovocircondarioimolese.it/
# these are the towns in the Circondario Imolese:
borgo_tossignano_end_november_2019 = 3264
casalfiumanese_end_november_2019 = 3460
castel_del_rio_end_november_2019 = 1213
castel_guelfo_end_november_2019 = 4563
cspt_end_november_2019 = 21026
dozza_end_november_2019 = 6582
fontanelice_end_november_2019 = 1960
imola_end_november_2019 = 69864
medicina_end_november_2019 = 16780
mordano_end_november_2019 = 4662

circondario = borgo_tossignano_end_november_2019+casalfiumanese_end_november_2019+castel_del_rio_end_november_2019+castel_guelfo_end_november_2019+cspt_end_november_2019+dozza_end_november_2019+fontanelice_end_november_2019+imola_end_november_2019+medicina_end_november_2019+mordano_end_november_2019


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

def compute_percentage(temp):
    return 100*temp/circondario

def circ_imolese_percentage(ax_f):
    """
    Update second axis according with first axis.
    """
    y1, y2 = ax_f.get_ylim()
    ax3_right.set_ylim(compute_percentage(y1), compute_percentage(y2))
    ax3_right.figure.canvas.draw()

fig, ax3 = plt.subplots(1)
ax3_right = ax3.twinx()
# https://matplotlib.org/3.1.1/gallery/subplots_axes_and_figures/fahrenheit_celsius_scales.html
ax3.callbacks.connect("ylim_changed", circ_imolese_percentage)
df3 = df[['positive','dead','total_recovered']]
df3 = df3.assign(positive_minus_dead_minus_recovered=df['positive']-df['dead']-df['total_recovered'])
df3.plot(drawstyle='steps-mid',ax=ax3)
#ax3.axhline(338)
ax3.set_xlabel('')
ax3.set_ylabel('persone (person)')
# translation according to https://github.com/pomber/covid19

def format_legend(s,v):
    if v!=0:
        return (s+' $\\Delta={:+.0f}$').format(v)
    return s+' $\\Delta=0$'

#ax3.legend(['$c=$totale positivi (confirmed){:+.0f}'.format(df3.diff().iloc[-1,0]),'$d$=totale deceduti (deaths){:+.0f}'.format(df3.diff().iloc[-1,1]),'$r$=totale guariti (recovered){:+.0f}'.format(df3.diff().iloc[-1,2]),'$c-d-r$'],loc='upper left')
L0 = format_legend('$c=$totale positivi (confirmed)',df3.diff().iloc[-1,0])
L1 = format_legend('$d$=totale deceduti (deaths)',df3.diff().iloc[-1,1])
L2 = format_legend('$r$=totale guariti (recovered)',df3.diff().iloc[-1,2])
ax3.legend([L0,L1,L2,'$c-d-r$'],loc='upper left')
ax3.set_title('COVID-19 Circondario Imolese, '+date.today().isoformat()+', $N={0}$'.format(circondario)+'\nfonte dati (data source): www.ausl.imola.bo.it')
ax3_right.set_ylabel('% pop. Circondario Imolese (% of Circondario Imolese population)')
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




pc = pd.read_csv("dpc-covid19-ita-regioni.csv", parse_dates=['data'])
pc.rename(columns={"data": "timestamp"},inplace=True)
pc['timestamp'] = pc['timestamp'].dt.floor('D')
pc.set_index('timestamp',inplace=True)
swabs = pc.loc[pc['denominazione_regione']=='Emilia-Romagna']['tamponi']
swabs = round(swabs*circondario/emilia_romagna_end_november_2019)
cumulative_swabs_inferredfrom_EmiRo_as_simple_proportion = swabs.copy()
swabs = swabs.diff()




confirmed = df[['delta_positive_from_yesterday']]

usca = pd.read_csv('data-USCA.txt',parse_dates=['timestamp'],na_values=999999999)
usca.set_index('timestamp',inplace=True)
usca_swab = usca['swab'].diff()

ausl = pd.read_csv('data-swabs_AUSL.txt',parse_dates=['timestamp'],na_values=999999999)
ausl.set_index('timestamp',inplace=True)
ausl_swab = ausl['cumulative_swabs_declared_by_AUSL'].diff()

result = pd.concat([swabs, confirmed, usca_swab, ausl_swab], axis=1)
print(result)

result2 = pd.DataFrame()
result2 = result2.assign(a=result['tamponi']-result['delta_positive_from_yesterday'],
b=result['swab']-result['delta_positive_from_yesterday'],
c=result['cumulative_swabs_declared_by_AUSL']-result['delta_positive_from_yesterday'],
)

fig, ax6 = plt.subplots(1)
result2.plot(ax=ax6,logy=True,colormap='Dark2_r',drawstyle='steps-mid')
ax6.set_xlabel('')
ax6.set_ylabel('')
ax6.yaxis.set_major_formatter(ScalarFormatter())
ax6.set_yticks([.5, 1, 2, 3, 10, 100])
ax6.axhline(1)
ax6.yaxis.grid()
ax6.set_title('Differenza tra tamponi e positivi giornalieri\n$a$=tamponi giornalieri in Emilia Romagna riscalati sulla popolazione del Circ. Imolese\n$b$=tamponi giornalieri USCA Circ. Imolese\n$c$=tamponi giornalieri AUSL\n$p$=positivi giornalieri Circ. Imolese')
ax6.legend(['$a-p$','$b-p$','$c-p$'])
ax6.figure.savefig('COVID-19-swabs.png',bbox_inches='tight')

swabs_declared_by_AUSL = pd.read_csv('data-swabs_AUSL.txt',parse_dates=['timestamp'],na_values=999999999)
swabs_declared_by_AUSL.set_index('timestamp',inplace=True)

cumulative_swabs = pd.concat([cumulative_swabs_inferredfrom_EmiRo_as_simple_proportion,swabs_declared_by_AUSL],axis=1)
fig, ax7 = plt.subplots(1)
cumulative_swabs.plot(ax=ax7,drawstyle='steps-mid')
ax7.figure.savefig('COVID-19-cumulative_swabs.png',bbox_inches='tight')

# vedi mail da INFN
# tentative_R = df[['positive','dead','total_recovered']]
# tentative_R = tentative_R.assign(R=df['positive']/(df['dead']+df['total_recovered']))
# del tentative_R['positive']
# del tentative_R['dead']
# del tentative_R['total_recovered']
# fig, ax8 = plt.subplots(1)
# tentative_R.plot(ax=ax8)
# ax8.figure.savefig('COVID-19-R.png',bbox_inches='tight')
