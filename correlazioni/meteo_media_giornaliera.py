import pandas as pd
from datetime import timedelta

year = 2015
fenomeno = "Precipitazione"
prov = "MI"
nome = "Precipitazione"

print("\nLoading data")
st = pd.read_csv('Stazioni_Meteorologiche.csv',sep=',', decimal='.')
data = pd.read_csv('DATI_METEO_'+str(year)+'.csv',sep=',', decimal='.')

print("\nMerging...")
data = pd.merge(st, data, how='inner', on=['IdSensore', 'IdSensore'])

print("\nFiltering...")
data = data.loc[data.Tipologia == fenomeno]
data = data.loc[data.Provincia == prov]
data = data.loc[data.IdSensore.isin(["19243", "9341", "8162", "19005", "5909", "3118", "6174", "14391", "5911", "6179", "6458", 
							"2002", "8149", "5908", "5897", "19021", "6185", "19244", "14121", "19009", "2001", "19008", 
							"5920", "19374", "14390", "6597", "2006", "19373", "8125", "19006", "2008", "19020"])]

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