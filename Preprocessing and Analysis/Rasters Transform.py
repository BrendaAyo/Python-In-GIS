# Import modules
import arcpy
import os

rasterfolder = arcpy.GetParameterAsText(0)  # Set Folder as Output directory

def project_rasters(rasterfolder):

#   Set Workspace
    gdb = "projected_rasters.gdb"  # Geodatabase where results will be stored
    raster_output_directory = os.path.join(rasterfolder, gdb)

#   Delete if gdb already exist
    if arcpy.Exists(raster_output_directory):
        arcpy.AddMessage("GDB already Exist!")
        arcpy.Delete_management(raster_output_directory)

#   Create Output GDB
    arcpy.CreateFileGDB_management(rasterfolder, "projected_rasters.gdb")
    arcpy.AddMessage("projected_rasters.gdb Created Succesfully")

#   Input Reference System
    input_Ref = "PROJCS['DHDN_3_Degree_Gauss_Zone_3',GEOGCS['GCS_Deutsches_Hauptdreiecksnetz',DATUM['D_Deutsches_Hauptdreiecksnetz',\
                SPHEROID['Bessel_1841',6377397.155,299.1528128]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Gauss_Kruger'],\
                PARAMETER['False_Easting',3500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',1.0],\
                PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

#   Output Reference System
    Output_Ref = "PROJCS['WGS_1984_UTM_Zone_32N',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',\
                6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Transverse_Mercator'],\
                PARAMETER['False_Easting',500000.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',9.0],PARAMETER['Scale_Factor',0.9996],\
                PARAMETER['Latitude_Of_Origin',0.0],UNIT['Meter',1.0]]"

#   Select & modify  rasters name and project rasters to output folder
    input_file_path = ""
    for filename in os.listdir(rasterfolder):
        if filename.endswith(".asc"):
            input_file_path=os.path.join(rasterfolder, filename)
            out_file_name = filename.split(".")
            output_file_path=os.path.join(raster_output_directory, out_file_name[0]+"_proj")
            print(filename+" Projected")
            #
            arcpy.management.ProjectRaster(input_file_path, output_file_path, Output_Ref, "NEAREST", "1000 1000","DHDN_To_WGS_1984_4_NTv2",None, input_Ref, "NO_VERTICAL")

    arcpy.AddMessage("Rasters Projected Succesfully")

# Calling Functions
def main():
    project_rasters(rasterfolder)
main()
    






