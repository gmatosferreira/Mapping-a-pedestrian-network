# 1. Processing phase

This phase consisted of aggregating the several files that resulted of each person on sight data collection. All of the work developed for this purpose was performed after importing all the layers (available at [resources](./resources) folder) that resulted from the field work to a QGIS project, where some scripts where executed for the aggregation purpose. These scripts, explained below, where programmed in Python and executed using the QGIS Python console editor, allowing for a batch execution of the complete files.

## 1.1. Join data

**Script**: [`1_joinPoints.py`](./1_joinPoints.py)

The first step was to gather all the different data collected in one layer (one per type of data collected - meaning one for intersections, one for obstacles and one for ways). So, for each type of data collected, the eight layers resulting from the field work where imported, as well as an empty geopackage with the same structure, [intersections.gpkg](./resources/intersections.gpkg), [ways.gpkg](./resources/ways.gpkg) and [obstacles.gpkg](./resources/obstacles.gpkg), where the output should be stored.

It is also important to mention that an extra layer ([intersections_extra.gpkg](./resources/intersections_extra.gpkg)) was created manually before running the script, to add some missing points that where identified by the person running the script and to map the ways edges (motivation explained in the next step).

> The script can only be executed once. However, the execution of [`1_reset.py`](./1_reset.py) reverts it, clearing the output layers and allowing for a re-run of the previous script. This can be useful is some error is spotted in the original layers (never edited, only read in both scripts) and a correction is applied, requiring a propagation to the aggregated version.

## 1.2. Create network

**Script**: [2_createNetwork.py](./2_createNetwork.py)

Once the three layers with the aggregated data where created ([intersections.gpkg](./resources/intersections.gpkg), [ways.gpkg](./resources/ways.gpkg) and [obstacles.gpkg](./resources/obstacles.gpkg)), the network could finally be created.

To ease the field work load, people where only asked to fill the form with the connections within the intersections, meaning that there was no data about the connections between different intersections. The mapping within the intersections is the first part of [2_createNetwork.py](./2_createNetwork.py) script (section `#1` of the code), which for each intersection, looks for the ids on the `Connections` attribute column and creates a line polygon connecting them.

After this, due to the difficulties merging the ways (lines polygons) with the intersections (points) and obstacles (also points) in a continuous network (the main problem was the discontinuities generated due to the non overlap of their coordinates), it was decided to follow a manual approach (section `#2` of the code), connecting only points through straight lines, which where then associated to the ways and obstacles attributes. There were performed three types of associations:

2.1. Direct association between points, to connect intersections between each other;

2.2. Direct association between points, with obstacles, identifying if they are short or long term;

2.3. Direct association between points, with the ID of a way, which had its attributes mapped to the resulting line connecting the points.

> These three steps can be edited in the script, corresponding, respectively, to the variables `manualDirect`, `manualBlocked` and `manual`.

> Like in the previous step, there is a script to clear the output layers, [`2_reset.py`](./2_reset.py), allowing for the re-run of the network generation script.