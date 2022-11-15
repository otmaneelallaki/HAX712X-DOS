#%%
import pandas as pd
import datetime
import numpy as np

# %%_________________________________________________________
def data():
    # link  for the data https://odre.opendatasoft.com/explore/dataset/eco2mix-national-cons-def/table/?disjunctive.nature&sort=-date_heure&refine.date_heure=2020
    #loading raw data 2019
    link2019 = "/Users/mac/Downloads/eco2mix-national-cons-def_2019.csv"
    usecols2019=['Date', 'Heure', "Consommation (MW)"] # variables we needs
    data2019 = pd.read_csv(link2019, usecols=usecols2019, sep = ";") # importin g our data

    #loading raw data 2020
    link2020 = "/Users/mac/Downloads/eco2mix-national-cons-def_2020.csv"
    usecols2020=['Date', 'Heure', "Consommation (MW)"] # variables we needs
    data2020 = pd.read_csv(link2020, usecols=usecols2020, sep = ";") # importin g our data

    #loading raw data 2021
    link2021 = "/Users/mac/Downloads/eco2mix-national-cons-def_2021.csv"
    usecols2021=['Date', 'Heure', "Consommation (MW)"] # variables we needs
    data2021 = pd.read_csv(link2021, usecols=usecols2021, sep = ";") # importin g our data

    #loading  half raw data 2022 
    linkHalf2022 = "/Users/mac/Downloads/eco2mix-national-cons-def_half2022.csv"
    usecolsHalf2022=['Date', 'Heure', "Consommation (MW)"] # variables we needs
    dataHalf2022 = pd.read_csv(linkHalf2022, usecols=usecolsHalf2022, sep = ";") # importin g our data

    #loading raw data 2022
    link2022 = "/Users/mac/Downloads/eco2mix-national-cons-def_2022.csv"
    usecols2022=['Date', 'Heure', "Consommation (MW)"] # variables we needs
    data2022 = pd.read_csv(link2022, usecols=usecols2022, sep = ";") # importin g our data

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
# %%
