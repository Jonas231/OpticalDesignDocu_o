#!/usr/bin/env python
# coding: utf-8

# In[1]:


import KDP_parser
import os
cwd = os.getcwd()
filename = os.path.join(cwd,os.path.join("KDP-2_examples","Cassegrain.DAT"))
#filename = "Newtonian.DAT"
r, L = KDP_parser.search_string_in_file(filename, "#", "PIKUP")


# In[2]:


coating, cv, cc, th, clap, thm, astop, tilt, refl, mat, refs, aimray, mode, fldrays, frays, frays2,flds = KDP_parser.return_optical_data(filename,r, L)


# In[ ]:





# In[ ]:





# In[ ]:




