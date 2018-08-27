import matplotlib.pyplot as plt
import pandas as pd
import shapefile as shp

df = pd.read_csv('result.csv',sep=';', decimal='.')
sf = shp.Reader("Regione_polygon.shp")

X = df["UTM_Est"]
Y = df["UTM_Nord"]
Z = df["Valore"]

plt.figure()

for shape in sf.shapeRecords():
    x = [i[0] for i in shape.shape.points[:]]
    y = [i[1] for i in shape.shape.points[:]]
	
    plt.plot(x,y)


plt.scatter(X,Y,edgecolors='none',c=Z, cmap='jet')
plt.colorbar()
plt.show()