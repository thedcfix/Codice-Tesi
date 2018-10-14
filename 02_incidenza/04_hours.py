import time
import numpy as np
import pandas as pd

# reading the data about strokes
start = time.time()
print("Loading data...")
data = pd.read_csv('tabella.csv',sep=',', decimal='.')
data["DATE_TIME"] = pd.to_datetime(data["DATE_TIME"])

# removing data for 2018, which are incomplete for the whole year
data = data.loc[data["DATE_TIME"].dt.year < 2018]

hours = data.groupby("ID_EMERG_HOUR_IN_DAY").size()

print("Saving...")
hours.to_csv("hours.csv", sep=';', decimal='.', header=False, index=True)