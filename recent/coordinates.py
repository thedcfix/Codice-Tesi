from pyproj import Proj, transform
import pandas as pd
import datetime
from datetime import timedelta
import time

def changeCoordinates(row):
        inProj = Proj('+init=EPSG:3003')
        outProj = Proj('+init=EPSG:32632')
        x1,y1 = row["VL_GEO_X"],row["VL_GEO_Y"]
        x2,y2 = transform(inProj,outProj,x1,y1)
        row["UTM32N_Est"] = x2
        row["UTM32N_Nord"] = y2
        return row
		
def changeCoordinates(row, db):
        inProj = Proj('+init=EPSG:3003')
        outProj = Proj('+init=EPSG:32632')
        x1,y1 = row["VL_GEO_X"],row["VL_GEO_Y"]
        x2,y2 = transform(inProj,outProj,x1,y1)
        row["UTM32N_Est"] = x2
        row["UTM32N_Nord"] = y2
        return row

# reading the data
start = time.time()

print("Loading data...")
data = pd.read_csv('tabella.csv',sep=';', decimal='.')

# removing null coordinates
data = data[~data['VL_GEO_X'].isnull()]
data = data[~data['VL_GEO_Y'].isnull()]

col_list = ["DT_EMERG_DAY", "DT_EMRG_OPEN_HH24MI", "VL_GEO_X", "VL_GEO_Y"]

selection = data[col_list]

#converting coordinates
interval = time.time()
print("Converting coordinates...")
selection = selection.apply(changeCoordinates, axis=1)
# dropping useless columns
selection.drop("VL_GEO_X", axis=1, inplace=True)
selection.drop("VL_GEO_Y", axis=1, inplace=True)
end = time.time()
print("The process took ", end - interval, " seconds")

# changing date format to match the stations' one: date-time
print("Changing dates format...")
selection["DATE_TIME"] = pd.to_datetime(selection.DT_EMERG_DAY, format='%d/%m/%Y') + pd.to_timedelta(selection.DT_EMRG_OPEN_HH24MI+":00")
selection["DATE_TIME"] = pd.to_datetime(selection["DATE_TIME"].dt.strftime('%Y/%m/%d %H:%M'))
# dropping useless columns
selection.drop("DT_EMERG_DAY", axis=1, inplace=True)
selection.drop("DT_EMRG_OPEN_HH24MI", axis=1, inplace=True)

# rounding to the previous 10-minutes interval
print("Rounding times to the previous 10 minutes...")
selection["DATE_TIME"] = selection["DATE_TIME"].apply(lambda dt: datetime.datetime(dt.year, dt.month, dt.day, dt.hour, 10*(dt.minute // 10)))

# generating the dates for the previous N_DAYS collecting samples every N_HOURS
print("Generating precedent lag periods...")

N_DAYS = 3
N_HOURS = 24

for i in range(int(24 * N_DAYS / N_HOURS)):
	hour = N_HOURS * (i+1)
	selection[str(hour) + "_H_DATE"] = selection["DATE_TIME"] + timedelta(hours=-hour)

print("Loading DBmeteo...")
db_meteo = pd.read_csv('DB_meteo.csv',sep=',', decimal='.')

# generating temperature values for each coordinates pair
selection = selection.apply(interpolateTemperature, db=db_meteo, axis=1)

print(selection)


end = time.time()
print("Creation completed. The process took ", end - start, " seconds")


# 

# selection.to_csv("tabella_con_coordinate.csv", sep=';', decimal='.', header=True, index=False)