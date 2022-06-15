#!/usr/bin/env python
# coding: utf-8

# ## Paraxial optics and predesign with python
# Here the open-source python package [RayTracing](https://github.com/DCC-Lab/RayTracing) is used.

# In[1]:



import warnings
warnings.filterwarnings('ignore')       # ignore warnings


from raytracing import *         # import RayTracing package


path = ImagingPath()
path.append(Space(d=50))
path.append(Lens(f=50, diameter=25))
path.append(Space(d=120))
path.append(Lens(f=70))
path.append(Space(d=100))
path.display()


# In[15]:


TITLE       = "Aperture behind lens acting as Field Stop"
DESCRIPTION = """ An object at z=0 (front edge of ImagingPath) is used with
default properties. Notice the aperture stop (AS) identified at the lens which
blocks the cone of light. The second aperture, after the lens, is the Field Stop
(FS) and limits the field of view."""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=100))
    path.append(Lens(f=50, diameter=30))
    path.append(Space(d=30))
    path.append(Aperture(diameter=30))
    path.append(Space(d=170))
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()


# In[17]:


TITLE       = "Simple microscope system"
DESCRIPTION = """
This is an extremely simple microscope with ideal lenses: the objective lens
(labelled 'Obj') has a focal length of 4 mm and is positionned 184 mm from the
tube lens (f=180 mm).  You can zoom using the mouse to inspect the object.
You can see the field of view (hollow blue arrow) and the object (filled blue
arrow) at the focal plan of the objective.
"""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=4))
    path.append(Lens(f=4, diameter=8, label='Obj'))
    path.append(Space(d=4 + 180))
    path.append(Lens(f=180, diameter=50, label='Tube Lens'))
    path.append(Space(d=180))
    path.display(ObjectRays(diameter=1, halfAngle=0.5),comments=comments)

if __name__ == "__main__":
    exampleCode()


# In[ ]:




