import pandas as pd
import time
import numpy as np
import pandas as pd
import pykrige.kriging_tools as kt
from pykrige.rk import OrdinaryKriging

# reading the data
start = time.time()

print("Loading data...")
data = pd.read_csv('common_2018.csv',sep=',', decimal='.')
stations = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')
#tab = pd.read_csv('tabella2.csv',sep=';', decimal='.')

# filtering on stations that are currently active and measure temperature
print("Filtering stations...")
stations = stations[stations['DataStop'].isnull()]
stations = stations.loc[stations['Tipologia'] ==  'Temperatura']


to_keep = ["IdSensore", "UTM_Nord", "UTM_Est"]
stations = stations[to_keep]

print("# of weather stations", len(stations))

merged = pd.merge(data, stations, how='inner', on=['IdSensore', 'IdSensore'])

group = merged.groupby(['DATE_TIME','UTM32N_Est','UTM32N_Nord'])

date = []
x = []
y = []
temp = []

for key, item in group:
    df = group.get_group(key)
    date.append(key[0])
    x.append(key[1])
    y.append(key[2])
    OK = OrdinaryKriging(df["UTM_Est"], df["UTM_Nord"], df["Valore"], variogram_model='linear',
                     verbose=False, enable_plotting=False)
    z, ss = OK.execute('grid', float(key[1]), float(key[2]))
    temp.append(z[0][0])
	
out = pd.DataFrame({'DATE': date, 'UTM_EST': x, 'UTM_NORD': y, 'TEMPERATURE':temp})

print(out)

end = time.time()
print("The process took ", end - start, " seconds")