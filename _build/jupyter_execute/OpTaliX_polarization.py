#!/usr/bin/env python
# coding: utf-8

# # OpTaliX: Polarization
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
df_var = pd.read_excel(filename, sheet_name = "Polarization", header = 0, index_col = 0)
df_var = df_var.dropna()   # drop nan values


# In[3]:


df_var


# In[ ]:





# In[ ]:




