#!/usr/bin/env python
# coding: utf-8

# ## Python: ray-optics
# The python package [ray-optics](https://ray-optics.readthedocs.io/en/latest/) is used to read some CodeV .seq files and ZEMAX .zmx files and do some analyses. Please install the most recent version of ray-optics, with "conda install -c conda-forge rayoptics==0.8.1" if 0.8.1 is the actual version.

# In[1]:




get_ipython().run_line_magic('matplotlib', 'inline')
# initialization
from rayoptics.environment import *


# In[2]:


root_pth = Path(rayoptics.__file__).resolve().parent


# In[3]:


opm, info = open_model(root_pth/"zemax/tests/354710-C-Zemax(ZMX).zmx", info=True)


# In[4]:


info


# In[5]:


opm


# In[8]:


sm  = opm['seq_model']
osp = opm['optical_spec']
pm = opm['parax_model']
em = opm['ele_model']
pt = opm['part_tree']
ar = opm['analysis_results']


# In[9]:


sm.list_model()


# In[10]:


pm.first_order_data()


# In[11]:


layout_plt = plt.figure(FigureClass=InteractiveLayout, opt_model=opm,
                        do_draw_rays=True, do_paraxial_layout=False).plot()


# In[12]:


abr_plt = plt.figure(FigureClass=RayFanFigure, opt_model=opm, data_type='Ray',
                     scale_type=Fit.All_Same).plot()


# One can see that not any glass is recognized:

# In[14]:


filename = r'C:\Work\OpTaliX\Test\AFL12-15.zmx'
opm, info = open_model(filename, info=True)
info


# In[ ]:




