import numpy as np

filename = r"C:\D\optical design software demos (other than Zemax)\free software\KDP-2\SPD.ASC"
def load_spd(filename):
    N_rays = int(np.loadtxt(filename, skiprows=0, max_rows = 1))-1
    spd_L = []
    for n in range(0, N_rays):
        #print("n = ", n)
        spd = np.loadtxt(filename, skiprows=1+n*25, max_rows=25, dtype='str')
        spd = np.char.replace(spd, 'D', 'E').astype(np.float)
        spd_L.append(spd)
    spd_L = np.array(spd_L)

    # x,y,z, l, m, n and wavelength number of chief ray at object surface
    # see KDP-2 manual, p. 178
    chief_ray_info = np.loadtxt(filename, skiprows = 1+n*25 + 25, max_rows = 6, dtype = 'str')
    chief_ray_info = np.char.replace(chief_ray_info , 'D', 'E').astype(np.float)
    return chief_ray_info, spd_L

chief_ray_info, spd_L = load_spd(filename)

import matplotlib as mpl
import matplotlib.pyplot as plt
mpl.rcParams['mathtext.default'] = 'regular'
plt.close("all")

def plot_spot_diag(spd_L, unit = "mum"):
    #unit = "mm"
    if unit == "mum":
        unit = "$\mu$m"
    if unit == "mm":
        fac = 1
    if unit == "$\mu$m":
        fac = 1000
    fig = plt.figure("spd", figsize =(4,4))
    ax = plt.subplot(111)
    ax.title.set_text('spot diagram')
    points_xy = spd_L[:,0,:]

    ax.set_xlabel('x-dist. / '+str(unit))
    ax.set_ylabel('y-dist. / '+str(unit))
    plt.minorticks_on()
    plt.grid(which='major', axis='both', color = 'lightgray', linestyle = ':')
    plt.grid(which='minor', axis='both', color = 'lightgray', linestyle = ':')
    plt.subplots_adjust(left=0.25, bottom=0.25, right=None, top=None, wspace=None, hspace=None)

    def centroidnp(arr):
        length = arr.shape[0]
        sum_x = np.sum(arr[:, 0])
        sum_y = np.sum(arr[:, 1])
        return sum_x/length, sum_y/length

    centroid = centroidnp(points_xy)
    ax.tick_params(axis='both', which = 'both', direction = 'in')

    points_xc = points_xy[:,0]-centroid[0]
    points_yc = points_xy[:,1]-centroid[1]
    ax.scatter(points_xc*fac, points_yc*fac, marker = '+', color = 'blue', linewidth = 0.25)
    centroidc = (0,0)
    ax.axhline(y=centroidc[1]*fac, color='lime', linestyle='--', linewidth = 0.5)
    ax.axvline(x=centroidc[0]*fac, color='lime', linestyle='--', linewidth = 0.5)


    Max = np.abs(np.max(points_xc*fac))
    Min = np.abs(np.min(points_xc*fac))
    Limx = np.max([Max,Min])
    Max = np.abs(np.max(points_yc*fac))
    Min = np.abs(np.min(points_yc*fac))
    Limy = np.max([Max,Min])

    Lim = np.max([Limx,Limy])
    ax.set_xlim(-Lim,Lim)
    ax.set_ylim(-Lim,Lim)

    ax.annotate(str(np.round(centroid,decimals = 3))+" mm", (centroidc[0]+Lim/20, centroidc[1]+Lim/20), fontsize = 8, color = 'lime')

    start = -np.floor(Lim*10)/10
    end = -start
    stepsize = end/2
    ax.xaxis.set_ticks(np.arange(start, end+stepsize, stepsize))
    ax.yaxis.set_ticks(np.arange(start, end+stepsize, stepsize))

plot_spot_diag(spd_L, unit = "mum")
