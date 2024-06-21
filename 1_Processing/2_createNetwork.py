# RUN ON QGIS PYTHON CONSOLE 
from qgis.core import QgsProject, QgsFeature, QgsGeometry, QgsPointXY, QgsField

# Arguments
point_layer = QgsProject.instance().mapLayersByName('intersections')[0]
ways_layer = QgsProject.instance().mapLayersByName('ways')[0]

newLines = []

# 1. Merge points by connections attribute
merged = set()
mergeCounter = 1
for point1 in point_layer.getFeatures():
    pid = int(point1.attributes()[point_layer.fields().lookupField('fid')])
    print("-------\nPoint", pid)
    if point1.attributes()[point_layer.fields().lookupField('Connections')]:
        connections = point1.attributes()[point_layer.fields().lookupField('Connections')].strip().replace("\n", ",").split(",")
    else: 
        connections = []
    
    # For each connection
    for c in connections:
        id = c.strip()
        # Validate that has not been merged yet
        if f"{pid}-{id}" in merged or f"{id}-{pid}" in merged:
            print(f"Already merged to {id}!")  
            continue
        merged.add(f"{pid}-{id}")
        id = int(id)
        
        print(f"Merging to {id}...")
        
        # Find point instance on layer
        point2 = None
        for candidate in point_layer.getFeatures():
            if int(candidate.attributes()[point_layer.fields().lookupField('fid')]) == id:
                point2 = candidate
                break
        if not point2:
            print("!! Connection not found!")
            continue
        
        # Create line merging them....
        line = QgsFeature()
        line.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(point1.geometry().asPoint()), QgsPointXY(point2.geometry().asPoint())]))
    
        line.setAttributes([
            mergeCounter, # fid
            point1.attributes()[point_layer.fields().lookupField('Lowered')] and point2.attributes()[point_layer.fields().lookupField('Lowered')], # Lowered
            point1.attributes()[point_layer.fields().lookupField('Semaphore')] and point2.attributes()[point_layer.fields().lookupField('Lowered')], # Semaphore 
            point1.attributes()[point_layer.fields().lookupField('Tactile')] and point2.attributes()[point_layer.fields().lookupField('Tactile')], # Tactile
            point1.attributes()[point_layer.fields().lookupField('Studs')] and point2.attributes()[point_layer.fields().lookupField('Studs')], # Studs
            point1.attributes()[point_layer.fields().lookupField('Painted')] and point2.attributes()[point_layer.fields().lookupField('Painted')], # Painted
            pid, # from
            id, # to 
            '+' in point1.attributes()[point_layer.fields().lookupField('MeetingAngle')] and '+' in point2.attributes()[point_layer.fields().lookupField('MeetingAngle')], # angleGT90
            False, # Narrow (< 1,2m)
            'Calçada portuguesa', # Pavement 
            False, # Obstacles Long Term 
            False, # Obstacles Short Term
            True, # Crossing
            False, # pedestrianOnly
            None
        ])
        
        mergeCounter += 1
        newLines.append(line)
        print("Merge done :)")
        
# 2. Merge points per manual association
# 2.1. Direct association without obstacles (From, To)
manualDirect = [
    (1014,1020), # Fill with extra associations....
]

# 2.2. Direct association with obstacles (From, To, BlockedShort, BlockedLong)
manualBlocked = [
    [2005,9001,False,True]
]

manual = [] # From, To, WayID, BlockedShort, BlockedLong
for t in manualDirect:
    manual.append([t[0], t[1], None, False, False])
for t in manualBlocked:
    manual.append([t[0], t[1], None, t[2], t[3]])
    
# 2.3. Direct association that crosses a way (From, To, WayID, BlockedShort, BlockedLong)
manual.append([2002,9006,2002,False,True])

print("\n\nManual association\n\n")
for pair in manual:
    print(f"Pair {pair}")

    # Find point instance on layer
    point1 = None
    for candidate in point_layer.getFeatures():
        if int(candidate.attributes()[point_layer.fields().lookupField('fid')]) == pair[0]:
            point1 = candidate
            break
    if not point1:
        print("!! Point1 not found!")
        continue
    point2 = None
    for candidate in point_layer.getFeatures():
        if int(candidate.attributes()[point_layer.fields().lookupField('fid')]) == pair[1]:
            point2 = candidate
            break
    if not point2:
        print("!! Point2 not found!")
        continue
    way = None
    if pair[2]:
        for candidate in ways_layer.getFeatures():
            if int(candidate.attributes()[point_layer.fields().lookupField('fid')]) == pair[2]:
                way = candidate
                break
        if not way:
            print("!! Way not found!")
            continue
    
    # Create line merging them....
    line = QgsFeature()
    line.setGeometry(QgsGeometry.fromPolylineXY([QgsPointXY(point1.geometry().asPoint()), QgsPointXY(point2.geometry().asPoint())]))

    line.setAttributes([
    mergeCounter, # fid
        False, # Lowered
        False, # Semaphore 
        False, # Tactile
        False, # Studs
        False, # Painted
        pair[0], # from
        pair[1], # to 
        False, # angleGT90
        '<' in way.attributes()[ways_layer.fields().lookupField('Width')] if way else False, # Narrow (< 1,2m)
        way.attributes()[ways_layer.fields().lookupField('Pavement')] if way else 'Calçada portuguesa', # Pavement 
        pair[4], # Obstacles Long Term 
        pair[3], # Obstacles Short Term
        False, # Crossing
        'Other' in way.attributes()[ways_layer.fields().lookupField('Category')] if way else False, # pedestrianOnly
        way.attributes()[ways_layer.fields().lookupField('fid')] if way else None
    ])

    mergeCounter += 1
    newLines.append(line)
    print("Merge done :)")

# 3. Add lines to the output layer
line_layer = QgsProject.instance().mapLayersByName('merged')[0]
line_layer.startEditing()
pr = line_layer.dataProvider()
pr.addFeatures(newLines) # Add new ones
line_layer.commitChanges()
QgsProject.instance().addMapLayer(line_layer)