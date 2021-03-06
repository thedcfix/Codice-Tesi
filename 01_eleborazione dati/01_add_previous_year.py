import pandas as pd
from multiprocessing import Process
import time
import multiprocessing as mp
from datetime import timedelta

def run(year, type):
	print("\nLoading", type, "data for year:", year)
	# loading the current year and the previuos year. The previous year is used to extract the last 6 days used to gather measures for lag periods
	table = pd.read_csv(str(year) + "_" + type + '.csv',sep=',', decimal='.')
	table_prev = pd.read_csv(str(year - 1) + "_" + type + '.csv',sep=',', decimal='.')

	# removing null records
	table = table[~table['Stato'].isnull()]
	table_prev = table_prev[~table_prev['Stato'].isnull()]
	
	# parsing date-time and rounding to the closest 10 minutes interval
	print("Changing dates format...")
	# data about air have a different format for 2018 =(
	if type == "ARIA" and year == 2018:
		table["DATE_TIME"] = pd.to_datetime(table.Data, format='%d/%m/%Y %I:%M:%S %p')
	else:
		table["DATE_TIME"] = pd.to_datetime(table.Data, format='%d/%m/%Y %H:%M:%S')
		
	table_prev["DATE_TIME"] = pd.to_datetime(table_prev.Data, format='%d/%m/%Y %H:%M:%S')

	# dropping useless columns
	table.drop("Data", axis=1, inplace=True)
	table.drop("Stato", axis=1, inplace=True)
	table.drop("idOperatore", axis=1, inplace=True)
	
	table_prev.drop("Data", axis=1, inplace=True)
	table_prev.drop("Stato", axis=1, inplace=True)
	table_prev.drop("idOperatore", axis=1, inplace=True)
	
	# selecting just the last 6 days for the previous year
	print("Selecting data for the last 6 days of the previous year...")
	table_prev = table_prev.loc[table_prev['DATE_TIME'] >= str(year - 1) + '-12-26 00:00:00']
	
	print("Concatenating frames...")
	frames = [table_prev, table]
	table = pd.concat(frames)

	print(table.head(20), "\n\n", table.tail(20))

	print("Saving...")
	table.to_csv("DATI_" + type + "_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)


if __name__ == '__main__':

	n_years = 4
	processes = []
	year = 2015

	start = time.time()
	
	# the process is memory intensive so the data are processed sequentially
	# first weather data
	for i in range(n_years):
		p = Process(target=run, args=(year + i, 'METEO',))
		p.start()
		p.join()
		
		end = time.time()
		print("The process took ", str(timedelta(seconds=(end-start))))
	
	# then pollution data
	for i in range(n_years):
		p = Process(target=run, args=(year + i, 'ARIA',))
		p.start()
		p.join()
		
		end = time.time()
		print("The process took ", str(timedelta(seconds=(end-start))))
	
	end = time.time()
	print("Creation completed. The process took ", str(timedelta(seconds=(end-start))))