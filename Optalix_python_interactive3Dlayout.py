# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 15:52:19 2022

@author: herbst
"""
import numpy as np
import matplotlib.pylab as plt
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors
import time 
import math

t0 = time.perf_counter()

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

# ===================================
## settings:
    
draw_sagittal = 0          # draw sagittal rays

Opacity = 0.15             # opacity of drawn "glass" surfaces, set to 0 for OpTaliX-like plot
show_labels = 0            # show labels: very slow in pyvista
plot_edge = 1              # plot minimal edges of lenses, corresponds to : EDG si..sj lin
edge_type = "rec"          # options: "lin", "rec", 
draw_rays_prior1 = 1       # draw rays prior to surface 1
thi_draw = 20             # draw rays prior to surface 1 for this length
draw_paraxial_data = 0
alt_color = 0


create_gif = 0             # generate a gif (of the rotating layout)

# these are the files written by the macro "L3D.mac":
filename_py = r'C:\Work\OpTaliX\Test\RAY_FAN_PY_ALL.txt'
filename_px = r'C:\Work\OpTaliX\Test\RAY_FAN_PX_ALL.txt'
filename_layout3D = r'C:\Work\OpTaliX\Test\LAYOUT_3D.txt'
filename_sag = r'C:\Work\OpTaliX\Test\SAG.txt'
filename_parax = r'C:\Work\OpTaliX\Test\paraxial.txt'
# ==================================


nsurfaces = int(np.loadtxt(filename_py, comments = 'C',max_rows=1)[0])
nwavelengths = int(np.loadtxt(filename_py, comments = 'C',max_rows=1)[1])
nfields = int(np.loadtxt(filename_py, comments = 'C',max_rows=1)[2])
stopsurface = int(np.loadtxt(filename_py, comments = 'C',max_rows=1)[3])

if nwavelengths > 1:
    wavelengths = np.loadtxt(filename_py, comments = 'C',skiprows = 2, max_rows=nwavelengths)[:,1]
else:
    wavelengths = np.loadtxt(filename_py, comments = 'C',skiprows = 2, max_rows=nwavelengths)[1]
    
fields = np.loadtxt(filename_py, comments = 'C',skiprows = 2+nwavelengths, max_rows=nfields)

rayfandata_py = np.loadtxt(filename_py, comments = 'C', skiprows = nwavelengths+2+nfields)


rayfandata_px = np.loadtxt(filename_px, comments = 'C', skiprows = nwavelengths+2+nfields) # , skiprows = nwavelengths+2+nfields

if nfields == 1:
    fields = np.array([fields])
    
n_fields = len(fields)

Lim = 0.02    # mm
#nwavelengths = 3


rayfandata_px_L= []
rayfandata_py_L = []
rayfandata_PY0_L = []

for s in range(0, nsurfaces):
    rayfandata_px_LL = []
    rayfandata_py_LL = []
    rayfandata_px00 = rayfandata_px[rayfandata_px[:,0]==s+1]
    rayfandata_py00 = rayfandata_py[rayfandata_py[:,0]==s+1]                 # select data by wavelength
    for w in range(0, nwavelengths):
        #print("w = ", w)
        rayfandata_px_LLL = []
        rayfandata_py_LLL = []
        rayfandata_px0 = rayfandata_px00[rayfandata_px00[:,1]==w+1]
        rayfandata_py0 = rayfandata_py00[rayfandata_py00[:,1]==w+1]                 # select data by wavelength
        
    
        
        for i in range(0, n_fields):
            rayfandata_px_LLL.append(rayfandata_px0[rayfandata_px0[:,2]==i+1])
            rayfandata_py_LLL.append(rayfandata_py0[rayfandata_py0[:,2]==i+1] )           # select data by field
            
        rayfandata_px_LL.append(np.array(rayfandata_px_LLL))
        rayfandata_py_LL.append(np.array(rayfandata_py_LLL))
        
    rayfandata_px_L.append(np.array(rayfandata_px_LL))
    rayfandata_py_L.append(np.array(rayfandata_py_LL))
 
                

#filename_layout3D = r'C:\Work\OpTaliX\Test\LAYOUT_3D.txt'
layout_3D_0 = np.loadtxt(filename_layout3D, comments = 'C')
layout_3D = layout_3D_0[1:]
thi = layout_3D_0[:,-1]

# calculate starting points of fields
if draw_rays_prior1:
    import pyvista as pv
    
    xypos0 = np.tan(fields[:,1:]*math.pi/180)*thi[0]
    
    xyzpos0 = np.stack((xypos0[:,0], xypos0[:,1], np.ones(len(xypos0))*thi[0])).T
    # create vectors:
    s = 0
    mesh_prior1_L = []
    mesh_prior1x_L = []
    for w in range(0, nwavelengths):
        for i in range(0, n_fields):
            
            for p in range(0, len(rayfandata_py_L[0][w][i])): 
                pos1 = np.stack((rayfandata_py_L[s][w][i][p,4],rayfandata_py_L[s][w][i][p,5] , rayfandata_py_L[s][w][i][p,6]+ layout_3D[s,3])).T 
                vec = pos1-xyzpos0[i]
                vec /= np.linalg.norm(vec)
                vec *= thi_draw 
                pos0 = pos1 + vec
                if p == 0:
                    mesh_prior1 = pv.lines_from_points(np.array([pos0,pos1]))
                else:
                    mesh_prior1 += pv.lines_from_points(np.array([pos0,pos1]))
                    
            if draw_sagittal:
                for p in range(0, len(rayfandata_px_L[0][w][i])): 
                    pos1x = np.stack((rayfandata_px_L[s][w][i][p,4],rayfandata_px_L[s][w][i][p,5] , rayfandata_px_L[s][w][i][p,6]+ layout_3D[s,3])).T 
                    vecx = pos1x-xyzpos0[i]
                    vecx /= np.linalg.norm(vecx)
                    vecx *= thi_draw 
                    pos0x = pos1x + vecx
                    if p == 0:
                        mesh_prior1x = pv.lines_from_points(np.array([pos0x,pos1x]))
                    else:
                        mesh_prior1x += pv.lines_from_points(np.array([pos0x,pos1x]))
                        
                    
            mesh_prior1_L.append(mesh_prior1)
            if draw_sagittal:
                mesh_prior1x_L.append(mesh_prior1x)
                
#filename_sag = r'C:\Work\OpTaliX\Test\SAG.txt'
sag = np.loadtxt(filename_sag, comments = 'C')


if draw_paraxial_data:
    import re
    #parax = np.loadtxt(filename_parax , comments = 'C')
    numeric_const_pattern = r"[-+]?\d*\.?\d+|\d+"
    rx = re.compile(numeric_const_pattern, re.VERBOSE)
    lines = tuple(open(filename_parax, 'r'))
    L_float = []
    for l in lines:
        L_float.append(rx.findall(l))
    L_float = list(filter(None, L_float))
    L_float[0] = [L_float[0][0],L_float[0][-1] ]
    L_float[1] = [L_float[1][0],L_float[1][-1] ]
    if len(L_float[-1]) == 3:
        L_float[-1] =[L_float[-1][0]+'E'+L_float[-1][1],L_float[-1][-1] ] 
    L_float[-2] = [L_float[-2][0],L_float[-2][-1] ]
    
    # L_float2 = []
    # for i in range(0,len(L_float)):
    #     L_float2.append(np.array(L_float[i]))
    L_float = np.array(L_float).astype(float)
    
    EFL = L_float[0,0]
    FNO = L_float[1,0]
    MAG = L_float[2,0]
    NOA = L_float[3,0]
    NA = L_float[4,0]
    BFL = L_float[5,0]
    DEF = L_float[6,0]
    IMD = L_float[7,0]
    OID = L_float[8,0]
    
    SH1 = L_float[0,1]
    SH2 = L_float[1,1]
    SEP = L_float[2,1]
    EPD = L_float[3,1]
    APD = L_float[4,1]
    SAP = L_float[5,1]
    PRD = L_float[6,1]
    OAL = L_float[7,1]
    SYL = L_float[8,1]
    
    


p = np.linspace(0, 2*np.pi, 50) 

import pyvista as pv
sag_data_L = []
mesh_L = []
mesh_prof_L = []
mesh_prof_Ly = []
mesh_circ_L = []
Z0 = 0

def circle_points(R=1):
    p = np.linspace(0, 2*np.pi, 50)
    x, y = R*np.cos(p), R*np.sin(p)
    #F = x**2 + y**2
    return x, y

sag_data_stop = sag[sag[:,0]==stopsurface]
r_stop = np.max(sag_data_stop[:,1])

n_mat = layout_3D[:,5]

r_max_L = []
points_circ_L = []
points_circ_L2 = []
surf_L = []
points_label_L = []
r_L = []
for s in range(0, nsurfaces):
    
    sag_data = sag[sag[:,0]==s+1]
    sag_data_L.append(sag_data)
    r = sag_data[:,1]
    r_L.append(r)
    #if n_mat[s-1] > 1:
    #   r2 = r_L[s-1]
        
    r_max_L.append(np.max(r))
    R, P = np.meshgrid(r, p)
    # Express the mesh in the cartesian system.
    X, Y = R*np.cos(P), R*np.sin(P)
    
    x_c, y_c= circle_points(R = np.max(r))
    #if n_mat[s-1] > 1:
    #    x_c, y_c= circle_points(R = np.max(r2))
    sa = sag_data[:,2:]
    Z = np.repeat(sa[np.newaxis, :, :], len(p), axis=0) + layout_3D[s,3]
    points = np.stack((X.flatten(), Y.flatten(), Z[:,:,0].flatten())).T
    mesh = pv.PolyData(points).delaunay_2d()
    mesh_prof_x = pv.lines_from_points(np.stack((r, np.zeros(len(r)), sa[:,0]+ layout_3D[s,3])).T)
    mesh_prof_y = pv.lines_from_points(np.stack((np.zeros(len(r)), r, sa[:,1]+ layout_3D[s,3])).T)
    points_circ = np.stack((x_c, y_c, layout_3D[s,3]*np.ones(len(y_c))+ np.min(sa)+np.max(sa) )).T
    mesh_circ = pv.lines_from_points(points_circ)
    mesh_L.append(mesh)
    mesh_prof_L.append(mesh_prof_x)
    mesh_prof_Ly.append(mesh_prof_y)
    mesh_circ_L.append(mesh_circ)
    points_circ_L.append(points_circ)
    points_circ_L2.append(points_circ)
    
    points_label_L.append(points_circ_L[s][int(len(points_circ_L[s])/2)])

atest = (np.stack((np.zeros(len(points_circ_L[s])), np.zeros(len(points_circ_L[s])), np.ones(len(points_circ_L[s])))).T)
#edge_type = "lin" 
points_element_L = []
for s in range(0, nsurfaces):    
    if n_mat[s] > 1:
        if edge_type == "lin":
            points_element = np.vstack((points_circ_L[s], points_circ_L[s+1] ))
            
            pointsc = pv.PolyData(points_element)
            surf = pointsc.delaunay_2d()#.reconstruct_surface()
            surf_L.append(surf)
            
        elif edge_type == "rec":
            x_c, y_c= circle_points(R = r_max_L[s])
            sa = sag_data_L[s][:,2:]
            points_circ1 = np.stack((x_c, y_c, layout_3D[s,3]*np.ones(len(y_c))+ np.min(sa)+np.max(sa) )).T
            x_c2, y_c2= circle_points(R = r_max_L[s])
            sa2 = sag_data_L[s+1][:,2:]
            
            points_circ2 = points_circ1+atest*layout_3D[s+1,3]#np.stack((x_c, y_c, layout_3D[s+1,3]*np.ones(len(y_c)))).T
            points_element = np.vstack((points_circ1, points_circ2 ))
            points_element_L.append(points_element)
            # if s > 1:
                
            #     sag_data = sag[sag[:,0]==s]
            #     sag_data2 = sag[sag[:,0]==s-1]
            #     sag_data_L.append(sag_data)
            #     r = sag_data[:,1]
            #     sa = sag_data[:,2:]
            #     x_c, y_c= circle_points(R = np.max(r))    
            #     points_circ = np.stack((x_c, y_c, layout_3D[s,3]*np.ones(len(y_c))+ np.min(sa)+np.max(sa) )).T
            #     points_circ_Lt = points_circ
            
            #     points_element = np.vstack((points_circ_Lt, points_circ_L[s]))
            # else:
            #     #points_element = np.vstack((points_circ_Lt, points_circ_L[s]))
            #     points_element = np.vstack((points_circ_L[s], points_circ_L[s+1] )) 
            M1 = np.min(sa)+np.max(sa)
            M2 = np.min(sa2)+np.max(sa2)
            print(M1-M2)
            
            mesh = pv.lines_from_points(points_circ_L[s])
            surf = mesh.extrude((0, 0, M2-M1+thi[s+1] ), capping=True)
            mesh_circ_L[s] += pv.lines_from_points(points_circ_L[s]+atest*(M2-M1+thi[s+1]))
            surf_L.append(surf)
    #Z0+= layout_3D[i,3]


#for s in range(0, nsurfaces):
#    if n_mat[s]>1:
    
s =1
sag_data = sag[sag[:,0]==s+1]
sag_data2 = sag[sag[:,0]==s]
sag_data_L.append(sag_data)
r = sag_data2[:,1]
sa = sag_data[:,2:]
x_c, y_c= circle_points(R = np.max(r))    
points_circ = np.stack((x_c, y_c, layout_3D[s,3]*np.ones(len(y_c))+ np.min(sa)+np.max(sa) )).T
points_circ_Lt = points_circ
points_element = np.vstack((points_circ_L[s], points_circ_Lt))
pointsc = pv.PolyData(points_element)
surf = pointsc.delaunay_2d()


mesh_ray_Ly = []
points_Ly = []
mesh_p_L = []

mesh_ray_Lx = []
mesh_p_L_x = []

for w in range(0, nwavelengths):
    for i in range(0, n_fields):
        
        for p in range(0, len(rayfandata_py_L[0][w][i])): 
            ray = []
            ray_x = []
            for s in range(0, nsurfaces):
                r = np.stack((rayfandata_py_L[s][w][i][p,4],rayfandata_py_L[s][w][i][p,5] , rayfandata_py_L[s][w][i][p,6]+ layout_3D[s,3])).T
                ray.append(r)
                
                
            ray = np.array(ray)
            mesh_ray = pv.lines_from_points(ray)
            mesh_p0 = pv.PolyData(ray)
            

            
            if p == 0:
                mesh_ray_g = mesh_ray
                mesh_p = mesh_p0
                

            else:
                mesh_ray_g += mesh_ray
                mesh_p += mesh_p0
                

                
        for p in range(0, len(rayfandata_px_L[0][w][i])): 
            ray_x = []
            for s in range(0, nsurfaces):
                r_x = np.stack((rayfandata_px_L[s][w][i][p,4],rayfandata_px_L[s][w][i][p,5] , rayfandata_px_L[s][w][i][p,6]+ layout_3D[s,3])).T
                ray_x.append(r_x)
            ray_x = np.array(ray_x)
            mesh_ray_x = pv.lines_from_points(ray_x)
            mesh_p0_x = pv.PolyData(ray_x)
            
            if p == 0:
                mesh_ray_g_x = mesh_ray_x
                mesh_p_x = mesh_p0_x
            else:
                mesh_ray_g_x += mesh_ray_x
                mesh_p_x += mesh_p0_x
                
        mesh_ray_Ly.append(mesh_ray_g)
        mesh_p_L.append(mesh_p)
        
        mesh_ray_Lx.append(mesh_ray_g_x)
        mesh_p_L_x.append(mesh_p_x)



# get refractive index / material
# fill volume between surfaces with glass.
    
   
#pl = pv.Plotter(border_width=1)
from pyvistaqt import BackgroundPlotter

if 'pl' in globals():
    pl.close()
    pl.clear()
if 1:
    if create_gif:
        pl = pv.Plotter(notebook=False, off_screen=True)
    else:
        pl = BackgroundPlotter(shape=(1, 1))
    
    #pl = pv.Plotter(shape=(1, 1))
    pl.set_background("white")  # "gray", top="black"
    #plotter.subplot(0, 0)
    Colorline = "gray"
    pv.create_axes_orientation_box(line_width=1, text_scale=0.366667, edge_color=Colorline, x_color=None, y_color=None, z_color=None, xlabel='X', ylabel='Y', zlabel='Z', x_face_color='red', y_face_color='green', z_face_color='blue', color_box=False, label_color=None, labels_off=False, opacity=0.5)
    pl.add_axes(color = Colorline)
    pl.add_bounding_box(color=Colorline, corner_factor=0.5, line_width=None, opacity=1.0, render_lines_as_tubes=False, lighting=None, reset_camera=None, outline=True, culling='front')
    pl.show_bounds(font_size = 15, color=Colorline)
#plotter.show()




poly = pv.PolyData(np.array(points_label_L))
poly["My Labels"] = [f"{i}" for i in range(poly.n_points)]


a_L = []

a = 0
for s in range(0, nsurfaces):
    if n_mat[s]>1: #or n_mat[s-1]>1:
        color_aper = 'red'
        color_aper = 'black'
    else:
        color_aper = 'black'
        
    if s == stopsurface-1:
        color_aper = 'blue'
        Linewidth = 2
    else:
        Linewidth = 1
    
    if s == nsurfaces-1:
        colorS = "white"
        ac1 = pl.add_mesh(mesh_L[s],show_edges=False, opacity = 0, color = colorS)
    else:
        if n_mat[s]>1:
            colorS = "cyan"
            if alt_color and (a% 2) == 0:
                colorS = "blue"
                a_L.append("blue")
            else:
                a_L.append("cyan")
            a += 1
        else:
            colorS = "white"
        ac1 = pl.add_mesh(mesh_L[s],show_edges=False, opacity = Opacity, color = colorS)
    ac2 = pl.add_mesh(mesh_prof_L[s],show_edges= True, opacity = 1, color = 'black')
    ac3 = pl.add_mesh(mesh_prof_Ly[s],show_edges= True, opacity = 1, color = 'black')
    ac4 = pl.add_mesh(mesh_circ_L[s],show_edges= True, opacity = 1, color = color_aper, line_width = Linewidth)
    
    if show_labels:
        pl.add_point_labels(poly, "My Labels", point_size=20, font_size=36)



cm_subsection = np.linspace(0.0, 1.0, n_fields) 
from matplotlib import cm
colors = ['blue', 'green', 'red', 'magenta', 'orange', "purple", "lime", "yellow"]

for i in range(0, len(mesh_ray_Ly)):    
    pl.add_mesh(mesh_ray_Ly[i],show_edges= True, opacity = 1, color = colors[i])
    pl.add_mesh(mesh_p_L[i],show_edges= True, opacity = 1, color = colors[i])
    
    if draw_rays_prior1:
       pl.add_mesh(mesh_prior1_L[i],show_edges= True, opacity = 1, color = colors[i])
        
if draw_sagittal:
    for i in range(0, len(mesh_ray_Lx)):       
        pl.add_mesh(mesh_ray_Lx[i],show_edges= True, opacity = 1, color = colors[i])
        pl.add_mesh(mesh_p_L_x[i],show_edges= True, opacity = 1, color = colors[i])
        
        if draw_rays_prior1:
            pl.add_mesh(mesh_prior1x_L[i],show_edges= True, opacity = 1, color = colors[i])    

if plot_edge:
    for i in range(0, len(surf_L)):
        pl.add_mesh(surf_L[i], color = a_L[i], opacity = Opacity)
        
    #pl.add_mesh(points_circ_Lt, color = 'orange', opacity = Opacity)
    #pl.add_mesh(surf, color = 'red', opacity = 1)


if draw_paraxial_data:
    print("add paraxial data")
    
    def show_plane(z = SH1, color = 'red', R = np.max(np.array(r_max_L))*1.05):
        x_p, y_p= circle_points(R = R)
        points_circ_p = np.stack((x_p, y_p, z*np.ones(len(y_p)))).T
        mesh_SH1 = pv.lines_from_points(points_circ_p)
        
        pl.add_mesh(mesh_SH1, color = color, opacity = 1)
        
    show_plane(z = SH1, color = 'red')
    show_plane(z = SH2, color = 'red')
    
    show_plane(z = SEP, color = 'blue', R = EPD/2)
    show_plane(z = OAL+SAP, color = 'blue', R = APD/2)
    
# cpos = [
#     (21.9930, 21.1810, -30.3780),
#     (-1.1640, -1.3098, -0.1061),
#     (0.8498, -0.2515, 0.4631),
# ]
pl.camera_position = 'zy'   
pl.enable_parallel_projection()
#pl.enable_image_style()
#pl.view_zy()
if not create_gif:
    # save as vtkjs
    pl.export_vtkjs("sample")
    pl.export_obj("sample")
    pl.export_html('sample.html')
    pl.export_gltf('sample.gltf') 
    pl.show()

# do some animation 
rot = np.linspace(1, 360, num = 36)
# Open a gif
if create_gif:
    pl.open_gif("rotate3D.gif")
    for r in range(0, len(rot)):
        pl.camera.azimuth = rot[r]
        print("frame = ", r)
        pl.write_frame()
    pl.close()
    
    


      
    
print("Elapsed time: ", np.round(time.perf_counter()-t0, decimals = 4), " s")