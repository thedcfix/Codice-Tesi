import pandas as pd
import time

N_DAYS = 5
N_HOURS = 12

for year in range (2015, 2018 + 1):
	print("Loading data for year", year)
	df = pd.read_csv("FINAL_" + str(year) + '.csv',sep=',', decimal='.')

	# filters are used to keep reasonable values
	# in some cases, when coordinates are fare from the closest station, the exponential model can lead to extremely high/low values. Those measures are cut
	df = df[df['TEMPERATURE'].between(-20, 40, inclusive=True)]
	
	# humidity % ranges between 0 and 100
	df = df[df['HUMIDITY'].between(0, 100, inclusive=True)]
	
	# other measures do not suffer for such problems
	
	# filter on existance
	df.dropna(inplace=True)
	
	# filter for lags
	for i in range(int(24 * N_DAYS / N_HOURS)):
		# generating the datetime every N_HOURS hours, up to N_DAYS before the stroke event
		hour = N_HOURS * (i+1)
		
		
		# filters are used to keep reasonable values
		# in some cases, when coordinates are fare from the closest station, the exponential model can lead to extremely high/low values. Those measures are cut
		df = df[df['TEMPERATURE' + '_' + str(hour) + 'H'].between(-20, 40, inclusive=True)]
		
		# humidity % ranges between 0 and 100
		df = df[df['HUMIDITY' + '_' + str(hour) + 'H'].between(0, 100, inclusive=True)]
		
		# other measures do not suffer for such problems
		
		# filter on existance
		df.dropna(inplace=True)
		
	df.to_csv("GOAL_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)
	print("=============================================\n")