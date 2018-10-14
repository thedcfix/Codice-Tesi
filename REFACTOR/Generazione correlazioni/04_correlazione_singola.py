import pandas as pd
from datetime import timedelta
import sys
import numpy
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr

ictus = pd.read_csv("DATA_zz.csv", sep=';', decimal=',')
temp = pd.read_csv("DATA_NO2.csv", sep=';', decimal=',')

a = ictus["COUNT"].values
b = temp["Valore"].values

mat = numpy.corrcoef(a,b)[0,1]

print(mat)

# R e p val
print(pearsonr(a,b))