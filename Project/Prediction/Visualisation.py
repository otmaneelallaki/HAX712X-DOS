#%%
import DataCollection  
#mathematical operations
import numpy as np

#data handling

#plotting
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

#machine learning and statistical methods
import statsmodels.api as sm

#dataframe index manipulations
import datetime

#muting unnecessary warnings if needed
import warnings
# %%____________________________________________-
ts = DataCollection.Data()
ts = ts.impo() # data from 2019-01-01 00:00:00 to 2022-11-14 23:45:00
ts.drop(["Gaz (MW)","Nucléaire (MW)"], axis=1, inplace=True)
#%%____________________________________________________________
#visual checking of data. Plotting by Pandas method, drawing axes by Matplotlib
f, ax = plt.subplots(figsize=(18,6),dpi=200);
plt.suptitle('France Electric Power Energy consumption (MW)', fontsize=24);
ts.plot(ax=ax,rot=90,ylabel='MW');
# %%___________________________________________________________________
#visual check of data at different scale
f, ax = plt.subplots(figsize=(18,6),dpi=200);
plt.suptitle('American Electric Power estimated energy consumption in MegaWatts (MW)', fontsize=36);
ts.iloc[34560:3*34560,:].plot(ax=ax,rot=90,fontsize=12); #Ploting two years 
#%%______________________________________________________________
#drawing a random sample of 5 indices without repetition
sample = sorted([x for x in np.random.choice(range(len(ts)), 5, replace=False)])

#zoom x scales for plotting
periods = [34360,2880,672]

#plotting random time intervals at different scales to observe any seasonality present
f, axes = plt.subplots(len(sample),3,dpi=400,figsize=(12,12));
plt.suptitle('{} random time window plotted at {} different scales'.format(len(sample),len(periods)), fontsize=24, x=0.5, y=0.95)
f.tight_layout(pad=3.0); 

#s for sample datetime start
for si,s in enumerate(sample):
    
    #p for period length
    for pi,p in enumerate(periods):
        ts.iloc[s:(s+p+1),:].plot(ax=axes[si][pi], legend=False, rot=90);
        #annotating datetime start
        axes[si][pi].annotate("Start at: " + ts.iloc[s:s+1,:].index[0].strftime("%d-%b-%Y %H:%M"), (0,1), xycoords='axes fraction')

# %%_____________________________________________________________________-
#drawing a random sample of 5 indices without repetition from sub sample, where current time is 04:00
sample = sorted([x for x in np.random.choice([x for x in ts.index[:-960] if x.minute == 15],5,replace=False)])

#checking persistence of daily seasonality by inspecting 5 random time window of 10 days
f, axes = plt.subplots(len(sample),1,dpi=200,figsize=(18,24));
f.tight_layout(pad=3.0)
plt.suptitle('Random time window samples with duraton of 10 days for inspecting daily seasonal effect', y = 1.01, fontsize=24)

#plotting time windows and drawing vertical lines at 04:00 each day
for si,s in enumerate(sample):
    ids = ts.index.to_list().index(s)
    idx = [ts.iloc[x:x+1,:].index.values for x in range(ids, ids + 960,96)]
    ts.iloc[ids:(ids+960),:].plot(ax=axes[si], legend=False, rot=90, ylabel='MW');
    axes[si].vlines(idx, axes[si].get_ylim()[0], axes[si].get_ylim()[1], colors='black', linestyles='dashed')

# %%____________________________________________
#drawing a random sample of 5 indices without repetition from sub sample of Mondays
sample = sorted([x for x in np.random.choice([x for x in ts.index[:-6720] if x.dayofweek == 0],5,replace=False)])

#checking persistence of weekly seasonality by inspecting 5 random time window of 10 days
f, axes = plt.subplots(len(sample),1,dpi=200,figsize=(18,24));
f.tight_layout(pad=3.0)
plt.suptitle('Random time window samples with duraton of 10 weeks for inspecting weekly seasonal effect', y = 1.01, fontsize=24)

#plotting time windows and drawing vertical lines at every Monday
for si,s in enumerate(sample):
    ids = ts.index.to_list().index(s)
    idx = [ts.iloc[x:x+1,:].index.values for x in range(ids, ids + 6720,672)]
    ts.iloc[ids:(ids+6720),:].plot(ax=axes[si], legend=False, rot=90, ylabel='MW');
    axes[si].vlines(idx, axes[si].get_ylim()[0], axes[si].get_ylim()[1], colors='black', linestyles='dashed')

# %%________________________________________________
#checking presence of yearly seasonality
f, axes = plt.subplots(dpi=200,figsize=(18,6));
f.tight_layout(pad=3.0);
plt.suptitle('One year time windows for inspecting yearly seasonal effect', y = 1.01, fontsize=24);

#plotting and drawing vertical lines at every New Year's Eve
#idx = [ts.loc[x:x+1*ts.index.freq,:].index.values for x in ts.index if x.dayofyear == 1]
ts.plot(ax=axes, legend=False, rot=90, ylabel='MW');
idx = [np.array(['2020-01-01T09:15:00.000000000'], dtype='datetime64[ns]'), 
      np.array(['2021-01-01T09:15:00.000000000'], dtype='datetime64[ns]'),
      np.array(['2022-01-01T09:15:00.000000000'], dtype='datetime64[ns]')]
