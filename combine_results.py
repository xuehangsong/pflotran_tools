import h5py as h5
import os
import numpy as np
import glob
from shutil import copyfile

simu_dir = "/pic/dtn/shua784/John_case_optim_5/"
simu_files = glob.glob(simu_dir+"pflotran*h5")
combined_file = simu_dir+"combined.h5"
# copyfile(simu_files[0], combined_file)

output_file = h5.File(combined_file, "w")
for ifile in simu_files:
    print(ifile)
    datafile = h5.File(ifile, "r")
    # times_str = [T for T in list(datafile.keys()) if "Time:" in T]
    # for igroup in times_str:
    groups = [T for T in list(datafile.keys()) if "Time:" in T]
    if ifile == simu_files[0]:
        groups = list(datafile.keys())
    for igroup in groups:
        print(igroup)
        datafile.copy(igroup, output_file)
    datafile.close()
output_file.close()


print("Hello World!")
