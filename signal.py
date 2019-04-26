import numpy as np
import matplotlib.pyplot as plt

input_path  = "./20190416-000000.csv"       #enter where to get input data
output_path = "./timeseries/"               #enter where output data should end up
variables   = ["Ts_hcor","w","q","CO2"]     #enter vars you want to plot
units       = ["K","m/s","g/kg","ppm"]      #enter units for vars you want to plot 
seperation  = 51                           #how man seperate plots you want( -1) 
#N = 100


data_arr = np.loadtxt(input_path,dtype='string',delimiter=";", skiprows = 1)    
data_dict = {"time":None,"u":None,"v":None,"w":None,"Ts":None,"Ts_hcor":None,"q":None,"CO2":None,"p":None}
w_dict = {"time":None,"u":None,"v":None,"w":None,"Ts":None,"Ts_hcor":None,"q":None,"CO2":None,"p":None}
mean_dict = {"time":None,"u":None,"v":None,"w":None,"Ts":None,"Ts_hcor":None,"q":None,"CO2":None,"p":None}
#temp_w_dict = {"time":None,"u":None,"v":None,"w":None,"Ts":None,"Ts_hcor":None,"q":None,"CO2":None,"p":None}


data_dict["time"] = data_arr[:,0]
data_dict["u"] = (data_arr[:,1]).astype(float)
data_dict["v"] = (data_arr[:,2]).astype(float)
data_dict["w"] = (data_arr[:,3]).astype(float)
data_dict["Ts"] = (data_arr[:,4]).astype(float)
data_dict["Ts_hcor"] = (data_arr[:,5]).astype(float)
data_dict["q"] = (data_arr[:,6]).astype(float)*1000
data_dict["CO2"] = (data_arr[:,7]).astype(float)
data_dict["p"] = (data_arr[:,8]).astype(float)

tmp = np.zeros(data_dict["Ts_hcor"].shape)
tmp2 = np.zeros(data_dict["q"].shape)


mask_Ts = np.ones((500,))/500.
mask_w  = np.ones((10,))/10.
mask_q  = np.ones((100,))/100.
mask_CO2= np.ones((60,))/60.
mask_dict = {"time":None,"u":None,"v":None,"w":mask_w,"Ts":None,"Ts_hcor":mask_Ts,"q":mask_q,"CO2":mask_CO2,"p":None}

ger_mean_temp = 15 + 273.15  ###roughly the mean temperature of germany (yearly avg)
indoor_temp = 20 + 273.15    ### room(toilet) temperature ( roughly ) 
indoor_RH = 30              ### rough estimate of toilet RH
indoor_q  = 0.622 * indoor_RH/(100.*1013)*6.112*np.exp((17.62 * (indoor_temp-273.15))/(243.12+(indoor_temp-273.15)))
indoor_q = indoor_q*1000

for j,var in enumerate(variables):

    
        
        mean_dict[var] = np.convolve(data_dict[var],mask_dict[var] ,mode="same")*1
        diff = np.abs(data_dict[var]-mean_dict[var])
        w_dict[var] = 1-np.exp(-diff/np.nanstd(data_dict[var]))
        #w_dict[var] = w_dict[var]/np.nansum(w_dict[var]) * 10

    


sigma = 15#np.nanstd(data_dict["Ts_hcor"]-indoor_temp)
for i in range(len(mean_dict["Ts_hcor"])):
    if mean_dict["Ts_hcor"][i] > indoor_temp:
        
        deltaT = data_dict["Ts_hcor"][i] - indoor_temp
        if deltaT > 0:
            tmp[i] = np.exp(-deltaT/sigma)
        elif deltaT < 0:
            tmp[i] = 0
            w_dict["Ts_hcor"][i] = 0
        else:
            print("wat")
            
    elif mean_dict["Ts_hcor"][i] < indoor_temp:
        deltaT = data_dict["Ts_hcor"][i] - indoor_temp
        if deltaT > 0:
            tmp[i] = 0
            w_dict["Ts_hcor"][i] = 0
        elif deltaT < 0:
            tmp[i] = np.exp(deltaT/sigma)
        else:
            print("wat")
            
    else:
        print("watwat")

#tmp = tmp/np.nansum(tmp) * 10

sigma = 1.5#np.nanstd(data_dict["q"]-indoor_q)
for i in range(len(mean_dict["q"])):
    if mean_dict["q"][i] > indoor_q:
        
        deltaq = data_dict["q"][i] - indoor_q
        if deltaq > 0:
            tmp2[i] = np.exp(-deltaq/sigma)
        elif deltaq < 0:
            tmp2[i] = 0
            w_dict["q"][i] = 0
        else:
            print("wat")
            
    elif mean_dict["q"][i] < indoor_q:
        deltaq = data_dict["q"][i] - indoor_q
        if deltaq > 0:
            tmp2[i] = 0
            w_dict["q"][i] = 0
        elif deltaq < 0:
            tmp2[i] = tmp2[i] = np.exp(deltaq/sigma)
        else:
            print("wat")
            
    else:
        print("watwat")        
        
    
                
        
        
sum_arr = w_dict["Ts_hcor"]+w_dict["CO2"]+w_dict["q"]+tmp+tmp2#+w_dict["w"]    

for i in range(len(sum_arr)):
    if np.isnan(sum_arr[i]) == True:
        sum_arr[i] = 0


index = np.where(sum_arr >= 1.3)

#for var in variables:
    
    #data_dict[var][index] = 0 ###mean_dict[var][index]*1


    
name = ""
for i in variables:
    name += i + "_"
    
dt = np.linspace(0,len(data_dict["time"])-1,seperation)
dt = np.round(dt).astype(int)


fig,ax = plt.subplots(4,1, sharex=True,figsize=(100,40))
test = np.zeros(data_dict["q"].shape)
test[index] = 1
for i in range(seperation-1):### default:seperation-1
    for j,var in enumerate(variables):

        interval = np.arange(dt[i], dt[i+1],1)
        ax[j].plot(interval,data_dict[var][dt[i]:dt[i+1]],linewidth=0.1,color = "k")
        ax2 = ax[j].twinx()
        
        ax2.plot(interval,test[dt[i]:dt[i+1]],linewidth=0.5,color = "b")
        ax2.set_ylim(0,2)
        
        
        locs = np.arange(dt[i],dt[i+1], 4000)
        
        plt.xticks(locs, data_dict["time"][locs])
        plt.xlabel("Date / Time")
        ax[j].set_ylabel(var +" in "+ units[j])
        #ax[0].set_ylim(280.5,284.0)
        #ax[1].set_ylim(-2.,2.)
        #ax[2].set_ylim(3.15,3.40)
        #ax[3].set_ylim(411,419)
        #ax[j].set_ylim(np.nanquantile(data_dict[var][dt[i]:dt[i+1]],0.9),np.nanquantile(data_dict[var][dt[i]:dt[i+1]],1))
                                        ####maybe find a better solution than quantile limits
        plt.xlim(interval[0],interval[-1])
        
        
        
    plt.tight_layout()
    
    plt.savefig(output_path + name + str(i) +"_timeseries_.png")
   
        
plt.close("all")






#name = ""
#for i in variables:
    #name += i + "_"
    
#dt = np.linspace(0,len(data_dict["time"])-1,seperation)
#dt = np.round(dt).astype(int)

#fig,ax = plt.subplots(4,1, sharex=True,figsize=(100,40))
    
#for i in range(1):
    #for j,var in enumerate(variables):

        #interval = np.arange(dt[i], dt[i+1],1)
        #ax[j].plot(interval,mean_dict[var][dt[i]:dt[i+1]],linewidth=0.1,color = "k")
        
        #locs = np.arange(dt[i],dt[i+1], 4000)
        
        #plt.xticks(locs, data_dict["time"][locs])
        #plt.xlabel("Date / Time")
        #ax[j].set_ylabel(var +" in "+ units[j])
        #ax[0].set_ylim(280.5,284.0)
        #ax[1].set_ylim(-2.,2.)
        #ax[2].set_ylim(3.15,3.40)
        #ax[3].set_ylim(411,419)
                                        #####maybe find a better solution than quantile limits
        #plt.xlim(interval[0],interval[-1])
        
        
    #plt.tight_layout()
    
    #plt.savefig(output_path + name + str(i) +"_mean_timeseries_.png")
   
        
#plt.close("all")
        