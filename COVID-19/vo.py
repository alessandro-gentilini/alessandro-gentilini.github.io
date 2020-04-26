# https://www.medrxiv.org/highwire/filestream/77015/field_highwire_adjunct_files/1/2020.04.17.20053157-2.xlsx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from graphviz import Digraph

df = pd.read_excel('2020.04.17.20053157-2.xlsx',sheet_name='anonymised_dataset')

# df = pd.read_csv("2020.04.17.20053157-2.csv")
#print(df)

# Each column represents a positive subjetc. Numbers in cells identify the type of contact occurred with the corresponding subjects in rows: 1=direct contact, as reported by the subject, 2=indirect contact (i.e. contact with a subject who had direct contact), 3=inferred contact (i.e. inferred from household)

# for i in range(0,len(df.columns)):
#     print(i,df.columns[i])

first_positive_column_id = 13
last_positive_column_id = 103
selector = df.iloc[:,first_positive_column_id:last_positive_column_id+1].notna()
valids = df[selector.any(axis='columns')]


#print(df['0db03881'].value_counts())

#print(df.iloc[:,first_positive_column_id].value_counts())
#print(df.iloc[300,:].value_counts())

nodes = []
for c in range(first_positive_column_id,last_positive_column_id+1):
    nodes.append({'id':str(df.columns[c]),'group':'positive'})


links=[]
dot = Digraph(comment='Vo Euganeo')
for r in range(0,len(valids)):    
    for c in range(first_positive_column_id,last_positive_column_id+1):
        #if df.columns[c] != '0db03881' and df.columns[c] != '297bbbdc':
            if valids.iloc[r,c] == 1:
                dot.edge(str(df.columns[c]),str(df.iloc[r,0]))
                links.append({'source':str(df.columns[c]),'target':str(df.iloc[r,0])})
                if not {'id':str(df.iloc[r,0])} in nodes:
                    nodes.append({'id':str(df.iloc[r,0])})
dot.render('./gv/vo.gv')

data = {"nodes":nodes,"links":links}

import json
with open('vo_graph.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)


for c in range(first_positive_column_id,last_positive_column_id+1):
    dot = Digraph(comment=df.columns[c])
    save_it = False
    contacts = 0
    for r in range(0,len(valids)):
        if valids.iloc[r,c] == 1:
            save_it = True
            dot.edge(str(df.columns[c]),str(df.iloc[r,0]))
            contacts = contacts+1
    if save_it:
        print(df.columns[c],contacts)
        dot.render('./gv/'+df.columns[c]+'.gv')

#print(valids)


# df = pd.DataFrame({"nomi": ['alessandro', 'bruno', 'carlo'], "alessandro": [np.nan,np.nan,1], "bruno": [np.nan,2,np.nan], "carlo":[np.nan,np.nan,np.nan]})
# print(df)
# first_positive_column_id = 1
# last_positive_column_id = 3
# selector = df.iloc[:,first_positive_column_id:last_positive_column_id+1].notna()
# print(selector)
# print(df[selector.any(axis='columns')])