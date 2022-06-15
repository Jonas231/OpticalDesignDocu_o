# -*- coding: utf-8 -*-
"""
Spyder Editor

Dies ist eine temporäre Skriptdatei.
"""
from raypier.api import RayTraceModel, GeneralLens, ParallelRaySource, SphericalFace, CircleShape, OpticalMaterial

### Build a couple of lenses ###
shape = CircleShape(radius=12.5)
f1 = SphericalFace(curvature=-50.0, z_height=0.0)
f2 = SphericalFace(curvature=1e20, z_height=5.0)
m = OpticalMaterial(glass_name="N-BK7")
lens1 = GeneralLens(centre=(0,0,0),
                    direction=(0,0,1),
                    shape=shape,
                    surfaces=[f1,f2],
                    materials=[m])
lens2 = GeneralLens(centre=(0,0,100.0),
                    direction=(0,0,1),
                    shape=shape,
                    surfaces=[f1,f2],
                    materials=[m])

### Add a source ###
src = ParallelRaySource(origin=(0,0,-50.0),
                        direction=(0,0,1),
                        rings=5,
                        show_normals=False,
                        display="wires",
                        opacity=0.1)

model = RayTraceModel(optics=[lens1,lens2],
                        sources=[src])

###Now open the GUI###
model.configure_traits()

model.trace_all()
for rays in src.traced_rays:
    one_ray = rays[0]
    print(one_ray.origin, one_ray.accumulated_path)
