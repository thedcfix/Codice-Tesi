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
sf = shp.Reader("Regione_polygon.shp")

# reading the data
data = pd.read_csv('result.csv',sep=';', decimal='.')
col_list = ["UTM_Est", "Utm_Nord", "Valore"]

z = data[col_list]
data = np.array(data[col_list])

X0, X1 = data[:,0].min(), data[:,0].max()
Y0, Y1 = data[:,1].min(), data[:,1].max()

# tutta allargata
X0 = 450000
X1 = 700000
Y0 = 4930000
Y1 = 5180000

# zone utili
# X0 = 463000
# X1 = 666000
# Y0 = 4950000
# Y1 = 5150000

# area hinterland
# X0 = 497000
# X1 = 536000
# Y0 = 5025000
# Y1 = 5060000

# # milano
# X0 = 506766
# X1 = 520915
# Y0 = 5033341
# Y1 = 5041470

NUM = 400.0

gridx = np.arange(X0, X1, (X1-X0)/NUM)
gridy = np.arange(Y0, Y1, (Y1-Y0)/NUM)

# Create the ordinary kriging object. Required inputs are the X-coordinates of
# the data points, the Y-coordinates of the data points, and the Z-values of the
# data points. If no variogram model is specified, defaults to a linear variogram
# model. If no variogram model parameters are specified, then the code automatically
# calculates the parameters by fitting the variogram model to the binned
# experimental semivariogram. The verbose kwarg controls code talk-back, and
# the enable_plotting kwarg controls the display of the semivariogram.
OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='spherical', verbose=False, enable_plotting=False)
#OK = UniversalKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='linear',
#					  drift_terms=['regional_linear'])
# Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
# grid of points, on a masked rectangular grid of points, or with arbitrary points.
# (See OrdinaryKriging.__doc__ for more information.)
z, ss = OK.execute('grid', gridx, gridy)

print("AVG sigma:", np.average(ss), "\nMAX sigma:", np.max(ss), "\nMIN sigma:", np.min(ss), "\nMEDIAN sigma:", np.median(ss), "\n75° percentile sigma:", 
		np.percentile(ss, 75), "\n90° percentile sigma:", np.percentile(ss, 90), "\n95° percentile sigma:", np.percentile(ss, 95), "\n99° percentile sigma:", np.percentile(ss, 99))

#colors = ["sandybrown" for x in range(int(NUM))]
#plt.hist(ss, bins=np.arange(ss.min(), ss.max()), color=colors)

extent = (X0,X1,Y0,Y1)
im = plt.imshow(z, cmap='inferno', aspect='auto', extent=extent, origin="lower") # pl is pylab imported a pl
plt.colorbar(im)

from scipy.ndimage import imread
im = imread('Maschera.png', mode='RGBA')
plt.imshow(im, extent=extent)

for shape in sf.shapeRecords():
	x = [i[0] for i in shape.shape.points[:]]
	y = [i[1] for i in shape.shape.points[:]]
	
	plt.plot(x,y)

#plt.axis('off')
plt.title('Biossido di azoto [µg/m^3]')
plt.xlabel('Longitudine [UTM32N_Est]')
plt.ylabel('Latitudine [UTM32N_Nord]')
plt.savefig("Mappa_biossido_azoto.png", dpi=300)
plt.show()

# Writes the kriged grid to an ASCII grid file.
#kt.write_asc_grid(gridx, gridy, z, filename="output.asc")