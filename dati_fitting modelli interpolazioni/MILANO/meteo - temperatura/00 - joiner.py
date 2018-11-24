import pandas as pd

temp_data_stations = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')
temp_data = pd.read_csv('DATI_2016.csv',sep=',', decimal='.')

temp_data_stations = temp_data_stations[temp_data_stations['DataStop'].isnull()]
temp_data_stations = temp_data_stations.loc[temp_data_stations['Tipologia'] ==  'Temperatura']

temp_data = temp_data.loc[temp_data['DATE_TIME'] == '2016-08-06 16:50:00']

join = pd.merge(temp_data_stations, temp_data, how='left', left_on=['IdSensore'], right_on=['IdSensore'])
join = join.sort_values(by=['IdSensore','DATE_TIME'])

join = join[~join['DATE_TIME'].isnull()]

print(join.head(10))
print(join.tail(10))

join.to_csv("result.csv", sep=';')