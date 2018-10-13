import pandas as pd
from datetime import timedelta
from scipy.ndimage.interpolation import shift
import numpy as np
from multiprocessing import Pool

year = 2015
inquinante = "Particelle sospese PM2.5"
citta = "Milano"
giornaliero = True
nome = "PM25"

def meteo_execute(year, fenomeno, prov, nome):
	print("\nLoading data")
	st = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')
	data = pd.read_csv('DATI_METEO_'+str(year)+'.csv',sep=',', decimal='.')

	print("\nMerging...")
	data = pd.merge(st, data, how='inner', on=['IdSensore', 'IdSensore'])

	print("\nFiltering...")
	data = data.loc[data.Tipologia == fenomeno]
	data = data.loc[data.Provincia == prov]
	
	if prov == "MI":
		# sensori città di Milano
		sensori = ["19243", "9341", "8162", "19005", "5909", "3118", "6174", "14391", "5911", "6179", "6458", 
					"2002", "8149", "5908", "5897", "19021", "6185", "19244", "14121", "19009", "2001", "19008", 
					"5920", "19374", "14390", "6597", "2006", "19373", "8125", "19006", "2008", "19020"]
	elif prov == "CO":
		sensori = ["9311", "9308", "19066", "8382", "8165", "8166", "9310", "19065"]
	elif prov == "LC":
		sensori = ["10376", "19116", "5878", "10381", "6588", "10377", "10382", "19117"]
	elif prov == "VA":
		sensori = ["8228", "5947", "8229", "6197", "5946"]
	elif prov == "BG":
		sensori = ["6433", "19104", "11654", "2441", "5859", "11840", "5864", "19105", "5867", "6103", "6158", "5860", 
					"2435", "6431", "2433", "2434", "19099", "5990", "5866", "5857", "6160", "19098"]
	elif prov == "BS":
		sensori = ["2417", "6795", "2415", "2414", "19076", "19077", "6792", "6796"]
	
	data = data.loc[data.IdSensore.isin(sensori)]

	data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

	data["DAY"] = data.DATE_TIME.dt.day
	data["MONTH"] = data.DATE_TIME.dt.month
	data["YEAR"] = data.DATE_TIME.dt.year
	data["DATE_TIME"] = data['DATE_TIME'].dt.strftime('%d/%m/%Y')
	data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])


	data = data.loc[data.DATE_TIME.dt.year == year]

	to_keep = ["YEAR", "MONTH", "DAY", "Valore"]
	data = data[to_keep]

	data = data.groupby(['YEAR', 'MONTH', 'DAY'])["Valore"].mean()
	print(data)

	data.to_csv("DATA_"+str(nome)+".csv", sep=';', decimal=',', header=True, index=False)

def execute(year, inquinante, citta, giornaliero, nome):
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
		print(nome, dati)
		arr = data["Valore"].shift(-1)
		arr[364] = dati.values[0]
		data["Valore"] = pd.Series(arr)

		data.to_csv("DATA_"+str(nome)+".csv", sep=';', decimal=',', header=True, index=False)
		
# main

year = 2015
citta = "Lecco"
prov = "LC"
# per cambiare città serve inserire i codici delle stazioni meteo di quella città nella funzione meteo

