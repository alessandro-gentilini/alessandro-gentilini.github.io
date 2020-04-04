import pandas as pd
import matplotlib.pyplot as plt
import json

df = pd.read_csv("data.txt", parse_dates=['timestamp'],skiprows=1,na_values=999999999)
df.set_index('timestamp',inplace=True)

# Daily graph
ax1 = df.plot.bar(y='delta_positive_from_yesterday')
ax1.set_xlabel('')
ax1.legend(['nuovi positivi ogni giorno (new positive every day)'])
ax1.figure.savefig('COVID-19-daily_delta_positive.png',bbox_inches='tight')

# Cumulative graph
df['positive'] = df['delta_positive_from_yesterday'].cumsum()
df['dead'] = df['delta_death_from_yesterday'].cumsum()

df2 = df[['positive','dead','total_recovered']]
ax2 = df2.plot()
ax2.set_xlabel('')
# translation according to https://github.com/pomber/covid19
ax2.legend(['totale positivi (confirmed)','totale deceduti (deaths)','totale guariti (recovered)'])
ax2.figure.savefig('COVID-19-cumulative.png',bbox_inches='tight')

# Print report "bollettino"-like
print(df2)

# Generate JSON data
df3 = df2.copy()
df3.reset_index(drop=False, inplace=True)
df3.rename(columns={"timestamp": "date", "positive": "confirmed", "dead": "deaths", "total_recovered": "recovered"}, inplace=True)
df3.fillna(method='ffill',inplace=True)
df3['confirmed'] = df3['confirmed'].astype(int)
df3['deaths'] = df3['deaths'].astype(int)
df3['recovered'] = df3['recovered'].astype(int)
df3['date'] = df3['date'].dt.strftime("%Y-%m-%d")

json_str = json.dumps(json.loads('{"Circondario Imolese": '+df3.to_json(orient='records')+"}"),indent=2)
with open("data.json", "w") as text_file:
    text_file.write(json_str)