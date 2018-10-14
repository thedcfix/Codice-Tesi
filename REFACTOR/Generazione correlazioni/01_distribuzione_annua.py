import pandas as pd
from datetime import timedelta
import os

print("\nLoading data")
data = pd.read_csv('tabella.csv',sep=',', decimal='.')
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])
data["DAY"] = data.DATE_TIME.dt.day
data["DATE_TIME"] = data['DATE_TIME'].dt.strftime('%d/%m/%Y')
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])


data = data.loc[data.DATE_TIME.dt.year == 2015]
data = data.loc[data.DS_TOWN == 'MILANO']

data = data.groupby(['ANNO', 'MESE', 'DAY']).count()

new = pd.date_range(start='1/1/2015', end='31/12/2015')
new = pd.DataFrame({'DATES': new, 'YEAR': new.year, 'MONTH': new.month, 'DAY': new.day})

data.to_csv("TEMP.csv", sep=';', decimal=',', header=True, index=True)

join = pd.read_csv('TEMP.csv',sep=';', decimal=',')
print(join)
data = pd.merge(new, join, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['ANNO', 'MESE', 'DAY'])
data = data.fillna(value=0)
data = data.rename(index=str, columns={"AAT": "COUNT"})

to_keep = ["DAY", "MONTH", "YEAR", "COUNT"]
data = data[to_keep]

data.to_csv("DATA_zz.csv", sep=';', decimal=',', header=True, index=False)
os.remove("TEMP.csv")