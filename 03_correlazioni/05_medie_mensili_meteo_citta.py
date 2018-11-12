import pandas as pd
from datetime import timedelta

for year in range (2015, 2018 + 1):
	# carico i dati dell'anno X
	print("\nLoading data for year", year)
	data = pd.read_csv("DATI_METEO_" + str(year) + '.csv',sep=',', decimal='.')
	stations = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')
	
	print("Merging data...")
	# joining the data to add stations' locations to every record
	merged = pd.merge(data, stations, how='inner', on=['IdSensore', 'IdSensore'])
	merged = merged[merged["Tipologia"].isin(["Umidità Relativa"])]
	merged["DATE_TIME"] = pd.to_datetime(merged["DATE_TIME"])

	# scalo di un giorno perchè i dati si riferiscono alla media del giorno precedente
	merged["DATE_TIME"] = merged["DATE_TIME"] + timedelta(hours=-24)

	result = merged
	
	result = result.loc[result.NomeStazione.isin(["Milano v.Juvara", "Milano P.zza Zavattari", "Milano v.Feltre", "Milano Niguarda", "Milano v.Brera", "Milano Lambrate", "Milano v.Marche", 
													"Milano v.Confalonieri", "Milano v.Rosellini"])]
	result["MONTH"] = result["DATE_TIME"].dt.month
	result = result.loc[result["DATE_TIME"].dt.year == year]
	
	to_keep = ["Valore", "DATE_TIME", "MONTH", "NomeStazione", "IdSensore"]
	result = result[to_keep]
	
	result = result.groupby(['MONTH']).mean()
	result = result["Valore"]

	print(result)
	
	result.to_csv("INQUINANTI_GIORNALIERI_" + str(year) + ".csv", sep=';', decimal=',', header=True, index=True)