# Geetika Rathee & Eline van Elburg
# 18 January 2016
# Assignment Lesson 11

# Imports
import os, os.path
import mapnik

try:
  from osgeo import ogr, osr
  print 'Import of ogr and osr from osgeo worked.  Hurray!\n'
except:
  print 'Import of ogr and osr from osgeo failed\n\n'

# Define the folder to save data
directory = '/home/user/Projects/AssignmentLesson11/data' 
if not os.path.exists(directory):
    os.makedirs(directory)

# Is the ESRI Shapefile driver available?
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

# Define filename of the shapefile
fn = "data/Assignment11.shp"
layername = "Buildings-WUR"

# Create shape file
ds = drv.CreateDataSource(fn)

# Set spatial reference
spatialReference = osr.SpatialReference()
#spatialReference.ImportFromEPSG(4326)
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

# Create Layer
layer = ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)

# Define three points in Wageningen
forum = ogr.Geometry(ogr.wkbPoint)
radix = ogr.Geometry(ogr.wkbPoint)
gaia = ogr.Geometry(ogr.wkbPoint)

# Assign location to points 
forum.SetPoint(0, 5.663713, 51.985349)
radix.SetPoint(0, 5.663562, 51.986806)
gaia.SetPoint(0, 5.665978, 51.987552)

# Make list of points
pointList = [forum, radix, gaia]

# Put the points in the layer
layerDefinition = layer.GetLayerDefn()
featureF = ogr.Feature(layerDefinition)
featureR = ogr.Feature(layerDefinition)
featureG = ogr.Feature(layerDefinition)

# Make a feature list
featureList = [featureF, featureR, featureG]

# add the points to the feature
for i in range(len(pointList)):
    featureList[i].SetGeometry(pointList[i])

# Add the features to the layer
for feature in featureList:
    layer.CreateFeature(feature)

# Make multipoint
multipoint = ogr.Geometry(ogr.wkbMultiPoint)
for building in pointList:
    multipoint.AddGeometry(building)

# Export to KML
f1=open("test.kml","w")
f1.write(str(multipoint.ExportToKML()))
f1.close()

###### Make a map with Mapnik #######

# file with symbol for point
file_symbol = os.path.join("data", "figs","marker.png")

# First we create a map
map = mapnik.Map(800, 400) #This is the final image size

#Lets put some sort of background color in the map
map.background = mapnik.Color("steelblue") # steelblue == #4682B4 

#Create the rule and style obj
r = mapnik.Rule()
s = mapnik.Style()

polyStyle= mapnik.PolygonSymbolizer(mapnik.Color("darkred"))
pointStyle = mapnik.PointSymbolizer(mapnik.PathExpression(file_symbol))
r.symbols.append(polyStyle)
r.symbols.append(pointStyle)

s.rules.append(r)
map.append_style("mapStyle", s)

# Adding point layer
layerPoint = mapnik.Layer("BuildingsWUR")
layerPoint.datasource = mapnik.Shapefile(file=os.path.join("data",
                                        "Assignment11.shp"))

layerPoint.styles.append("mapStyle")

#adding polygon
layerPoly = mapnik.Layer("polyLayer")
layerPoly.datasource = mapnik.Shapefile(file=os.path.join("data","figs",
                                        "ne_110m_coastline.shp"))
layerPoly.styles.append("mapStyle")

# Add layers to map
map.layers.append(layerPoly)
map.layers.append(layerPoint)

#Set boundaries 
#boundsLL = (1.3,51.979, 8.306,53.162) #(minx, miny, maxx,maxy)
#map.zoom_to_box(mapnik.Box2d(*boundsLL)) # zoom to bbox
map.zoom_all()

mapnik.render_to_file(map, os.path.join("data" , "figs",
                                        "mapnik_map.png"), "png")
print "All done - check content"

# Destroy datasource
ds.Destroy()


    

