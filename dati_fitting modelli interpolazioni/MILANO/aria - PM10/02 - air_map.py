import numpy as np
import pykrige.kriging_tools as kt
from pykrige.rk import OrdinaryKriging
from pykrige.uk import UniversalKriging
import pandas as pd

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.patches as mpatches

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import shapefile as shp
sf = shp.Reader("L090102_ComuneMilano.shp")

# reading the data
data = pd.read_csv('result.csv',sep=';', decimal='.')
col_list = ["UTM_Est_x", "Utm_Nord_x", "Valore"]

rr = data
#leave one out
#non = "Milano v.Feltre"
non = ""
#data = data.loc[data.NomeStazione != non]

#selezione colonne
data = np.array(data[col_list])

X0, X1 = data[:,0].min(), data[:,0].max()
Y0, Y1 = data[:,1].min(), data[:,1].max()

# # milano
X0 = 502500
X1 = 522400
Y0 = 5025000
Y1 = 5044000

NUM = 400.0

gridx = np.arange(X0, X1, (X1-X0)/NUM)
gridy = np.arange(Y0, Y1, (Y1-Y0)/NUM)

OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='spherical', verbose=False, enable_plotting=False)
z, ss = OK.execute('grid', gridx, gridy)

print("AVG sigma:", np.average(ss), "\nMAX sigma:", np.max(ss), "\nMIN sigma:", np.min(ss), "\nMEDIAN sigma:", np.median(ss), "\n75° percentile sigma:", 
		np.percentile(ss, 75), "\n90° percentile sigma:", np.percentile(ss, 90), "\n95° percentile sigma:", np.percentile(ss, 95), "\n99° percentile sigma:", np.percentile(ss, 99))

extent = (X0,X1,Y0,Y1)
im = plt.imshow(z, cmap='Wistia', aspect='auto', extent=extent, origin="lower")
plt.colorbar(im)

from scipy.ndimage import imread
im = imread('Maschera_Milano.png', mode='RGBA')
plt.imshow(im, extent=extent)

for shape in sf.shapeRecords():
	x = [i[0] for i in shape.shape.points[:]]
	y = [i[1] for i in shape.shape.points[:]]
	
	plt.plot(x,y)

data = rr
delta = []
dev = []
import math

print("\n\n--- Delta PM10 rispetto alle misurazioni delle centraline ---\n\n")
for staz in ["Milano - P.zza Zavattari", "Milano - P.zza Abbiategrasso", "Milano - Parco Lambro", "Milano - Pascal Città Studi", "Milano - Verziere", "Milano - via Juvara", "Milano - via Senato", "Milano - viale Liguria", "Milano - viale Marche"]:
	if len(data.loc[data.NomeStazione_x == staz]["Valore"]) == 1:
		val = float(data.loc[data.NomeStazione_x == staz]["Valore"])
		res, sigma = OK.execute('grid', float(data.loc[data.NomeStazione_x == staz]["UTM_Est_x"]), float(data.loc[data.NomeStazione_x == staz]["Utm_Nord_x"]))
		res = res[0][0]
		dev_std = math.sqrt(abs(sigma[0][0]))
		#if staz != non:
		plt.scatter(float(data.loc[data.NomeStazione_x == staz]["UTM_Est_x"]), float(data.loc[data.NomeStazione_x == staz]["Utm_Nord_x"]), color='red', marker='o')
		dev.append(dev_std)
		delta.append(res-val)
		print("Centralina di "+staz+"\nVal. letto:", val, "\tVal. interpolato:", res, "\tDelta:", res-val, "\tDev_std:", dev_std)
		
print("\n\nAVG delta:", np.mean(delta), "\nAVG STD_DEV:", np.mean(dev))


#plt.axis('off')
plt.title('PM10 [µg/m^3]')
plt.xlabel('Longitudine [UTM32N_Est]')
plt.xticks([502500,507600, 513700, 519100,522400])
plt.ylabel('Latitudine [UTM32N_Nord]')
plt.savefig("Mappa_PM10.png", dpi=300)
plt.show()