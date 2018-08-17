import pandas as pd
from multiprocessing import Process
import time
import multiprocessing as mp
from datetime import timedelta

def run(year):
	print("Loading data for year:", year)
	table = pd.read_csv(str(year) + '.csv',sep=',', decimal='.')
	# loading the last 6 days of the previous year
	table_prev = pd.read_csv(str(year - 1) + '.csv',sep=',', decimal='.')

	# removing null records
	table = table[~table['Stato'].isnull()]
	table_prev = table_prev[~table_prev['Stato'].isnull()]

	# parsing date-time and rounding to the closest 10 minutes interval
	print("Changing dates format...")
	table["DATE_TIME"] = pd.to_datetime(table.Data, format='%d/%m/%Y %H:%M:%S')
	table_prev["DATE_TIME"] = pd.to_datetime(table_prev.Data, format='%d/%m/%Y %H:%M:%S')

	# dropping useless columns
	table.drop("Data", axis=1, inplace=True)
	table.drop("Stato", axis=1, inplace=True)
	table.drop("idOperatore", axis=1, inplace=True)
	
	table_prev.drop("Data", axis=1, inplace=True)
	table_prev.drop("Stato", axis=1, inplace=True)
	table_prev.drop("idOperatore", axis=1, inplace=True)
	
	# selecting just the last 6 days
	print("Selecting data for the last 6 days of the previous year...")
	table_prev = table_prev.loc[table_prev['DATE_TIME'] > str(year - 1) + '-12-26']
	
	print("Concatenating frames...")
	frames = [table_prev, table]
	table = pd.concat(frames)

	print(table.head(20), "\n\n", table.tail(20))

	print("Saving...")
	table.to_csv("DATI_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)


if __name__ == '__main__':

	n_years = 4
	processes = []
	year = 2015

	start = time.time()
	
	# the process is memory intensive so the data are processed sequentially
	for i in range(n_years):
		p = Process(target=run, args=(year + i,))
		p.start()
		p.join()
		
		end = time.time()
		print("The process took ", str(timedelta(seconds=(end-start))))
	
	end = time.time()
	print("Creation completed. The process took ", str(timedelta(seconds=(end-start))))