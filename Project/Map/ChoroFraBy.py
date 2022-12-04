import numpy as np
import pandas as pd
import geopandas as gpd
import folium
import webbrowser


class ChoroFraBy:

    """ Show a choropleth Map of France with the Electricity
    Consumption from 2019 to 2021 """
    
    
    def createMap(COL):
        
        """
        Choose a France by region or by departments.
        The argument must be 'REG' or 'DEP'

        """

        url_shape_dep = 'https://www.data.gouv.fr/fr/datasets/r/92f37c92-3aae-452c-8af1-c77e6dd590e5'
        f_shape_dep = gpd.read_file(url_shape_dep)

        url_shape_reg = 'https://www.data.gouv.fr/fr/datasets/r/d993e112-848f-4446-b93b-0a9d5997c4a4'
        f_shape_reg = gpd.read_file(url_shape_reg)
        
        f_consumption_dep = pd.read_csv('./DataSet/departements_consumption.csv')
        f_consumption_dep['DEP'] = f_consumption_dep['DEP'].astype(str)

        f_consumption_reg = pd.read_csv('./DataSet/regions_consumption.csv')
        f_consumption_reg['REG'] = f_consumption_reg['REG'].astype(str)

        if COL == 'DEP':
            f_consumption = f_consumption_dep
            f_shape = f_shape_dep
            f_key = "feature.properties.dep"

        elif COL == 'REG':
            f_consumption = f_consumption_reg
            f_shape = f_shape_reg
            f_key = "feature.properties.reg"

        else : raise Exception("please give any of the following values as arguments : 'DEP' or 'REG' ")
        
        url_tiles = 'http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.jpg'
        
        bins = list(f_consumption["Conso"].quantile([0, 0.25, 0.5, 0.75, 1]))
        
        m = folium.Map(location   = [47, 3],
                       zoom_start = 5,
                       tiles      = url_tiles,
                       attr       = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, under <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a>. Data by <a href="http://openstreetmap.org">OpenStreetMap</a>, under <a href="http://creativecommons.org/licenses/by-sa/3.0">CC BY SA</a>.')

        folium.Choropleth(
            geo_data     = f_shape,
            name         = "map",
            data         = f_consumption,
            columns      = [COL, "Conso"],
            key_on       = f_key,
            fill_color   = "YlOrRd",
            fill_opacity = 1,
            line_opacity = 0.4,
            legend_name  = "Consumption (MWh)",
        ).add_to(m)

        return m

    
    def show_in_browser(COL):

        """ Open the map in your browser """

        map = ChoroFraBy.createMap(COL)
        webbrowser.open_new_tab('map')
