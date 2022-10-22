#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
import os 
#%%

os.getcwd()
data = pd.read_csv('/Users/mac/Desktop/M-SSD/Devlopement logicial /project/prediction/eco2mix-regional-cons-def.csv', sep = ";")
print(data.isna().sum())


# %%
data2 = data.loc[:, "Code INSEE région": "Consommation (MW)"].copy()
print(np.shape(data2))
# %%
print(data2.columns)
data2.isna().sum()

# %%
data2.dropna()
# %%

plt.plot(data["Consommation (MW)"][1000:1200])
# %%
data[['Région']].value_counts()   # sort data sachant les modalités de la varibale Region

# %%
count = data2.groupby('Région')['Consommation (MW)'].count() 
# %%
by_Region = data2.groupby("Région")

# %%
data2['Région'].value_counts(normalize=True)  # calcule les poids 
nbr_moda = np.shape(data2['Région'].value_counts(normalize=True) )[0] 
Index = data2['Région'].value_counts(normalize=True).index # les Régions 

#%%
#dataEXtra = pd.DataFrame()
#for modal in range(nbr_moda):
   # dataEXtra[[Index[modal]]] = by_Region.get_group(Index[modal])
by_Reg_Breta = by_Region.get_group("Bretagne")
Breta = by_Reg_Breta[["Consommation (MW)"]]
plt.plot(Breta[1000: 1500])

# %%
diff_Breta = Breta.diff(1)
diff_Breta[1000: 1500].plot(figsize=(10, 6))
# %%
plot_acf(diff_Breta[1000: 1500], lags = 50)
#plot_pacf(diff_Breta[1000: 1500], lags = 50)



# %%
from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm
# %%
model = sm.tsa.arima.ARIMA(diff_Breta, order=(0,1,0))
result = model.fit()
print(result.summary())
# %%