if __name__ == '__main__':
	with Pool(9) as p:
		if citta in ["Milano"]:
			p.starmap(execute, [(year, "Monossido di Carbonio", citta, False, "CO"), (year, "Biossido di Azoto", citta, False, "NO2"),
									(year, "Ossidi di Azoto", citta, False, "NOx"), (year, "Ozono", citta, False, "O3"), (year, "Biossido di Zolfo", citta, False, "SO2"), 
									(year, "Ammoniaca", citta, True, "AMMONIACA"), (year, "Benzene", citta, True, "BENZENE"), (year, "PM10 (SM2005)", citta, True, "PM10"), 
									(year, "Particelle sospese PM2.5", citta, True, "PM25")])
		elif citta in ["Bergamo", "Varese"]:
			p.starmap(execute, [(year, "Monossido di Carbonio", citta, False, "CO"), (year, "Biossido di Azoto", citta, False, "NO2"),
									(year, "Ossidi di Azoto", citta, False, "NOx"), (year, "Ozono", citta, False, "O3"), (year, "Biossido di Zolfo", citta, False, "SO2"), 
									(year, "PM10 (SM2005)", citta, True, "PM10"), (year, "Particelle sospese PM2.5", citta, True, "PM25")])
		elif citta in ["Como", "Lecco"]:
			p.starmap(execute, [(year, "Monossido di Carbonio", citta, False, "CO"), (year, "Biossido di Azoto", citta, False, "NO2"),
									(year, "Ossidi di Azoto", citta, False, "NOx"), (year, "Ozono", citta, False, "O3"), (year, "Biossido di Zolfo", citta, False, "SO2"), 
									(year, "Benzene", citta, True, "BENZENE"), (year, "PM10 (SM2005)", citta, True, "PM10"), 
									(year, "Particelle sospese PM2.5", citta, True, "PM25")])
	
	with Pool(1) as p:
		if citta in ["Milano", "Bergamo", "Lecco"]:
			p.starmap(meteo_execute, [(year, "Direzione Vento", prov, "DIREZIONE VENTO"), (year, "Radiazione Globale", prov, "RADIAZIONE GLOBALE"), (year, "Temperatura", prov, "TEMPERATURA"), 
									(year, "Umidità Relativa", prov, "UMIDITA"), (year, "Velocità Vento", prov, "VELOCITA VENTO")])
		elif citta in ["Como"]:
			p.starmap(meteo_execute, [(year, "Direzione Vento", prov, "DIREZIONE VENTO"), (year, "Temperatura", prov, "TEMPERATURA"), 
									(year, "Umidità Relativa", prov, "UMIDITA"), (year, "Velocità Vento", prov, "VELOCITA VENTO")])
		elif citta in ["Varese"]:
			p.starmap(meteo_execute, [(year, "Temperatura", prov, "TEMPERATURA"), (year, "Umidità Relativa", prov, "UMIDITA")])
							
	d1 = pd.read_csv('DATA_DIREZIONE VENTO.csv', sep=';', decimal=',')
	d2 = pd.read_csv('DATA_RADIAZIONE GLOBALE.csv', sep=';', decimal=',')
	d3 = pd.read_csv('DATA_TEMPERATURA.csv', sep=';', decimal=',')
	d4 = pd.read_csv('DATA_UMIDITA.csv', sep=';', decimal=',')
	d5 = pd.read_csv('DATA_VELOCITA VENTO.csv', sep=';', decimal=',')

	d6 = pd.read_csv('DATA_AMMONIACA.csv', sep=';', decimal=',')
	d6 = d6.rename(columns={'Valore': 'Ammoniaca'})
	d7 = pd.read_csv('DATA_BENZENE.csv', sep=';', decimal=',')
	d7 = d7.rename(columns={'Valore': 'Benzene'})
	d8 = pd.read_csv('DATA_CO.csv', sep=';', decimal=',')
	d8 = d8.rename(columns={'Valore': 'Monossido di Carbonio'})
	d9 = pd.read_csv('DATA_NO2.csv', sep=';', decimal=',')
	d9 = d9.rename(columns={'Valore': 'Biossido di Azoto'})
	d10 = pd.read_csv('DATA_NOx.csv', sep=';', decimal=',')
	d10 = d10.rename(columns={'Valore': 'Ossidi di Azoto'})
	d11 = pd.read_csv('DATA_O3.csv', sep=';', decimal=',')
	d11 = d11.rename(columns={'Valore': 'Ozono'})
	d12 = pd.read_csv('DATA_PM10.csv', sep=';', decimal=',')
	d12 = d12.rename(columns={'Valore': 'PM10'})
	d13 = pd.read_csv('DATA_PM25.csv', sep=';', decimal=',')
	d13 = d13.rename(columns={'Valore': 'PM2.5'})
	d14 = pd.read_csv('DATA_SO2.csv', sep=';', decimal=',')
	d14 = d14.rename(columns={'Valore': 'Biossido di Zolfo'})

	d15 = pd.read_csv('DATA_zz.csv', sep=';', decimal=',')

	# --
	if citta not in ["Varese"]:
		d15["Direzione Vento"] = d1
	if citta in ["Milano", "Bergamo", "Varese"]:
		d15["Radiazione Globale"] = d2
	d15["Temperatura"] = d3
	d15["Umidita Relativa"] = d4
	if citta not in ["Varese"]:
		d15["Velocita Vento"] = d5
	
	# a Como mancano le rilevazioni di ammoniaca
	if citta in ["Milano"]:
		data = pd.merge(d15, d6, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])

		data = pd.merge(data, d7, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
		data = pd.merge(data, d8, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
	elif citta in ["Como", "Lecco"]:
		data = pd.merge(d15, d7, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
		data = pd.merge(data, d8, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
		
	# a Bergamo mancano benzene e ammoniaca
	elif citta in ["Bergamo", "Varese"]:
		data = pd.merge(d15, d8, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
	
	
	data = pd.merge(data, d9, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
	data = pd.merge(data, d10, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
	data = pd.merge(data, d11, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
	data = pd.merge(data, d12, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
	data = pd.merge(data, d13, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
	data = pd.merge(data, d14, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])

	data.drop("DAY", axis=1, inplace=True)
	data.drop("MONTH", axis=1, inplace=True)
	data.drop("YEAR", axis=1, inplace=True)

	data.to_csv("YYY.csv", sep=';', decimal=',', header=True, index=False)