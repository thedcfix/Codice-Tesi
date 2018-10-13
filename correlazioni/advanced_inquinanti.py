import pandas as pd
from datetime import timedelta
from scipy.ndimage.interpolation import shift
import numpy as np

year = 2015
inquinante = "Particelle sospese PM2.5"
citta = "Como"
giornaliero = True
nome = "PM25"

print("\nLoading data")
st = pd.read_csv('Stazioni_qualit__dell_aria.csv',sep=',', decimal='.')
data = pd.read_csv('DATI_ARIA_' + str(year) + '.csv',sep=',', decimal='.')

print("\nMerging...")
data = pd.merge(st, data, how='inner', on=['IdSensore', 'IdSensore'])

print("\nFiltering...")
data = data.loc[data.NomeTipoSensore == inquinante]
data = data.loc[data.Comune == citta]

data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

data["DAY"] = data.DATE_TIME.dt.day
data["MONTH"] = data.DATE_TIME.dt.month
data["YEAR"] = data.DATE_TIME.dt.year
data["DATE_TIME"] = data['DATE_TIME'].dt.strftime('%d/%m/%Y')
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

data = data.loc[data.DATE_TIME.dt.year == year]

#--
data = data.groupby(['YEAR', 'MONTH', 'DAY'])["Valore"].mean()

new = pd.date_range(start='1/1/'+str(year), end='31/12/'+str(year))
new = pd.DataFrame({'DATES': new, 'YEAR': new.year, 'MONTH': new.month, 'DAY': new.day})

data.to_csv("TEMP.csv", sep=';', decimal=',', header=True, index=True)

join = pd.read_csv('TEMP.csv',sep=';', decimal=',')
data = pd.merge(new, join, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
to_keep = ["DAY", "MONTH", "YEAR", "Valore"]
data = data[to_keep]

data.to_csv("DATA_"+str(nome)+".csv", sep=';', decimal=',', header=True, index=False)

if giornaliero == True:
	print("\nProcessing daily data...")
	# per inquinanti giornalieri
	#--
	st2 = pd.read_csv('Stazioni_qualit__dell_aria.csv',sep=',', decimal='.')
	dati = pd.read_csv('DATI_ARIA_'+str(year+1)+'.csv',sep=',', decimal='.')
	dati = pd.merge(st2, dati, how='inner', on=['IdSensore', 'IdSensore'])
	#--

	dati = dati.loc[dati.NomeTipoSensore == inquinante]
	dati = dati.loc[dati.Comune == citta]

	dati["DATE_TIME"] = pd.to_datetime(dati["DATE_TIME"])

	dati["DAY"] = dati.DATE_TIME.dt.day
	dati["MONTH"] = dati.DATE_TIME.dt.month
	dati["YEAR"] = dati.DATE_TIME.dt.year
	dati["DATE_TIME"] = dati['DATE_TIME'].dt.strftime('%d/%m/%Y')
	dati["DATE_TIME"] = pd.to_datetime(dati["DATE_TIME"])

	dati = dati.loc[dati.DATE_TIME.dt.year == year + 1]
	# il primo giorno dell'anno dopo ha la media inquinanti del giorno prima
	dati = dati.loc[dati.MONTH == 1]
	dati = dati.loc[dati.DAY == 1]
	dati = dati.groupby(['YEAR', 'MONTH', 'DAY'])["Valore"].mean()

	arr = data["Valore"].shift(-1)
	arr[364] = dati.values[0]
	data["Valore"] = pd.Series(arr)

	data.to_csv("DATA_"+str(nome)+".csv", sep=';', decimal=',', header=True, index=False)