from pyproj import Proj, transform
import pandas as pd
import datetime
from datetime import timedelta
import time
import pykrige.kriging_tools as kt
from pykrige.rk import OrdinaryKriging
from pykrige.rk import UniversalKriging

def changeCoordinates(row):
	inProj = Proj('+init=EPSG:3003')
	outProj = Proj('+init=EPSG:32632')
	x1,y1 = row["VL_GEO_X"],row["VL_GEO_Y"]
	x2,y2 = transform(inProj,outProj,x1,y1)
	row["UTM32N_Est"] = x2
	row["UTM32N_Nord"] = y2
	return row

def interpolate(data, measure):
	start = time.time()
	print("Loading weather stations...")
	stations = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')

	# filtering on stations that are currently active and measures the required measure
	print("Filtering stations...")
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
			OK = OrdinaryKriging(df["UTM_Est"], df["UTM_Nord"], df["Valore"], variogram_model='linear', verbose=False, enable_plotting=False)
			z = OK.execute('grid', key[1], key[2])
			temp.append(round(float(z[0][0][0]), 1))
		except Exception:
			temp.append(-999.0)
	
	if measure == "Temperatura":
		out = pd.DataFrame({'DATE': date, 'UTM_EST': x, 'UTM_NORD': y, 'TEMPERATURE':temp})
	elif measure == "Radiazione Globale":
		out = pd.DataFrame({'DATE': date, 'UTM_EST': x, 'UTM_NORD': y, 'RADIATION':temp})
	elif measure == "Umidità Relativa":
		out = pd.DataFrame({'DATE': date, 'UTM_EST': x, 'UTM_NORD': y, 'HUMIDITY':temp})

	print("# of stations used for the interpolation:", len(df["UTM_Est"]))
	print("# of records analyzed:", len(temp))

	# print("Saving...")
	# out.to_csv("complete_temperature" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)

	end = time.time()
	print("The process took ", end - start, " seconds")
	return out

# disables a useless warning
pd.options.mode.chained_assignment = None

# reading the data about strokes
start = time.time()
print("Loading data...")
data = pd.read_csv('tabella.csv',sep=',', decimal='.')

col_list = ["DATE_TIME", "VL_GEO_X", "VL_GEO_Y"]

selection = data[col_list]

# converting coordinates to UTM32N
print("Converting coordinates...")
interval = time.time()
selection = selection.apply(changeCoordinates, axis=1)

# dropping useless columns
selection.drop("VL_GEO_X", axis=1, inplace=True)
selection.drop("VL_GEO_Y", axis=1, inplace=True)
end = time.time()
print("The process took ", end - interval, " seconds")

N_DAYS = 3
N_HOURS = 24

selection["DATE_TIME"] = pd.to_datetime(selection["DATE_TIME"])

# generating interpolated values
# +1 is for accounting 2018, which by default is expluded by the rage function
for year in range (2015, 2018 + 1):
	# loading the data about all the sensors at all the times in the year
	print("Loading sensors data for year: ", year)
	data = pd.read_csv("DATI_" + str(year) + '.csv', sep=',', decimal='.')
	data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])
	
	# joining the sensors data with the strokes data on the basis of the date 
	print("Extracting common elements...")
	common_start = pd.merge(selection, data, how='inner', on=['DATE_TIME', 'DATE_TIME'])
	
	common = interpolate(common_start, "Temperatura")
	#common["TEMPERATURE"] = common_tmp["TEMPERATURE"]
	
	print(common)
	
	# common_tmp = interpolate(common, "Radiazione Globale")
	# common["RADIATION"] = common_tmp["RADIATION"]
	
	common_tmp = interpolate(common_start, "Umidità Relativa")
	common["HUMIDITY"] = common_tmp["HUMIDITY"]
	
	print(common)
	
	original_date = selection["DATE_TIME"]
	
	# generating lag periods
	for i in range(int(24 * N_DAYS / N_HOURS)):
		
		# generating the datetime every N_HOURS hours, up to N_DAYS before the stroke event up to
		hour = N_HOURS * (i+1)
		selection["DATE_TIME"] = selection["DATE_TIME"] + timedelta(hours=-hour)
		
		# joining the sensors data with the strokes data on the basis of the date, using a generated lag period date for the strokes data
		print("Extracting common elements...")
		common_start = pd.merge(selection, data, how='inner', on=['DATE_TIME', 'DATE_TIME'])
		
		common_tmp = interpolate(common_start, "Temperatura")
		common[str(hour) + "_TEMPERATURE"] = common_tmp["TEMPERATURE"]
		
		print(common)
		
		# common_tmp = interpolate(common_start, "Radiazione Globale")
		# common[str(hour) + "_RADIATION"] = common_tmp["RADIATION"]
		
		common_tmp = interpolate(common_start, "Umidità Relativa")
		common[str(hour) + "_HUMIDITY"] = common_tmp["HUMIDITY"]
		
		print(common)
	
	print("Saving...")
	common.to_csv("test_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)

end = time.time()
print("Creation completed. The process took ", end - start, " seconds")
print(selection.head(20))