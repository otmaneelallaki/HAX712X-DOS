Examples of ClassModel
======================

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
    >>> df.tail(5)
                            Consommation (MW)  Gaz (MW)  Nucléaire (MW)
        Time                                                            
        2022-12-06 17:45:00            70553.0    8359.0         36545.0
        2022-12-06 18:00:00            71257.0    8350.0         36543.0
        2022-12-06 18:15:00            71685.0    8229.0         36522.0
        2022-12-06 18:30:00            72746.0    8248.0         36495.0
        2022-12-06 18:45:00            72746.0    8318.0         36491.0

Calling the Dos class and creating featurs by calling the *createFeatures()* 
method, setting 0 as parametres to mention to Electricity Consommation, 1 for Gaz and 2 for Nuclear

::
    >>> Model = md.Dos(df, 0, 2022, 12, 8)  
    >>> Featurs = Model.createFeatures()
    >>> Featurs.head(4)

                            Consommation (MW)  Gaz (MW)  Nucléaire (MW)  minute  ...  dayofmonth     lag1     lag2     lag3
        Time                                                                      ...                                       
        2022-12-06 18:00:00            71257.0    8350.0         36543.0       0  ...           6  76880.0  47161.0  64641.0
        2022-12-06 18:15:00            71685.0    8229.0         36522.0      15  ...           6  77336.0  48289.0  65521.0
        2022-12-06 18:30:00            72746.0    8248.0         36495.0      30  ...           6  77792.0  48745.0  66010.0
        2022-12-06 18:45:00            72746.0    8318.0         36491.0      45  ...           6  78373.5  49813.0  66808.0

        [4 rows x 12 columns]
Fiting the model by calling the class *fitModel()* and prediction of 8 decembre 
::
    >>> reg = Model.fitModel()
    >>> dayPred, date = Model.DayPred(reg)
    >>> dayPred  
                     Date  Heure  Consommation (MW)
        0  2022-12-08  00:00       63028.617188
        1  2022-12-08  00:15       62377.496094
        2  2022-12-08  00:30       60382.480469
        3  2022-12-08  00:45       59399.277344
        4  2022-12-08  01:00       58877.019531
Last thing is to call Plot method by using this command.

::
    >>> Model.plot(dayPred,date)

.. figure:: ./Figure_1.pdf
   :height: 350
   :width: 700
   :scale: 95
   :align: center
   :class: with-shadow
   :alt: Chart