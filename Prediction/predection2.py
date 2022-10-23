#%%
from dataclasses import replace
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf
import os 

#%%
os.getcwd()
data = pd.read_csv('/Users/mac/Desktop/M-SSD/Devlopement logicial /project/prediction/eco2mix-regional-cons-def.csv', sep = ";")
print(data.isna().sum()) # calcule data missing 


# %%
Consumtion = data.loc[:, "Date": "Consommation (MW)"].copy()  # get only the comumns from date to the consumtion
print(np.shape(Consumtion))   # desplay the shape of my data
Consumtion.drop(axis=1, columns=["Date - Heure"], inplace=True)
# %%
#Add the region columns to the Consumption data
Consumtion["Region"] = data["Région"]
Consumtion.columns
#splite data into groupes, On start by
Consumtion[['Region']].value_counts()   # the effectives
by_Region = Consumtion.groupby(by ="Region")   #A groupby operation involves some combination of splitting the object, applying a function, and combining the results. This can be used to group large amounts of data and compute operations on these groups.
print(by_Region.mean())   # calcul the barycentre of each region 
index = by_Region.groups.keys()  # get the groups name
modalite_1 = list(index)[3] 
by_Reg_Breta = by_Region.get_group(modalite_1)


# %%
by_Reg_Breta.isna().sum()   # check the missing values 
mean_Breta = by_Reg_Breta['Consommation (MW)'].mean()
by_Reg_Breta["Consommation (MW)"].fillna(mean_Breta, inplace = True)  # Replace all the misssing data by its mean 
# %%
## ADAPT OLD to create the by_Reg_Breta['Time']
time_improved = pd.to_datetime(by_Reg_Breta['Date'] +
                               ' ' + by_Reg_Breta['Heure'],
                               format='%Y-%m-%d %H:%M')

by_Reg_Breta['Time'] = time_improved  # add the Time to the data
by_Reg_Breta.set_index('Time', inplace=True) # set time as index
# remove useles columns
del by_Reg_Breta['Heure']
del by_Reg_Breta['Date']
del by_Reg_Breta["Region"]
# %%
by_Reg_Breta = by_Reg_Breta.sort_index(ascending=True)  # sort data with time
by_Reg_Breta.head(5)
by_Reg_Breta.tail(5)
#%%
#the same for Normandie
modalite_2 = list(index)[-6]     # Normandie
by_Reg_Norm = by_Region.get_group(modalite_2)

by_Reg_Norm.isna().sum()   # check the missing values 
mean_Norm= by_Reg_Breta['Consommation (MW)'].mean()
by_Reg_Breta["Consommation (MW)"].fillna(mean_Norm, inplace = True)  # Replace all the misssing data by its mean 
## ADAPT OLD to create the by_Reg_Breta['Time']
time_improved_N = pd.to_datetime(by_Reg_Norm['Date'] +
                               ' ' + by_Reg_Norm['Heure'],
                               format='%Y-%m-%d %H:%M')

by_Reg_Norm['Time'] = time_improved_N  # add the Time to the data
by_Reg_Norm.set_index('Time', inplace=True) # set time as index
# remove useles columns
del by_Reg_Norm['Heure']
del by_Reg_Norm['Date']
del by_Reg_Norm["Region"]



# %%

fig, axes = plt.subplots(2, 2, figsize=(12, 12), sharex=True)

axes[0,0].plot(by_Reg_Breta)
axes[0,0].set_title("consumation per 30 min Breta")
axes[0,0].set_ylabel("time")
axes[1,0].plot(by_Reg_Breta['2013':].resample('M').mean())  
axes[1,0].set_title("mean consumation per month Breta ")
axes[1,0].set_ylabel("time")

axes[0,1].plot(by_Reg_Norm)
axes[0,1].set_title("consumation per 30 min Norma")
axes[0,1].set_ylabel("time")
axes[1,1].plot(by_Reg_Norm['2013':].resample('M').mean())  
axes[1,1].set_title("mean consumation per month Norma ")
axes[1,1].set_ylabel("time")
plt.show()


# %%


fig, axes = plt.subplots(2, 1, figsize=(10, 5), sharex=True)

axes[0].plot(by_Reg_Breta['2013'].resample('d').max() )
axes[0].plot(by_Reg_Breta['2013'].resample('d').min())

axes[0].set_title("time")
axes[0].set_ylabel("Consum : daily average in Bretagne")

axes[1].plot(by_Reg_Norm['2013'].resample('d').max(),  '--')
axes[1].plot(by_Reg_Norm['2013'].resample('d').min(),  '-.')

axes[1].set_title("time")
axes[1].set_ylabel("Consum : daily average in Normandie")
# %%
