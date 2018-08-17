import pandas as pd
import time
import numpy as np
import pandas as pd
import pykrige.kriging_tools as kt
from pykrige.rk import OrdinaryKriging
from pykrige.rk import UniversalKriging
import multiprocessing as mp

def interpolate(year):
	start = time.time()
	print("Loading data for year:", year)
	data = pd.read_csv('common_' + str(year) + '.csv',sep=',', decimal='.')
	stations = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')

	# filtering on stations that are currently active and measure temperature
	print("Filtering stations...")
	stations = stations[stations['DataStop'].isnull()]
	stations = stations.loc[stations['Tipologia'] ==  'Temperatura']

	# keeping only the useful fields
	to_keep = ["IdSensore", "UTM_Nord", "UTM_Est"]
	stations = stations[to_keep]

	# joining the data to add stations' locations to every record
	merged = pd.merge(data, stations, how='inner', on=['IdSensore', 'IdSensore'])

	# grouping by date and coordinates of the stroke event. In this way I retrieve a group contaning all the sensor reads, for all the stations, for every stroke (ca 189 values, i.e.
	# the number of stations in Lombardy, for every stroke. Then I use the coordinates of those stations and the read values to generate an interpolation for the value at the location
	# of the stroke. Every interpolation uses all data available data in Lombardy to increase precision.
	group = merged.groupby(['DATE_TIME','UTM32N_Est','UTM32N_Nord'])

	date = []
	x = []
	y = []
	temp = []

	print("Interpolating values...")

	for key, item in group:
		df = group.get_group(key)
		date.append(key[0])
		x.append(key[1])
		y.append(key[2])
		
		# if the location coincides with one of the weather stations, a singular matrix is generated. Being not invertible, the algorithm cannot invert it to generate the weights
		# if such an error occurs, I add the fake value -999.0 to the list of temperatures and then I cut the entire record to keep only the valid ones
		try:
			OK = UniversalKriging(df["UTM_Est"], df["UTM_Nord"], df["Valore"], variogram_model='linear', drift_terms=['regional_linear'], verbose=False, enable_plotting=False)
			z = OK.execute('grid', float(key[1]), float(key[2]))
			temp.append(round(float(z[0][0][0]), 1))
		except Exception:
			temp.append(-999.0)
		
	out = pd.DataFrame({'DATE': date, 'UTM_EST': x, 'UTM_NORD': y, 'TEMPERATURE':temp})

	print("# of stations used for the interpolation:", len(df["UTM_Est"]))
	print("# of records analyzed:", len(temp))

	print("Saving...")
	out.to_csv("complete_temperature" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)

	end = time.time()
	print("The process took ", end - start, " seconds")
	print(out.head(20))

if __name__ == '__main__':
	# reading the data
	start = time.time()

	pool = mp.Pool(processes=1)
	pool.map(interpolate, range(2015, 2018 + 1))
	
	end = time.time()
	print("Operation completed. The process took ", end - start, " seconds")