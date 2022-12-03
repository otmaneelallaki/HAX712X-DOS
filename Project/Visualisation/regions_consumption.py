import pandas as pd
import numpy as np
import os
import pooch


url_cons = 'https://data.enedis.fr/explore/dataset/consommation-annuelle-residentielle-par-adresse/download/?format=csv&timezone=Europe/Berlin&lang=fr&use_labels_for_header=true&csv_separator=%3B'
path_target = './consommation-annuelle-residentielle-par-adresse.csv'
path, fname = os.path.split(path_target)
pooch.retrieve(url_cons, path = path, fname = fname, known_hash = None)
selected = ['Code INSEE de la commune', 'Consommation annuelle moyenne de la commune (MWh)']
df_cons = pd.read_csv('consommation-annuelle-residentielle-par-adresse.csv', usecols = selected, sep = ";", float_precision = 'legacy')
df_cons = df_cons.drop_duplicates().reset_index(drop = True)
df_cons.rename(columns = {'Code INSEE de la commune':'COM', 'Consommation annuelle moyenne de la commune (MWh)':'Conso'}, inplace = True)


url_com = 'https://www.insee.fr/fr/statistiques/fichier/5057840/commune2021-csv.zip'
path_target2 = './commune2021-csv.zip'
path2, fname2 = os.path.split(path_target2)
pooch.retrieve(url_com, path = path2, fname = fname2, known_hash = None)
COL = 'DEP'
selected2 = ['COM', COL]
df_2 = pd.read_csv('./commune2021-csv.zip', compression='zip', usecols = selected2, sep = ",")


df_cons[['COM']] = df_cons[['COM']].astype(str)

conso_col = pd.merge(df_cons, df_2, on='COM')
conso_col = conso_col[['Conso', COL]]
conso_col = conso_col.dropna()
conso_col.round({'Conso': 2})

for i in conso_reg[COL]:
    conso_col.loc[conso_col[COL] == i,'Conso'] = conso_col[ conso_col[COL] == i]['Conso'].mean()
    conso_col = conso_col.drop_duplicates()

conso_col[COL] = conso_col[COL].astype(int)
conso_col[COL] = conso_col[COL].astype(str)



conso_col.to_csv('conso_dep.csv', index=False)

