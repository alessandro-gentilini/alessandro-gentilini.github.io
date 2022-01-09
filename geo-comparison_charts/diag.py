import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('err.txt')

fig, ax = plt.subplots(1,1)
ax.plot(df.idx,df.freq)

ax.figure.savefig('diagnose.png',bbox_inches='tight')

