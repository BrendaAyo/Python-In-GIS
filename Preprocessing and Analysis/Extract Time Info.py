# Import modules
import arcpy
import os

gdb = arcpy.GetParameterAsText(0) #  Establish Geodatabase as Input

def ExtractYearMonth(gdbpath):

#       Set workspace
        workspace = os.path.join(gdbpath)

#       Reading Input Features
        Input_path_points = os.path.join(workspace, "Eagle_Owl_Points_proj")
        input_field = '!timestamp!'
        new_field_name = 'Year_Month'

#       Delete if field already exists
        field_names = [f.name for f in arcpy.ListFields(Input_path_points)]
        if new_field_name in field_names:
                arcpy.AddMessage('Field {0} Already Exists!'.format(new_field_name))
                arcpy.DeleteField_management(Input_path_points, [new_field_name])

#       Add field
        arcpy.management.AddField(Input_path_points, new_field_name, "TEXT", 9, field_alias=new_field_name, field_is_nullable="NULLABLE")
        arcpy.AddMessage("Field Year_Month Added")

#       Update field with the month
        arcpy.management.CalculateField(Input_path_points, new_field_name, "str(" + input_field + ").split('-',2)[0]+str(" + input_field + ").split('-',2)[1]", "PYTHON_9.3")
        arcpy.AddMessage("Extract Year & Month Info Done Succesfully")

# Calling Functions
def main():
        ExtractYearMonth(gdb)
main()
