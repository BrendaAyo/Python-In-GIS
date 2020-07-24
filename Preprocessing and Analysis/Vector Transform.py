# Import modules
import arcpy
import os

gdb = arcpy.GetParameterAsText(0)   #  Establish Geodatabase as Input

def Vector_Transform(gdbpath):

#   Set Workspace
    workspace = os.path.join(gdbpath)

#   Reading Input Features
    Input_path_points = os.path.join(workspace, "Eagle_Owl_Points")
    Input_path_lines  = os.path.join(workspace, "Eagle_Owl_Lines")

#   Showing Error msg in case Inputs do not Exist
    if arcpy.Exists(Input_path_points) == False:
        arcpy.AddMessage("Eagle_Owl_Points does not Exist!")
    if arcpy.Exists(Input_path_lines) == False:
        arcpy.AddMessage("Eagle_Owl_Lines does not Exist!")

#   Define Output Files
    output_path_points = os.path.join(workspace, "Eagle_Owl_Points_proj")
    output_path_Lines = os.path.join(workspace, "Eagle_Owl_Lines_proj")

#   Delete if output files already exist
    if arcpy.Exists(output_path_points):
        arcpy.AddMessage("Feature already Exist!")
        arcpy.Delete_management(output_path_points)
    if arcpy.Exists(output_path_Lines):
        arcpy.AddMessage("Feature already Exist!")
        arcpy.Delete_management(output_path_Lines)

#   Define Output Reference System
    Output_Ref="PROJCS['WGS_1984_UTM_Zone_32N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',\
            6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],\
            PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',0.9996],\
            PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

#   Projecting Input Features
    arcpy.management.Project(Input_path_points, output_path_points,Output_Ref )
    arcpy.management.Project(Input_path_lines, output_path_Lines,Output_Ref )
    arcpy.AddMessage("Datasets has been projected")

# Calling Functions
def main():
    Vector_Transform(gdb)

main()

