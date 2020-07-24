# Import modules
import os
import arcpy


inputfolderpath = arcpy.GetParameterAsText(0) # Established Output Directory

def shp2fc(inputfolderpath):

#   Shapefiles directory
    shapefile_input_directory = inputfolderpath

#   Input Shp files
    Input_shp_points = os.path.join(shapefile_input_directory, "points.shp")
    Input_shp_lines  = os.path.join(shapefile_input_directory, "lines.shp")

#   Ouput gdb name and directory
    gdb = "Eagle_Owls.gdb"
    gdb_output_directory = os.path.join(shapefile_input_directory, gdb)

#   Delete in case gdb already exist
    if arcpy.Exists(gdb_output_directory):
        arcpy.AddMessage("Geodatabase already exists!")
        arcpy.Delete_management(gdb_output_directory)

#   Output Feature Classes
    Output_fc_points = os.path.join(gdb_output_directory, "Eagle_Owl_Points")
    Output_fc_lines  = os.path.join(gdb_output_directory, "Eagle_Owl_Lines")

#   Create gdb
    arcpy.CreateFileGDB_management(shapefile_input_directory, gdb)
    arcpy.AddMessage("GDB Created Succesfully")

#   Converting Shps to Feature Classes
    arcpy.CopyFeatures_management(Input_shp_points, Output_fc_points)
    arcpy.CopyFeatures_management(Input_shp_lines, Output_fc_lines)
    arcpy.AddMessage("Conversion from Shp to FC done Succesfully")

#   Calling Functions
def main():
        shp2fc(inputfolderpath)
main()
