# Import modules
from matplotlib import pyplot as plt
from matplotlib import colors as cls
import numpy as np
import os
import arcpy 


gdb = arcpy.GetParameterAsText(0)           #   Establish Geodatabase as input
plotname = arcpy.GetParameterAsText(1)      #  Set output plot directory & name

def scaterplot(gdbpath, plotname):

#   Set workspace
    workspace = os.path.join(gdbpath)

#   Input owl point feature class
    input_path_points = os.path.join(workspace, "Eagle_Owl_Points_proj")

    #Attributes of the layer that are going to be used at the Cursor
    attr = ['animal_sex', 'FlightH', 'MeanTemp', 'timestamp']

    zm = []
    tm = []
    dm = []
    zf = []
    tf = []
    df = [] 

    with arcpy.da.SearchCursor(input_path_points, attr) as cursor:
        for feat in cursor:
            #Get data male
            if feat[0] == "m":
                z1 = feat[1]
                t1 = feat[2]/10
                d1= int(str(feat[3].split('-')[1]))
                zm.append(z1)
                tm.append(t1)
                dm.append(d1)

            #Get data female
            else:
                z1 = feat[1]
                t1 = feat[2]/10
                d1= int(str(feat[3].split('-')[1]))
                zf.append(z1)
                tf.append(t1)
                df.append(d1)  

    #Normalize colors months
    total_range = cls.Normalize(vmin = 1, vmax = 12)

    #Plot figure
    fig = plt.figure()

    #First subplot
    ax1 = plt.subplot(211)

    #First subplot, labl = Male and label y = Altitude
    ax1.title.set_text('Male')
    ax1.set_ylabel('Altitude')

    #Axis y limits and difference
    ax1.set_ylim(0, 2501)

    #Axis y from -1000 to 2501 with a difference of 500
    ax1.yaxis.set_ticks(np.arange(0, 2501, 500))
    ax1.yaxis.set_ticklabels(np.arange(0, 2501, 500))

    #Axis x limits and difference
    ax1.set_xlim(-2.5, 22.5)
    ax1.xaxis.set_ticks(np.arange(-2.5, 22.5, 2.5))
    ax1.xaxis.set_ticklabels(np.arange(-2.5, 22.5, 2.5))

    #Plot subplot 1 with legend and sparcing = proporcional
    scat1 = ax1.scatter(tm, zm, c=dm, label='Male', alpha=0.5, norm=total_range)
    cb1 = plt.colorbar(scat1, spacing = 'proporcional')
    cb1.set_label('Month')

    #Second subplot, label = Female and label y = Altitude
    ax2 = plt.subplot(212)
    ax2.title.set_text('Female')
    ax2.set_ylabel('Altitude')

    #X axis will be temperature and will be join for botw subplots
    ax2.set_xlabel('Temperature')

    #Axis y limits and difference
    ax2.set_ylim(0, 2501)

    #Axis y from -1000 to 2501 with a difference of 500
    ax2.yaxis.set_ticks(np.arange(0, 2501, 500))
    ax2.yaxis.set_ticklabels(np.arange(0, 2501, 500))

    #Axis x from -1000 to 2501 with a difference of 500
    ax2.set_xlim(-2.5, 22.5)
    ax2.xaxis.set_ticks(np.arange(-2.5, 22.5, 2.5))
    ax2.xaxis.set_ticklabels(np.arange(-2.5, 22.5, 2.5))


    #Plot subplot 2 with legend and sparcing = proporcional
    scat2 = ax2.scatter(tf, zf, c=df, label='Female', alpha=0.5, norm=total_range)
    cb2 = plt.colorbar(scat2, spacing = 'proporcional')
    cb2.set_label('Month')

    #Both subplots share x axis
    ax1.get_shared_x_axes().join(ax1, ax2)
    ax1.set_xticklabels([])

    #Save figure as png
    plt.savefig(plotname + '.png')
    arcpy.AddMessage("Scatterplot Created Succesfully!")

# Calling Functions
def main():
    scaterplot(gdb, plotname)
main()
