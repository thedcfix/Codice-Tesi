import pandas as pd
from pyproj import Proj, transform
from osgeo import gdal

def changeCoordinates(row):
	inProj = Proj('+init=EPSG:3003')
	outProj_UTM32N = Proj('+init=EPSG:32632')
	outProj_LONG_LAT = Proj('+init=EPSG:4326')
	
	x1,y1 = row["VL_GEO_X"],row["VL_GEO_Y"]
	x2,y2 = transform(inProj,outProj_UTM32N,x1,y1)
	x3,y3 = transform(inProj,outProj_LONG_LAT,x1,y1)
	row["UTM32N_Est"] = x2
	row["UTM32N_Nord"] = y2
	row["Longitude"] = x3
	row["Latitude"] = y3
	
	return row
	
def getElevation(points_list):
	driver = gdal.GetDriverByName('GTiff')
	filename = "SRTM_NE_250m.tif" #path to raster
	dataset = gdal.Open(filename)
	band = dataset.GetRasterBand(1)
	
	cols = dataset.RasterXSize
	rows = dataset.RasterYSize
	transform = dataset.GetGeoTransform()
	
	xOrigin = transform[0]
	yOrigin = transform[3]
	pixelWidth = transform[1]
	pixelHeight = -transform[5]
	
	data = band.ReadAsArray(0, 0, cols, rows)
	elevations = []
	
	for point in points_list:
		col = int((point[0] - xOrigin) / pixelWidth)
		row = int((yOrigin - point[1] ) / pixelHeight)
		
		elevations.append(data[row][col])
	
	return elevations

print("Loading data...")
tabella = pd.read_csv('Tabella ictus completa.csv',sep=';', decimal=',')

# dropping duplicates
tabella = tabella.drop_duplicates()

# removing null coordinates
tabella = tabella[~tabella['VL_GEO_X'].isnull()]
tabella = tabella[~tabella['VL_GEO_Y'].isnull()]

# converting coordinates to UTM32N
print("Converting coordinates...")
tabella = tabella.apply(changeCoordinates, axis=1)

# gathering altitude
print("Gathering altitudes...")
coord = tabella[['Longitude','Latitude']]
coord = [tuple(x) for x in coord.values]

tabella["ALTITUDE"] = getElevation(coord)

tabella.drop("Longitude", axis=1, inplace=True)
tabella.drop("Latitude", axis=1, inplace=True)


# parsing date-time and rounding to the closest 10 minutes interval
print("Adjusting dates...")
tabella["DATE_TIME"] = pd.to_datetime(tabella.DT_EMERG_DAY, format='%d/%m/%Y') + pd.to_timedelta(tabella.DT_EMRG_OPEN_HH24MI+":00")
tabella["DATE_TIME"] = tabella["DATE_TIME"].dt.round('10min')

print(tabella)

print("Saving...")
tabella.to_csv("tabella.csv", sep=',', decimal='.', header=True, index=False)