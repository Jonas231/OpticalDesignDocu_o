import numpy as np

filename = r"C:\D\optical design software demos (other than Zemax)\free software\KDP-2\CARDTEXT.dat"
def load_Gaussian(filename, nfob = 1):
    """
    read Gaussian beam propagation output, see p. 166 (KDP-Manual
    mainly: w(z) at 1/e^2, R(z), note: still need location!
    - The gaussian beam 1/e2 semi-diameter at each specified surface. = w(z)
    - The wavefront radius of curvature after interaction with each specified surface at that surface. = R(z)
    - The distance to the next beam waist after interaction with each specified surface. = thickness between surfaces
    - The gaussian beam 1/e2 semi-diameter at the next waist after interaction with each specified surface = w0
    :param filename:
    :param nfob:
    :return:
    """
    N_img = np.loadtxt(filename, skiprows=0, max_rows = 1,  dtype=np.str)
    N_img = int(np.char.replace(N_img, 'D', 'E').astype(np.float))
    #print(N_img)
    yfob_L = []
    xfob_L = []
    zobj_L = []
    xz_d_L = []
    yz_d_L = []
    xz_data_L = []
    yz_data_L = []
    for n in range(0, N_img+1):

        if nfob == 1:
            #print("n = ", n)
            yfob = np.loadtxt(filename, skiprows=4+n*18, max_rows=1, dtype='str')[-1]
            yfob = yfob.astype(float)
            yfob_L.append(yfob)

            xfob = np.loadtxt(filename, skiprows=5+n*18, max_rows=1, dtype='str')[-1]
            xfob = xfob.astype(float)
            xfob_L.append(xfob)

            zobj = np.loadtxt(filename, skiprows=6+n*18, max_rows=1, dtype='str')[-3]
            #print(zobj)
            zobj = zobj.astype(float)
            zobj_L.append(zobj)

            xz_d = np.loadtxt(filename, skiprows=7+n*18, max_rows=1, dtype='str')[-3]
            xz_d = xz_d.astype(float)
            xz_d_L.append(xz_d)

            xz_legend = np.loadtxt(filename, skiprows=13 + n * 18, max_rows=1, dtype='str')
            xz_data = np.loadtxt(filename, skiprows=14+n*18, max_rows=1, dtype='str')
            xz_data = xz_data.astype(float)
            xz_data_L.append(xz_data)

            yz_legend = np.loadtxt(filename, skiprows=17 + n * 18, max_rows=1, dtype='str')
            yz_data = np.loadtxt(filename, skiprows=18+n*18, max_rows=1, dtype='str')
            yz_data = yz_data.astype(float)
            yz_data_L.append(yz_data)
        else:
            for y in range(0, nfob):
                for x in range(0, nfob):

                    # print("n = ", n)
                    yfob = np.loadtxt(filename, skiprows=4 + n * 18*nfob*nfob + y*18 + x*18, max_rows=1, dtype='str')[-1]
                    yfob = yfob.astype(float)
                    yfob_L.append(yfob)

                    xfob = np.loadtxt(filename, skiprows=5 + n * 18*nfob*nfob + y*18 + x*18, max_rows=1, dtype='str')[-1]
                    xfob = xfob.astype(float)
                    xfob_L.append(xfob)

                    zobj = np.loadtxt(filename, skiprows=6 + n * 18*nfob*nfob + y*18 + x*18, max_rows=1, dtype='str')[-3]
                    # print(zobj)
                    zobj = zobj.astype(float)
                    zobj_L.append(zobj)

                    xz_d = np.loadtxt(filename, skiprows=7 + n * 18*nfob*nfob + y*18 + x*18, max_rows=1, dtype='str')[-3]
                    xz_d = xz_d.astype(float)
                    xz_d_L.append(xz_d)

                    xz_legend = np.loadtxt(filename, skiprows=13 + n * 18*nfob*nfob + y*18 + x*18, max_rows=1, dtype='str')
                    xz_data = np.loadtxt(filename, skiprows=14 + n * 18*nfob*nfob + y*18 + x*18, max_rows=1, dtype='str')
                    xz_data = xz_data.astype(float)
                    xz_data_L.append(xz_data)

                    yz_legend = np.loadtxt(filename, skiprows=17 + n * 18*nfob*nfob + y*18 + x*18, max_rows=1, dtype='str')
                    yz_data = np.loadtxt(filename, skiprows=18 + n * 18*nfob*nfob + y*18 + x*18, max_rows=1, dtype='str')
                    yz_data = yz_data.astype(float)
                    yz_data_L.append(yz_data)

    yfob_L = np.array(yfob_L)
    xfob_L = np.array(xfob_L)
    zobj_L = np.array(zobj_L)
    xz_d_L = np.array(xz_d_L)
    xz_data_L = np.array(xz_data_L)
    yz_data_L = np.array(yz_data_L)

    return yfob_L, xfob_L, zobj_L, (xz_legend, xz_data_L), (yz_legend, yz_data_L)

nfob = 11

yfob, xfob, zobj, xz_data, yz_data = load_Gaussian(filename, nfob = 1)

# compare results with single TEM00 Gaussian beam
# Rayleigh length
import math
w0 = 0.2       # waist [mm]
wavelength = 587.56e-6      # [mm]
zR = math.pi*w0**2/wavelength
# waist(z):
z = np.arange(0, 400+100, step = 100)
w = w0*np.sqrt(1+(z/zR)**2)
# wavefront radius(z)
R = z*(1 + (zR/z)**2)
# --> Übereinstimmung!