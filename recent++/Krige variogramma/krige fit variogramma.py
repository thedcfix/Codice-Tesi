import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.patches as mpatches

def SVh( P, h, bw ):
    '''
    Experimental semivariogram for a single lag
    '''
    pd = squareform( pdist( P[:,:2] ) )
    N = pd.shape[0]
    Z = list()
    for i in range(N):
        for j in range(i+1,N):
            if( pd[i,j] >= h-bw )and( pd[i,j] <= h+bw ):
                Z.append( ( P[i,2] - P[j,2] )**2.0 )
    return np.sum( Z ) / ( 2.0 * len( Z ) )
 
def SV( P, hs, bw ):
    '''
    Experimental variogram for a collection of lags
    '''
    sv = list()
    for h in hs:
        sv.append( SVh( P, h, bw ) )
    sv = [ [ hs[i], sv[i] ] for i in range( len( hs ) ) if sv[i] > 0 ]
    return np.array( sv ).T
 
def C( P, h, bw ):
    '''
    Calculate the sill
    '''
    c0 = np.var( P[:,2] )
    if h == 0:
        return c0
    return c0 - SVh( P, h, bw )
	
def spherical( h, a, C0 ):
    '''
    Spherical model of the semivariogram
    '''
    # if h is a single digit
    if type(h) == np.float64:
        # calculate the spherical function
        if h <= a:
            return C0*( 1.5*h/a - 0.5*(h/a)**3.0 )
        else:
            return C0
    # if h is an iterable
    else:
        # calcualte the spherical function for all elements
        a = np.ones( h.size ) * a
        C0 = np.ones( h.size ) * C0
        return list(map( spherical, h, a, C0 ))
		
def exponential( h, a, c ):
    '''
    Exponential model of the semivariogram
    '''
    a, c = float( a ), float( c )
    return c*( 1.0 - np.exp( -h/a ) )
	
def gaussian( h, a, c ):
    '''
    Gaussian model of the semivariogram
    '''
    a, c = float( a ), float( c )
    return c*( 1.0 - np.exp( -h**2.0/a**2.0 ) )

def opt( fct, x, y, C0, parameterRange=None, meshSize=1000 ):
    if parameterRange == None:
        parameterRange = [ x[1], x[-1] ]
    mse = np.zeros( meshSize )
    a = np.linspace( parameterRange[0], parameterRange[1], meshSize )
    for i in range( meshSize ):
        mse[i] = np.mean( ( y - fct( x, a[i], C0 ) )**2.0 )
    return a[ mse.argmin() ]
	
def cvmodel( P, model, hs, bw ):
    '''
    Input:  (P)      ndarray, data
            (model)  modeling function
                      - spherical
                      - exponential
                      - gaussian
            (hs)     distances
            (bw)     bandwidth
    Output: (covfct) function modeling the covariance
    '''
    # calculate the semivariogram
    sv = SV( P, hs, bw )
	# calculate the nugget
    nugget = sv[1][0] - 0
    # calculate the sill
    C0 = C( P, hs[0], bw )# + nugget
    # calculate the optimal parameters
    param = opt( model, sv[0], sv[1], C0 )
    # return a covariance function
    covfct = lambda h, a=param: model( h, a, C0 )
    return covfct
	
def krige( P, model, hs, bw, u, N ):
    '''
    Input  (P)     ndarray, data
           (model) modeling function
                    - spherical
                    - exponential
                    - gaussian
           (hs)    kriging distances
           (bw)    kriging bandwidth
           (u)     unsampled point
           (N)     number of neighboring
                   points to consider
    '''
 
    # covariance function
    covfct = cvmodel( P, model, hs, bw )
    # mean of the variable
    mu = np.mean( P[:,2] )
 
    # distance between u and each data point in P
    d = np.sqrt( ( P[:,0]-u[0] )**2.0 + ( P[:,1]-u[1] )**2.0 )
    # add these distances to P
    P = np.vstack(( P.T, d )).T
    # sort P by these distances
    # take the first N of them
    P = P[d.argsort()[:N]]
 
    # apply the covariance model to the distances
    k = covfct( P[:,3] )
    # cast as a matrix
    k = np.matrix( k ).T
 
    # form a matrix of distances between existing data points
    K = squareform( pdist( P[:,:2] ) )
    # apply the covariance model to these distances
    K = covfct( K.ravel() )
    # re-cast as a NumPy array -- thanks M.L.
    K = np.array( K )
    # reshape into an array
    K = K.reshape(N,N)
    # cast as a matrix
    K = np.matrix( K )
 
    # calculate the kriging weights
    weights = np.linalg.inv( K ) * k
    weights = np.array( weights )
 
    # calculate the residuals
    residuals = P[:,2] - mu
 
    # calculate the estimation
    estimation = np.dot( weights.T, residuals ) + mu
 
    return float( estimation )
	
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

DISTANCE_KM = 100
LAG_M = 1000

# reading the data
data = pd.read_csv('result.csv',sep=';', decimal='.')
col_list = ["UTM_Est", "UTM_Nord", "Valore"]

data = np.array(data[col_list])

# bandwidth, plus or minus 500 meters
bw = LAG_M

# lags in 1000 meter increments from zero to 14Km
hs = np.arange(0,DISTANCE_KM * 1000, LAG_M)
sv = SV( data, hs, bw )



plt.plot( sv[0], sv[1], '.-' )
plt.xlabel('Lag [Km]')
plt.ylabel('Semivariance')
plt.title('Sample Semivariogram') ;
plt.savefig('sample_semivariogram.png',fmt='png',dpi=200)

# range_value = 0.95 * sv[1][-1]
# nugget = sv[1][0] - 0

# print(nugget)

# for value in range(len(sv[1])):
	# if sv[1][value] >= range_value:
		# range = sv[0][value]
		# break

# print(range)

# model fitting
sp = cvmodel(data, model=spherical, hs=np.arange(0,DISTANCE_KM * 1000, LAG_M), bw=LAG_M)

plt.plot( sv[0], sv[1], '.-' )
plt.plot( sv[0], sp(sv[0])) ;
plt.title('Exponential Model')
plt.ylabel('Semivariance')
plt.xlabel('Lag [m]')
plt.savefig('semivariogram_model.png',fmt='png',dpi=200)
		
print(krige( data, exponential, hs, bw, (521463.91, 5102074.63), 16 ))