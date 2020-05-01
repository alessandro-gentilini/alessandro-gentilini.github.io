import zipfile
import glob
import os

zips = glob.glob("./flussi_MTS/*.zip")
for z in zips:
    bn = os.path.basename(z)
    n = os.path.splitext(bn)[0]
    print(z,n)
    with zipfile.ZipFile(z, 'r') as zip_ref:
        zip_ref.extractall('.')
        os.rename('RilevazioniPerCorsia.csv','RilevazioniPerCorsia-'+n+'.csv')
        os.rename('RilevazioniPerPostazione.csv','RilevazioniPerPostazione-'+n+'.csv')