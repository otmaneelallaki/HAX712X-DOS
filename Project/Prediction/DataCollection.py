import pandas as pd
import datetime
import numpy as np
import pooch  # download data / avoid re-downloading
import os

def data():
    #loading raw data 2019
    url2019 = "https://bit.ly/3hVlwrl"
    path_target = "./eco2mix-national-cons-def2019.csv"
    path, fname = os.path.split(path_target)
    pooch.retrieve(url2019, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`

    usecols2019=['Date', 'Heure', "Consommation (MW)"] # variables we needs
    data2019 = pd.read_csv("./eco2mix-national-cons-def2019.csv",usecols=usecols2019, sep = ";") # importin g our data
    
    #loading raw data 2020
    url2020 = "https://bit.ly/3tLbMCE"
    path_target = "./eco2mix-national-cons-def2020.csv"
    path, fname = os.path.split(path_target)
    pooch.retrieve(url2020, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`

    usecols2020=['Date', 'Heure', "Consommation (MW)"] # variables we needs
    data2020 = pd.read_csv("./eco2mix-national-cons-def2020.csv",usecols=usecols2020, sep = ";") # importin g our data
    
    #loading raw data 2021
    url2021 = "https://bit.ly/3tId29N"
    path_target = "./eco2mix-national-cons-def2021.csv"
    path, fname = os.path.split(path_target)
    pooch.retrieve(url2021, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`

    usecols2021=['Date', 'Heure', "Consommation (MW)"] # variables we needs
    data2021 = pd.read_csv("./eco2mix-national-cons-def2021.csv",usecols=usecols2021, sep = ";") # importin g our data
    
    #loading  half raw data 2022 
    url2022half = "https://bit.ly/3gisk1Y"
    path_target = "./eco2mix-national-cons-def_half2022.csv"
    path, fname = os.path.split(path_target)
    pooch.retrieve(url2022half, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`

    usecolshalf2022=['Date', 'Heure', "Consommation (MW)"] # variables we needs
    dataHalf2022 = pd.read_csv("./eco2mix-national-cons-def_half2022.csv",usecols=usecolshalf2022, sep = ";") # importin g our data
    
    #loading raw data 2022
    url2022 = "https://bit.ly/3VgREnT"
    path_target = "./eco2mix-national-cons-def2022.csv"
    path, fname = os.path.split(path_target)
    pooch.retrieve(url2022, path=path, fname=fname, known_hash=None)  # if needed `pip install pooch`

    usecols2022=['Date', 'Heure', "Consommation (MW)"] # variables we needs
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

    # _________________________________________________________-
    for nan in range(np.shape(data2019)[0]-1):    # fil nan  2010
        if data2019[["Consommation (MW)"]].isna().iloc[:,0][nan]:
            data2019.loc[:,"Consommation (MW)"][nan] = (data2019.loc[:,"Consommation (MW)"][nan-1] +data2019.loc[:,"Consommation (MW)"][nan+1])/2 # replace nan by the mean between 2 samples 
    data2019.loc[:,"Consommation (MW)"][nan+1] =  data2019.loc[:,"Consommation (MW)"][nan]
    print(data2019.isna().sum()) # calcule data missing


    for nan in range(np.shape(data2020)[0]-1):    # fil nan  2020
        if data2020[["Consommation (MW)"]].isna().iloc[:,0][nan]:
            data2020.loc[:,"Consommation (MW)"][nan] = (data2020.loc[:,"Consommation (MW)"][nan-1] +data2020.loc[:,"Consommation (MW)"][nan+1])/2 # replace nan by the mean between 2 samples 
    data2020.loc[:,"Consommation (MW)"][nan+1] =  data2020.loc[:,"Consommation (MW)"][nan]
    print(data2020.isna().sum()) # calcule data missing

    for nan in range(np.shape(data2021)[0]-1):    # fil nan  2021
        if data2021[["Consommation (MW)"]].isna().iloc[:,0][nan]:
            data2021.loc[:,"Consommation (MW)"][nan] = (data2021.loc[:,"Consommation (MW)"][nan-1] +data2021.loc[:,"Consommation (MW)"][nan+1])/2 # replace nan by the mean between 2 samples 
    data2021.loc[:,"Consommation (MW)"][nan+1] =  data2021.loc[:,"Consommation (MW)"][nan]
    print(data2021.isna().sum()) # calcule data missing

    for nan in range(np.shape(dataHalf2022)[0]-1):    # fil nan  2021
        if dataHalf2022[["Consommation (MW)"]].isna().iloc[:,0][nan]:
            dataHalf2022.loc[:,"Consommation (MW)"][nan] = (dataHalf2022.loc[:,"Consommation (MW)"][nan-1] +dataHalf2022.loc[:,"Consommation (MW)"][nan+1])/2 # replace nan by the mean between 2 samples 
    dataHalf2022.loc[:,"Consommation (MW)"][nan+1] =  dataHalf2022.loc[:,"Consommation (MW)"][nan]
    print(dataHalf2022.isna().sum()) # calcule data missing
    #_______________________________________________________________-
    # now our data is clean let's magre them 
    frames = [data2019, data2020, data2021, dataHalf2022, data2022]
    ts = pd.concat(frames) 
    return ts