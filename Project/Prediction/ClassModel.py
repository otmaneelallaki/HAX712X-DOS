#import DataCollection  
import pandas as pd
import numpy as np
import datetime as dt
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
import statsmodels.api as sm

class Dos():
    """  Class featurs  """
    def __init__(self, data, energie) -> None:
        self.data = data
        self.energie = energie 
        """"
        In this part we are going   :ref:`Data Collection <DataCol>`:
        """

    def createFeatures(self):
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
        target = self.data.columns[self.energie]
        target_map = self.data[target].to_dict()
        self.data['lag1'] = (self.data.index - pd.Timedelta('364 days')).map(target_map)
        self.data['lag2'] = (self.data.index - pd.Timedelta('30 days')).map(target_map)
        self.data['lag3'] = (self.data.index - pd.Timedelta('7 days')).map(target_map)
        return self.data

    def fitModel(self):
        target = self.data.columns[self.energie]
        FEATURES = ['dayofyear', 'minute', 'dayofweek', 'month', 'year',
                    'lag1','lag2','lag3']
        TARGET = target 
        
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


    def DayPred(self,year,month,day, reg):
        """
        Predict confidence scores for samples.
        The confidence score for a sample is proportional to the signed
        distance of that sample to the hyperplane.

        :param Year: The Year for which day we want to predict.
        :type Year: int

        :param month: The month for which day we want to predict.
        :type month: int

        :param day: The day for which day we want to predict.
        :type day: int
        """
        liste = []
        for i in range (96):
            liste.append(str(dt.datetime(year, month, day, 0, 0) + dt.timedelta(minutes=(i)*15)))
        DayDate = pd.to_datetime(np.array(liste))
        target = self.data.columns[self.energie]
        dayFeaturs = pd.DataFrame()
        dayFeaturs['dayofyear'] = DayDate.dayofyear
        dayFeaturs['minute']    = DayDate.minute
        dayFeaturs['dayofweek'] = DayDate.dayofweek
        dayFeaturs['month']     = DayDate.month
        dayFeaturs['year']      = DayDate.year
        target_map         = self.data[target].to_dict()
        dayFeaturs['lag1'] = (DayDate - pd.Timedelta('364 days')).map(target_map)
        dayFeaturs['lag2'] = (DayDate - pd.Timedelta('30 days')).map(target_map)
        dayFeaturs['lag3'] = (DayDate - pd.Timedelta('7 days')).map(target_map)
        
        pred    = reg.predict(dayFeaturs)
        #day_pred    = pd.DataFrame(day_pred, index=DayDate, columns= ['predicted day'])
        Date       = DayDate.strftime('%Y-%m-%d')
        Hour       = DayDate.strftime('%H:%M')
        day_pred                        = pd.DataFrame()
        day_pred["Date"]                = Date
        day_pred["Heure"]               = Hour
        day_pred[target]   = pred

        return  day_pred, DayDate

    def plot(self,day_pred, DayDate ):
        target = self.data.columns[self.energie]
        
        day_pred = day_pred[target].values
        day_pred    = pd.DataFrame(day_pred, index=DayDate, columns= ['predicted day'])
        f, ax = plt.subplots(figsize=(12,6),dpi=200);
        plt.suptitle('2022 Dec 8 Forcasting {}'.format(target), fontsize=24);
        day_pred.plot(ax=ax,rot=90,ylabel='MW',legend= "Predicted day ");
        plt.show()


