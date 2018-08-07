import pandas as pd

print("Loading data...")
tabella = pd.read_csv('Tabella ictus completa.csv',sep=';', decimal=',')

# removing null coordinates
tabella = tabella[~tabella['VL_GEO_X'].isnull()]
tabella = tabella[~tabella['VL_GEO_Y'].isnull()]

# parsing date-time and rounding to the closest 10 minutes interval
print("Adjusting dates...")
tabella["DATE_TIME"] = pd.to_datetime(tabella.DT_EMERG_DAY, format='%d/%m/%Y') + pd.to_timedelta(tabella.DT_EMRG_OPEN_HH24MI+":00")
tabella["DATE_TIME"] = tabella["DATE_TIME"].dt.round('10min')

print(tabella)

print("Saving...")
tabella.to_csv("tabella.csv", sep=',', decimal='.', header=True, index=False)