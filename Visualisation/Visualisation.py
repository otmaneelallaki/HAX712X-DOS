#%%
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.offline import plot
#%%

data = pd.read_csv("/Users/mac/Desktop/consommation-annuelle-residentielle-par-adresse.csv", sep = ";")
data.head(4)
# %%

# %%
data.columns
# %%
data[['Code IRIS']].value_counts().sum()   # the effectives
data[['Nom IRIS']].value_counts().sum()   # the effectives

# %%
fig = px.scatter(
    data,
    x="Consommation annuelle moyenne de la commune (MWh)",
    y="Consommation annuelle moyenne de la commune (MWh)",
    animation_frame="Année",
    animation_group="Code INSEE de la commune",
    #size="pop",
    #color="continent",
    hover_name="Code INSEE de la commune",
    log_x=True,
    size_max=55,
    range_x=[1, 10000],
    range_y=[1, 20],
)
fig.show("notebook")
# %%
