import pandas as pd
from datetime import timedelta
import sys
import numpy
import matplotlib.pyplot as plt


d1 = pd.read_csv('DATA_DIREZIONE VENTO.csv', sep=';', decimal=',')
d2 = pd.read_csv('DATA_RADIAZIONE GLOBALE.csv', sep=';', decimal=',')
d3 = pd.read_csv('DATA_TEMPERATURA.csv', sep=';', decimal=',')
d4 = pd.read_csv('DATA_UMIDITA.csv', sep=';', decimal=',')
d5 = pd.read_csv('DATA_VELOCITA VENTO.csv', sep=';', decimal=',')

d6 = pd.read_csv('DATA_AMMONIACA.csv', sep=';', decimal=',')
d6 = d6.rename(columns={'Valore': 'Ammoniaca'})
d7 = pd.read_csv('DATA_BENZENE.csv', sep=';', decimal=',')
d7 = d7.rename(columns={'Valore': 'Benzene'})
d8 = pd.read_csv('DATA_CO.csv', sep=';', decimal=',')
d8 = d8.rename(columns={'Valore': 'Monossido di Carbonio'})
d9 = pd.read_csv('DATA_NO2.csv', sep=';', decimal=',')
d9 = d9.rename(columns={'Valore': 'Biossido di Azoto'})
d10 = pd.read_csv('DATA_NOx.csv', sep=';', decimal=',')
d10 = d10.rename(columns={'Valore': 'Ossidi di Azoto'})
d11 = pd.read_csv('DATA_O3.csv', sep=';', decimal=',')
d11 = d11.rename(columns={'Valore': 'Ozono'})
d12 = pd.read_csv('DATA_PM10.csv', sep=';', decimal=',')
d12 = d12.rename(columns={'Valore': 'PM10'})
d13 = pd.read_csv('DATA_PM25.csv', sep=';', decimal=',')
d13 = d13.rename(columns={'Valore': 'PM2.5'})
d14 = pd.read_csv('DATA_SO2.csv', sep=';', decimal=',')
d14 = d14.rename(columns={'Valore': 'Biossido di Zolfo'})

d15 = pd.read_csv('DATA_zz.csv', sep=';', decimal=',')

# --
d15["Direzione Vento"] = d1
d15["Radiazione Globale"] = d2
d15["Temperatura"] = d3
d15["Umidita Relativa"] = d4
d15["Velocita Vento"] = d5

data = pd.merge(d15, d6, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])

data = pd.merge(data, d7, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
data = pd.merge(data, d8, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
data = pd.merge(data, d9, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
data = pd.merge(data, d10, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
data = pd.merge(data, d11, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
data = pd.merge(data, d12, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
data = pd.merge(data, d13, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])
data = pd.merge(data, d14, how='left', left_on=['YEAR', 'MONTH', 'DAY'], right_on=['YEAR', 'MONTH', 'DAY'])

data.drop("DAY", axis=1, inplace=True)
data.drop("MONTH", axis=1, inplace=True)
data.drop("YEAR", axis=1, inplace=True)

data.to_csv("YYY.csv", sep=';', decimal=',', header=True, index=False)