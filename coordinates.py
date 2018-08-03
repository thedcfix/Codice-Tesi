from pyproj import Proj, transform

inProj = Proj('+init=EPSG:3003')
outProj = Proj('+init=EPSG:32632')
x1,y1 = 1521409,5101897
x2,y2 = transform(inProj,outProj,x1,y1)
print(x1,y1)
print(x2,y2)