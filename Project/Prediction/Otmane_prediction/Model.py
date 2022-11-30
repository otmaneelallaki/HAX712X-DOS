#%%
import DataCollection  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import xgboost as xgb
from sklearn.metrics import mean_squared_error
color_pal = sns.color_palette()
plt.style.use('fivethirtyeight')
sns.set()

#machine learning and statistical methods
import statsmodels.api as sm

from sklearn.model_selection import TimeSeriesSplit
# %%____________________________________________-
ts = DataCollection.data() # data from 2019-01-01 00:00:00 to 2022-11-14 23:45:00
# %%
test_size = np.shape(ts.loc["2022-01-01 00:00:00":,])[0]
tsp       = TimeSeriesSplit(n_splits=2, test_size=test_size, gap=0)

# %%
def create_features(ts):
    """
    Create time series features based on time series index.
    """
    ts = ts.copy()
    ts['minute']     = ts.index.minute
    ts['dayofweek']  = ts.index.dayofweek
    ts['month']      = ts.index.month
    ts['year']       = ts.index.year
    ts['dayofyear']  = ts.index.dayofyear
    ts['dayofmonth'] = ts.index.day
    ts['weekofyear'] = ts.index.isocalendar().week
    return ts

ts = create_features(ts)
#%%
def add_lags(ts):
    target_map = ts['Consommation (MW)'].to_dict()
    ts['lag1'] = (ts.index - pd.Timedelta('364 days')).map(target_map)
    ts['lag2'] = (ts.index - pd.Timedelta('30 days')).map(target_map)
    ts['lag3'] = (ts.index - pd.Timedelta('7 days')).map(target_map)
    return ts
ts = add_lags(ts)
# %%
for train_idx, val_idx in tsp.split(ts):
    train = ts.iloc[train_idx]
    test  = ts.iloc[val_idx]
    train = create_features(train)
    test  = create_features(test)

    FEATURES = ['dayofyear', 'minute', 'dayofweek', 'month','year','lag1', 'lag2', 'lag3']
    TARGET   = 'Consommation (MW)'

    X_train  = train[FEATURES]
    y_train  = train[TARGET]

    X_test   = test[FEATURES]
    y_test   = test[TARGET]

    reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
                           n_estimators=1000,
                           early_stopping_rounds=50,
                           objective='reg:linear',
                           max_depth=3,
                           learning_rate=0.01)
    reg.fit(X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=100)
# %%__________ day  2022-11-22
usecolsday20 = ['Date', 'Heure', "Consommation (MW)"]
day20        = pd.read_csv('/Users/mac/downloads/day22.csv', usecols=usecolsday20, sep = ";")
#%%
time_improved = pd.to_datetime(day20['Date'] +
                                   ' ' + day20['Heure'],
                                   format='%Y-%m-%d %H:%M')
day20['Time'] = time_improved  # add the Time to the data
day20.set_index('Time', inplace=True) # set time as index
    # remove useles columns
del day20['Heure']
del day20['Date']
day20 = day20.sort_index(ascending=True)

#day20 = create_features(day20)


# %%
def PredectDay(data):
    target_map = ts['Consommation (MW)'].to_dict()

    data['dayofyear'] = data.index.dayofyear
    data['minute'] = data.index.minute
    data['dayofweek'] = data.index.dayofweek
    #data['quarter'] = ts.index.quarter
    data['month'] = data.index.month
    data['year'] = data.index.year
    data['lag1'] = (data.index - pd.Timedelta('364 days')).map(target_map)
    data['lag2'] = (data.index - pd.Timedelta('30 days')).map(target_map)
    data['lag3'] = (data.index - pd.Timedelta('7 days')).map(target_map)
    dayfeaytures = data.drop(['Consommation (MW)'], axis=1)
    return dayfeaytures
# %%
dayfeatures = PredectDay(day20)
# %%
realday  = day20['Consommation (MW)']
index = realday.index
day_pred = reg.predict(dayfeatures)
day_pred = pd.DataFrame(day_pred, index=index, columns= ['Consommation (MW)'])
score = np.sqrt(mean_squared_error(realday, day_pred)) 
precentage = np.mean(day_pred)/np.mean(realday)
# %%
f, ax = plt.subplots(figsize=(12,6),dpi=200);
plt.suptitle('Prediction day Energy consumption (MW)', fontsize=24);
day_pred.plot(ax=ax,rot=90,ylabel='MW');
realday.plot(ax=ax,rot=90,ylabel='MW');
ax.legend(["day Predict", "Real day"],loc="upper right")
plt.show()