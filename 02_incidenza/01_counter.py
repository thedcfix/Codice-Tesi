import pandas as pd

year = 2017

print("Data for year", year)

data = pd.read_csv('tabella.csv',sep=',', decimal='.')
data = data.loc[data.CD_PROVINCE.isin(['BG', 'BS', 'CO', 'CR', 'LC', 'LO', 'MB', 'MI', 'MN', 'PV', 'SO', 'VA'])]

data = data.loc[data.ANNO == year]

data = data.groupby(['CD_PROVINCE', 'AC_SESSO']).count()

to_keep = ['AAT']
data = data[to_keep]

print(data)