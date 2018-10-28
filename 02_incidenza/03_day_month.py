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

data["DAY_OF_WEEK"] = data["DATE_TIME"].dt.dayofweek

days = data.groupby("DAY_OF_WEEK").size()
months = data.groupby("MESE").size()
combined = data.groupby(["MESE", "DAY_OF_WEEK"]).size()

print("Saving...")
#days.to_csv("days.csv", sep=';', decimal='.', header=False, index=True)
months.to_csv("months.csv", sep=';', decimal='.', header=False, index=True)
#combined.to_csv("combined.csv", sep=';', decimal='.', header=False, index=True)