from scipy.interpolate import RegularGridInterpolator
import numpy as np
import h5py as h5


def model_to_proj(origin, angle, coord):
    return([origin[0]+coord[0]*np.cos(angle)-coord[1]*np.sin(angle),
            origin[1]+coord[0]*np.sin(angle)+coord[1]*np.cos(angle)])


def proj_to_model(origin, angle, coord):
    return([(coord[0]-origin[0])*np.cos(angle) + (coord[1]-origin[1])*np.sin(angle),
            (coord[1]-origin[1])*np.cos(angle) - (coord[0]-origin[0])*np.sin(angle)])


simu_dir = "/pic/dtn/shua784/John_case_optim_5/"
ori_simu = h5.File(simu_dir+"combined.h5", "r")
#ori_simu = h5.File(simu_dir+"pflotran_bigplume-001.h5", "r")
new_simu_template = h5.File(simu_dir+"1.6km_template.h5", "r")
output_file = h5.File(simu_dir+"mapped.h5", "w")

ori_mesh = dict()
ori_mesh["x0"] = 593000
ori_mesh["y0"] = 114500
ori_mesh["z0"] = 88
ori_mesh["rot"] = 0


new_mesh = dict()
new_mesh["x0"] = 594186
new_mesh["y0"] = 115943
new_mesh["z0"] = 90
new_mesh["rot"] = 15/180*np.pi


x = ori_simu["Coordinates"]["X [m]"][:]
y = ori_simu["Coordinates"]["Y [m]"][:]
z = ori_simu["Coordinates"]["Z [m]"][:]
dx = np.diff(x)
dy = np.diff(y)
dz = np.diff(z)

nx = len(dx)
ny = len(dy)
nz = len(dz)
x = x[0: nx] + 0.5 * dx
y = y[0: ny] + 0.5 * dy
z = z[0: nz] + 0.5 * dz
ori_mesh["x"] = x
ori_mesh["y"] = y
ori_mesh["z"] = z
ori_mesh["nx"] = nx
ori_mesh["ny"] = ny
ori_mesh["nz"] = nz


x = new_simu_template["Coordinates"]["X [m]"][:]
y = new_simu_template["Coordinates"]["Y [m]"][:]
z = new_simu_template["Coordinates"]["Z [m]"][:]
dx = np.diff(x)
dy = np.diff(y)
dz = np.diff(z)

nx = len(dx)
ny = len(dy)
nz = len(dz)
x = x[0: nx] + 0.5 * dx
y = y[0: ny] + 0.5 * dy
z = z[0: nz] + 0.5 * dz
new_mesh["x"] = x
new_mesh["y"] = y
new_mesh["z"] = z
new_mesh["nx"] = nx
new_mesh["ny"] = ny
new_mesh["nz"] = nz

new_grids = [[ix, iy, iz] for ix in x for iy in y for iz in z]

mapping_grids = [model_to_proj(
    [new_mesh["x0"], new_mesh["y0"]], new_mesh["rot"], igrid[0:2]) for igrid in new_grids]
mapping_grids = [proj_to_model(
    [ori_mesh["x0"], ori_mesh["y0"]], ori_mesh["rot"], igrid) for igrid in mapping_grids]
mapping_grids = np.c_[np.asarray(mapping_grids), np.asarray(new_grids)[:, 2]]

output_group = ["Coordinates", "Provenance"]
for igroup in output_group:
    print(igroup)
    new_simu_template.copy(igroup, output_file)

times_str = [T for T in list(ori_simu.keys()) if "Time:" in T]
for itime in times_str:
    print(itime)
    group = output_file.create_group(itime)
    for idataset in list(ori_simu[itime].keys()):
        dataset_interpolator = RegularGridInterpolator(
            (ori_mesh["x"], ori_mesh["y"], ori_mesh["z"]),
            ori_simu[itime][idataset].value,
            method="nearest")
        interp_dataset = dataset_interpolator(mapping_grids)
        group.create_dataset(idataset, data=interp_dataset.reshape(
            (new_mesh['nx'], new_mesh['ny'], new_mesh['nz']), order="C"))

output_file.close()
new_simu_template.close()
ori_simu.close()
