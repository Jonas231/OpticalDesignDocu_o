#!/usr/bin/env python
# coding: utf-8

# # KDP-2 Operands: Gaussian beams
# 
# These are the operands of Gaussian beams.

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


filename = r'C:\Work\Tools\OpticalDesign_Doku\KDP-2_optimization_operands.xlsx'

df_gb = pd.read_excel(filename, sheet_name = "Gaussian beam", header = 1, index_col = 0)
df_gb = df_gb.dropna()   # drop nan values


# In[3]:



df_gb


# In[ ]:





# In[ ]:





# In[ ]:




