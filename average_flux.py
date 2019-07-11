import h5py as h5
import numpy as np
import matplotlib.pyplot as plt

simu_dir = "/global/cscratch1/sd/xhsong/npt/base/multi/"

coord = h5.File(simu_dir+"Coordinates", "r")
x = coord["Coordinates"]["X [m]"][:]
y = coord["Coordinates"]["Y [m]"][:]
z = coord["Coordinates"]["Z [m]"][:]
dx = np.diff(x)
dy = np.diff(y)
dz = np.diff(z)
nx = len(dx)
ny = len(dy)
nz = len(dz)
ox = x[0]
oy = y[0]
oz = z[0]
ex = x[-1]
ey = y[-1]
ez = z[-1]
x = x[0:-1]+0.5*dx
y = y[0:-1]+0.5*dy
z = z[0:-1]+0.5*dz
coord.close()

selected_z = np.where(z < 104)[0]

fname = "Time:  "+"{:6.5E}".format(itime)+" h"
snapshot = h5.File(simu_dir+fname, "r")
material = snapshot[fname]["Material_ID"][:]
snapshot.close()

material_x = material[1:-1, :, selected_z]
material_y = material[:, 1:-1, selected_z]


average_darcy = []
# for itime in np.arange(70125, 70127):
for itime in np.arange(8784, 70127):
    fname = "Time:  "+"{:6.5E}".format(itime)+" h"
    snapshot = h5.File(simu_dir+fname, "r")
    x_darcy = snapshot[fname]["Liquid X-Flux Velocities"][:]
    x_darcy = np.array([0.5*x_darcy[x, :, :]+0.5*x_darcy[x+1, :, :]
                        for x in range(x_darcy.shape[0]-1)])
    x_darcy = x_darcy[:, :, selected_z]
    y_darcy = snapshot[fname]["Liquid Y-Flux Velocities"][:]
    y_darcy = np.array([0.5*y_darcy[:, x, :]+0.5*y_darcy[:, x, :]
                        for x in range(y_darcy.shape[1]-1)])
    y_darcy = np.swapaxes(y_darcy, 0, 1)
    y_darcy = y_darcy[:, :, selected_z]
    snapshot.close()

    single_darcy = [itime, np.mean(x_darcy[material_x == 1]),
                    np.mean(y_darcy[material_y == 1])]
    print(single_darcy)
    average_darcy.append(single_darcy)

np.savetxt("average_hanford_darcy.txt",
           np.array(average_darcy),
           delimiter=',',
           header="t(h), x(m/h), y(m/h)")

imgfile = "test.png"
fig = plt.figure()
ax = plt.subplot(111)
ax.plot(np.array(average_darcy)[:, 0], np.array(
    average_darcy)[:, 1], label="vx")
ax.plot(np.array(average_darcy)[:, 0], np.array(
    average_darcy)[:, 2], label="vy")
ax.legend()
fig.savefig(imgfile)
plt.close(fig)
