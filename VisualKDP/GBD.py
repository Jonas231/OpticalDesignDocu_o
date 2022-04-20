"""
Implements Gaussian Beam Decomposition:
see e.g: https://doi.org/10.1117/1.OE.54.3.035105

"""

import numpy as np

#
def create_Gaussians_mac(file, wry = 1, wrx = 1, bdy = 1, bdx = 1, TEM00 = 0):
    """
    Define a Gaussian beam
    """
    # Gaussian beam specification commands, p.69
    # WRY ... YZ-plane gaussian beam 1/e^2 diameter of surface 1
    # WRX ... XZ-plane [lens units]
    # BDY ... YZ-plane beam divergence of surface 1
    # BDX ... XZ-plane [mrad]
    # BDY TEM00 ... TEM00 mode laser beam
    # BDX TEM00

    file = open(file, "w")
    def write_line(file, L):
        file.writelines(L)
        file.write("\n")

    write_line(file, L=['u l'])
    write_line(file, L=['wry, '+str(wry)])
    write_line(file, L=['wrx, ' + str(wrx)])
    write_line(file, L=['bdy, '+str(bdy)])
    write_line(file, L=['bdx, ' + str(bdx)])
    if TEM00:
        write_line(file, L=['bdy TEM00'])
        write_line(file, L=['bdx TEM00'])
    write_line(file, L=['end'])
    file.close()

def Gaussian_prop(file, spec = 'BEAM', Nsur = 0, y_fob = 0, x_fob = 0, z_obj_shift = 0, wavelength =''):
    """
    GAUSSIAN BEAM PROPAGATION, p. 166 (KDP-Manual)
    :param file:
    :param spec:
    :return:
    """
    # GAUSSIAN BEAM PROPAGATION, p. 166
    file = open(file, "a+")
    def write_line(file, L):
        file.writelines(L)
        file.write("\n")

    write_line(file, L=['output cp'])
    #write_line(file, L=['output file GBD_results.dat'])
    write_line(file, L=['get isn'])
    write_line(file, L=['write'])
    for i in range(0, Nsur+1):
        write_line(file, L=['beam, '+str(i)+', '+str(y_fob)+', '+str(x_fob)+', '+str(z_obj_shift)+', '+str(wavelength)])
    write_line(file, L=['output tp'])
    file.close()

def multi_Gaussian_prop(file, spec = 'BEAM', Nsur = 0, y_fob = 0, x_fob = 0, z_obj_shift = 0, wavelength =''):
    # GAUSSIAN BEAM PROPAGATION, p. 166
    file = open(file, "a+")

    def write_line(file, L):
        file.writelines(L)
        file.write("\n")

    write_line(file, L=['output cp'])
    #write_line(file, L=['output file GBD_results.dat'])
    write_line(file, L=['get isn'])
    write_line(file, L=['write'])

    for i in range(0, Nsur + 1):
        #write_line(file, L=[str(Nsur)])
        for y in range(0,len(y_fob)):
            for x in range(0, len(x_fob)):

                write_line(file, L=['beam, ' + str(i) + ', ' + str(y_fob[y,x]) + ', ' + str(x_fob[y,x]) + ', ' + str(z_obj_shift) + ', ' + str(wavelength)])

    write_line(file, L=['output tp'])
    file.close()


path_KDP_mac = r'C:\D\optical design software demos (other than Zemax)\free software\KDP-2\GBD.DAT'

create_Gaussians_mac(path_KDP_mac, wry = 0.2, wrx = 0.2, bdy = 1, bdx = 1, TEM00 = 1)
Gaussian_prop(path_KDP_mac, spec = 'BEAM', Nsur = 5, y_fob = 0, x_fob = 0, z_obj_shift = 0, wavelength ='')