axes.vlines(idx, axes.get_ylim()[0], axes.get_ylim()[1], colors='black', linestyles='dashed');

# %%____________________________________________________
#extracting daily seasonality from raw time series
sd_96 = sm.tsa.seasonal_decompose(ts, period=96) 

#extracting weekly seasonality from time series adjusted by daily seasonality
sd_672 = sm.tsa.seasonal_decompose(ts - np.array(sd_96.seasonal).reshape(-1,1), period=672)
# the year = 30.44*14 days
#(np.shape(data2019)[0] + np.shape(data2020)[0] +np.shape(data2021)[0] )/(3*4*12*24)
#extracting yearly seasonality from time series adjusted by daily and weekly seasonality
sd_35066 = sm.tsa.seasonal_decompose(ts - np.array(sd_672.seasonal).reshape(-1,1), period=35066)
# %%_____________________________________________________
#drawing figure with subplots, predefined size and resolution
f, axes = plt.subplots(5,1,figsize=(18,24),dpi=200);

#setting figure title and adjusting title position and size
plt.suptitle('Summary of seasonal decomposition', y=0.92, fontsize=24);

#plotting trend component
axes[0].plot(sd_35066.trend)
axes[0].set_title('Trend component', fontdict={'fontsize': 18});

#drawing black dashed vertical lines between y axis limits
axes[0].vlines(datetime.datetime(2020,6,1), axes[0].get_ylim()[0], axes[0].get_ylim()[1], colors='black', linestyles='dashed');

#placing three comments in text boxes
axes[0].text(datetime.datetime(2019,9,1), 52500, 'Decreasing trend',
             ha='center', va='center', bbox=dict(fc='white', ec='b', boxstyle='round'));
axes[0].text(datetime.datetime(2020,9,1), 53000, 'Increasing trend',
             ha='center', va='center', bbox=dict(fc='white', ec='b', boxstyle='round'));
axes[0].text(datetime.datetime(2020,5,15), 52000, 'COVID 2019',
             ha='center', va='center', bbox=dict(fc='white', ec='b', boxstyle='round'));

#plotting daily seasonal component
axes[1].plot(sd_96.seasonal[:1000]);
axes[1].set_title('Daily seasonal component', fontdict={'fontsize': 18});
axes[1].annotate('Higher \n daytime values', xy=(0.54, 0.50),
            xycoords='axes fraction',
            va='center', ha='center',
            xytext=(0.9, 0.9),
            textcoords='axes fraction',
            bbox=dict(boxstyle='round', fc='w', ec='b'));
axes[1].annotate('Lower \n nighttime values', xy=(0.54, 0.50),
            xycoords='axes fraction',
            va='center', ha='center',
            xytext=(0.9, 0.1),
            textcoords='axes fraction',
            bbox=dict(boxstyle='round', fc='w', ec='b'));

#plotting weekly seasonal component
axes[2].plot(sd_672.seasonal[120000:120000+ 4704]);
axes[2].set_title('Weekly seasonal component', fontdict={'fontsize': 18});

#placing comment in annotation with text box and arrow
axes[2].annotate('Leaked daily \n seasonal effects', xy=(0.775, 0.75),
            xycoords='axes fraction',
            va='center', ha='center',
            xytext=(0.775, 0.25),
            textcoords='axes fraction',
            bbox=dict(boxstyle='round', fc='w', ec='b'),
            arrowprops=dict(color='black',
                            arrowstyle='->',
                            connectionstyle='arc3'));
axes[2].annotate('Weekdays', xy=(0.39, 0.71),
            xycoords='axes fraction',
            va='center', ha='center',
            xytext=(0.39, 0.27),
            textcoords='axes fraction',
            bbox=dict(boxstyle='round', fc='w', ec='b'),
            arrowprops=dict(color='black',
                            arrowstyle='-[',
                            mutation_scale=45,
                            connectionstyle='arc3'));
axes[2].annotate('Weekends', xy=(0.197, 0.55),
            xycoords='axes fraction',
            va='center', ha='center',
            xytext=(0.197, 0.90),
            textcoords='axes fraction',
            bbox=dict(boxstyle='round', fc='w', ec='b'),
            arrowprops=dict(color='black',
                            arrowstyle='-[',
                            mutation_scale=15,
                            connectionstyle='arc3'));

#plotting yearly seasonality
axes[3].plot(sd_35066.seasonal);
axes[3].set_title('Yearly seasonal component', fontdict={'fontsize': 18});

#placing comments in annotations with text boxes and arrows
axes[3].annotate('Summer', xy=(0.36, 0.50),
            xycoords='axes fraction',
            va='center', ha='center',
            xytext=(0.43, 0.05),
            textcoords='axes fraction',
            bbox=dict(boxstyle='round', fc='#f5f88f', ec='b'));
axes[3].annotate('Winter', xy=(0.54, 0.50),
            xycoords='axes fraction',
            va='center', ha='center',
            xytext=(0.5, 0.74),
            textcoords='axes fraction',
            bbox=dict(boxstyle='round', fc='#f5f88f', ec='b'));

#plotting residual of decomposition
axes[4].plot(sd_35066.resid);
axes[4].set_title('Residual component', fontdict={'fontsize': 18});

#setting label for each y axis
for a in axes:
    a.set_ylabel('MW');
plt.show();

# %%
