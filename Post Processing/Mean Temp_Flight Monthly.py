# Import modules
import arcpy
import os
import matplotlib.pyplot as plt
import numpy as np

gdb = arcpy.GetParameterAsText(0)        #  Establish Geodatabase as input
plotname = arcpy.GetParameterAsText(1)   #  Set output plot directory & name

def FlightTemp(gdbpath, plotname):

#   Set workspace
    workspace = os.path.join(gdbpath)

#   Input owl point feature class
    input_path_points = os.path.join(workspace, "Eagle_Owl_Points_proj")

#   Setting output name parameters
    Table1 = "Mean_Hight_Month"

#   Calculate the statsitical tabel with mean temperature and mean flight hight for all month
    arcpy.analysis.Statistics(input_path_points, Table1, [["FlightH", "MEAN"], ["FlightH", "STD"], ["Meantemp_10", "MEAN"], ["Meantemp_10","STD"]], "Month")

#   Conver tabel field to numppy array
    array_M = arcpy.da.TableToNumPyArray(Table1, 'Month')
    array_F = arcpy.da.TableToNumPyArray(Table1, 'MEAN_FlightH')
    array_T = arcpy.da.TableToNumPyArray(Table1, 'MEAN_Meantemp_10')
    array_FS = arcpy.da.TableToNumPyArray(Table1, 'STD_FlightH')
    array_TS = arcpy.da.TableToNumPyArray(Table1, 'STD_Meantemp_10')


#   Convert the float numbers to integers pre procees for ploting
    labels =['','Feb', 'Apr', 'June','Aug','Oct','Dec']
    x1 = array_M.astype(np.integer)
    y1 = array_T.astype(np.integer)
    z1 = array_F.astype(np.integer)

#   Add some text for labels, title and custom x-axis tick labels, etc.
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].bar(x1, y1, color = 'brown', align='center', edgecolor = 'green')
    axarr[0].set_title('Temperature and Flight Height Vs Months', fontsize = 10)
    axarr[1].bar(x1, z1, color = 'blue', align='center', edgecolor = 'green')
    axarr[0].set_ylabel("Temperature")
    axarr[1].set_ylabel("Flight Height")
    axarr[0].set_xticklabels(labels)
    f.subplots_adjust(hspace = 0.2)

#   Plotting Result
    plt.savefig(plotname + ".png", dpi = 300)
    arcpy.AddMessage("Plot Created Succesfully!")

# Calling Functions
def main():
    FlightTemp(gdb, plotname)
main()




