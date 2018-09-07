import pandas as pd

data = pd.read_csv('tabella.csv',sep=',', decimal='.')
data = data.loc[data.CD_PROVINCE.isin(['BG', 'BS', 'CO', 'CR', 'LC', 'LO', 'MB', 'MI', 'MN', 'PV', 'SO', 'VA'])]

data = data.loc[data.ANNO == 2017]

data = data.groupby(['CD_PROVINCE']).count()

to_keep = ['AAT']
data = data[to_keep]

print(data)