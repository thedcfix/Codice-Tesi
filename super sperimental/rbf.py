import numpy as np
from sklearn.gaussian_process import GaussianProcess
import pandas as pd
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

print("Loading data for 2016")
data = pd.read_csv('DATI_2016.csv',sep=',', decimal='.')
stations = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')

# filtering on stations that are currently active and measure temperature
print("Filtering stations...")
stations = stations[stations['DataStop'].isnull()]
stations = stations.loc[stations['Tipologia'] ==  'Temperatura']

# joining the data to add stations' locations to every record
merged = pd.merge(data, stations, how='inner', on=['IdSensore', 'IdSensore'])

merged["DATE_TIME"] = pd.to_datetime(merged.DATE_TIME)

data = merged.loc[(merged['DATE_TIME'] == "2016-12-27 12:30:00")]

w = data.Quota.values
x = data.UTM_Est.values
y = data.UTM_Nord.values
z = data.Valore.values

XY = [list(t) for t in zip(x, y, w)]

gp = GaussianProcess( theta0=0.1, thetaL=.001, thetaU=1., nugget=0.0001)

gp.fit(XY, z)

predicted = gp.predict([[516154, 5043934, 150]])
print(predicted)

predicted = gp.predict([[563407, 5023034, 71]])
print(predicted)

# predicted = gp.predict([[657154, 4993934]])
# print(predicted)

# predicted = gp.predict([[566154, 5083934]])
# print(predicted)

# predicted = gp.predict([[562154, 5113934]])
# print(predicted)

# predicted = gp.predict([[605154, 5143934]])
print(predicted)

predicted = gp.predict([[589154, 5153934, 2307]])
print(predicted)