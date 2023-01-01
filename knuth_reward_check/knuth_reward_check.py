from names_dataset import NameDataset, NameWrapper
import pandas as pd
import requests


nd = NameDataset()
html = requests.get('https://www-cs-faculty.stanford.edu/~knuth/boss.html')
df = pd.read_html(html.text)[1]

name = []
country = []
gender = []

cnt = 0
total = 0
for n in df[0]:
    total = total+1
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