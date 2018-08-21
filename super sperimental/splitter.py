import pandas as pd
import datetime
from datetime import timedelta

# disables a useless warning
pd.options.mode.chained_assignment = None

# reading the data about strokes
print("Loading data...")
data = pd.read_csv('tabella.csv',sep=',', decimal='.')
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

col_list = ["DATE_TIME", "UTM32N_Est", "UTM32N_Nord"]
selection = data[col_list]

print(selection)

N_DAYS = 3
N_HOURS = 24

for year in range (2015, 2018 + 1):
	# salvo: tabella intera dell'anno X, tabella ridotta dell'anno X e le tabelle ridotte dei lag period
	
	print("Working on data for year:", year)
	total = data.loc[data.DATE_TIME.dt.year == year]
	reduced = selection.loc[selection.DATE_TIME.dt.year == year]
	
	total["IDX"] = total.index
	reduced["IDX"] = reduced.index
	
	print("Saving original and reduced table...") 
	total.to_csv("tabella_completa_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)
	reduced.to_csv("tabella_ridotta_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)
	
	print("Generating lag periods...")
	for i in range(int(24 * N_DAYS / N_HOURS)):
		# generating the datetime every N_HOURS hours, up to N_DAYS before the stroke event
		hour = N_HOURS * (i+1)
		lag = reduced
		
		lag["DATE_TIME"] = reduced["DATE_TIME"] + timedelta(hours=-hour)
		lag["IDX"] = lag.index
		
		lag.to_csv("tabella_ridotta_" + str(year) + "_" + str(hour) + "H.csv", sep=',', decimal='.', header=True, index=False)