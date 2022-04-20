#!/usr/bin/env python
# coding: utf-8

# # OpTaliX to CodeV to RayOptics / Rayopt
# At first install the python package "ray-optics" (conda install rayoptics --channel conda-forge). 
# 

# In[1]:


# initialization of ray-optics
from rayoptics.environment import *


# In[2]:


import os
cwd = os.getcwd()
filename = os.path.join(cwd, os.path.join('OpTaliX','AFL12-15.seq'))


# In[3]:


root_pth = Path(rayoptics.__file__).resolve().parent
opm = open_model(filename)


# In[4]:


sm  = opm['seq_model']
osp = opm['optical_spec']
pm = opm['parax_model']
em = opm['ele_model']
pt = opm['part_tree']
ar = opm['analysis_results']


# In[ ]:


sm.list_model()


# In[ ]:




