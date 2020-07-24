# Import modules
import arcpy
import os

gdb = arcpy.GetParameterAsText(0)           #   Establish Geodatabase as input
raster = arcpy.GetParameterAsText(1)        #   DEM Raster with Elevation Information

def flyCalculation(gdbpath, rasterfile):

# Set workspace
    workspace = os.path.join(gdbpath)

#input point feature class
    input_path_points = os.path.join(workspace, "Eagle_Owl_Points_proj")

# Input input_raster  file
    input_raster = os.path.join(workspace, rasterfile)

# define the variables
    input_field = '!timestamp!'
    field1 = "FlightH"
    field2 = "GroundEl"
    field3 = "Month"
    
# Check if a 'GroundElevation and flight height ' field already exists, if yes, delete it
    field_names = [f.name for f in arcpy.ListFields(input_path_points)]
    if(field1 or field2) in field_names:
        arcpy.AddMessage("Field Already Exist!")
        arcpy.DeleteField_management(input_path_points, [field1, field2, field3])
     
# Add the  fields to the vector file
    arcpy.AddField_management(input_path_points, field1, 'Double')
    arcpy.management.AddField(input_path_points, field3, "TEXT", 9, field_is_nullable="NULLABLE")
    arcpy.AddMessage("Fields: {0} & {1} Created Succesfully!".format(field1, field3))
    

#Update field with the month
    arcpy.management.CalculateField(input_path_points, field3, "str(" + input_field + ").split('-',2)[1]", "PYTHON_9.3")

# Check out extension
    if arcpy.CheckExtension('Spatial') == 'Available':
        arcpy.CheckOutExtension('Spatial')
    else:
        # Print error message
        arcpy.AddMessage("Required Spatial extension not available")
    arcpy.sa.ExtractMultiValuesToPoints(input_path_points, [[input_raster, field2]], "NONE")
    arcpy.management.CalculateField(input_path_points, field1, "!height! - !GroundEl!", "PYTHON_9.3", None)

# check in extension (give it back)
    arcpy.CheckInExtension('Spatial')
    # Create update cursor updating flight hight values 
    upd_cursor1 = arcpy.da.UpdateCursor(input_path_points, ['FlightH'])

# Loop for updating the track_se1 fields of new features
    for row in upd_cursor1:   
        if row[0] > -5 and row[0] <= 0:
            row[0] = 0
            #updatiing the cursor values 
            upd_cursor1.updateRow(row)    
        elif(row[0] <= -5):
            row[0] = None
            #updatig values
            upd_cursor1.updateRow(row)
       

# Create update cursor for deleting rows
    upd_cursor2 = arcpy.da.UpdateCursor(input_path_points,['FlightH','speed'])

# Loop for deleting row have Null or speed equal to zero
    for row in upd_cursor2:   
        if (row[0] == None) or (row[1] == 0):
            upd_cursor2.deleteRow()
    del upd_cursor2        
    arcpy.AddMessage("Ground Elevation Extracted Succesfully!")

# Calling Functions
def main():
        flyCalculation(gdb, raster)
main()
