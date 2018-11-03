import pandas as pd
import time
import sys

data = pd.read_csv('CONCLUSIONE_2015.csv',sep=';', decimal=',')
data = data.loc[data.DS_TOWN == "MILANO"]
data.to_csv("CONCLUSIONE_2015.csv", sep=';', decimal=',', header=True, index=False)

# calcolo ictus e media per ogni giorno
data["DATE_TIME_x"] = pd.to_datetime(data["DATE_TIME_x"])
data["DAY"] = data.DATE_TIME_x.dt.day

src = data

numero = data.groupby(['ANNO', 'MESE', 'DAY'])["DATE_TIME_x"].size()
media = data.groupby(['ANNO', 'MESE', 'DAY'])[str(sys.argv[1])].mean()

data = pd.DataFrame({'EVENTI': numero, 'MEDIA '+str(sys.argv[1]): media})
data.to_csv("OUT_GIORNO.csv", sep=';', decimal=',', header=True)

# calcolo ictus e media per specifico datetime
# data = src
# numero = data.groupby(["DATE_TIME_x"]).size()
# media = data.groupby(["DATE_TIME_x"])[str(sys.argv[1])].mean()

# data = pd.DataFrame({'EVENTI': numero, 'MEDIA '+str(sys.argv[1]): media})
# data.to_csv("OUT_TIMESTAMP.csv", sep=';', decimal=',', header=True)