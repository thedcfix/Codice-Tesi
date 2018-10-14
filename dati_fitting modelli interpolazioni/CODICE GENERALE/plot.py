import matplotlib.pyplot as plt
import pandas as pd
import shapefile as shp

df = pd.read_csv('result.csv',sep=';', decimal='.')
sf = shp.Reader("Codice-Tesi//shapefile//Regione_polygon.shp")

X = df["UTM_Est"]
Y = df["UTM_Nord"]
#Y = df["Utm_Nord"]
Z = df["Valore"]

plt.figure()

for shape in sf.shapeRecords():
	x = [i[0] for i in shape.shape.points[:]]
	y = [i[1] for i in shape.shape.points[:]]
	
	plt.plot(x,y)

for i in range(len(X)):
	# plt.scatter(X,Y,edgecolors='none', marker='^')
	plt.scatter(X[i], Y[i], color='gold', marker='^')

#plt.title('Temperature stations')
#plt.ylabel('UTM32N_NORTH')
#plt.xlabel('UTM32N_EAST')
plt.axis('off')
#plt.xticks([])
#plt.yticks([])
plt.savefig("Stazioni ", dpi=300)
plt.show()


#colori:
# temperatura: coral
# umidità: darkturquoise
# ozono: mediumvioletred
# ossidi di azoto: forestgreen
# biossido di azoto: chocolate
# monossido di carbonio: 
# PM10: y
# Benzene: royalblue
# PM25: r
