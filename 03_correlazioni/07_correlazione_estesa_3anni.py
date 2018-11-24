import pandas as pd
data = pd.read_csv('CORR_PM10.csv',sep=';', decimal=',')

step = 5
base = 0
top = 150
current = base

dict = {}
current = base

while True:
	if current == top:
		break

	out = data.query(str(current) + ' < V0 < ' + str(current + step))
	tot = out.COUNT.sum()
	current += step
	dict[current + step/2] = tot
	#print("Range:", current-1, current, tot, out)
	
print(dict)
out = pd.DataFrame(list(dict.items()), columns=['BIN', 'COUNT'])
out.to_csv("OUT__.csv", sep=';', decimal=',', header=True, index=False)