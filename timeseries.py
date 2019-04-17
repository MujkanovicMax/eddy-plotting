import datetime as dt
import numpy as np
import datetime
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)



#######################################################################################################################################
#################################                Inputs                    ############################################################
#######################################################################################################################################

input_path  = "./20190416-000000.csv"       #enter where to get input data
output_path = "./timeseries/"               #enter where output data should end up
variables   = ["Ts_hcor","w","q","CO2"]     #enter vars you want to plot
units       = ["K","m/s","g/kg","ppm"]      #enter units for vars you want to plot 
seperation  = 51                           #how man seperate plots you want( -1)


#######################################################################################################################################
#################################              Array Stuff                 ############################################################
#######################################################################################################################################

data_arr = np.loadtxt(input_path,dtype='string',delimiter=";", skiprows = 1)    

data_dict = {"time":None,"u":None,"v":None,"w":None,"Ts":None,"Ts_hcor":None,"q":None,"CO2":None,"p":None}
data_dict["time"] = data_arr[:,0]
data_dict["u"] = (data_arr[:,1]).astype(float)
data_dict["v"] = (data_arr[:,2]).astype(float)
data_dict["w"] = (data_arr[:,3]).astype(float)
data_dict["Ts"] = (data_arr[:,4]).astype(float)
data_dict["Ts_hcor"] = (data_arr[:,5]).astype(float)
data_dict["q"] = (data_arr[:,6]).astype(float)*1000
data_dict["CO2"] = (data_arr[:,7]).astype(float)
data_dict["p"] = (data_arr[:,8]).astype(float)


#######################################################################################################################################
#################################              Plotting Loop               ############################################################
#######################################################################################################################################
name = ""
for i in variables:
    name += i + "_"
    
dt = np.linspace(0,len(data_dict["time"])-1,seperation)
dt = np.round(dt).astype(int)

fig,ax = plt.subplots(4,1, sharex=True,figsize=(100,40))
    
for i in range(seperation-1):
    for j,var in enumerate(variables):

        interval = np.arange(dt[i], dt[i+1],1)
        ax[j].plot(interval,data_dict[var][dt[i]:dt[i+1]],linewidth=0.1,color = "k")
        locs = np.arange(dt[i],dt[i+1], 4000)
        
        plt.xticks(locs, data_dict["time"][locs])
        plt.xlabel("Date / Time")
        ax[j].set_ylabel(var +" in "+ units[j])
        #ax[j].set_ylim(np.nanquantile(data_dict[var],0.05),np.nanquantile(data_dict[var],0.95))   ####maybe find a better solution than quantile limits
        plt.xlim(interval[0],interval[-1])
        
    plt.tight_layout()
    
    plt.savefig(output_path + name + str(i) +"_timeseries_.png")
   
        
plt.close("all")     












