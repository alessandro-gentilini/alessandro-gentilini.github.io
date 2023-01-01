from names_dataset import NameDataset, NameWrapper
import pandas as pd
import requests

nd = NameDataset()
html = requests.get('https://www-cs-faculty.stanford.edu/~knuth/boss.html')
df = pd.read_html(html.text)[1]

name = []
country = []
gender = []
amount = []
decimal_cents = []

cnt = 0
total = 0
for index, row in df.iterrows():
    total = total+1
    n = row[0]
    tokens = n.split()
    info = []
    t_countries = []
    t_genders = []
    cnt_surname = 0
    for t in tokens:
        nw = NameWrapper(nd.search(t))
        info.append([nw.country,nw.gender])
        t_countries.append(nw.country)        
        if nw.gender=='':
            cnt_surname = cnt_surname+1
        else:
            t_genders.append(nw.gender)

    if cnt_surname==1 and len(set(t_countries))==1 and len(set(t_genders))==1:
        cnt = cnt+1
        name.append(n)
        country.append(t_countries[0])
        gender.append(t_genders[0])
        amount.append(row[1])
        decimal_cents.append(int(row[1].replace('0x$','').replace('.',''),16))

result = pd.DataFrame({'name':name,'amount':amount,'country':country,'gender':gender, 'decimal_cents':decimal_cents})        

print(result['country'].value_counts().to_markdown())




def to_hexdollar(n):
    s = str(hex(n)).replace('0x','0x$')
    p = len(s)-2
    return s[:p]+'.'+s[p:]

result2 = result.groupby('country').sum().sort_values(by=['decimal_cents'],ascending=False)
result2['0x$'] = result2.apply(lambda row: to_hexdollar(row.decimal_cents),axis=1)
result2 = result2.drop(columns=['decimal_cents'])
print(result2.to_markdown())