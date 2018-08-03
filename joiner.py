import pandas as pd

temp_data_stations = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')
temp_data = pd.read_csv('2018.csv',sep=',', decimal='.')

temp_data_stations = temp_data_stations[temp_data_stations['DataStop'].isnull()]
temp_data_stations = temp_data_stations.loc[temp_data_stations['Tipologia'] ==  'Temperatura']

temp_data = temp_data.loc[temp_data['Data'] == '20/07/2018 09:00:00 PM']
temp_data['Data'] = pd.to_datetime(temp_data['Data'], format='%d/%m/%Y %H:%M:%S %p')

join = pd.merge(temp_data_stations, temp_data, how='left', left_on=['IdSensore'], right_on=['IdSensore'])
join = join.sort_values(by=['IdSensore','Data'])

join = join[~join['Data'].isnull()]

print(join.head(10))
print(join.tail(10))

join.to_csv("result.csv", sep=';')