import pandas as pd
data = pd.read_csv('CORR_PM10.csv',sep=';', decimal=',')
import time

step = 5
base = 0
top = 165
current = base

dict = {}
count = {}
current = base

while True:
	if current >= top:
		break

	out = data.query(str(current) + ' < V0 < ' + str(current + step))
	tot = out.COUNT.sum()
	cnt = out.V0.count()
	current += step
	dict[current + step/2] = tot
	count[current + step/2] = cnt
	#print("Range:", current-1, current, tot, out)
	
print(dict)
out = pd.DataFrame(list(dict.items()), columns=['BIN', 'COUNT'])
out.to_csv("OUT__.csv", sep=';', decimal=',', header=True, index=False)

cnt = pd.DataFrame(list(count.items()), columns=['BIN', 'AVG'])
cnt.to_csv("OUT__CNT.csv", sep=';', decimal=',', header=True, index=False)