#%%
import os
import pooch
import numpy as np
import pandas as pd
import geopandas as gpd
import folium

url_shape = 'https://www.data.gouv.fr/fr/datasets/r/92f37c92-3aae-452c-8af1-c77e6dd590e5'
region_shape = gpd.read_file(url_shape)

region_consumption = pd.read_csv('conso_dep.csv')
region_consumption['DEP'] = region_consumption['DEP'].astype(str)

bins = list(region_consumption["Conso"].quantile([0, 0.25, 0.5, 0.75, 1]))
m = folium.Map(location   = [47, 3],
               zoom_start = 5,
               tiles      = None)

folium.Choropleth(
    geo_data     = region_shape,
    name         = "map",
    data         = region_consumption,
    columns      = ["DEP", "Conso"],
    key_on       = "feature.properties.dep",
    fill_color   = "YlOrRd",
    fill_opacity = 0.7,
    line_opacity = 0.2,
    legend_name  = "Consumption (MWh)",
).add_to(m)

m

# %% to open in firefox, the following command will save the map
# as a html file in your local repository, then you open it
m.save("map.html")
