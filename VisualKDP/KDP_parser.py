# this is a basic file to test things
import time
import math

start = time.time()
import numpy as np

def search_string_in_file(file_name, string_to_search, not_string = "!"):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    # see: https://thispointer.com/python-search-strings-in-a-file-and-get-line-numbers-of-lines-containing-the-string/

    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line and (not_string not in line):
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    # L = np.array(list_of_results)
    return read_obj, np.array(list_of_results)

def search_string(file_name,read_obj, string_to_search, not_string = '!', not_string2 = '!'):
    line_number = 0
    list_of_results = []
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line and (not_string not in line) and (not_string2 not in line):
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    return np.array(list_of_results)


def return_optical_data(file_name,r, L):
    """
    COATING ,   0.00000000000000
    CV      ,   0.00000000000000
    TH      ,  0.100000000000000E+21
    RAYERROR   0.00000000000000
    AIR
    """
    # Open the file in read only mode
    #with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
    #    for line in read_obj:
    coating_L = []
    cv_L = []
    th_L = []

    rayerror_L = []
    mat_L = []
    #print("L = ", L[:,0])

    L_EOS = search_string(file_name, r, "EOS")  # FLDSRAYS
    line_EOS = np.float(L_EOS[0][0])

    for i in range(0, len(L)):
        coating = np.float(np.loadtxt(file_name, skiprows = int(L[i,0]), max_rows = 1,dtype='str')[2])
        coating_L.append(coating)
        cv = np.float(np.loadtxt(file_name,skiprows=int(L[i, 0])+1, max_rows=1,dtype='str')[2])
        cv_L.append(cv)
        #th = np.float(np.loadtxt(file_name,skiprows=int(L[i, 0])+2, max_rows=1,dtype='str')[2])
        #th_L.append(th)
        #rayerror = np.loadtxt(file_name,skiprows=int(L[i, 0])+3, max_rows=1,dtype='str')[1]
        #rayerror_L.append(rayerror)
        #mat = np.loadtxt(file_name,skiprows=int(L[i, 0])+4, max_rows=1,dtype='str')
        #mat_L.append(mat)
        #print(rayerror)
    #print(mat_L)
    #print(rayerror_L)
    coating = np.array(coating_L)
    cv = np.array(cv_L)
    #th = np.array(th_L)
    rayerror = np.array(rayerror_L)
    #mat = np.array(mat_L)

    cc_L = []
    L_cc = search_string(file_name, r, "CC")
    #print("L_cc: ", L_cc)
    for i in range(0, len(L_cc)):
        if (int(L_cc[i,0])-1)< line_EOS:
            cc = np.array(np.loadtxt(file_name, skiprows = int(L_cc[i,0])-1, max_rows = 1,dtype='str'))[2]
            #print("clap:", cc)
            cc_L.append(cc)
    cc = np.array(cc_L)
    print("cc: ", cc)
    cc_pos_L = []
    for j in range(0,len(L_cc)):
        if (int(L_cc[j, 0]) - 1) < line_EOS:
            cc_pos = np.min(np.argwhere(L_cc[j, 0] <= L[:, 0]))-1
            cc_pos_L.append(cc_pos)
    cc_pos = np.unique(np.array(cc_pos_L))

    th_L = []
    L_th = search_string(file_name, r, "TH", not_string = "FOLLOWING", not_string2 = "THM")
    print("L_th: ", L_th)
    for i in range(0, len(L_th)):
        th = np.array(np.loadtxt(file_name, skiprows = int(L_th[i,0])-1, max_rows = 1,dtype='str'))
        print("th:", th)
        th_L.append(th)
    th = np.array(th_L)[:,2].astype(np.float)

    def find_elem(file_name, r, keyword):
        clap_L = []
        L_clap = search_string(file_name, r, keyword)       # clear aperture
        #print("L_clap: ", L_clap, len(L_clap))
        for i in range(0, len(L_clap)):
            clap = np.array(np.loadtxt(file_name, skiprows = int(L_clap[i,0])-1, max_rows = 1,dtype='str'))
            #print("clap:", clap)
            clap_L.append(clap)
        print("clap_L: ", clap_L)
        clap = clap_L#np.array(clap_L)
        #print(L_clap[:,0])
        clap_pos_L = []
        for j in range(0, len(L_clap)):
            if L_clap[j,0] <= L[-1,0]:
                clap_pos = np.min(np.argwhere(L_clap[j,0] <= L[:,0]))-1
            else:
                clap_pos = len(L)-1
            clap_pos_L.append(clap_pos)
        return clap, clap_pos_L

    clap, clap_pos_L = find_elem(file_name, r, keyword = "CLAP")
    thm_L = []
    thm_pos_L = []
    L_thm = search_string(file_name, r, "THM")  # clear aperture
    #thm_pos = np.argwhere(L_thm[:, 0] <= L[:, 0])
    #print("L_thm: ", np.array(L_thm[:,0]))
    for j in range(0,len(L_thm)):
        thm_pos = np.min(np.argwhere(L_thm[j, 0] <= L[:, 0]))-1
        thm_pos_L.append(thm_pos)

    #print("thm_pos: ", thm_pos_L)
    for i in range(0, len(L_thm)):
        thm = np.array(np.loadtxt(file_name, skiprows = int(L_thm[i,0])-1, max_rows = 1,dtype='str'))
        #print("clap:", clap)
        thm_L.append(thm)

        thm_pos_L.append(thm_pos)
    thm = np.array(thm_L)
    #print(L_thm[:,0][0])
    thm_pos = np.unique(np.array(thm_pos_L))

    L_astop = search_string(file_name, r, "ASTOP")  # aperture stop
    #print("L_astop: ", L_astop)
    astop_pos = np.min(np.argwhere(L_astop[:, 0] <= L[:, 0])) - 1

    L_tilt = search_string(file_name, r, "TILT")  # tilt
    #print("L_tilt: ", L_tilt)
    #print(L_tilt[0][0])
    #print(L_tilt[0][1])
    tilt_pos_L = []
    tilt_L = []
    tilttype_L = []
    for j in range(0, len(L_tilt)):
        tilt_pos = np.min(np.argwhere(L_tilt[j, 0] < L[:, 0])) - 1
        tilt_pos_L.append(tilt_pos)
        tilt = np.loadtxt(file_name, skiprows=int(L_tilt[j][0])-1, max_rows = 1, dtype='str', delimiter=',')
        tilttype = tilt[0][4:]
        tilt = tilt[1:].astype(np.float)
        tilt_L.append(tilt)
        tilttype_L.append(tilttype)
    tilt_pos = np.unique(np.array(tilt_pos_L))
    tilt_L = np.array(tilt_L)
    tilttype_L = np.array(tilttype_L)
    #print("tilt: ", tilt)

    refl, refl_pos_L = find_elem(file_name, r, keyword="REFL")
    refl_pos = np.unique(np.array(refl_pos_L))

    keywords = "AIR" or "OHARA"
    mat, mat_pos_L = find_elem(file_name, r, keyword=keywords)

    L_refs = search_string(file_name, r, "REFS")  # reflector
    #print("L_refs: ", L_refs)
    refs_pos = np.min(np.argwhere(L_refs[:, 0] <= L[:, 0])) - 1

    L_aimray = search_string(file_name, r, "AIMRAY")  # aimray
    #print("L_aimray: ", L_aimray[0][1], L_aimray[1][1:])
    L_aimray = [L_aimray[0][1],L_aimray[1][1:]]

    L_mode = search_string(file_name, r, "MODE")  # mode
    #print("L_mode: ", L_mode)
    mode = L_mode[0][1]
    sptwt = np.loadtxt(file_name, skiprows=int(L_mode[0][0]), max_rows = 1, dtype='str', delimiter=',')[1:].astype(np.float)
    sptwt2 = np.loadtxt(file_name, skiprows=int(L_mode[0][0])+1, max_rows = 1, dtype='str', delimiter=',')[1:].astype(np.float)
    L_FLDSRAYS = search_string(file_name, r, "FLDSRAYS")  # FLDSRAYS
    #print("L_FLDSRAYS: ", L_FLDSRAYS[0][0])
    fldrays = np.float(L_FLDSRAYS[0][1][12:])
    # read all field rays

    frays = np.loadtxt(file_name, skiprows=int(L_FLDSRAYS[0][0]), max_rows=200, dtype='str')
    frays = np.char.replace(frays, 'D', 'E').astype(np.float)
    #print(frays.shape)
    frays2 = np.loadtxt(file_name, skiprows=int(L_FLDSRAYS[0][0])+200, max_rows=500, dtype='str')
    frays2 = np.char.replace(frays2, 'D', 'E').astype(np.float)
    #print(frays2.shape)

    # FLDS MAX
    L_fldsmax = search_string(file_name, r, "FLDS MAX")  # mode
    flds = np.loadtxt(file_name, skiprows=int(L_fldsmax[0][0]), dtype='str', delimiter = ',')[:,1:].astype(np.float)
    #print(flds.shape)
    #flds = flds[:,].astype(np.float)

    return coating, cv, (cc_pos,cc),th, (clap_pos_L,clap), (thm_pos,thm), astop_pos, (tilt_pos, tilt_L, tilttype_L), refl_pos, (mat_pos_L, mat), refs_pos, L_aimray, mode, fldrays, frays, frays2, flds

import os
cwd = os.path.get_cwd()
filename = os.path.join(cwd,"Cassegrain.DAT")
#filename = "Newtonian.DAT"
r, L = search_string_in_file(filename, "#", "PIKUP")
coating, cv, cc, th, clap, thm, astop, tilt, refl, mat, refs, aimray, mode, fldrays, frays, frays2,flds = return_optical_data(filename,r, L)


# =============================================================0
# transfer to pyrate
n_surfaces = len(L)


if 0:
    shape_L = []
    builduplist = []
    for i in range(0, n_surfaces):
        shape = {"shape": "Conic", "curv": cv[i]}

        shape_L.append(shape)
        elem_L = []
        elem_L.append(shape)

        elem_L.append({"decz": th[i]})
        elem_L.append(None)
        if i == 0:
            elem_L.append("source")
        elif i == n_surfaces-1:
            elem_L.append("image")
        else:
            elem_L.append(str(i))

        if i == astop:
            elem_L.append({"is_stop": True})
        else:
            elem_L.append({})
        for j in range(0, len(refl)):
            if i == refl[j]:
                elem_L.append( {"is_mirror": True})

        builduplist.append(tuple(elem_L))
    builduplist = np.array(builduplist)

    # definition of optical system
    from pyrateoptics.raytracer.ray import RayBundle
    from pyrateoptics.raytracer.analysis.optical_system_analysis import\
        OpticalSystemAnalysis
    from pyrateoptics import build_simple_optical_system, draw
    from VisualOpticsPy import draw3D

    (s, sysseq) = build_simple_optical_system(builduplist)

from pyrateoptics.raytracer.material.material_isotropic import\
    ConstantIndexGlass
from pyrateoptics.raytracer.surface_shape import Conic
from pyrateoptics.raytracer.optical_element import OpticalElement
from pyrateoptics.raytracer.optical_system import OpticalSystem
from pyrateoptics.raytracer.surface import Surface
from pyrateoptics.raytracer.aim import Aimy

from pyrateoptics.raytracer.aperture import CircularAperture
# no elliptic aperture class exists in pyrate (have to define it here):
from VisualOpticsPy.aperture_add import EllipticAperture
#from pyrateoptics.raytracer.aperture import EllipticAperture

from pyrateoptics.raytracer.localcoordinates import LocalCoordinates

from pyrateoptics import draw
from VisualOpticsPy import draw3D

import logging
logging.basicConfig(level=logging.INFO)


wavelength = 0.5876e-3

# definition of optical system

# v = np.ones(3)# + 0.001*np.random.random(3)
# myeps = np.diag(v)
th = np.insert(th, 0,0)       # object is at origin of system
th[th> 1e10] = 0.1111
lc_L = []
s = OpticalSystem.p()
name_L = []
tiltflag = 0
tilt_a_L = []
CS_L = []
to_deg = 1/180*math.pi
for i in range(0, n_surfaces):
    tiltnext = 0
    if i == 0:
        name = "object"
    elif i == n_surfaces-1:
        name = "image"
    else:
        name = str(i)

    if i in tilt[0]:
        for j in range(0, len(tilt[0])):
            if i == tilt[0][j]:
                tilt_a = tilt[1][j]
                if tilt[2][j] == "     BEN     ":
                    tiltnext = 1
                else:
                    tiltnext = 0
    else:
        tilt_a = np.zeros(3)
    name_L.append(name)
    if i == 0:
        CS = s.rootcoordinatesystem.name
    else:
        CS = lc_L[i-1].name
    CS_L.append(CS)

    if tiltflag == 0:
        lc_L.append(s.addLocalCoordinateSystem(LocalCoordinates.p(name=name, decz=th[i], tiltx = tilt_a[0]*to_deg, tilty=tilt_a[1], tiltz = tilt_a[2], tiltThenDecenter = 0),
                                 refname=CS))
    if tiltflag == 1:
        lc_L.append(s.addLocalCoordinateSystem(
            LocalCoordinates.p(name=name, decz=th[i], tiltx=tilt_a_L[i-1][0]*to_deg, tilty=-tilt_a_L[i-1][1], tiltz=-tilt_a_L[i-1][2], tiltThenDecenter = 1),
                                refname=CS_L[i]))
    if tiltnext:
        tiltflag = 1
        #tilt_a = -tilt_a_L[i-1]
    else:
        tiltflag = 0
    tilt_a_L.append(tilt_a)
tilt_a_L = np.array(tilt_a_L)
CS_L = np.array(CS_L)

    # note: s.rootcoordinatesystem.name is global coordinate system
lc_L = np.array(lc_L)

# air = AnisotropicMaterial(lc0, myeps)  # tests for anisotropic mirror
air = ConstantIndexGlass.p(lc_L[0], 1.0)
s.material_background = air

surf_L = []
for i in range(0, n_surfaces):
    Shape = Conic.p(lc_L[i], curv=cv[i])
    if i in clap[0]:
        for j in range(0, len(clap[1])):
            if i == clap[0][j]:
                Aperturetype = clap[1][j][1]
                if Aperturetype == ',':
                    Aperturetype = "Circular"
                if Aperturetype == "Circular":
                    Aperture = CircularAperture.p(lc_L[clap[0][j]], maxradius=np.float(clap[1][j][2]), minradius = 1)       # which type of aperture
                elif Aperturetype == 'ELIP':
                    Aperture = EllipticAperture.p(lc_L[clap[0][j]], cay=np.float(clap[1][1][3]), cax=np.float(clap[1][1][5]), Yd = np.float(clap[1][1][7]), Xd = np.float(clap[1][1][9]))
        surf_L.append(Surface.p(lc_L[i], shape = Shape, aperture = Aperture))      # shape = , curv =, aperture = CircularAperture
    else:
        surf_L.append(Surface.p(lc_L[i], shape=Shape))
        # Surface.p(lc6, aperture=CircularAperture.p(lc6, maxradius=20.0))
surf_L = np.array(surf_L)

global_cs = s.rootcoordinatesystem
elem = OpticalElement.p(global_cs, name="optical_element")
elem.addMaterial("air", air)

for i in range(0, len(surf_L)):
    elem.addSurface(name_L[i], surf_L[i], (None, None))

s.addElement("optical_element", elem)

