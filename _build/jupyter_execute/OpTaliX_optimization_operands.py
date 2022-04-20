#!/usr/bin/env python
# coding: utf-8

# # OpTaliX: Optimization Targets  / Constraints
# 
# These are the items which can be set as targets or constraints (in the merit function) during optimization.

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
df_targets = pd.read_excel(filename, sheet_name = "Targets", header = 0, index_col = 0)
df_targets = df_targets.dropna()   # drop nan values


# In[3]:


df_targets


# In[ ]:





# In[ ]:




