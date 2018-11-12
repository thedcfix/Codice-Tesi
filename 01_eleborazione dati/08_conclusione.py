import pandas as pd
from datetime import timedelta
import sys

for year in range(2015, 2018):
	print("\nLoading data for year", year)
	tabella = pd.read_csv('tabella_completa_' + str(year) + '.csv',sep=',', decimal='.')
	dati = pd.read_csv('GOAL_' + str(year) + '.csv',sep=',', decimal='.')

	data = pd.merge(tabella, dati, how='inner', left_on=['IDX', 'DATE_TIME', 'UTM32N_Nord', 'UTM32N_Est'], right_on=['IDX', 'DATE_TIME', 'UTM32N_Nord', 'UTM32N_Est'])
	print("Saving...")
	data.to_csv('CONCLUSIONE_' + str(year) + '.csv', sep=';', decimal=',', header=True, index=False)