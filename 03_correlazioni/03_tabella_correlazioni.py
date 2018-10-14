import pandas as pd
from datetime import timedelta
import sys
import numpy
import matplotlib.pyplot as plt

ictus = pd.read_csv("OUT.csv", sep=';', decimal=',')
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