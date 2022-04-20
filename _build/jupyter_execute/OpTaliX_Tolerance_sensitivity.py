#!/usr/bin/env python
# coding: utf-8

# # OpTaliX: Tolerance and Sensitivity Analysis
# 
# These are ...

# In[1]:


import pandas as pd
import itables
from itables import init_notebook_mode, show
import itables.options as opt

init_notebook_mode(all_interactive=True)

opt.lengthMenu = [50, 100, 200, 500]
#opt.classes = ["display", "cell-border"]
#opt.classes = ["display", "nowrap"]

opt.columnDefs = [{"className": "dt-left", "targets": "_all"}, {"width": "500px", "targets": 1}]


# In[2]:


import os
cwd = os.getcwd()
filename = os.path.join(cwd, os.path.join('Excel', 'OpTaliX_optimization_operands.xlsx'))
df_var = pd.read_excel(filename, sheet_name = "Tolerance and Sensitivity Data", header = 0, index_col = 0)
df_var = df_var.dropna()   # drop nan values


# In[3]:


df_var


# Using Tolerance Sensitivity Items in Optimization
# If optimizing (minimizing) for tolerance sensitivity, the various tolerance sensitivity items described in the previous section should be understood as aberrations added to the targets/constraints (merit function) list.
# 
# See also the syntax for defining tolerance sensitivity. Here is a typical example in the optimization targets/constraints list:
# 
# 
# efl = 100  Focal length shall be exactly 100mm.  
# spd 0  Spot diameter (rms) shall be zero (minimized) for all fields, wavelengths, zoom positions.  
# tsa s1..5 f1..2 w1 0  Tolerance sensitivity on surface tilt about X-axis shall be minimized for surfaces 1-5, fields 1-2 and wavelength number 1.  
# tsy 0  Tolerance sensitivity on surface Y-decenter shall be minimized for all surfaces, all fields and all wavelengths defined in the optical system configuration.  
# 
# 
# 
# Note: Do not attempt to request a tolerance sensitivity item to become exactly zero, e.g. 'TSA = 0' as this is impossible on optical elements/surfaces that have optical effect. Instead minimize it by omitting the equal '=' sign in the constraints definition, e.g. 'TSA 0'. 

# In[ ]:




