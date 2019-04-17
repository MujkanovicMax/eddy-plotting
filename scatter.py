import numpy as np
import matplotlib.pyplot as plt

data_arr = np.loadtxt("./20190402-170845.csv",delimiter=";", skiprows = 1, usecols=(1,2,3,4,5,6,7,8))

data_dict = {"u":None,"v":None,"w":None,"Ts":None,"Ts_hcor":None,"q":None,"CO2":None,"p":None}

data_dict["u"] = data_arr[:,0]
data_dict["v"] = data_arr[:,1]
data_dict["w"] = data_arr[:,2]
data_dict["Ts"] = data_arr[:,3]
data_dict["Ts_hcor"] = data_arr[:,4]
data_dict["q"] = data_arr[:,5]*1000
data_dict["CO2"] = data_arr[:,6]
data_dict["p"] = data_arr[:,7]


x1=[1]
y1=[1]

data_names = np.array(["w","Ts_hcor","q","CO2"])

for i in data_names:
    

#plt.subplot(1,1,1)
#H1,x1,y1=np.histogram2d(data_dict["w"], data_dict["Ts_hcor"],bins=100, range=[[np.nanmin(data_dict["w"]),np.nanmax(data_dict["w"])],[np.nanmin(data_dict["Ts_hcor"]),np.nanmax(data_dict["Ts_hcor"])]])
#H1 = H1.T
#X, Y = np.meshgrid(x1, y1)
#plt.pcolormesh(X, Y, H1)
#plt.xlabel('w in m/s')
#plt.ylabel('Ts_hcor in K')
#plt.xlim(np.nanmin(data_dict["w"]),np.nanmax(data_dict["w"]))
#plt.ylim(np.nanmin(data_dict["Ts_hcor"]),np.nanmax(data_dict["Ts_hcor"]))

#plt.subplot(1,1,1)
#H2,x1,y1=np.histogram2d(data_dict["w"], data_dict["q"],bins=100, range=[[np.nanmin(data_dict["w"]),np.nanmax(data_dict["w"])],[np.nanmin(data_dict["q"]),np.nanmax(data_dict["q"])]])
#H2 = H2.T
#X, Y = np.meshgrid(x1, y1)
#plt.pcolormesh(X, Y, H2)
#plt.xlabel('w in m/s')
#plt.ylabel('q in g/kg')
#plt.xlim(np.nanmin(data_dict["w"]),np.nanmax(data_dict["w"]))
#plt.ylim(np.nanmin(data_dict["q"]),np.nanmax(data_dict["q"]))

#plt.figure()
#H3,x1,y1=np.histogram2d(data_dict["w"], data_dict["CO2"],bins=100, range=[[np.nanmin(data_dict["w"]),np.nanmax(data_dict["w"])],[np.nanmin(data_dict["CO2"]),np.nanmax(data_dict["CO2"])]])
#H3 = H3.T
#X, Y = np.meshgrid(x1, y1)
#plt.pcolormesh(X, Y, H3)
#plt.xlabel('w in m/s')
#plt.ylabel('CO2 conc in ppm')
#plt.xlim(np.nanmin(data_dict["w"]),np.nanmax(data_dict["w"]))
#plt.ylim(np.nanmin(data_dict["CO2"]),np.nanmax(data_dict["CO2"]))

#plt.subplot(1,1,1)
#H4,x1,y1=np.histogram2d(data_dict["Ts_hcor"], data_dict["q"],bins=100, range=[[np.nanmin(data_dict["Ts_hcor"]),np.nanmax(data_dict["Ts_hcor"])],[np.nanmin(data_dict["q"]),np.nanmax(data_dict["q"])]])
#H4 = H4.T
#X, Y = np.meshgrid(x1, y1)
#plt.pcolormesh(X, Y, H4)
#plt.xlabel('Ts_hcor in K')
#plt.ylabel('q in g/kg')
#plt.xlim(np.nanmin(data_dict["Ts_hcor"]),np.nanmax(data_dict["Ts_hcor"]))
#plt.ylim(np.nanmin(data_dict["q"]),np.nanmax(data_dict["q"]))

plt.subplot(1,1,1)
H5,x1,y1=np.histogram2d(data_dict["Ts_hcor"], data_dict["CO2"],bins=100, range=[[np.nanmin(data_dict["Ts_hcor"]),np.nanmax(data_dict["Ts_hcor"])],[np.nanmin(data_dict["CO2"]),np.nanmax(data_dict["CO2"])]])
H5 = H5.T
X, Y = np.meshgrid(x1, y1)
plt.pcolormesh(X, Y, H5)
plt.xlabel('Ts_hcor in K')
plt.ylabel('CO2 conc in ppm')
plt.xlim(np.nanmin(data_dict["Ts_hcor"]),np.nanmax(data_dict["Ts_hcor"]))
plt.ylim(np.nanmin(data_dict["CO2"]),np.nanmax(data_dict["CO2"]))

#plt.figure()
#H6,x1,y1=np.histogram2d(data_dict["q"], data_dict["CO2"],bins=100, range=[[np.nanmin(data_dict["q"]),np.nanmax(data_dict["q"])],[np.nanmin(data_dict["CO2"]),np.nanmax(data_dict["CO2"])]])
#H6 = H6.T
##plt.imshow(H6, interpolation="nearest", origin="low", extent=[x1[0], x1[-1], y1[0], y1[-1]])
#X, Y = np.meshgrid(x1, y1)
#plt.pcolormesh(X, Y, H6)
#plt.xlabel('q in g/kg')
#plt.ylabel('CO2 conc in ppm')
#plt.xlim(np.nanmin(data_dict["q"]),np.nanmax(data_dict["q"]))
#plt.ylim(np.nanmin(data_dict["CO2"]),np.nanmax(data_dict["CO2"]))

plt.tight_layout()

plt.savefig("Thcor__CO2_hist.png",dpi=1000)
