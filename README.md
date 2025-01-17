# Multiple-Vector-to-Raster-Processing-with-Styling
Automate batch rasterization of multiple vector layers, apply styles and organize raster layers in QGIS.

# Description
This QGIS Python script automates the batch rasterization of selected vector layers, focusing on the DEPTH2D field. It applies predefined styles and color ramps to the generated raster layers, organizing them directly above their corresponding vector layers in the QGIS project. This tool is specifically tailored for engineers and GIS professionals working on flood modeling or similar tasks.

# Features
Batch rasterize multiple selected vector layers.
Automatically apply predefined styles and color ramps to each raster.
Organize raster layers directly above their corresponding vector layers in the project structure.
Ensures a streamlined and visually intuitive workflow.

# Usage Instructions

Load your vector layers into QGIS.
Place the script batch_vector_to_raster_with_styling.py(or any other styling of preference) in your Python script folder or run it directly from the Python console in QGIS. Alternatively, if you do not need the styling, you can delete the styling steps of the code
Ensure the required style file (depth_style.qml) is accessible and modify its path in the script.
Run the script and select multiple vector layers in the prompted dialog.
Raster layers will be generated and organized above their corresponding vector layers.

# Prerequisites
QGIS installed (tested with version 3.x).
Necessary libraries: PyQt5 and QGIS Core.
Style file: depth_style.qml (ensure the path is correctly set in the script).