surf_list = []
for i in range(0, len(name_L)):
    if i in refl:
        if 1:
        #for j in range(0, len(refl)):
            if i != astop:
                La = (name_L[i], {"is_mirror": True})
            elif i == astop:
                La = (name_L[i], {"is_stop": True}, {"is_mirror": True})
            #elif i == astop and i != refl[j]:
            #    La = (name_L[i], {"is_stop": True})
            surf_list.append(La)
    else:
        if i == astop:
            La = (name_L[i], {"is_stop": True})
        else:
            surf_list.append((name_L[i], {}))
surf_list_array = np.array(surf_list)
#surf_list = np.unique(surf_list_array).tolist()
sysseq = [("optical_element", surf_list)]
#sysseq = [("optical_element",
#           [
#                ("object", {}),
#                ("m1", {"is_mirror": True})
#            ]
#           )
#          ]
# ==========================================================

#from pyrateoptics.raytracer.analysis.optical_system_analysis import OpticalSystemAnalysis
#from pyrateoptics.raytracer.ray import RayBundle
#osa = OpticalSystemAnalysis(s, sysseq, name="Analysis")

#wavelength = 0.5876e-3
#(o, k, E0) = osa.collimated_bundle(121, {"startz": -5., "radius": 11.43},
#                                  wave=wavelength)
#initialbundle = RayBundle(x0=o, k0=k, Efield0=E0, wave=wavelength)

#r2 = s.seqtrace(initialbundle, sysseq)

Stopsize = np.float(clap[1][np.where(clap[0] == astop)[0][0]][2])
#a = Aimy(s, sysseq, name="Aimy", stopsize = Stopsize, num_pupil_points=5)
#a.pupil_raster = raster.MeridionalFan()
from pyrateoptics.raytracer.globalconstants import degree
from pyrateoptics.sampling2d import raster
from pyrateoptics import raytrace

#raysdict = {"radius": 5.0, "startz": -5., "starty": -20., "anglex": 1*degree,
#            "raster": raster.MeridionalFan()}
#r_red = raytrace(s, sysseq, 20, raysdict, wave=wavelength, traceoptions={})[0]

if 0:
    initbundle1 = a.aim(np.array([0, 0]))
    initbundle2 = a.aim(np.array([0, 0.5 * degree]))
    initbundle3 = a.aim(np.array([0, -0.5 * degree]))

    (pp1, r1p) = s.para_seqtrace(a.pilotbundle, initbundle1, sysseq)
    (pp2, r2p) = s.para_seqtrace(a.pilotbundle, initbundle2, sysseq)
    (pp3, r3p) = s.para_seqtrace(a.pilotbundle, initbundle3, sysseq)

    r1r = s.seqtrace(initbundle1, sysseq)
    r2r = s.seqtrace(initbundle2, sysseq)
    r3r = s.seqtrace(initbundle3, sysseq)


#sourcesurf = s.elements["optical_element"].surfaces["object"]
do_not_plot = [surf_L[0]]
#do_not_plot = []

# draw rays without raytracing in pyrateoptics
# read rays from ray file
# draw rays in pyvista

draw(s, do_not_draw_surfaces=do_not_plot)
#if plotter in globals():
#    plotter.close()

plotter = draw3D.draw3D_pyvista(s, vertices=10, do_not_draw_surfaces=do_not_plot)
#plotter = draw3D.draw3D_pyvista(s, [(r1p, "blue"), (r2p, "green"), (r3p, "orange")])

# draw(s, r2)
#sourcesurf = s.elements["stdelem"].surfaces["source"]
#surf1 = s.elements["stdelem"].surfaces["1"]

#draw(s, r2, do_not_draw_surfaces=[sourcesurf, surf1], do_not_draw_raybundles=[initialbundle])
#draw3D.draw3D_pyvista(s, vertices=50, do_not_draw_surfaces=[sourcesurf])
# ============================================================
end = time.time()
print("Duration: ", np.round(end - start, decimals = 2), " s")