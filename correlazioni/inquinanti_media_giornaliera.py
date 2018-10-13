import pandas as pd
from datetime import timedelta

print("\nLoading data")
st = pd.read_csv('Stazioni_qualit__dell_aria.csv',sep=',', decimal='.')
data = pd.read_csv('DATI_ARIA_2015.csv',sep=',', decimal='.')

print("\nMerging...")
data = pd.merge(st, data, how='inner', on=['IdSensore', 'IdSensore'])

print("\nFiltering...")
data = data.loc[data.NomeTipoSensore == "Ozono"]
data = data.loc[data.Comune == "Milano"]

data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

data["DAY"] = data.DATE_TIME.dt.day
data["MONTH"] = data.DATE_TIME.dt.month
data["YEAR"] = data.DATE_TIME.dt.year
data["DATE_TIME"] = data['DATE_TIME'].dt.strftime('%d/%m/%Y')
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])


data = data.loc[data.DATE_TIME.dt.year == 2015]

to_keep = ["YEAR", "MONTH", "DAY", "Valore"]
data = data[to_keep]

data = data.groupby(['YEAR', 'MONTH', 'DAY'])["Valore"].mean()
print(data)

data.to_csv("DATA_OZ_zz.csv", sep=';', decimal=',', header=True, index=False)