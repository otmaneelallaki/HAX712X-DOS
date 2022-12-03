#%%
from Project.Prediction import ClassModel as np
# %%_________EXemple of ClassModel ---------------
# %%
Object = np.Featurs()
# %%
ts = Object.ImportData()
# %%
Object.createFeatures()
# %%
reg = Object.fitModel()
# %%
dayPred = Object.DayPred(2022,11,10,reg)
# %%
Object.plot(dayPred)
# %%
