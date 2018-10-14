import pandas as pd
from datetime import timedelta
import sys

VAR = str(sys.argv[1])

year = 2015

print("\nLoading data")
# tabella = pd.read_csv('tabella_completa_' + str(year) + '.csv',sep=',', decimal='.')
# dati = pd.read_csv('GOAL_' + str(year) + '.csv',sep=',', decimal='.')

# data = pd.merge(tabella, dati, how='inner', left_on='IDX', right_on='IDX')

data = pd.read_csv('CONCLUSIONE_' + str(year) + '.csv', sep=';', decimal=',')

delta = 12

for day in range(1, 5 + 1):
	if day == 1:
		time = VAR
	else:
		time = VAR + "_" + str(24 * (day - 1)) + "H"
	
	
	# delta nei giorni precedenti
	data["DELTA_" + VAR + "_" + str(day-1) + str(day) + "D"] = data[VAR + "_" + str(24 * day) + "H"] - data[time]
	
	# 12H meno ictus + 24H - 12H suddiviso in H1 e H2 rispettivamente
	data["DELTA_" + VAR + "_" + str(12) + "_H1_D" + str(day-1) + str(day)] = data[VAR + "_" + str(delta) + "H"] - data[time]
	time = VAR + "_" + str(12 * day) + "H"
	data["DELTA_" + VAR + "_" + str(12) + "_H2_D" + str(day-1) + str(day)] = data[VAR + "_" + str(24 * day) + "H"] - data[time]
	
	delta += 24

data.to_csv('CONCLUSIONE_' + str(year) + '.csv', sep=';', decimal=',', header=True, index=False)