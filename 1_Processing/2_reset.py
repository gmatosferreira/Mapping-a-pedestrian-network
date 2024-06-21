from qgis.core import QgsProject, QgsFeature, QgsGeometry, QgsPointXY

line_layer = QgsProject.instance().mapLayersByName('merged')[0]

line_layer.startEditing()
# Clear existing features from the layer
for feature in line_layer.getFeatures():
    line_layer.dataProvider().deleteFeatures([feature.id()])

line_layer.commitChanges()
QgsProject.instance().addMapLayer(line_layer)