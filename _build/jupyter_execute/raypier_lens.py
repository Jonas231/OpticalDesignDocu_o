#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import sys; sys.path.insert(0,'..')
from raypier.api import RayTraceModel, GeneralLens, ParallelRaySource, SphericalFace, CircleShape, OpticalMaterial

# check
from raypier import tracer
print(tracer.__file__)

if 1:
    ### Build a couple of lenses ###
    shape = CircleShape(radius=12.5)
    f1 = SphericalFace(curvature=-50.0, z_height=0.0)
    f2 = SphericalFace(curvature=50.0, z_height=5.0)
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


# In[5]:


model.ipython_view(400,300)


# In[ ]:





# In[ ]:




