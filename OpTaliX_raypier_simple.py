# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""
import numpy as np

coeffs = [0.683740494, 0.420323613, 0.58502748, 0.00460352869, 0.0133968856, 64.4932732]  # coefficients of Sellmeier equation.
Lmin = 0.18
Lmax = 2.3     # micrometer
from raypier.api import OpticalMaterialFromFormula
m1 = OpticalMaterialFromFormula(formula_id = 2, coefs = coeffs, wavelen_min = Lmin, wavelen_max = Lmax)


from raypier.api import GeneralLens, AxiconFace, PlanarFace, OpticalMaterial, CircleShape,\
            RayTraceModel, CollimatedGaussletSource, EFieldPlane, GaussletCapturePlane, IntensitySurface, ParallelRaySource, SphericalFace, AsphericFace
 
Shape = CircleShape(radius=6.25)                  # APE-Y [mm]     
cuy_L = [0.0, -0.13537295248409, 0.0, 0.0]    # curvatures [1/mm]
rad_L = 1/np.array(cuy_L)                    # radius of curvature [mm]
rad_L[rad_L == np.inf] = 1e10
thi_L = [1e+20, 0, 4, 16.32032337]          # thickness [mm]
# aspheric coefficients
asp_L = [np.array([], dtype='<U118'),
 np.array(['  ASP -0.6700000000      0.3440000000E-04  0.1430000000E-06   0.000000000       0.000000000       0.000000000       0.000000000       0.000000000       0.000000000       0.000000000'],
       dtype='<U181'),
 np.array([], dtype='<U118'),
 np.array([], dtype='<U118')]

sut_L = ['S', 'A', 'S', 'S']             # surface type

# semi-apertures:
ape_L = [" 1   0.000000000       0.000000000       0.000000000       0.000000000       0.000000000        1   0   0   1 ''",
 " 1   5.625000000       5.625000000       0.000000000       0.000000000       0.000000000        1   0   0   1 ''",
 " 1   6.250000000       6.250000000       0.000000000       0.000000000       0.000000000        1   0   0   1 ''",
 " 1  0.1676174929E-04  0.1676174929E-04   0.000000000       0.000000000       0.000000000        1   0   0   1 ''"]
 
Nsurfaces = 4

if 1:
    ### Build a couple of lenses ###
    shape_L = []
    radius_L = []
    f_L = []
    for i in range(1,Nsurfaces):
        radius_L.append(float(ape_L[i][5:5+10]))
        shape_L.append(CircleShape(radius=radius_L[i-1]))
        print("dia: ", float(ape_L[i][5:5+10]))
        if sut_L[i] == "S":
            print("i: ",i , " sphere")
            
            if rad_L[i] == 1e10:
                f_L.append(PlanarFace(z_height=thi_L[i]))
            else:
                f_L.append(SphericalFace(curvature=rad_L[i], z_height=thi_L[i]))        # curvature is "radius of curvature"
        if sut_L[i] == "A":
            print("i: ",i , " asphere")
            asp_coeffs = asp_L[i][0].split()
            asphere = AsphericFace(z_height=thi_L[i],
                                  curvature=rad_L[i],            
                                  conic_const= float(asp_coeffs[1]),
                                  A4 = float(asp_coeffs[2]),  # A
                                  A6 = float(asp_coeffs[3]), #I'm not 100% sure if the signs of the polynomial terms are right.
                                  A8 = float(asp_coeffs[4]), # C
                                  A10 = float(asp_coeffs[5]), # D
                                  A12 = float(asp_coeffs[6]), # E
                                  A14 = float(asp_coeffs[7]), # F
                                  A16 = float(asp_coeffs[8])#, # G
                                  #A18 = asp_coeffs[9]  # H
                                  )
            f_L.append(asphere)


lens  = GeneralLens(centre=(0,0,0),
                    direction=(0,0,1),
                    shape=Shape,
                    surfaces=[f_L[0], f_L[1]],
                    materials=[m1])

### Add a source ###
src = ParallelRaySource(origin=(0,0,-20.0),
                        direction=(0,0,1),
                        rings=2,
                        show_normals=False,
                        display="wires",
                        opacity=0.1,
                        radius = 5)

capture = GaussletCapturePlane(centre=(0,0,thi_L[-1]), 
                               direction=(0,0,1),
                               width=15.0,
                               height=15.0)


model = RayTraceModel(optics=[lens],
                      sources=[src],
                      probes=[capture])
#model.ipython_view(800,600)
model.configure_traits()

#model.trace_all()
#for rays in src.traced_rays:
#    one_ray = rays[0]
#    print("ray: ", one_ray.origin, one_ray.accumulated_path)
    
    
print("finished")
