# %%
import pandas as pd

# %% on garde seulement la commune et sa région
df = pd.read_csv('commune_2022.csv', sep=',')
commune = df[['COM', 'REG']]

# %% conso, renommage et suppression des doublons
df2 = pd.read_csv('consommation-annuelle-residentielle-par-adresse.csv', sep=';')
df2.rename(columns = {'Code INSEE de la commune':'COM'}, inplace = True)
df2.rename(columns = {'Consommation annuelle moyenne de la commune (MWh)':'Conso'}, inplace = True)
conso = df2[['COM', 'Conso']]
conso = conso.drop_duplicates()

# %% compatibilité entre les deux bases de données
commune.dtypes
conso['COM'] = conso['COM'].astype(object)
conso.dtypes
# %%
conso.head(9)

# %%
commune.head(9)

# %%
commune[ commune['COM'] == '76157' ]

# %%
conso['COM'] == 76157

# %%
conso_reg = pd.merge(conso_com2, commune2, on='COM')


# %%
conso_reg
# %%
