import numpy as np
import matplotlib.pyplot as plt

input_path  = "./20190416-000000.csv"       #enter where to get input data
output_path = "./timeseries/"               #enter where output data should end up
variables   = ["Ts_hcor","w","q","CO2"]     #enter vars you want to plot
units       = ["K","m/s","g/kg","ppm"]      #enter units for vars you want to plot 
seperation  = 51                           #how man seperate plots you want( -1) 
N = 100


data_arr = np.loadtxt(input_path,dtype='string',delimiter=";", skiprows = 1)    

data_dict = {"time":None,"u":None,"v":None,"w":None,"Ts":None,"Ts_hcor":None,"q":None,"CO2":None,"p":None}
w_dict = {"time":None,"u":None,"v":None,"w":None,"Ts":None,"Ts_hcor":None,"q":None,"CO2":None,"p":None}
mean_dict = {"time":None,"u":None,"v":None,"w":None,"Ts":None,"Ts_hcor":None,"q":None,"CO2":None,"p":None}
data_dict["time"] = data_arr[:,0]
data_dict["u"] = (data_arr[:,1]).astype(float)
data_dict["v"] = (data_arr[:,2]).astype(float)
data_dict["w"] = (data_arr[:,3]).astype(float)
data_dict["Ts"] = (data_arr[:,4]).astype(float)
data_dict["Ts_hcor"] = (data_arr[:,5]).astype(float)
data_dict["q"] = (data_arr[:,6]).astype(float)*1000
data_dict["CO2"] = (data_arr[:,7]).astype(float)
data_dict["p"] = (data_arr[:,8]).astype(float)





mask = np.ones((N,))/N

for j,var in enumerate(variables):


    mean_dict[var] = np.convolve(data_dict[var],mask ,mode="same")
    diff = data_dict[var]-mean_dict[var]
    w_dict[var] = diff/np.nanstd(data_dict[var])

sum_arr = w_dict["Ts_hcor"]+w_dict["w"]+w_dict["CO2"]+w_dict["q"]    

for i in range(len(sum_arr)):
    if np.isnan(sum_arr[i]) == True:
        sum_arr[i] = 0


index = np.where(sum_arr > 0.01)

#for var in variables:
    
    #data_dict[var][index] = mean_dict[var][index]

    
name = ""
for i in variables:
    name += i + "_"
    
dt = np.linspace(0,len(data_dict["time"])-1,seperation)
dt = np.round(dt).astype(int)

fig,ax = plt.subplots(4,1, sharex=True,figsize=(100,40))
    
for i in range(1):
    for j,var in enumerate(variables):

        interval = np.arange(dt[i], dt[i+1],1)
        ax[j].plot(interval,data_dict[var][dt[i]:dt[i+1]],linewidth=0.1,color = "k")
        
        locs = np.arange(dt[i],dt[i+1], 4000)
        
        plt.xticks(locs, data_dict["time"][locs])
        plt.xlabel("Date / Time")
        ax[j].set_ylabel(var +" in "+ units[j])
        ax[0].set_ylim(280.5,284.0)
        ax[1].set_ylim(-2.,2.)
        ax[2].set_ylim(3.15,3.40)
        ax[3].set_ylim(411,419)
                                        ####maybe find a better solution than quantile limits
        plt.xlim(interval[0],interval[-1])
        
        ax2 = ax[j].twinx()
        ax2.plot(interval,w_dict[var][dt[i]:dt[i+1]],linewidth=0.1,color = "b")
        ax2.set_ylim(-2,2)
        
    plt.tight_layout()
    
    plt.savefig(output_path + name + str(i) +"_timeseries_.png")
   
        
plt.close("all")
        