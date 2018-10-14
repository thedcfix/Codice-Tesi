import pandas as pd
from datetime import timedelta

for year in range (2015, 2018 + 1):
	# carico i dati dell'anno X
	print("\nLoading data for year", year)
	data = pd.read_csv("DATI_ARIA_" + str(year) + '.csv',sep=',', decimal='.')
	stations = pd.read_csv('Stazioni_qualit__dell_aria.csv',sep=',', decimal='.')
	
	if year != 2018:
		# carico il dataset dell'anno precedente per poter includere il 31 dicembre
		data_prev = pd.read_csv("DATI_ARIA_" + str(year+1) + '.csv',sep=',', decimal='.')
		
		data_prev["DATE_TIME"] = pd.to_datetime(data_prev["DATE_TIME"])
		data_prev["DATE_TIME"] = data_prev["DATE_TIME"] + timedelta(hours=-24)
		
		data_prev = data_prev.loc[data_prev["DATE_TIME"].dt.year == year]
		
		print("Merging data for previous year...")
		# joining the data to add stations' locations to every record
		merged = pd.merge(data_prev, stations, how='inner', on=['IdSensore', 'IdSensore'])
		merged = merged[merged["NomeTipoSensore"].isin(["PM10 (SM2005)", "Particelle sospese PM2.5", "Benzene"])]
		
		data_prev = merged
		# keeping only the last day of the year
		data_prev = data_prev.loc[data_prev["DATE_TIME"] == str(year)+"-12-31"]
	
	print("Merging data...")
	# joining the data to add stations' locations to every record
	merged = pd.merge(data, stations, how='inner', on=['IdSensore', 'IdSensore'])
	merged = merged[merged["NomeTipoSensore"].isin(["PM10 (SM2005)", "Particelle sospese PM2.5", "Benzene"])]
	merged["DATE_TIME"] = pd.to_datetime(merged["DATE_TIME"])

	# scalo di un giorno perchè i dati si riferiscono alla media del giorno precedente
	merged["DATE_TIME"] = merged["DATE_TIME"] + timedelta(hours=-24)
	
	if year != 2018:
		frames = [merged, data_prev]
		result = pd.concat(frames)
	else:
		result = merged
	
	print(result["DATE_TIME"].head(20))
	print(result["DATE_TIME"].tail(20))

	result.to_csv("INQUINANTI_GIORNALIERI_" + str(year) + ".csv", sep=',', decimal='.', header=True, index=False)