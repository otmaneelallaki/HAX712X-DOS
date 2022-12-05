Examples
========

Here an application of the ConsumptionBy and ChoroFraBy classes:

The extracts from the tables produced by ConsumptionBy:
------------------------------- 
::

    >>> from Project.Map import ConsumptionBy as cb
    >>> import pandas as pd
    >>> import numpy as np
    

Load the data 
-------------
::

    >>> df_dep = cb.getDataFast('DEP')
    >>> df_reg = cb.getDataFast('REG')
    >>> print(df_dep)
    >>> print(df_reg)
