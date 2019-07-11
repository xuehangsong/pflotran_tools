import os
import numpy as np
import fileinput
import sys

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)


dir_prefix = "/global/cscratch1/sd/xhsong/sensitivity_2/old_pflotran/multi_realizations/"
final_file = "2duniform-000.h5"
input_file = "2duniform.in"
simu_dir = [dir_prefix+str(i+1)+"/" for i in range(6)]
nreaz = 2000

unfinished_reaz=dict()
for idir in simu_dir:
    unfinished_reaz[idir] = []    
    for ireaz in range(nreaz):
        if not os.path.isfile(idir+str(ireaz+1)+"/"+final_file):
            unfinished_reaz[idir].append(idir+str(ireaz+1)+"/")
#            print(idir+str(ireaz+1)+"/")

old_restart_line = "RESTART 2duniform-restart.chk"
new_restart_line = "### RESTART 2duniform-restart.chk"
for idir in simu_dir:
    if(len(unfinished_reaz)>0):
        for ireaz in unfinished_reaz[idir]:
            ireaz_input = ireaz+input_file
            replaceAll(ireaz_input,old_restart_line,new_restart_line)

old_restart_line = "WALLCLOCK_STOP 11.50 h"
new_restart_line = "WALLCLOCK_STOP 11.00 h"
for idir in simu_dir:
    if(len(unfinished_reaz)>0):
        for ireaz in unfinished_reaz[idir]:
            ireaz_input = ireaz+input_file
            replaceAll(ireaz_input,old_restart_line,new_restart_line)
            
            
for idir in simu_dir:
    if(len(unfinished_reaz)>0):
        unfinished_index = []
        for ireaz in unfinished_reaz[idir]:
            print(ireaz)
            unfinished_index.append(ireaz.split("/")[-2])
        fname = open(idir+"index.txt", 'w')
        fname.write("#!/bin/bash -l \n")
        fname.write("#SBATCH -A m1800 \n")
        fname.write("#SBATCH -q regular \n")
        fname.write("#SBATCH -N 1 \n")
        fname.write("#SBATCH --array="+",".join(unfinished_index)+" \n")    
        fname.write("#SBATCH -t 12:00:00 \n")
        fname.write("#SBATCH -J G"+idir.split("/")[-2]+" \n")
        fname.write("#SBATCH -L SCRATCH \n")
        fname.write("#SBATCH -C haswell \n")
        fname.write("echo SLURM_ARRAY_TASK_ID=${SLURM_ARRAY_TASK_ID} \n")
        fname.write("cd /global/cscratch1/sd/xhsong/sensitivity_2/old_pflotran/multi_realizations/"+idir.split("/")[-2]+"/${SLURM_ARRAY_TASK_ID} \n")
        fname.write("srun -n 24  ~/pflotran-edison-intel-old  -pflotranin 2duniform.in -realization_id 1 \n")    
        fname.close()
