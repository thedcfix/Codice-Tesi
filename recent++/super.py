from pyproj import Proj, transform
import pandas as pd
import datetime
from datetime import timedelta
import time
import pykrige.kriging_tools as kt
from pykrige.rk import OrdinaryKriging
from pykrige.rk import UniversalKriging
import numpy as np
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

def interpolate(data, measure):
	start = time.time()
	print("\nLoading weather stations...")
	stations = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')

	# filtering on stations that are currently active and measures the required measure
	print("Filtering ", measure.lower(), " stations...")
	stations = stations[stations['DataStop'].isnull()]
	stations = stations.loc[stations['Tipologia'] ==  str(measure)]

	# keeping only the useful fields
	to_keep = ["IdSensore", "UTM_Nord", "UTM_Est"]
	stations = stations[to_keep]

	# joining the data to add stations' locations to every record
	merged = pd.merge(data, stations, how='inner', on=['IdSensore', 'IdSensore'])

	# grouping by date and coordinates of the stroke event. In this way I retrieve a group contaning all the sensor reads, for all the stations, for every stroke (ca 189 values, i.e.
	# the number of stations in Lombardy, for every stroke. Then I use the coordinates of those stations and the read values to generate an interpolation for the value at the location
	# of the stroke. Every interpolation uses all data available data in Lombardy to increase precision.
	group = merged.groupby(['IDX', 'DATE_TIME', 'UTM32N_Est', 'UTM32N_Nord'])
	
	print("# of groups:", len(group))
	
	if measure == "Temperatura":
		model = 'exponential'
		print("Interpolation model:", model)
	elif measure == "Umidità Relativa":
		model='spherical'
		print("Interpolation model:", model)
	
	id = []
	value = []

	print("Interpolating values...")
	
	for key, item in group:
		df = group.get_group(key)
		
		# if the location coincides with one of the weather stations, a singular matrix is generated. Being not invertible, the algorithm cannot invert it to generate the weights
		# if such an error occurs, I add the fake value -999.0 to the list of temperatures and then I cut the entire record to keep only the valid ones
		try:
			OK = OrdinaryKriging(df["UTM_Est"], df["UTM_Nord"], df["Valore"], variogram_model=model, verbose=False, enable_plotting=False)
			z = OK.execute('grid', key[2], key[3])
			
			id.append(key[0])
			value.append(round(z[0][0][0], 1))
		except Exception:
			id.append(key[0])
			value.append(-999.0)
	
	if measure == "Temperatura":
		out = pd.DataFrame({'IDX': id, 'TEMPERATURE':value})
	elif measure == "Umidità Relativa":
		out = pd.DataFrame({'IDX': id, 'HUMIDITY':value})
	
	print("# of stations used for the interpolation:", len(df["UTM_Est"]))
	print("# of records analyzed:", len(value))
	
	end = time.time()
	print("The process took ", end - start, " seconds", "\n")
	return out

N_DAYS = 3
N_HOURS = 24

file_to_open = '_24H'

start = time.time()

for year in range (2015, 2018 + 1):
	# carico i dati dell'anno X
	print("Loading data for year", year, file_to_open)
	data = pd.read_csv("DATI_" + str(year) + '.csv',sep=',', decimal='.')
	
	print("Loading table for year", year)
	table = pd.read_csv("tabella_ridotta_" + str(year) + file_to_open + '.csv',sep=',', decimal='.')
	
	print("# of records: ", len(table))
	
	# converto le date in date time prima del join
	data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])
	table["DATE_TIME"] = pd.to_datetime(table["DATE_TIME"])
	
	# joining the sensors data with the strokes data on the basis of the date 
	print("Extracting common elements...")
	common = pd.merge(table, data, how='inner', on=['DATE_TIME', 'DATE_TIME'])
	
	common_start = interpolate(common, "Temperatura")
	table = pd.merge(table, common_start, how='left', on=['IDX', 'IDX'])
	
	common_start = interpolate(common, "Umidità Relativa")
	table = pd.merge(table, common_start, how='left', on=['IDX', 'IDX'])
	
	table.to_csv("weather_" + str(year) + file_to_open + ".csv", sep=',', decimal='.', header=True, index=False)
	print("=============================================\n")