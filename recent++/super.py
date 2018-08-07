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
		
def interpolateTemperature(row, db):
	local = db.loc[db['Data'] == row['Data']]
	print(local)

# disables a useless warning
pd.options.mode.chained_assignment = None

# reading the data
start = time.time()
print("Loading data...")
data = pd.read_csv('tabella.csv',sep=',', decimal='.')

col_list = ["DATE_TIME", "VL_GEO_X", "VL_GEO_Y"]

selection = data[col_list]

#converting coordinates
print("Converting coordinates...")
interval = time.time()
selection = selection.apply(changeCoordinates, axis=1)
# dropping useless columns
selection.drop("VL_GEO_X", axis=1, inplace=True)
selection.drop("VL_GEO_Y", axis=1, inplace=True)
end = time.time()
print("The process took ", end - interval, " seconds")

# generating the dates for the previous N_DAYS collecting samples every N_HOURS
print("Generating precedent lag periods...")

N_DAYS = 3
N_HOURS = 24

print("Loading data for year: ", 2018)
data = pd.read_csv("DATI_" + str(2018) + '.csv', sep=',', decimal='.')

selection["DATE_TIME"] = pd.to_datetime(selection["DATE_TIME"])
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

print(selection.head(20))
print(data.head(20))
print("Extracting common elements...")
common = pd.merge(selection, data, how='inner', on=['DATE_TIME', 'DATE_TIME'])
print(common.tail(250000))
common.to_csv("common_" + str(2018) + ".csv", sep=',', decimal='.', header=True, index=False)

# for i in range(int(24 * N_DAYS / N_HOURS)):
	# hour = N_HOURS * (i+1)
	# selection[str(hour) + "_H_DATE"] = selection["DATE_TIME"] + timedelta(hours=-hour)

# +1 is for accounting 2018, which by default is expluded by the rage function
# for year in range (2015, 2018 + 1):
    # print("Loading data for year: ", year)
    # data = pd.read_csv(str(year) + '.csv', sep=',', decimal='.')
    # data["Data"] = pd.to_datetime(data.Data, format='%d/%m/%Y %H:%M:%S')
    # table = selection.loc[selection["DATE_TIME"].dt.year == year]
    # print("# of records:", len(table))
    # # print("Creating index column to univocally address records...")
    # # table['INDEX'] = range(1, len(table) + 1)
    # print("Extracting common elements...")
    # #common = pd.merge(left=data, left_on='Data', right=table, right_on='DATE_TIME')
    # common = pd.merge(table, data, how='left', left_on=['DATE_TIME'], right_on=['Data'])
    # common.drop("idOperatore", axis=1, inplace=True)
    # common.drop("DATE_TIME", axis=1, inplace=True)
    # print("Saving...")
    # common.to_csv("common_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)

# end = time.time()
# print("Creation completed. The process took ", end - start, " seconds")
# print(selection.head(20))