import pandas as pd

total = pd.read_csv('DCIS_POPRES1_07092018121116059.csv',sep=',', decimal='.')

provinces = ['Varese', 'Como', 'Sondrio', 'Milano', 'Bergamo', 'Brescia', 'Pavia', 'Cremona', 'Mantova', 'Lecco', 'Lodi', 'Monza e della Brianza']
out = pd.DataFrame(columns=['Territorio', 'Sesso', 'TIME', 'Value'])

for province in provinces:
	# filtro i dati sulla provincia
	data = total.loc[total['Territorio'] == province]
	# filtro i dati sulla popolazione totale
	data = data.loc[data['Stato civile'] == 'totale']
	main = data

	for year in range (2014, 2018 + 1):
		data = main
		# filtro sull'anno
		data = data.loc[data['TIME'] == year]
		# filtro i dati totali
		data = data.loc[data['ETA1'] == 'TOTAL']

		to_keep = ['Territorio', 'Sesso', 'TIME', 'Value']
		data = data[to_keep]
		
		frames = [out, data]
		out = pd.concat(frames)

out.to_csv("DATI_PROVINCE.csv", sep=',', decimal='.', header=True, index=False)
print(out)