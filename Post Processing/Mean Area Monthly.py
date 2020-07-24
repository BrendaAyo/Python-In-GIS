# Import modules
import arcpy
import os
import matplotlib.pyplot as plt
import numpy as np

gdb = arcpy.GetParameterAsText(0)           #   Establish Geodatabase as input a
plotname = arcpy.GetParameterAsText(1)      #   Set output plot directory & name

def ConvexTemp(gdbpath, plotname):

#   Set workspace
    workspace = os.path.join(gdbpath)

#   Input owl point feature class
    input_path_points = os.path.join(workspace, "Eagle_Owl_Points_proj")

#   Creating Month Field
    field = "Month"
    input_field = '!timestamp!'

#   Check if field already exists
    field_names = [f.name for f in arcpy.ListFields(input_path_points)]
    if field in field_names:
        arcpy.AddMessage("Field already exists!")
        arcpy.DeleteField_management(input_path_points, field)

#   Add the  fields to the vector file
    arcpy.management.AddField(input_path_points, field, "TEXT", 9, field_is_nullable = "NULLABLE")

#   Update field with the month info
    arcpy.management.CalculateField(input_path_points, field, "str(" + input_field + ").split('-',2)[1]", "PYTHON_9.3")

#   Setting output name parameters
    Convex_Hull = "MinimumBounding"
    Table1 = "Mean_Temp_Month"
    Table2 = "Mean_Area_Month"

#   Calculate the mean temperature for each month and save them in Table1
    arcpy.analysis.Statistics(input_path_points, Table1,[["Meantemp_10", "MEAN"]], "Month")

#   Calculate the cconvex Hull and save it the geodatabase with aggergation with each bird and month
    arcpy.management.MinimumBoundingGeometry(input_path_points, Convex_Hull, "CONVEX_HULL", "LIST", [["tag_ident"],["Month"]], "NO_MBG_FIELDS")

#   Calculate the mean area for each month and save them in Table2
    arcpy.analysis.Statistics(Convex_Hull, Table2, [["Shape_Area", "MEAN"]], "Month")

#   Converts to numpy array
    array_M = arcpy.da.TableToNumPyArray(Table2, 'Month')
    array_A = arcpy.da.TableToNumPyArray(Table2, 'MEAN_Shape_Area')
    array_T = arcpy.da.TableToNumPyArray(Table1, 'MEAN_Meantemp_10')

#   Convert the float numbers to integers pre procees for ploting
    labels = ['','Feb', 'Apr', 'June','Aug','Oct','Dec']
    x1 = array_M.astype(np.integer)
    y1 = array_T.astype(np.integer)
    z1 = array_A.astype(np.integer)

#   Add some text for labels, title and custom x-axis tick labels, etc.
    f, axarr = plt.subplots(2, sharex = True)
    axarr[0].bar(x1, y1, color = 'brown', align = 'center', edgecolor = 'green')
    axarr[0].set_title('Temperature and Convex Hull Vs Months', fontsize = 10)
    axarr[1].bar(x1, z1, color = 'blue', align = 'center', edgecolor = 'green')
    axarr[0].set_ylabel("Temperature")
    axarr[1].set_ylabel("Convex Hull")
    axarr[0].set_xticklabels(labels)
    f.subplots_adjust(hspace = 0.2)

#   Plotting Result
    plt.savefig(plotname + ".png", dpi = 300)
    arcpy.AddMessage("Plot Created Succesfully!")

# Calling Functions
def main():
    ConvexTemp(gdb, plotname)
main()


