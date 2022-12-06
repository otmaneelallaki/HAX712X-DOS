Examples of maps
================

Here an application of the ConsumptionBy and ChoroFraBy classes:

The extracts from the tables produced by ConsumptionBy:
-------------------------------------------------------
::

    >>> from Project.Map import ConsumptionBy as cb
    >>> import pandas as pd
    >>> import numpy as np
    
    >>> df_dep = cb.getDataFast('DEP')
    >>> df_reg = cb.getDataFast('REG')
    >>> print(df_dep)
    >>> print(df_reg)
    

Choropleth Map
--------------
::

    >>> from Project.Map import ChoFraBy as cfb
    
    >>> import numpy as np
    >>> import pandas as pd
    >>> import geopandas as gpd
    >>> import folium
    >>> import webbrowser
    >>> from ConsumptionBy import ConsumptionBy
    
    >>> Map = cfb.createMap('Dep', 'fast')
    >>> print(Map)

    