def fob_caob_arrays(lfob = 0, nfob = 1, lcaob = 0, ncaob = 1):
    # origin of wavefront on surface 0
    # (depends on fob definition - in [mm] or [angle])
    if lfob != 0 and nfob != 1:
        x_fob_a = np.linspace(-lfob, lfob, num = nfob)
        y_fob_a = np.linspace(-lfob, lfob, num = nfob)
    else:
        x_fob_a = 0
        y_fob_a = 0
    # center of clear aperture assigned to surface 1
    # (for each of the above defined origins)
    if lfob != 0 and nfob != 1:
        x_caob_a = np.linspace(-lcaob, lcaob, num = ncaob)
        y_caob_a = np.linspace(-lcaob, lcaob, num = ncaob)
    else:
        x_caob_a = 0
        y_caob_a = 0

    if lfob != 0 and nfob != 1:
        xx_fob, yy_fob = np.meshgrid(x_fob_a, y_fob_a)
    else:
        xx_fob = 0
        yy_fob = 0
    if lcaob != 0 and ncaob != 1:
        xx_caob, yy_caob = np.meshgrid(x_caob_a, y_caob_a)
    else:
        xx_caob = 0
        yy_caob = 0
    #return x_fob_a, y_fob_a, x_caob_a, y_caob_a
    return xx_fob, yy_fob, xx_caob, yy_caob


xx_fob, yy_fob, xx_caob, yy_caob = fob_caob_arrays(lfob = 0, nfob = 1, lcaob = 0, ncaob = 1)
xx_fob, yy_fob, xx_caob, yy_caob = fob_caob_arrays(lfob = 10, nfob = 11, lcaob = 0, ncaob = 1)

#multi_Gaussian_prop(path_KDP_mac, spec = 'BEAM', Nsur = 5, y_fob = yy_fob, x_fob = xx_fob, z_obj_shift = 0, wavelength ='')


# define normalized 2D gaussian
def gaus2d(x=0, y=0, mx=0, my=0, sx=1, sy=1):

    g = 1. / (2. * np.pi * sx * sy) * np.exp(-((x - mx)**2. / (2. * sx**2.) + (y - my)**2. / (2. * sy**2.)))
    return g

def FWHMofGauss(c):
    FWHM = 2*np.sqrt(2*np.log(2))*c
    r_1overesquared = np.sqrt(2)*FWHM/(2*np.sqrt(np.log(2)))
    return FWHM, r_1overesquared


Lim = -10
x = np.linspace(-Lim, Lim)
y = np.linspace(-Lim, Lim)
x, y = np.meshgrid(x, y) # get 2D variables instead of 1D

from matplotlib.patches import Ellipse
# produce various displaced Gaussians
Nx = 20
Ny = 20
a = 1
import matplotlib.pylab as plt
colors = plt.cm.jet(np.linspace(0,1,Nx))
Centersx = np.linspace(-Lim*a,Lim*a,num = Nx)
Centersy = np.linspace(-Lim*a,Lim*a,num = Ny)
ells = []
for ix in range(0, Nx):
    for iy in range(0, Ny):
        g = gaus2d(x, y, mx=Centersx[ix], my=Centersy[iy], sx=1, sy=1)
        if ix == 0 and iy == 0:
            z = g
        else:
            z += g
        FWHM, r = FWHMofGauss(1)
        ells.append(Ellipse(xy=(Centersx[ix],Centersy[iy]),width=r,
                height=r, angle=0, edgecolor=colors[ix], lw=1, facecolor='none'))

from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


fig = plt.figure()

# syntax for 3-D plotting
ax = plt.subplot(121,projection='3d')

# syntax for plotting
ax.plot_surface(x, y, z, cmap='viridis', edgecolor='black', lw=0.5, rstride=1, cstride=1, alpha=0.5)
ax2 = plt.subplot(122)
for e in ells:
    ax2.add_artist(e)
b = 1.2
ax2.set_xlim(-10*b,10*b)
ax2.set_ylim(-10*b,10*b)
ax2.set_aspect('equal', adjustable='box')
ax.set_title('2d Gaussian')
plt.subplots_adjust(left = 0.05, right = 0.95,wspace = 0.5)
plt.show()