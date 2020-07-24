# Import modules
import os
import arcpy

gdb = arcpy.GetParameterAsText(0)           #   Establish Geodatabase as input
gdbraster = arcpy.GetParameterAsText(1)     #   Establish Geodatabase with raster files as input

def Extract_Temprature(gdbpath, raster_gdbpath):
#   Set workspace
    workspace = os.path.join(gdbpath)

#   Input owl point feature class
    input_path_points = os.path.join(workspace, "Eagle_Owl_Points_proj")

#   Directory containing rasters to be renamed
    raster_workspace = os.path.join(raster_gdbpath)

#   Create unique id for joining data
    field_name="ID"
    field_names = [f.name for f in arcpy.ListFields(input_path_points)]
    if field_name in field_names:
        print('exists')
        arcpy.DeleteField_management(input_path_points, [field_name])
    arcpy.AddField_management(input_path_points, field_name, "LONG", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.CalculateField_management(input_path_points, field_name, '!OBJECTID!', "PYTHON_9.3")

#   Path to intermediate geodatabase to store intermediate results
    target_workspace = r'C:\TryOuts.gdb'

#   Create intermediate geodatabase
    if os.path.isdir(target_workspace):
        print('exists')
        arcpy.Delete_management(target_workspace)
    print("create tryouts")
    arcpy.CreateFileGDB_management("C:/", "TryOuts.gdb", "9.2")

#   spliting data into feture classes on the basis of year_month fields to extract mean monthly temperature from rasters
    field = 'Year_Month'
    arcpy.analysis.SplitByAttributes(input_path_points, target_workspace, field)
    print('Feature spliting done....')

#   Rename temprature rasters according to the months and year
    arcpy.env.workspace = raster_workspace
    for raster in arcpy.ListRasters():
        # get the raster name and file extension
        fileName,fileExtension = os.path.splitext(raster)
        # fileNameParts like TAMM_01_2012_01_proj
        # fileNameParts[0] = TAMM
        # fileNameParts[1] = 01
        # fileNameParts[2] = 2012
        # fileNameParts[3] = 01
        # fileNameParts[4] = proj
        fileNameParts = fileName.split('_')

        if(len(fileNameParts)>1):
            compactFileName = "T" + fileNameParts[2] + fileNameParts[1] + fileExtension
            arcpy.Rename_management(raster,compactFileName)
    print('Renaming rasters done')

#   Extract Temperature Values to Points
    if arcpy.CheckExtension ('Spatial') == 'Available':
        arcpy.CheckOutExtension ('Spatial')

#   Start a loop in the raster list and within that loop strip the "." extension off the file name and replace with ".tif"
    arcpy.env.workspace = raster_workspace
    rasters = arcpy.ListRasters()
    for ras in rasters:
        tiff = ras.replace(".", ".tif")

    #Check to make sure the feature class name exists that corresponds to the raster name
        if arcpy.Exists(os.path.join(target_workspace, tiff)):

    #Extract the raster values to the points
            arcpy.sa.ExtractMultiValuesToPoints(os.path.join(target_workspace, tiff), ras)
    arcpy.CheckInExtension('Spatial')
    print('extraction of temprature on each point done')

    #adding mean temprature field to original point data
    new_field_name = 'MeanTemp'

#   Check if the field already exists
    Main_featureclass = input_path_points
    field_names = [f.name for f in arcpy.ListFields(Main_featureclass)]
    if new_field_name in field_names:
        print('exists')
        arcpy.DeleteField_management(Main_featureclass, [new_field_name])

#   Add field (if it not exists)
    arcpy.management.AddField(Main_featureclass, new_field_name, "LONG", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)

#   Store year_month data in numpy to get unique values list
    data = arcpy.da.TableToNumPyArray(Main_featureclass, 'Year_Month')
    uniq=numpy.unique(data['Year_Month'])
    querystring=""
    for uniquemonth in uniq:
        columnname="T"+uniquemonth
        field_names = [f.name for f in arcpy.ListFields(Main_featureclass)]
        if columnname in field_names:
            print('exists')
            arcpy.DeleteField_management(Main_featureclass, [columnname])
        print(uniquemonth)
        arcpy.JoinField_management(Main_featureclass,"ID", target_workspace+"\T"+uniquemonth, "ID", ["T"+uniquemonth])
        arcpy.management.CalculateField(Main_featureclass,columnname , "updateValue(!"+columnname+"!)", "PYTHON_9.3", r"def updateValue(value):\n  if value == None:\n   return '0'\n  else: return value")
        querystring=querystring+"+!"+columnname+"!"
    querystring=querystring[1:]
    print("data joining with original dataset is done")

#   Merge all tempratures in one column
    arcpy.management.CalculateField(Main_featureclass, new_field_name, querystring, "PYTHON_9.3", None)

#   Delete joined multiple fields from original dataset
    for uniquemonth in uniq:
        columnname="T"+uniquemonth
        field_names = [f.name for f in arcpy.ListFields(Main_featureclass)]
        if columnname in field_names:
            print('exists')
            arcpy.DeleteField_management(Main_featureclass, [columnname])

#   Create new field to divide extracted temprature according to metadata of temprature rasters
    new_field_name1 = 'MeanTemp_10'

#   Check if the field already exists
    field_names = [f.name for f in arcpy.ListFields(Main_featureclass)]
    if new_field_name1 in field_names:
        print('exists')
        arcpy.DeleteField_management(Main_featureclass, [new_field_name1])

#   Add field (if it not exists)
    arcpy.management.AddField(Main_featureclass, new_field_name1, "DOUBLE", None, None, None, None, "NULLABLE", "NON_REQUIRED", None)
    arcpy.management.CalculateField(Main_featureclass, new_field_name1, "!"+new_field_name+"!", "PYTHON_9.3", None)
    arcpy.management.CalculateField(Main_featureclass, new_field_name1, "!"+new_field_name1+"!/10", "PYTHON_9.3", None)

# Calling Functions
def main():
    Extract_Temprature(gdb, gdbraster)
main()



