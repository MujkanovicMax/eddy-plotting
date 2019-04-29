import numpy as np
import matplotlib.pyplot as plt
from timeseries import plotTimeseries

########################################################################################################################################
##################################                Inputs                    ############################################################
########################################################################################################################################

input_path  = "./20190416-000000.csv"       #enter where to get input data
output_path = "./timeseries/"               #enter where output data should end up
variables   = ["Ts_hcor","q","w","p","CO2"]     #enter vars you want to plot
units       = ["K","g/kg","m/s","rad","ppm"]      #enter units for vars you want to plot 
seperation  = 51                           #how man seperate plots you want( -1) 

########################################################################################################################################
##################################              Array Stuff                 ############################################################
########################################################################################################################################

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

tmp = np.zeros(data_dict["Ts_hcor"].shape)
tmp2 = np.zeros(data_dict["q"].shape)

#######################################################################################################################################
#################################            masks for running mean            ########################################################
#######################################################################################################################################


mask_Ts = np.ones((500,))/500.              ###10 data points measured roughly every second 
mask_w  = np.ones((50,))/50.
mask_q  = np.ones((100,))/100.
mask_CO2= np.ones((60,))/60.
mask_dict = {"time":None,"u":mask_w,"v":mask_w,"w":mask_w,"Ts":None,"Ts_hcor":mask_Ts,"q":mask_q,"CO2":mask_CO2,"p":mask_w}

#######################################################################################################################################
#################################              Parameters                  ############################################################
#######################################################################################################################################

#ger_mean_temp = 15 + 273.15        ###roughly the mean temperature of germany (yearly avg)
indoor_temp = 20 + 273.15           ### room(toilet) temperature ( roughly ) 
indoor_RH = 30                      ### rough estimate of indoor RH
indoor_q  = 0.622 * indoor_RH/(100.*1013)*6.112*np.exp((17.62 * (indoor_temp-273.15))/(243.12+(indoor_temp-273.15)))    ###indoor q
indoor_q = indoor_q*1000    ###g/kg


#######################################################################################################################################
#################################              Running Mean                ############################################################
#######################################################################################################################################

for j,var in enumerate(variables):

        
        #data_dict[var][np.where(np.isnan(data_dict[var]) == True)] = 0
        mean_dict[var] = np.convolve(data_dict[var],mask_dict[var] ,mode="same")*1
        diff = np.abs(data_dict[var]-mean_dict[var])
        w_dict[var] = 1-np.exp(-diff/np.nanstd(data_dict[var]))
        #w_dict[var] = w_dict[var]/np.nansum(w_dict[var]) * 10

for j,var in enumerate(["u","v","w"]):

        
        #data_dict[var][np.where(np.isnan(data_dict[var]) == True)] = 0
        mean_dict[var] = np.convolve(data_dict[var],mask_dict[var] ,mode="same")*1
        diff = np.abs(data_dict[var]-mean_dict[var])
        w_dict[var] = 1-np.exp(-diff/np.nanstd(data_dict[var]))    
######################################################################################################################################
################################             Termperature weighting             ######################################################
######################################################################################################################################

sigma = 15                                                                          #np.nanstd(data_dict["Ts_hcor"]-indoor_temp)
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

#######################################################################################################################################
#################################                 Humidity weighting             ######################################################
#######################################################################################################################################

sigma = 1.5                                                                             #np.nanstd(data_dict["q"]-indoor_q)
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
        
#######################################################################################################################################
#################################             Windvector/angle weighting         ######################################################
#######################################################################################################################################    

angle_w = np.zeros(data_dict["w"].shape)
u = mean_dict["u"]
v = mean_dict["v"]
w = mean_dict["w"]

for i in range(len(data_dict["w"])):
    angle_w[i] = np.arccos(np.dot(np.array([u[i],v[i],w[i]]), np.array([0,0,1]))/(np.sqrt(u[i]*u[i]+v[i]*v[i]+w[i]*w[i]))) 
 
angle_w = np.exp(-angle_w/np.pi)
 
#######################################################################################################################################
#################################             Score calculation/Filter mask      ######################################################
#######################################################################################################################################        
        
sum_arr = w_dict["Ts_hcor"]+w_dict["CO2"]+w_dict["q"]+tmp+tmp2#+w_dict["w"]    

#for i in range(len(sum_arr)):
    #if np.isnan(sum_arr[i]) == True:
        #sum_arr[i] = 0

sum_arr[np.where(np.isnan(sum_arr) == True)] = 0


index = np.where(sum_arr >= 1.3)



#for var in variables:
    
    #data_dict[var][index] = 0 ###mean_dict[var][index]*1

#######################################################################################################################################
#################################              Plotting Loop               ############################################################
#######################################################################################################################################
#u = mean_dict["u"]
#v = mean_dict["v"]
#w = mean_dict["w"]
#mean_dict["time"] = data_dict["time"]
#data_dict["w"] = mean_dict["w"]

#for i in range(len(data_dict["w"])):
    #data_dict["p"][i] = np.arccos(np.dot(np.array([u[i],v[i],w[i]]), np.array([0,0,1]))/(np.sqrt(u[i]*u[i]+v[i]*v[i]+w[i]*w[i]))) 

#data_dict["p"][np.where(data_dict["p"] >= 1.6)] = 1.6 

#plotTimeseries(data_dict, variables, units, seperation, output_path, test = 20, lw = 0.5)
    


