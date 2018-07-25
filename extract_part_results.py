import h5py as h5
import os
import numpy as np

os.chdir("/global/cscratch1/sd/xhsong/flux_estimation")

case_name = "homo_2"
output_name = "homo_2_24"
pflotran_name = "pflotran_ERT"
datafile = h5.File(case_name+"/"+pflotran_name+".h5","r")   
output_times = range(8760,(8760+100*24))
output_times = range(8760,21889,24)

if os.path.isfile(case_name+"/"+output_name+".h5"):
    os.remove(case_name+"/"+output_name+".h5")  

output_file = h5.File(case_name+"/"+output_name+".h5","w")   

output_group = ["Coordinates","Provenance"]
for itime in output_times:
    groupname = "Time:  "+"{0:.5E}".format(itime)+" h"
    output_group = np.append(output_group,groupname)
for igroup in output_group:
    print(igroup)
    datafile.copy(igroup,output_file)
datafile.close()
output_file.close()

#output_file = h5.File(case_name+"/"+output_name+".h5","r")   
# if os.path.isfile(case_name+"/"+output_name+".h5"):
#     os.remove(case_name+"/"+output_name+".h5")  
#groupnames = list(datafile.keys())





print("Hello World!")
