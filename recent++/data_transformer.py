import pandas as pd
from multiprocessing import Process
import time

def run(year):
	print("Loading data for year:", year)
	table = pd.read_csv(str(year) + '.csv',sep=',', decimal='.')

	# removing null records
	table = table[~table['Stato'].isnull()]

	# parsing date-time and rounding to the closest 10 minutes interval
	print("Changing dates format...")
	table["DATE_TIME"] = pd.to_datetime(table.Data, format='%d/%m/%Y %H:%M:%S')

	# dropping useless columns
	table.drop("Data", axis=1, inplace=True)
	table.drop("Stato", axis=1, inplace=True)
	table.drop("idOperatore", axis=1, inplace=True)

	print(table.head(20))

	print("Saving...")
	table.to_csv("DATI_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)


if __name__ == '__main__':

	n_thread = 5
	processes = []
	year = 2014

	start = time.time()

	for p_number in range(n_thread):
		p = Process(target=run, args=(year,))
		p.start()
		processes.append(p)
		year += 1
	
	for p in processes:
		p.join()
		
	end = time.time()
	print("Creation completed. The process took ", end - start, " seconds")