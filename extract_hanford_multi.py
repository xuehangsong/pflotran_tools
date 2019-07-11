# SUMMARY:      pt_mainpy
# USAGE:        extract velocity values from Hanford simulation
# ORG:          Pacific Northwest National Laboratory
# AUTHOR:       Xuehang Song
# E-MAIL:       xuehang.song@pnnl.gov
# ORIG-DATE:    Dec-2018
# DESCRIPTION:
# DESCRIPTION-END


import h5py as h5
import os
import glob
import numpy as np
import matplotlib.pyplot as plt

reazs = [8+12*x for x in  range(20)]

# h5_index = np.arange(3)
# reazs = [8+12*x for x in  range(2)]

for index_ireaz,ireaz in enumerate(reazs):
    print(ireaz)

    h5_prefix = "/global/cscratch1/sd/chenxy/Xuehang/240_1/"+str(ireaz)+"/2duniform-"

    h5_files = np.sort(glob.glob(h5_prefix+"*"+".h5"))    

    csv_file = "/global/homes/x/xhsong/averaged_vec/"+str(index_ireaz)+".csv"
    fig_name = "/global/homes/x/xhsong/averaged_vec/"+str(index_ireaz)+".png"

    ave_vec = []
    times = []
    for ifile in h5_files:
        print(ifile)

        simu_file = h5.File(ifile,"r")
        time_index = [x for x in list(simu_file.keys()) if "Time" in x][0]

        #get x,y,z
        x = simu_file["Coordinates"]["X [m]"][:]
        x = x[0:-1]+np.diff(x)*0.5
        nx = len(x)
        z = simu_file["Coordinates"]["Z [m]"][:]
        z = z[0:-1]+np.diff(z)*0.5    
        nz = len(z)
        y = np.asarray([1])
        ny = 1
        # x_array = np.tile(x.reshape(nx,1,1),nz)
        # x_array = np.repeat(x,nz).reshape(nx,1,nz)
        x_array = np.meshgrid(y,x,z)[1]
        z_array = np.meshgrid(y,x,z)[2]    


        material = simu_file[time_index]['Material_ID'][:]
        vec_x = simu_file[time_index]['Liquid X-Velocity [m_per_h]'][:]
        satu = simu_file[time_index]['Liquid_Saturation'][:]
        selected_cell = (satu>=0.999999999999999)*(material==1)
        ave_vec+=[np.average(vec_x[selected_cell],weights=x_array[selected_cell]*z_array[selected_cell])]
        times+=[float(time_index.split(" ")[2])]


    vec_output = np.column_stack((times,ave_vec))

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(vec_output[:,0],vec_output[:,1])
    ax.set_ylabel("Darcy vec (m/h)")
    ax.set_xlabel('Time (h)')
    ax.ticklabel_format(style="sci", axis="xy", scilimits=(0, 0))
    fig.tight_layout()
    fig.savefig(fig_name, dpi=600, transparent=False)
    fig.clf()


    np.savetxt(csv_file,vec_output,delimiter=",",header="Time (h),Darcy Vec (m/h)")
