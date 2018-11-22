import pandas as pd
import time
import sys

data1 = pd.read_csv('CONCLUSIONE_2015.csv',sep=';', decimal=',')
data2 = pd.read_csv('CONCLUSIONE_2016.csv',sep=';', decimal=',')
data3 = pd.read_csv('CONCLUSIONE_2017.csv',sep=';', decimal=',')

year = 2015

frames = [data1, data2, data3]
data = pd.concat(frames)
data = data.loc[data.DS_TOWN == "MILANO"]
#data = data.loc[data.ANNO == year]

data.to_csv("CONCLUSIONE.csv", sep=';', decimal=',', header=True, index=False)

# calcolo ictus e media per ogni giorno
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])
data["DAY"] = data.DATE_TIME.dt.day

numero = data.groupby(['ANNO', 'MESE', 'DAY'])["DATE_TIME"].size()
media = data.groupby(['ANNO', 'MESE', 'DAY'])[str(sys.argv[1])].mean()

data = pd.DataFrame({'EVENTI': numero, 'MEDIA '+str(sys.argv[1]): media})
data.to_csv("OUT_GIORNO.csv", sep=';', decimal=',', header=True)

print("Correlazione con", str(sys.argv[1]), "anni 2015-2017:", data["EVENTI"].corr(data['MEDIA '+str(sys.argv[1])]))
print(round(data["EVENTI"].corr(data['MEDIA '+str(sys.argv[1])]), 3))