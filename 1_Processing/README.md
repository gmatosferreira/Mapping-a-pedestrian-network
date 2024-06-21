# 1. Processing phase

This phase consisted of aggregating the several files that resulted of each person on sight data collection. All of the work developed for this purpose was performed after importing all the layers that resulted from the field work to a QGIS project, where some scripts where executed for the aggregation purpose. These scripts, explained below, where programmed in Python and executed using the QGIS Python console editor, allowing for a batch execution of the complete files.

## 1.1. Join points

**Script**: [`1_joinPoints.py`](./1_joinPoints.py)

The first step was to gather all the intersections in one layer. For this, the eight layers resulting from the field work where imported, as well as an empty geopackage with the same structure, [intersections.gpkg](./resources/intersections.gpkg), where the output should be stored.

It is also important to mention that an extra layer ([intersections_extra.gpkg](./resources/intersections_extra.gpkg)) was created manually before running the script, to add some missing points that where identified by the person running the script.

> The script can only be executed once. However, the execution of [`1_reset.py`](./1_reset.py) reverts it, clearing the [intersections.gpkg](./resources/intersections.gpkg) layer and allowing for a re-run of the previous script. This can be useful is some error is spotted in the original layers (never edited, only read in both scripts) and a correction is applied, requiring a propagation to the aggregated version.



