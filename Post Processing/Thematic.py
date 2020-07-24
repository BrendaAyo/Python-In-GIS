# Import modules
from matplotlib import pyplot as plt
from matplotlib import colors as cls
from matplotlib.pyplot import figure
import numpy as np
import arcpy
import os


gdb = arcpy.GetParameterAsText(0)       #  Establish Geodatabase as input
folder = arcpy.GetParameterAsText(1)    #   Set Folder as Output directory
Id = arcpy.GetParameterAsText(2)        #   ID for Querying Owls Selection

def thematic_plot(gdbpath, Maps_output_dir, tag_ident):

#   Set workspace
    workspace = os.path.join(gdbpath)

#   input point feature class
    Input_path_points = os.path.join(workspace, "Eagle_Owl_Points_proj")

#   output directory to save maps
    output_path = os.path.join(Maps_output_dir)

#   tag id to filter the data and import filtered data to numpy
    tag_id = tag_ident

# Definition Query
    whereclause = '"tag_ident" = ' + "'" + tag_id + "'"
    arr = arcpy.da.FeatureClassToNumPyArray(Input_path_points, ('long', 'lat', 'Meantemp_10','FlightH','tag_ident','Year_Month','animal_sex'), whereclause)

#   Declare figure and axix
    f,(ax0,ax1) = plt.subplots(1,2,sharey=True,figsize=(24,15),facecolor='lightslategray')

    # Access single features in the places layer
    # And plot them
    x =arr['long']
    y = arr['lat']
    temp =arr['Meantemp_10']
    height =arr['FlightH']

    #Create temprature and altitude maps for whole dataset for one bird
    f.suptitle('Avg. Monthly Temp & Height Map for Bird ID '+tag_id+' Gender = '+arr['animal_sex'][0]+'  M.Altitude = '+str(round(np.average(arr['FlightH']))), fontsize=40)

    #Plot for Altitude
    scat1=ax1.scatter(x,y,c=height,cmap='cool',s=5)
    cb1=plt.colorbar(scat1,spacing='proportional',orientation='horizontal',ax=ax1)
    cb1.set_label('Height',fontsize=20)
    ax1.axis('equal')
    ax1.set_facecolor('0.30')
    ax1.set_title('Height of Bird id '+tag_id,fontsize=20)

    #Plot for temprature
    scat=ax0.scatter(x,y,c=temp,cmap='cool',s=5)
    cb0=plt.colorbar(scat,spacing='proportional',orientation='horizontal',ax=ax0)
    cb0.set_label('Temprature',fontsize=20)
    ax0.set_title('Mean Monthly Temprature ',fontsize=20)
    ax0.axis('equal')
    ax0.set_facecolor('0.30')
    filename=output_path+"/"+tag_id+".png"
    plt.savefig(filename,dpi=300,format='png')
    Unique_months = np.unique(arr['Year_Month'])

    #Filter whole data on monthly basis
    i=0
    for um in Unique_months:
        #create figure and axis for monthly plots
        f,(ax0,ax1) = plt.subplots(1,2,sharey=True,figsize=(24,15))

        #create subset of numpy
        sub_arr=np.extract(arr['Year_Month']==um,arr)
        print(np.average(sub_arr['Meantemp_10']))
        f.suptitle('Mean Monthly Temp = '+str(round(np.average(sub_arr['Meantemp_10'])))+'°C Mean Height = '+str(round(np.average(sub_arr['FlightH'])))+'m for '+um, fontsize=40)
        print(sub_arr)
        x1 =sub_arr['long']
        y1 = sub_arr['lat']
        temp1 =sub_arr['Meantemp_10']
        height1 =sub_arr['FlightH']

        #create altitude scatter plot for each month
        sub_scat1=ax1.scatter(x1,y1,c=height1,cmap='cool',s=5)
        sub_cb1=plt.colorbar(sub_scat1,spacing='proportional',orientation='horizontal',ax=ax1)
        sub_cb1.set_label('Height',fontsize=20)
        ax1.axis('equal')
        ax1.set_title('Height of Bird id '+tag_id+'& '+um,fontsize=20)
        ax1.set_facecolor('0.30')

        #create temprature scatter plot for each month
        sub_scat0=ax0.scatter(x1,y1,c=temp1,cmap='cool',s=5)
        sub_cb0=plt.colorbar(sub_scat0,spacing='proportional',orientation='horizontal',ax=ax0)
        sub_cb0.set_label('Temprature',fontsize=20)
        ax0.axis('equal')
        ax0.set_title('Mean Monthly Temprature',fontsize=20)
        ax0.set_facecolor('0.30')
        filename=output_path+"/"+tag_id+"_"+um+".png"
        plt.savefig(filename,dpi=300,format='png')
        print(i)
        arcpy.AddMessage("Thematic Plot Created Succesfully!")

# Calling Functions
def main():
        thematic_plot(gdb, folder, Id)
main()
