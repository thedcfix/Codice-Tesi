import numpy as np
import pandas as pd
import pykrige.kriging_tools as kt
from pykrige.rk import OrdinaryKriging


# reading the data
data = pd.read_csv('result.csv',sep=';', decimal='.')
col_list = ["UTM_Est", "UTM_Nord", "Valore"]

z = data[col_list]
data = np.array(data[col_list])

# Create the ordinary kriging object. Required inputs are the X-coordinates of
# the data points, the Y-coordinates of the data points, and the Z-values of the
# data points. If no variogram model is specified, defaults to a linear variogram
# model. If no variogram model parameters are specified, then the code automatically
# calculates the parameters by fitting the variogram model to the binned
# experimental semivariogram. The verbose kwarg controls code talk-back, and
# the enable_plotting kwarg controls the display of the semivariogram.
OK = OrdinaryKriging(data[:, 0], data[:, 1], data[:, 2], variogram_model='spherical',
                     verbose=False, enable_plotting=False)

# Creates the kriged grid and the variance grid. Allows for kriging on a rectangular
# grid of points, on a masked rectangular grid of points, or with arbitrary points.
# (See OrdinaryKriging.__doc__ for more information.)
z, ss = OK.execute('grid', 648005.0, 5083600.0)

print(z)
print(ss)