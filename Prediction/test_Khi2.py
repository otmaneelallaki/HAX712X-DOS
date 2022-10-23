
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 13:43:52 2022

@author: EL ALLAKI otmane
"""
#%%
from scipy.stats import chi2_contingency as chi2_contingency
import numpy as np
import pandas as pd

link = "https://odre.opendatasoft.com/explore/dataset/eco2mix-regional-cons-def/export/?disjunctive.libelle_region&disjunctive.nature&sort=-date_heure&q.from_date.date_heure=date_heure%3E%3D%222019-12-31T23:00:00Z%22"
data = pd.read_csv("/Users/mac/Desktop/eco2mix-regional-cons-def.csv", sep = ";") # data from 2020-01-01 to 2022-10-23
print(np.shape(data))
print(data.isna().sum()) # calcule data missing = 0
#%%
 
X = data["Consommation (MW)"].to_numpy()   # chnage the columns "Région" to array and pot it in X variable
bins = np.linspace(X.min(), X.max(), num = 50)
X_regroupe = pd.cut(X, bins=bins)   # classes regroupement  
effectifs_classes = pd.value_counts(X_regroupe)  # effectifs
cont_table = pd.crosstab(data["Région"], X_regroupe) # cross table  

khi2, pval , ddl , contingent_theorique = chi2_contingency(cont_table)
print(pval)    # P_value < 0.05, mrans there is à depnedance between variable "Région" and "Consommation" 
# %%
