
# #########################################################################
# pyqgis for QGIS version 3.0 and up
# #########################################################################
import processing
import csv
from qgis.core import QgsVectorLayer, QgsVectorFileWriter, QgsCoordinateReferenceSystem, QgsWkbTypes

# Create a layer through a shapefile, WFS or WKT csv file
def getLayer(path, file, data_source, link, extension):
    if data_source == 'ogr':
        path = "%s%s%s.shp"%(path,extension,file)
    elif data_source == 'WFS':
        path = "%s%s"%(link,file)
    elif data_source == 'delimitedtext':
        path = path

    layer = QgsVectorLayer(path, file, data_source)
    return layer


# Returns the number of features in a layer
def countLayerFeatures(layer):
    return layer.featureCount()


# create the crs. crs input: 'EPSG:4202'
def setCRS(crs):
    return QgsCoordinateReferenceSystem(crs)


# Export a layer as a shapefile
def exportAsShp(layer,output_path,crs):
    QgsVectorFileWriter.writeAsVectorFormat(layer, 
                                            output_path, 
                                            "utf-8",
                                            crs,
                                            'ESRI Shapefile', 
                                            )

# export a layer to a csv file with WKT. geomType: QgsWkbTypes.Point, QgsWkbTypes.MultiPolygon, etc. 
def export_layer_to_csv(layer,output_path,crs,geomType):
    QgsVectorFileWriter.writeAsVectorFormat(layer, 
                                            output_path, 
                                            "utf-8", 
                                            crs, 
                                            "CSV", 
                                            layerOptions=['GEOMETRY=AS_WKT'], 
                                            overrideGeometryType=geomType, 
                                            forceMulti = False, 
                                            includeZ = False
                                            )

# reduce the number of vertices in a polygon by a given tolerance.
def simplifyGeometry(layer, output_path, tolerance):
    parameters = {'INPUT': layer, 
                'TOLERANCE': tolerance, 
                'OUTPUT': output_path}

    processing.run("qgis:simplifygeometries", parameters)

    return QgsVectorLayer(output_path, 'simplified', 'ogr')


# merge multiple layers together. layers_lst: list of layers to merge. 'merged_file': name of the layer to appear in qgis
def mergeMultipleLayers(layers_lst,merged_file_path):
    parameters = {'LAYERS': layers_lst, 
                  'CRS': 'EPSG:4202', 
                  'OUTPUT': merged_file_path}

    processing.run("qgis:mergevectorlayers", parameters)  
    
    return QgsVectorLayer(merged_file_path, 'merged_file', 'ogr')

