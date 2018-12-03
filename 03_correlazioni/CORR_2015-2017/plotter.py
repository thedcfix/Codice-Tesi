import matplotlib.pyplot as plt
import pandas as pd
import sys

nome = 'CORR_'+str(sys.argv[1])

data = pd.read_csv(nome+'.csv',sep=';', decimal=',')

data = data[["COUNT", "Valore"]]
print(data.head(5))

plt.figure()
plt.rc('grid', linestyle="dashed")
plt.rc('axes', axisbelow=True)
plt.scatter(data.Valore, data.COUNT, color='royalblue', marker='o')
plt.grid()
if str(sys.argv[1]) == 'TEMPERATURE':
	plt.xlabel("Temperatura [°C]")
elif str(sys.argv[1]) == 'HUMIDITY':
	plt.xlabel("Umidità relativa [%]")
elif str(sys.argv[1]) == 'CO':
	plt.xlabel(str(' '.join(sys.argv[2:]))+" [mg/m^3]")
else:
	plt.xlabel(str(' '.join(sys.argv[2:]))+" [µg/m^3]")
	
plt.ylabel("Numero di ictus")

plt.savefig(nome, dpi=300)
plt.show()