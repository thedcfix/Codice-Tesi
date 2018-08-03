import pandas as pd
import time
import gc

# reading weather data
print("Loading data...")
start = time.time()
data_2014 = pd.read_csv('2014.csv', sep=',', decimal='.')
data_2015 = pd.read_csv('2015.csv', sep=',', decimal='.')
data_2016 = pd.read_csv('2016.csv', sep=',', decimal='.')
data_2017 = pd.read_csv('2017.csv', sep=',', decimal='.')
data_2018 = pd.read_csv('2018.csv', sep=',', decimal='.')
end = time.time()
print("The process took ", end - start, " seconds")

#reading stations' data
print("Loading stations...")
stations = pd.read_csv('Stazioni_Meteorologiche.csv', sep=',', decimal='.')

#filtering on stations that are currently active and measure temperature
print("Filtering stations...")
stations = stations[stations['DataStop'].isnull()]
stations = stations.loc[stations['Tipologia'] ==  'Temperatura']

#concatenating all the data in a single frame and dropping useless column
print("Concatenating frames...")
frames = [data_2014, data_2015, data_2016, data_2017, data_2018]
result = pd.concat(frames)
result.drop(['idOperatore'], axis=1, inplace=True)

# deleting old frames and calling garbage collector to save memory
del [[data_2014, data_2015, data_2016, data_2017, data_2018]]
gc.collect()

#getting the IDs of the filtered stations
print("Data selection...")
stations = stations['IdSensore']
result = result[result['IdSensore'].isin(stations.values)]

print("Saving...")
result.to_csv("DB_meteo.csv", sep=',', decimal='.', header=True, index=False)

end = time.time()
print("Creation completed. The process took ", end - start, " seconds")