import pandas as pd

data1 = pd.read_csv('15.csv',sep=';', decimal=',')
data2 = pd.read_csv('16.csv',sep=';', decimal=',')
data3 = pd.read_csv('17.csv',sep=';', decimal=',')

frames = [data1, data2, data3]
data = pd.concat(frames)

data.to_csv("TOT.csv", sep=';', decimal=',', header=True, index=False)