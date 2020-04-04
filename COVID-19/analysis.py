import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.txt", parse_dates=['timestamp'],skiprows=1,na_values=999999999)
df.set_index('timestamp',inplace=True)

# daily
ax1 = df.plot.bar(y='delta_positive_from_yesterday')
ax1.set_xlabel('')
ax1.legend(['nuovi positivi ogni giorno (new positive every day)'])
ax1.figure.savefig('COVID-19-daily_delta_positive.png',bbox_inches='tight')

# cumulative
df['positive'] = df['delta_positive_from_yesterday'].cumsum()
df['dead'] = df['delta_death_from_yesterday'].cumsum()

df2 = df[['positive','dead','total_recovered']]
ax2 = df2.plot()
ax2.set_xlabel('')
# translation according to https://github.com/pomber/covid19
ax2.legend(['totale positivi (confirmed)','totale deceduti (deaths)','totale guariti (recovered)'])
ax2.figure.savefig('COVID-19-cumulative.png',bbox_inches='tight')

# report "bollettino"
print(df2)
