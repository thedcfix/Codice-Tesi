import matplotlib.pyplot as plt
import pandas as pd
import shapefile as shp
from pyproj import Proj, transform

df = pd.read_csv('result.csv',sep=';', decimal='.')
sf = shp.Reader("Regione_polygon.shp")

X = df["UTM_Est"]
Y = df["UTM_Nord"]
#Y = df["Utm_Nord"]
Z = df["Valore"]

citta = [("Milano",45.4773,9.1815), ("Monza",45.5834,9.2759), ("Bergamo",45.6989,9.67), ("Brescia",45.5257,10.2283), ("Como",45.8109,9.0885), ("Cremona",45.1371,10.029), 
		("Lecco",45.8566,9.4039), ("Lodi",45.3145,9.5039), ("Mantova",45.153,10.7748), ("Pavia",45.1854,9.1625), ("Sondrio",46.1699,9.8702), ("Varese",45.83,8.823)]

plt.figure()

for shape in sf.shapeRecords():
	x = [i[0] for i in shape.shape.points[:]]
	y = [i[1] for i in shape.shape.points[:]]
	
	plt.plot(x,y)

for i in range(len(X)):
	# plt.scatter(X,Y,edgecolors='none', marker='^')
	plt.scatter(X[i], Y[i], color='royalblue', marker='^')
	
for city in citta:
	inProj = Proj('+init=EPSG:4326')
	outProj_UTM32N = Proj('+init=EPSG:32632')
	
	x1,y1 = city[2],city[1]
	x2,y2 = transform(inProj,outProj_UTM32N,x1,y1)
	plt.scatter(x2, y2, color='red', marker='o')

#plt.title('Temperature stations')
#plt.ylabel('UTM32N_NORTH')
#plt.xlabel('UTM32N_EAST')
plt.axis('off')
#plt.xticks([])
#plt.yticks([])
plt.savefig("Stazioni ", dpi=300)
plt.show()

print("Numero stazioni:", len(X))

#colori:
# temperatura: coral
# umidità: darkturquoise
# ozono: mediumvioletred
# ossidi di azoto: forestgreen
# biossido di azoto: chocolate
# monossido di carbonio: mediumpurple
# PM10: y
# Benzene: royalblue
# PM25: r
