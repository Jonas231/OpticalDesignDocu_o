# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 15:52:19 2022

@author: herbst
"""
import numpy as np
import matplotlib.pylab as plt
from matplotlib import cm
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors
import time 

t0 = time.perf_counter()


def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return np.array([sum_x/length, sum_y/length])



# execute "spo file C:\Work\OpTaliX\Test\spot.txt" in OpTaliX
# execute "psf file C:\Work\OpTaliX\Test\diff_psf.txt" in OpTaliX
# execute "psf file C:\Work\OpTaliX\Test\diff_psf.txt" in OpTaliX
filename = r'C:\Work\OpTaliX\Test\spot.txt'

filename_diff_psf = r'C:\Work\OpTaliX\Test\diff_psf.txt'
filename_diff_psf_info = r'C:\Work\OpTaliX\Test\PSF_PATCH.txt'

spotdata = np.loadtxt(filename)

diff_psfdata = np.loadtxt(filename_diff_psf,skiprows = 3 )[:,1:]
diff_psfdata_info = np.loadtxt(filename_diff_psf_info,skiprows = 1 )
wavl = diff_psfdata_info[0]
NA = diff_psfdata_info[1]
N_diff = diff_psfdata_info[2]
d = diff_psfdata_info[3]*N_diff
x = np.linspace(-d/2, d/2, num = int(N_diff))
X, Y = np.meshgrid(x,x)

r0 = 0.61*wavl*1e-3/(1*np.sin(NA))
#r02 = 

# plot diffraction psf

if 1:
    plt.close("all")
    fig_diff = plt.figure("diffraction psf")
    #ax = plt.subplot(111)
    ax = fig_diff.add_subplot(111, projection='3d')
    #ax.plot(x, diff_psfdata[0,:])
    if 1:
        ax.plot_wireframe(X, Y, diff_psfdata)
    else:
        Z = diff_psfdata
        norm = plt.Normalize(Z.min(), Z.max())
        colors = cm.viridis(norm(Z))
        rcount, ccount, _ = colors.shape
        surf = ax.plot_surface(X, Y, Z, rcount=rcount, ccount=ccount,
                               facecolors=colors, shade=False)
        surf.set_facecolor((0,0,0,0))
        plt.show()
