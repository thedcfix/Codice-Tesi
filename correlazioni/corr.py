import pandas as pd
from datetime import timedelta
import sys
import numpy
import matplotlib.pyplot as plt

ictus = pd.read_csv("DATA_zz.csv", sep=';', decimal=',')
temp = pd.read_csv("DATA_TEMP_zz.csv", sep=';', decimal=',')
oz = pd.read_csv("DATA_OZ_zz.csv", sep=';', decimal=',')

a = ictus["COUNT"].values
b = temp["Valore"].values
c = oz["Valore"].values

# mat = numpy.corrcoef(a,c)[0,1]

# print(mat)

# from scipy.stats.stats import pearsonr

# # R e p val
# print(pearsonr(a,c))

ictus = pd.read_csv("OOO.csv", sep=';', decimal=',')
print(ictus.corr())

yea = ictus.corr()

fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(yea,cmap='coolwarm', vmin=-1, vmax=1)
fig.colorbar(cax)
ticks = numpy.arange(0,len(ictus.columns),1)
ax.set_xticks(ticks)
plt.xticks(rotation=90)
ax.set_yticks(ticks)
ax.set_xticklabels(ictus.columns)
ax.set_yticklabels(ictus.columns)
plt.show()