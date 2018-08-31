import pandas as pd
import time

N_DAYS = 3
N_HOURS = 24

file_to_open = ''

start = time.time()

for year in range (2015, 2018 + 1):
	# carico i dati dell'anno X
	print("Loading data for year", year, file_to_open)
	weather = pd.read_csv("weather_" + str(year) + '.csv',sep=',', decimal='.')
	pollutants = pd.read_csv("pollutants_" + str(year) + '.csv',sep=',', decimal='.')
	pollutants_daily = pd.read_csv("pollutants_daily_" + str(year) + '.csv',sep=',', decimal='.')
	
	pollutants = pollutants.drop(['DATE_TIME', 'UTM32N_Est', 'UTM32N_Nord', 'ALTITUDE'], axis=1)
	pollutants_daily = pollutants_daily.drop(['DATE_TIME', 'UTM32N_Est', 'UTM32N_Nord', 'ALTITUDE'], axis=1)
	
	# joining the sensors data with the strokes data on the basis of the date 
	print("Joining elements...")
	common = pd.merge(weather, pollutants, how='inner', on=['IDX', 'IDX'])
	common = pd.merge(common, pollutants_daily, how='inner', on=['IDX', 'IDX'])
	
	# merging lag periods
	for i in range(int(24 * N_DAYS / N_HOURS)):
		# generating the datetime every N_HOURS hours, up to N_DAYS before the stroke event
		hour = N_HOURS * (i+1)
		print("Loading gap period for hour", hour)
		weather = pd.read_csv("weather_" + str(year) + "_" + str(hour) + 'H.csv',sep=',', decimal='.')
		pollutants = pd.read_csv("pollutants_" + str(year) + "_" + str(hour) + 'H.csv',sep=',', decimal='.')
		pollutants_daily = pd.read_csv("pollutants_daily_" + str(year) + "_" + str(hour) + 'H.csv',sep=',', decimal='.')
		
		weather = weather.drop(['DATE_TIME', 'UTM32N_Est', 'UTM32N_Nord', 'ALTITUDE'], axis=1)
		pollutants = pollutants.drop(['DATE_TIME', 'UTM32N_Est', 'UTM32N_Nord', 'ALTITUDE'], axis=1)
		pollutants_daily = pollutants_daily.drop(['DATE_TIME', 'UTM32N_Est', 'UTM32N_Nord', 'ALTITUDE'], axis=1)
		
		weather = weather.rename(index=str, columns={"TEMPERATURE": "TEMPERATURE_" + str(hour) + "H", "HUMIDITY": "HUMIDITY_" + str(hour) + "H"})
		pollutants = pollutants.rename(index=str, columns={"CO": "CO_" + str(hour) + "H", "O3": "O3" + str(hour) + "H", "NOx": "NOx_" + str(hour) + "H", "NO2": "NO2_" + str(hour) + "H"})
		pollutants_daily = pollutants_daily.rename(index=str, columns={"PM10": "PM10_" + str(hour) + "H", "PM25": "PM25_" + str(hour) + "H", "BENZENE": "BENZENE_" + str(hour) + "H"})
		
		# joining the sensors data with the strokes data on the basis of the date 
		print("Joining elements...")
		common = pd.merge(common, weather, how='inner', on=['IDX', 'IDX'])
		common = pd.merge(common, pollutants, how='inner', on=['IDX', 'IDX'])
		common = pd.merge(common, pollutants_daily, how='inner', on=['IDX', 'IDX'])
	
	common.to_csv("FINAL_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)
	print("=============================================\n")