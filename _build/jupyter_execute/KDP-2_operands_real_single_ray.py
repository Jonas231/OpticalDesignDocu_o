#!/usr/bin/env python
# coding: utf-8

# # Real single ray 
# 
# These are the real single ray operands. Real raytracing is exact raytracing without paraxial approximation.

# In[1]:


import pandas as pd
import itables
from itables import init_notebook_mode, show
import itables.options as opt

init_notebook_mode(all_interactive=True)

opt.lengthMenu = [50, 100, 200, 500]
#opt.classes = ["display", "cell-border"]
#opt.classes = ["display", "nowrap"]

opt.columnDefs = [{"className": "dt-left", "targets": "_all"}, {"width": "500px", "targets": 4}]
#opt.maxBytes = 0
#pd.get_option('display.max_columns')
#pd.get_option('display.max_rows')



# In[2]:


import os
cwd = os.getcwd()
filename = os.path.join(cwd, os.path.join('Excel', 'KDP-2_optimization_operands.xlsx'))

df_RSR = pd.read_excel(filename, sheet_name = "real single ray", header = 1, index_col = 0)
df_RSR = df_RSR.dropna()   # drop nan values


# In[3]:



df_RSR


# In[ ]:





# In[ ]:





# In[ ]:




