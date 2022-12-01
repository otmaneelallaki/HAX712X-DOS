#%%
import numpy as np
import pandas as pd
import geopandas as gpd
import folium
 
# %%
#url = ("https://....")
#region_shape = f"{url}/....json"
#region_consumption = f"{url}/....csv"

region_consumption = pd.read_csv("conso_reg.csv")
region_shape = gpd.read_file('regions.geojson')
region_consumption['REG'] = region_consumption['REG'].astype(str)

#%%
bins = list(region_consumption["Conso"].quantile([0, 0.25, 0.5, 0.75, 1]))
m = folium.Map(location=[47, 3], zoom_start=5)

folium.Choropleth(
    geo_data=region_shape,
    name="map",
    data=region_consumption,
    columns=["REG", "Conso"],
    key_on="feature.properties.code",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Consumption (MWh)",
).add_to(m)

folium.LayerControl().add_to(m)

"""
just add a layer control to able/disable the data on the map

"""

m

