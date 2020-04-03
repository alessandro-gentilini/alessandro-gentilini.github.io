import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.txt", index_col=0, parse_dates=True,skiprows=1)
df.sort_values(by=['timestamp'],inplace=True,ascending=True)

df.plot()

df['positive'] = df['delta_positive_from_yesterday'].cumsum()
df['dead'] = df['delta_death_from_yesterday'].cumsum()


df2 = df[['positive','dead','total_recovered']]
df2.index = df.index
ax2 = df2.plot()
ax2.set_xlabel('data')
ax2.legend(['totale positivi','totale deceduti','totale guariti'])
ax2.figure.savefig('COVID-19.png',bbox_inches='tight')

plt.show()
