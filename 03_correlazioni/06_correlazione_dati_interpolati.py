import pandas as pd
import time
import sys
import os

data1 = pd.read_csv('CONCLUSIONE_2015.csv',sep=';', decimal=',')
data2 = pd.read_csv('CONCLUSIONE_2016.csv',sep=';', decimal=',')
data3 = pd.read_csv('CONCLUSIONE_2017.csv',sep=';', decimal=',')
tab = pd.read_csv('tabella.csv',sep=',', decimal='.')

for year in range(2015, 2018):
	# leggo i file completamente analizzati degli anni 2015/2017
	frames = [data1, data2, data3]
	data = pd.concat(frames)
	data = data.loc[data.DS_TOWN == "MILANO"]
	data = data.loc[data.ANNO == year]
	
	data.to_csv("CONCLUSIONE.csv", sep=';', decimal=',', header=True, index=False)
	
	# renaming di comodo (riciclo codice)
	dati = data
	data = tab
	
	# creo la lista di quanti ictus ci sono ogni giorno, riempiendo con 0 i giorni senza eventi
	data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])
	data["DAY"] = data.DATE_TIME.dt.day
	data["DATE_TIME"] = data['DATE_TIME'].dt.strftime('%d/%m/%Y')
	data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])
	
	data = data.loc[data.DATE_TIME.dt.year == year]
	data = data.loc[data.DS_TOWN == 'MILANO']
	
	data = data.groupby(['ANNO', 'MESE', 'DAY']).count()
	
	new = pd.date_range(start='1/1/'+str(year), end='31/12/'+str(year))
	new = pd.DataFrame({'DATES': new, 'YEAR': new.year, 'MONTH': new.month, 'DAY': new.day})
	
	data.to_csv("TEMP.csv", sep=';', decimal=',', header=True, index=True)
	
	join = pd.read_csv('TEMP.csv',sep=';', decimal=',')
	data = pd.merge(new, join, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['ANNO', 'MESE', 'DAY'])
	data = data.fillna(value=0)
	data = data.rename(index=str, columns={"AAT": "COUNT"})

	to_keep = ["DAY", "MONTH", "YEAR", "COUNT"]
	data = data[to_keep]
	
	data.to_csv("TEMP.csv", sep=';', decimal=',', header=True, index=False)
	
	# inverto il renaming
	data = dati
	
	# associo le medie del fenomeno X ai giorni dell'anno
	data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

	data["DAY"] = data.DATE_TIME.dt.day
	data["MONTH"] = data.DATE_TIME.dt.month
	data["YEAR"] = data.DATE_TIME.dt.year
	data["DATE_TIME"] = data['DATE_TIME'].dt.strftime('%d/%m/%Y')
	data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

	data = data.loc[data.DATE_TIME.dt.year == year]
	
	data = data.groupby(['YEAR', 'MONTH', 'DAY'])[str(sys.argv[1])].mean()

	new = pd.date_range(start='1/1/'+str(year), end='31/12/'+str(year))
	new = pd.DataFrame({'DATES': new, 'YEAR': new.year, 'MONTH': new.month, 'DAY': new.day})

	data.to_csv("TEMP2.csv", sep=';', decimal=',', header=True, index=True)

	join = pd.read_csv('TEMP2.csv',sep=';', decimal=',')
	data = pd.merge(new, join, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
	to_keep = ["DAY", "MONTH", "YEAR", str(sys.argv[1])]
	data = data[to_keep]

	data.to_csv("TEMP2.csv", sep=';', decimal=',', header=True, index=False)
	
	one = pd.read_csv('TEMP.csv',sep=';', decimal=',')
	two = pd.read_csv('TEMP2.csv',sep=';', decimal=',')
	data = pd.merge(one, two, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
	
	os.remove("TEMP.csv")
	os.remove("TEMP2.csv")
	data.to_csv("YEA.csv", sep=';', decimal=',', header=True, index=False)
	
	data = pd.DataFrame({'EVENTI': data["COUNT"], 'MEDIA '+str(sys.argv[1]): data[sys.argv[1]]})
	data.to_csv("OUT_GIORNO.csv", sep=';', decimal=',', header=True)
	
	#print("Correlazione con", str(sys.argv[1]), "anno", year, ":", data["EVENTI"].corr(data['MEDIA '+str(sys.argv[1])]))
	print(round(data["EVENTI"].corr(data['MEDIA '+str(sys.argv[1])]), 3))