from qgis.core import QgsProject, QgsRasterLayer, QgsLayerTreeLayer
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QPushButton, QAbstractItemView
import os
import processing

# Custom dialog for multi-selection
class MultiSelectDialog(QDialog):
    def __init__(self, layer_names):
        super().__init__()
        self.setWindowTitle("Select Layers")
        self.selected_layers = []
        
        layout = QVBoxLayout()
        
        # Create a list widget for displaying layers
        self.list_widget = QListWidget()
        self.list_widget.addItems(layer_names)
        self.list_widget.setSelectionMode(QAbstractItemView.MultiSelection)  # Enable multi-selection
        layout.addWidget(self.list_widget)
        
        # Add OK and Cancel buttons
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        layout.addWidget(self.ok_button)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)
        
        self.setLayout(layout)
    
    def get_selected_layers(self):
        # Get selected layers from the list widget
        return [item.text() for item in self.list_widget.selectedItems()]

# Function to select multiple layers
def select_multiple_layers():
    # Get a list of all loaded layer names
    layer_names = [layer.name() for layer in QgsProject.instance().mapLayers().values()]
    
    # Open the custom multi-selection dialog
    dialog = MultiSelectDialog(layer_names)
    if dialog.exec_():
        return dialog.get_selected_layers()
    else:
        return []

# Function to apply a style to a raster layer
def apply_style(layer, style_file_path):
    if not os.path.exists(style_file_path):
        print(f"Style file not found: {style_file_path}")
        return
    layer.loadNamedStyle(style_file_path)
    layer.triggerRepaint()
    print(f"Applied style from {style_file_path} to layer {layer.name()}")

# Function to automate vector-to-raster batch processing for DEPTH2D
def automate_vector_to_raster_depth():
    # Get the user-selected layers
    selected_layer_names = select_multiple_layers()
    
    if not selected_layer_names:
        print("No layers selected!")
        return

    # Path to the style file for DEPTH2D
    depth_style_path = "G:/Cloud-Drive_max@flussig.com.au/05_QGIS RESOURCES/PYTHON SCRIPTS/Automate vector to raster batch process/depth_style.qml"

    # Get the layer tree root
    layer_tree_root = QgsProject.instance().layerTreeRoot()
    
    # Iterate through the selected layers
    for layer_name in selected_layer_names:
        # Get the selected input layer
        input_layer = QgsProject.instance().mapLayersByName(layer_name)[0]
        input_layer_path = input_layer.dataProvider().dataSourceUri().split('|')[0]  # Extract the file path of the input layer
        output_folder = os.path.dirname(input_layer_path)  # Get the folder where the input file is located
        
        # Define the field to rasterize
        field = "DEPTH2D"
        
        # Set the resolution
        resolution = 0.5  # You can make this dynamic with user input if needed
        
        # Define output file path with suffix
        output_file = os.path.join(output_folder, f"{field}_{layer_name}_raster.tif")  # Save in the same folder as the input
        
        # Set parameters for rasterization
        params = {
            'INPUT': input_layer_path,
            'FIELD': field,
            'BURN': 0,  # Default burn value
            'UNITS': 1,  # 1 = Georeferenced units
            'WIDTH': resolution,
            'HEIGHT': resolution,
            'EXTENT': input_layer.extent(),  # Use the layer's extent
            'NODATA': 0,
            'OUTPUT': output_file  # Output file path
        }
        
        # Run the rasterization
        try:
            result = processing.run("gdal:rasterize", params)
            output_raster_path = result['OUTPUT']
            
            # Create a raster layer from the output file
            raster_layer = QgsRasterLayer(output_raster_path, f"{field}_{layer_name}_raster")
            if not raster_layer.isValid():
                print(f"Failed to load raster layer: {output_raster_path}")
                continue
            
            # Add the raster layer to the project without loading it into the default group
            QgsProject.instance().addMapLayer(raster_layer, False)
            
            # Place the raster layer directly above the corresponding vector layer
            vector_layer_node = layer_tree_root.findLayer(input_layer.id())
            if vector_layer_node:
                parent_group = vector_layer_node.parent()
                children = parent_group.children()  # Get all child nodes
                vector_layer_index = children.index(vector_layer_node)  # Find the index of the vector layer node
                raster_layer_node = QgsLayerTreeLayer(raster_layer)
                parent_group.insertChildNode(vector_layer_index + 1, raster_layer_node)  # Insert raster layer above vector layer
            
            # Apply the style
            apply_style(raster_layer, depth_style_path)
            apply_style(raster_layer, depth_style_path)  # Apply the style again as per your request

            print(f"Raster created for layer '{layer_name}' with field '{field}'. Saved as {output_file}.")
        except Exception as e:
            print(f"Error processing layer '{layer_name}': {e}")

    print("Batch rasterization completed!")

# Run the function
automate_vector_to_raster_depth()
