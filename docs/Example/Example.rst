Examples
========

Here an example of how we cloud use the Dos's package:

The Impodtation of the Package:
------------------------------- 
::

    >>> from Project.Prediction import ClassModel as md
    >>> from Project.Prediction import DataCollection as dc
    >>> import pandas as pd

Load the data 
-------------
::

    >>> df = dc.Data()
    >>> df = df.impo() # data from 2019-01-01 00:00:00 to 2022-11-14 23:45:00
    >>> df.head(10)
                        Time  Consommation (MW)  Gaz (MW)  Nucléaire (MW)
        0  2019-01-01 00:00:00            64207.0    3430.0         55577.0
        1  2019-01-01 00:15:00            63684.5    3229.5         55894.0
        2  2019-01-01 00:30:00            63162.0    3029.0         56211.0
        3  2019-01-01 00:45:00            62042.5    2943.5         55625.0
        4  2019-01-01 01:00:00            60923.0    2858.0         55039.0
        5  2019-01-01 01:15:00            60826.0    2862.0         55154.0
        6  2019-01-01 01:30:00            60729.0    2866.0         55269.0
        7  2019-01-01 01:45:00            60428.0    2845.5         55109.5
        8  2019-01-01 02:00:00            60127.0    2825.0         54950.0
        9  2019-01-01 02:15:00            59786.5    2828.5         54998.5

set **Time** as index:

::

    >>> df.set_index("Time", inplace = True)
    >>> df.index = pd.to_datetime(df.index)
    >>> df.head(5)
                            Consommation (MW)  Gaz (MW)  Nucléaire (MW)
        Time                                                            
        2019-01-01 00:00:00            64207.0    3430.0         55577.0
        2019-01-01 00:15:00            63684.5    3229.5         55894.0
        2019-01-01 00:30:00            63162.0    3029.0         56211.0
        2019-01-01 00:45:00            62042.5    2943.5         55625.0
        2019-01-01 01:00:00            60923.0    2858.0         55039.0