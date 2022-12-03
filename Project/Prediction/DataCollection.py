#%%
import pandas as pd
import datetime
import numpy as np
import pooch  # download data / avoid re-downloading
import os

class Data():
    def __init__(self, data = pd.DataFrame()) -> None:
        self.data = data

    def impo(self):
        self.data = pd.read_csv("./DataSet.csv")
        return

    def importData(self):
        #loading raw data 2019
        url2019 = "https://bit.ly/3hVlwrl"
        path_target = "./eco2mix-national-cons-def2019.csv"
        path, fname = os.path.split(path_target)
        pooch.retrieve(url2019, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`
        usecols2019=['Date', 'Heure', "Consommation (MW)","Nucléaire (MW)", "Gaz (MW)"] # variables we needs
        data2019 = pd.read_csv("./eco2mix-national-cons-def2019.csv",usecols=usecols2019, sep = ";") # importin g our data

        #loading raw data 2020
        url2020 = "https://bit.ly/3tLbMCE"
        path_target = "./eco2mix-national-cons-def2020.csv"
        path, fname = os.path.split(path_target)
        pooch.retrieve(url2020, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`
        usecols2020=['Date', 'Heure', "Consommation (MW)","Nucléaire (MW)", "Gaz (MW)"] # variables we needs
        data2020 = pd.read_csv("./eco2mix-national-cons-def2020.csv",usecols=usecols2020, sep = ";") # importin g our data

        #loading raw data 2021
        url2021 = "https://bit.ly/3tId29N"
        path_target = "./eco2mix-national-cons-def2021.csv"
        path, fname = os.path.split(path_target)
        pooch.retrieve(url2021, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`
        usecols2021=['Date', 'Heure', "Consommation (MW)", "Nucléaire (MW)", "Gaz (MW)"] # variables we needs
        data2021 = pd.read_csv("./eco2mix-national-cons-def2021.csv",usecols=usecols2021, sep = ";") # importin g our data

        #loading  half raw data 2022 
        url2022half = "https://bit.ly/3gisk1Y"
        path_target = "./eco2mix-national-cons-def_half2022.csv"
        path, fname = os.path.split(path_target)
        pooch.retrieve(url2022half, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`
        usecolshalf2022=['Date', 'Heure', "Consommation (MW)","Nucléaire (MW)", "Gaz (MW)"] # variables we needs
        dataHalf2022 = pd.read_csv("./eco2mix-national-cons-def_half2022.csv",usecols=usecolshalf2022, sep = ";") # importin g our data

        #loading raw data 2022
        url2022 = "https://bit.ly/3VgREnT"
        path_target = "./eco2mix-national-cons-def2022.csv"
        path, fname = os.path.split(path_target)
        pooch.retrieve(url2022, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`
        usecols2022=['Date', 'Heure', "Consommation (MW)", "Nucléaire (MW)", "Gaz (MW)"] # variables we needs
        data2022 = pd.read_csv("./eco2mix-national-cons-def2022.csv",usecols=usecols2022, sep = ";") # importin g our data
        data2022.dropna(inplace=True) 
        print(data2022.isna().sum())

        # __________________________________________________________________________
        time_improved = pd.to_datetime(data2019['Date'] +
                                       ' ' + data2019['Heure'],
                                       format='%Y-%m-%d %H:%M')
        data2019['Time'] = time_improved  # add the Time to the data
        data2019.set_index('Time', inplace=True) # set time as index
        # remove useles columns
        del data2019['Heure']
        del data2019['Date']
        data2019 = data2019.sort_index(ascending=True)

        time_improved = pd.to_datetime(data2020['Date'] +
                                       ' ' + data2020['Heure'],
                                       format='%Y-%m-%d %H:%M')
        data2020['Time'] = time_improved  # add the Time to the data
        data2020.set_index('Time', inplace=True) # set time as index
        # remove useles columns
        del data2020['Heure']
        del data2020['Date']
        data2020 = data2020.sort_index(ascending=True)

        time_improved = pd.to_datetime(data2021['Date'] +
                                       ' ' + data2021['Heure'],
                                       format='%Y-%m-%d %H:%M')
        data2021['Time'] = time_improved  # add the Time to the data
        data2021.set_index('Time', inplace=True) # set time as index
        # remove useles columns
        del data2021['Heure']
        del data2021['Date']
        data2021 = data2021.sort_index(ascending=True)

        time_improved = pd.to_datetime(dataHalf2022['Date'] +
                                       ' ' + dataHalf2022['Heure'],
                                       format='%Y-%m-%d %H:%M')
        dataHalf2022['Time'] = time_improved  # add the Time to the data
        dataHalf2022.set_index('Time', inplace=True) # set time as index
        # remove useles columns
        del dataHalf2022['Heure']
        del dataHalf2022['Date']
        dataHalf2022 = dataHalf2022.sort_index(ascending=True)

        time_improved = pd.to_datetime(data2022['Date'] +
                                       ' ' + data2022['Heure'],
                                       format='%Y-%m-%d %H:%M')
        data2022['Time'] = time_improved  # add the Time to the data
        data2022.set_index('Time', inplace=True) # set time as index
        # remove useles columns
        del data2022['Heure']
        del data2022['Date']
        data2022 = data2022.sort_index(ascending=True)

        #--------------------------------------------------
        frames = [data2019, data2020, data2021, dataHalf2022, data2022]
        self.data = pd.concat(frames) 
        return self.data

    def Filnan(self):
        # _________________________________________________________-
        for nan in range(np.shape(self.data)[0]-1):    # fil nan  2010
            if self.data[["Consommation (MW)"]].isna().iloc[:,0][nan] :
                self.data.loc[:,"Gaz (MW)"][nan] = (self.data.loc[:,"Gaz (MW)"][nan-1] +self.data.loc[:,"Gaz (MW)"][nan+1])/2 # replace nan by the mean between 2 samples 
                self.data.loc[:,"Nucléaire (MW)"][nan] = (self.data.loc[:,"Nucléaire (MW)"][nan-1] +self.data.loc[:,"Nucléaire (MW)"][nan+1])/2 # replace nan by the mean between 2 samples 
                self.data.loc[:,"Consommation (MW)"][nan] = (self.data.loc[:,"Consommation (MW)"][nan-1] +self.data.loc[:,"Consommation (MW)"][nan+1])/2 # replace nan by the mean between 2 samples 
        self.data.loc[:,"Consommation (MW)"][nan+1] =  self.data.loc[:,"Consommation (MW)"][nan]
        return self.data
# %%
#data = Data()
# %%
#ts = data.importData()
#ts = data.Filnan()
# %%

# %%
#ts.to_csv("./DataSet.csv")

# %%
