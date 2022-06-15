#!/usr/bin/env python
# coding: utf-8

# # Gaussian beam raytracing and propagation in OpTaliX

# As example the asphere "AFL12-15" of the asphericon lens catalog available in OpTaliX is used. Here the geometric spot is much smaller than the Airy disc, i.e. the lens is diffraction limited.
# ![image.png](attachment:image.png)

# Gaussian beam tracing in OpTaliX is described in the reference manual in the section "Image Evaluation". A differential raytracing procedure (following Arnaud, Kogelnik and Li, and Herloski, Marshall and Antos) seems to be used to represent the propagation of a gaussian beam by tracing paraxial rays. The description suggests that only simple astigmatic Gaussian beams can be traced in OpTaliX. 
# 
# Look at this note from the manual: "In this context, note that the Gaussian beam analysis (BEA)
# as described in section 14.3 only models paraxial quantities of ideal Gaussian beams and does not
# include wave aberrations."
# 
# 
# A nice review and procedure of Gaussian beam raytracing and optimization (including general astigmatic Gaussian beams) is given by [Colbourne](https://www.semanticscholar.org/paper/Generally-astigmatic-Gaussian-beam-representation-Colbourne/6708287c4855b2a2de2919aa051a95f6355e7e07), see also [Lumentum](https://resource.lumentum.com/s3fs-public/technical-library-items/skew-ray-gaussian-beam-optimization.pdf).

# In the following table the Gaussian beam analysis commands implemented in OpTaliX are listed:

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

import os
cwd = os.getcwd()
filename = os.path.join(cwd, os.path.join('Excel', 'OpTaliX_commands.xlsx'))
df_var = pd.read_excel(filename, sheet_name = "Gaussian beams", header = 0, index_col = 0)
df_var = df_var.dropna()   # drop nan values
df_var


# For the above example lens the command "bea" (bea ? --> provides a settings dialog) 
# ![image.png](attachment:image.png)
# generates this output:
Gaussian Beam Analysis:

 Wavelength =      0.28500 micron
 M-squared  =      1.00000

 X/Z-Plane :
         Spot Size    Waist Size    Waist Dist    Divergence     RFR Radius    Rayleigh R.    Fresnel
   #           SRX           WRX           ZWX           GDX            RCX           RRX         No.
   0      0.005000      0.005000      0.000000      0.018142                                    0.000
   1      0.005000      0.004999      0.007553      0.012158    0.22387E+02      0.275485       0.022
   2      0.048801      0.004999     -2.675085      0.018145   -0.27035E+01      0.275485       0.678
   3      0.272163      0.004999    -14.995408      0.018145   -0.15000E+02      0.275485

 Y/Z-Plane :
         Spot Size    Waist Size    Waist Dist    Divergence     RFR Radius    Rayleigh R.    Fresnel
   #           SRY           WRY           ZWY           GDY            RCY           RRY         No.
   0      0.005000      0.005000      0.000000      0.018142                                    0.000
   1      0.005000      0.004999      0.007553      0.012158    0.22387E+02      0.275485       0.022
   2      0.048801      0.004999     -2.675085      0.018145   -0.27035E+01      0.275485       0.678
   3      0.272163      0.004999    -14.995408      0.018145   -0.15000E+02      0.275485

# Another feature implemented in OpTaliX is physical optics propagation (with the following restrictions: "Diffraction beam propagation assumes coherent (monochromatic) radiation. Partial coherence or
# non-monochromatic light cannot be modelled by this option.
# In the current implementation, only axial conditions can be modelled. Decentered and/or tilted configurations
# or skew beams should be avoided. This capability is subject to later releases.")
# 
# For the above example lens the command "bpr" (bpr ? --> provides a settings dialog) generates this output:

# ![image.png](attachment:image.png)

# ![image.png](attachment:image.png)

# In[ ]:





# In[ ]:




