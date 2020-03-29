import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.txt", index_col=0, parse_dates=True,skiprows=1)
df.sort_values(by=['timestamp'],inplace=True,ascending=True)

df.plot()

df['positive'] = df['delta_positive_yesterday'].cumsum()
df['dead'] = df['delta_death_yesterday'].cumsum()
#print(df.index)
#print(df.info(verbose=True))

df2 = df[['positive','dead','recovered']]
df2.index = df.index


df2.plot()

plt.show()
