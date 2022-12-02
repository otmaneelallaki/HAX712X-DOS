#%%
import DataCollection  
import pandas as pd
import numpy as np
import datetime as dt
import xgboost as xgb

class Featurs():
    """  Class featurs  """
    def __init__(self, data= pd.DataFrame()) -> None:
        self.data = data

    def ImportData(self):
        """ Importing our time serier from DataCollection Model """
        self.data = DataCollection.data()
        #self.data = pd.read_csv('/Users/mac/Desktop/HAX712X-DOS/Project/Prediction/Prediction_Sofiane/eco2mix-national-cons-def_2019-2022.csv', sep = ",")
        #self.data= self.data.set_index('Time')
        #self.data.index = pd.to_datetime(self.data.index)
        return self.data

    def create_features(self):
        """
        Create time series features based on time series index.
        """
        self.data = self.data.copy()
        self.data['minute']     = self.data.index.minute
        self.data['dayofweek']  = self.data.index.dayofweek
        self.data['month']      = self.data.index.month
        self.data['year']       = self.data.index.year
        self.data['dayofyear']  = self.data.index.dayofyear
        self.data['dayofmonth'] = self.data.index.day
        
        target_map = self.data['Consommation (MW)'].to_dict()
        self.data['lag1'] = (self.data.index - pd.Timedelta('364 days')).map(target_map)
        self.data['lag2'] = (self.data.index - pd.Timedelta('30 days')).map(target_map)
        self.data['lag3'] = (self.data.index - pd.Timedelta('7 days')).map(target_map)
        return self.data


class FitModel():
    """
    Fiting our Model : Gradient boosting-based
    """
    def __init__(self, data) -> None:
        self.data = data

    def fitModel(self):
        FEATURES = ['dayofyear', 'minute', 'dayofweek', 'month', 'year',
                    'lag1','lag2','lag3']
        TARGET = 'Consommation (MW)'
        
        X_all = self.data[FEATURES]
        y_all = self.data[TARGET]
        
        reg = xgb.XGBRegressor(base_score=0.5,
                               booster='gbtree',    
                               n_estimators=500,
                               objective='reg:linear',
                               max_depth=3,
                               learning_rate=0.01)
        reg.fit(X_all, y_all,
                eval_set=[(X_all, y_all)],
                verbose=100)

        return reg


class DayPredict():
    """
    Day Prediction 
    """
    def __init__(self, data) -> None:
        self.data = data

    def DayFeaturs(self,year,month,day, reg):
        """
        Extract the features of the model from the date format

        Return to a DataFrame 
        """
        liste = []
        for i in range (96):
            liste.append(str(dt.datetime(year, month, day, 0, 0) + dt.timedelta(minutes=(i)*15)))
        DayDate = pd.to_datetime(np.array(liste))

        dayFeaturs = pd.DataFrame()
        dayFeaturs['dayofyear'] = DayDate.dayofyear
        dayFeaturs['minute']    = DayDate.minute
        dayFeaturs['dayofweek'] = DayDate.dayofweek
        dayFeaturs['month']     = DayDate.month
        dayFeaturs['year']      = DayDate.year
        target_map  = self.data['Consommation (MW)'].to_dict()
        dayFeaturs['lag1'] = (DayDate - pd.Timedelta('364 days')).map(target_map)
        dayFeaturs['lag2'] = (DayDate - pd.Timedelta('30 days')).map(target_map)
        dayFeaturs['lag3'] = (DayDate - pd.Timedelta('7 days')).map(target_map)
        
        
        day_pred    = reg.predict(dayFeaturs)
        day_pred    = pd.DataFrame(day_pred, index=DayDate, columns= ['predicted day'])
        
        return  day_pred
