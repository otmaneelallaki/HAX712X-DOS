# %%
import pandas as pd
import numpy as np

# %% with just keep the city and his land
df = pd.read_csv('commune_2022.csv', sep=',')
commune = df[['COM', 'REG']]

# %% conso, rename and delete the duplicates
df2 = pd.read_csv('consommation-annuelle-residentielle-par-adresse.csv', sep=';')
df2.rename(columns = {'Code INSEE de la commune':'COM'}, inplace = True)
df2.rename(columns = {'Consommation annuelle moyenne de la commune (MWh)':'Conso'}, inplace = True)
conso = df2[['COM', 'Conso']]
conso = conso.drop_duplicates()

# %% compatibility between the two databases
conso[['COM']] = conso[['COM']].astype(str)

# %%
conso_reg = pd.merge(conso, commune, on='COM')

# %%
conso_reg = conso_reg[['Conso' , 'REG' ]]
conso_reg = conso_reg.dropna()
conso_reg.round({'Conso': 2})


# %%
for i in conso_reg['REG']:
    conso_reg.loc[conso_reg.REG==i,'Conso']=conso_reg[conso_reg['REG']==i]['Conso'].mean()

# %%
conso_reg = conso_reg.drop_duplicates()

# %%   the code for the french region (REG) must match with the usual JSON files
conso_reg['REG'] = conso_reg['REG'].astype(int)
conso_reg['REG'] = conso_reg['REG'].astype(str)


# %%
conso_reg.to_csv('conso_reg.csv', index=False)

