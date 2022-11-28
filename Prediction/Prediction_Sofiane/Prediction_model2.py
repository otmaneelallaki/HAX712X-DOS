#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import xgboost as xgb
from sklearn.metrics import mean_squared_error
color_pal = sns.color_palette()
plt.style.use('fivethirtyeight')

from sklearn.model_selection import TimeSeriesSplit
# %%
os.getcwd()
df = pd.read_csv('./eco2mix-national-cons-def_2019-2022.csv', sep = ",")
# %%
df=df.rename(columns={"Time": "Time", "Consommation (MW)": "Consommation_MW"})
# %%
df= df.set_index('Time')
df.index = pd.to_datetime(df.index)
# %%
df.plot(style='.',
        figsize=(15, 5),
        color=color_pal[0],
        title='Consommation éléctéricité en MW')
plt.show()
# %%
df['Consommation (MW)'].plot(kind='hist', bins=500)

# %%
train=df.loc[df.index < '01-01-2021']
# %%
test=df.loc[df.index >= '01-01-2021']

# %%
fix,ax=plt.subplots(figsize=(15,5))
train.plot(ax=ax,label='Training Set',title='Data Train/Test Split')
test.plot(ax=ax,label='Test Set')
ax.axvline('01-01-2021',color='black',ls='--')
ax.legend(['Training Set','Test Set'])
plt.show()

# %%
tss = TimeSeriesSplit(n_splits=5, test_size=24*365*1, gap=24)
df = df.sort_index()
# %%
fig, axs = plt.subplots(5, 1, figsize=(15, 15), sharex=True)

fold = 0
for train_idx, val_idx in tss.split(df):
    train = df.iloc[train_idx]
    test = df.iloc[val_idx]
    train['Consommation (MW)'].plot(ax=axs[fold],
                          label='Training Set',
                          title=f'Data Train/Test Split Fold {fold}')
    test['Consommation (MW)'].plot(ax=axs[fold],
                         label='Test Set')
    axs[fold].axvline(test.index.min(), color='black', ls='--')
    fold += 1
plt.show()

# %%
def create_features(df):
    """
    Create time series features based on time series index.
    """
    df = df.copy()
    df['hour'] = df.index.hour
    df['dayofweek'] = df.index.dayofweek
    df['quarter'] = df.index.quarter
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofyear'] = df.index.dayofyear
    df['dayofmonth'] = df.index.day
    df['weekofyear'] = df.index.isocalendar().week
    return df

df = create_features(df)

# %%
def add_lags(df):
    target_map = df['Consommation (MW)'].to_dict()
    df['lag1'] = (df.index - pd.Timedelta('364 days')).map(target_map)
    df['lag2'] = (df.index - pd.Timedelta('728 days')).map(target_map)
    df['lag3'] = (df.index - pd.Timedelta('1092 days')).map(target_map)
    return df
df=add_lags(df)

# %%
tss = TimeSeriesSplit(n_splits=5, test_size=24*365*1, gap=24)
df = df.sort_index()

fold = 0
preds = []
scores = []
for train_idx, val_idx in tss.split(df):
    train = df.iloc[train_idx]
    test = df.iloc[val_idx]

    train = create_features(train)
    test = create_features(test)

    FEATURES = ['dayofyear', 'hour', 'dayofweek', 'quarter', 'month','year',
                'lag1','lag2','lag3']
    TARGET = 'Consommation (MW)'

    X_train = train[FEATURES]
    y_train = train[TARGET]

    X_test = test[FEATURES]
    y_test = test[TARGET]

    reg = xgb.XGBRegressor(base_score=0.5, booster='gbtree',    
                           n_estimators=1000,
                           early_stopping_rounds=50,
                           objective='reg:linear',
                           max_depth=3,
                           learning_rate=0.01)
    reg.fit(X_train, y_train,
            eval_set=[(X_train, y_train), (X_test, y_test)],
            verbose=100)

    y_pred = reg.predict(X_test)
    preds.append(y_pred)
    score = np.sqrt(mean_squared_error(y_test, y_pred))
    scores.append(score)

# %%
print(f'Score across folds {np.mean(scores):0.4f}')
print(f'Fold scores:{scores}')
# %%
df = create_features(df)

FEATURES = ['dayofyear', 'hour', 'dayofweek', 'quarter', 'month', 'year',
            'lag1','lag2','lag3']
TARGET = 'Consommation (MW)'

X_all = df[FEATURES]
y_all = df[TARGET]

reg = xgb.XGBRegressor(base_score=0.5,
                       booster='gbtree',    
                       n_estimators=500,
                       objective='reg:linear',
                       max_depth=3,
                       learning_rate=0.01)
reg.fit(X_all, y_all,
        eval_set=[(X_all, y_all)],
        verbose=100)
# %%
df.index.max()

# %%
future = pd.date_range('2022-11-14','2022-12-09', freq='15min')
future_df = pd.DataFrame(index=future)
future_df['isFuture'] = True
df['isFuture'] = False
df_and_future = pd.concat([df, future_df])
df_and_future = create_features(df_and_future)
df_and_future = add_lags(df_and_future)
# %%
future_w_features = df_and_future.query('isFuture').copy()
# %%
future_w_features['pred'] = reg.predict(future_w_features[FEATURES])
# %%
future_w_features['pred'].plot(figsize=(10, 5),
                               color=color_pal[4],
                               ms=1,
                               lw=1,
                               title='Future Predictions')
plt.show()
# %%
prediction=future_w_features.loc[(future_w_features.index >= '2022-12-8') &  (future_w_features.index < '2022-12-9') ]



# %%
prediction=prediction.drop(columns=['Consommation (MW)','hour',
             'dayofweek','quarter','month','year','dayofyear','dayofmonth',
             'weekofyear',	'lag1'	,'lag2'	,'lag3'	,'isFuture'])
# %%
prediction.index=prediction.index.rename('Time')

# %%
prediction=prediction.rename(columns={'pred':'Consommation (MW)'})
# %%
