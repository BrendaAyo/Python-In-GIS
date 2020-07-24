# Import modules
import arcpy
import os

gdb = arcpy.GetParameterAsText(0)   #  Establish Geodatabase as Input
csv = arcpy.GetParameterAsText(1)   #  Require CSV document as input

def add_gender(gdbpath, input_csv):

# Set workspace
    workspace = os.path.join(gdbpath)

# Reading csv data
    csv_data = input_csv

# Reading Input Features
    Input_path_points = os.path.join(workspace, "Eagle_Owl_Points_proj")

# Exporting .csv to dbf table
    dbf_table_name = "Eagle_owl"
    output_dbf_path = os.path.join(workspace, dbf_table_name)
    if arcpy.Exists(output_dbf_path):
            arcpy.Delete_management(output_dbf_path) # Delete in case file already exist
    arcpy.CopyRows_management(csv_data, output_dbf_path)
    arcpy.AddMessage("dbf Table Created Succesfully")

#Delete if field already exists
    in_table = output_dbf_path
    new_field = "tag_st_id"
    field_names = [f.name for f in arcpy.ListFields(in_table)]
    if new_field in field_names:
        arcpy.AddMessage('Field Already Exists!')
        arcpy.DeleteField_management(in_table, [new_field])

# Add field to dbf table
    arcpy.AddField_management(in_table, new_field, "TEXT", 5, "", "", "", "NULLABLE", "REQUIRED")
    arcpy.AddMessage("Field Added Succesfully")

# Calculate ID Field in String type
    arcpy.CalculateField_management(in_table, new_field, '!tag_id!', "PYTHON_9.3")

 # Join gender field to Eagle FC points
    # Set the Join parameters
    joinField1 = "tag_ident"
    joinTable = in_table
    joinField2 = new_field
    fieldList = ["animal_sex"]

# Executing Join Field
    arcpy.JoinField_management(Input_path_points, joinField1, joinTable, joinField2, fieldList)
    arcpy.AddMessage("Join Field Done Succesfully")

# Calling Functions
def main():
        add_gender(gdb, csv)
main()



