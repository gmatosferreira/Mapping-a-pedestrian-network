from qgis.core import QgsProject, QgsFeature, QgsGeometry, QgsPointXY

point_layer = QgsProject.instance().mapLayersByName('intersections')[0]

point_layer.startEditing()
# Clear existing features from the layer
for feature in point_layer.getFeatures():
    point_layer.dataProvider().deleteFeatures([feature.id()])

point_layer.commitChanges()
QgsProject.instance().addMapLayer(point_layer)

obstacles_layer = QgsProject.instance().mapLayersByName('obstacles')[0]

obstacles_layer.startEditing()
# Clear existing features from the layer
for feature in obstacles_layer.getFeatures():
    obstacles_layer.dataProvider().deleteFeatures([feature.id()])

obstacles_layer.commitChanges()
QgsProject.instance().addMapLayer(obstacles_layer)

ways_layer = QgsProject.instance().mapLayersByName('ways')[0]

ways_layer.startEditing()
# Clear existing features from the layer
for feature in ways_layer.getFeatures():
    ways_layer.dataProvider().deleteFeatures([feature.id()])

ways_layer.commitChanges()
QgsProject.instance().addMapLayer(ways_layer)