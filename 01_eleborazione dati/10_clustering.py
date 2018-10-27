import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import Counter

print("Loading data...")
db = pd.read_csv("DATA.csv", sep=';', decimal=',')

print (db.values)
data = db.values

samples = []

print("Normalizing arrays...")
for arr in data:
	arr = arr / arr.mean()
	samples.append(arr)

print("Generating model...")
kmeans = KMeans(n_clusters=125, random_state=0).fit(np.array(samples))

print("Making predictions..")
prediction = kmeans.predict(np.array(samples))

print("Most frequent trendes:")
c = Counter(prediction)
print(c.most_common(10))

print("Adding column to dataset...")
db["CLUSTER"] = pd.Series(prediction)

print(db)
db.to_csv("DATA_CLUSTERED.csv", sep=';', decimal=',', header=True, index=False)
print("=============================================\n")