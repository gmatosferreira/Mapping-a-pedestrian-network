from qgis.core import QgsProject, QgsFeature, QgsGeometry, QgsPointXY, QgsFields, QgsField

files = [
    ['goncalo', 1000],
    ['vitor', 2000],
    ['madalena', 3000],
    ['tomas', 4000],
    ['joao', 5000],
    ['marcelo', 6000],
    ['martin', 8000],
    ['miguel', 7000],
    ['extra', 9000]
]

points = []
obstacles = []
ways = []

for process in files:
    print(f"Processing", process[0])
    print("> Intersections...")
    point_layer = QgsProject.instance().mapLayersByName(f"intersections_{process[0]}")[0]
    
    # Define fields for the new layer (add or modify fields as needed)
    new_fields = QgsFields()
    for field in point_layer.fields():
        new_fields.append(QgsField(field.name(), field.type()))
    
    for p in point_layer.getFeatures():
        # Duplicate point feature
        new_feature = QgsFeature(new_fields)
        new_feature.setGeometry(p.geometry())
        
        # Update attribute values (modify as needed)
        for field in point_layer.fields():
            val = p.attribute(field.name())
            if (field.name() == 'fid'):
                val = int(val) + process[1]
            elif (field.name() == 'Connections') and val:
                vals = []
                connections = val.strip().replace("\n", ",").split(",")
                for c in connections:
                    vals.append(str(int(c.strip()) + process[1]))
                val = ','.join(vals)
            new_feature.setAttribute(field.name(), val)
        
        # Write the new feature to the new layer
        points.append(new_feature)
        
    if QgsProject.instance().mapLayersByName(f"obstacles_{process[0]}"):
        print("> Obstacles...")
        obs_layer = QgsProject.instance().mapLayersByName(f"obstacles_{process[0]}")[0]
        
        # Define fields for the new layer (add or modify fields as needed)
        new_fields = QgsFields()
        for field in obs_layer.fields():
            new_fields.append(QgsField(field.name(), field.type()))
        
        for p in obs_layer.getFeatures():
            # Duplicate point feature
            new_feature = QgsFeature(new_fields)
            new_feature.setGeometry(p.geometry())
            
            # Update attribute values (modify as needed)
            for field in obs_layer.fields():
                val = p.attribute(field.name())
                if (field.name() == 'fid'):
                    val = int(val) + process[1]
                new_feature.setAttribute(field.name(), val)
            
            # Write the new feature to the new layer
            obstacles.append(new_feature)
    else:
        print("> No obstacles...")
        
    if QgsProject.instance().mapLayersByName(f"ways_{process[0]}"):
        print("> Ways...")
        ways_layer = QgsProject.instance().mapLayersByName(f"ways_{process[0]}")[0]
        
        # Define fields for the new layer (add or modify fields as needed)
        new_fields = QgsFields()
        for field in ways_layer.fields():
            new_fields.append(QgsField(field.name(), field.type()))
        
        for p in ways_layer.getFeatures():
            # Duplicate point feature
            new_feature = QgsFeature(new_fields)
            new_feature.setGeometry(p.geometry())
            
            # Update attribute values (modify as needed)
            for field in ways_layer.fields():
                val = p.attribute(field.name())
                if (field.name() == 'fid'):
                    val = int(val) + process[1]
                new_feature.setAttribute(field.name(), val)
            
            # Write the new feature to the new layer
            ways.append(new_feature)
    else:
        print("> No ways...")
        

join_layer_points = QgsProject.instance().mapLayersByName('intersections')[0]
join_layer_points.startEditing()
pr = join_layer_points.dataProvider()
pr.addFeatures(points) # Add new ones
join_layer_points.commitChanges()
QgsProject.instance().addMapLayer(join_layer_points)


join_layer_obstacles = QgsProject.instance().mapLayersByName('obstacles')[0]
join_layer_obstacles.startEditing()
pr = join_layer_obstacles.dataProvider()
pr.addFeatures(obstacles) # Add new ones
join_layer_obstacles.commitChanges()
QgsProject.instance().addMapLayer(join_layer_obstacles)


join_layer_ways = QgsProject.instance().mapLayersByName('ways')[0]
join_layer_ways.startEditing()
pr = join_layer_ways.dataProvider()
pr.addFeatures(ways) # Add new ones
join_layer_ways.commitChanges()
QgsProject.instance().addMapLayer(join_layer_ways)