#!/usr/bin/env python
# coding: utf-8

# ## Gaussian beam raytracing in ZEMAX

# ### Built-in methods
# 
# As described in the tutorial [Modeling Laser Beam Propagation in OpticStudio](https://www.zemax.com/blogs/free-tutorials/modeling-laser-beam-propagation-in-opticstudio) there are 3 built-in methods "in OpticStudio sequential mode to model Gaussian beam propagation. They are:
# 
# - The ray-based approach
# - Paraxial Gaussian Beam analysis
# - Physical Optics Propagation "
# 
# #### Limitations:
# 
# - The ray-based approach:
# 
# "As we know the laser beam diffracts as it propagates through the space, which cannot be modeled by ray-based approach. While we know that the focused spot size reported by the ray based calculation is not accurate in this case, this does not mean the result of our optimization to find the location of the best focus is invalid."
# 
# - Paraxial Gaussian Beam analysis:
# 
# "The limit is that the calculation of Gaussian beam parameters is based upon paraxial ray data, therefore the results may not be accurate for systems which have large aberrations, or those cannot be described by paraxial optics, such as non-rotationally symmetric systems. This feature also ignores all apertures, and assumes the Gaussian beam propagates well within the apertures of all the lenses in the system."
# 
# - Physical Optics Propagation
# 
# Does not condsider decenter and tilts. Generally astigmatic gaussian beams cannot be modelled.

# These methods either do no consider diffraction or are not applicable in case of decenters and tilts. They are also not suited to provide a layout of Gaussian beams within a general optical system. Gaussian beams are not properly represented during optimization
# 

# ### User-defined methods
# There are however dlls and zpl macros which allow to model generally astigmatic Gaussian beams in OpticStudio:
# - In non-sequential mode: 
#     [Link](https://community.zemax.com/code-exchange-10/dll-source-non-sequential-astigmatic-gaussian-1695)
# - In sequential mode:
#     [Link](ttps://support.zemax.com/hc/en-us/articles/1500005489661-Using-skew-rays-to-model-Gaussian-beams-webinar)
#     
# A nice review and procedure of Gaussian beam raytracing and optimization in sequential mode (including general astigmatic Gaussian beams) is given by [Colbourne](https://www.semanticscholar.org/paper/Generally-astigmatic-Gaussian-beam-representation-Colbourne/6708287c4855b2a2de2919aa051a95f6355e7e07), see also [Lumentum](https://resource.lumentum.com/s3fs-public/technical-library-items/skew-ray-gaussian-beam-optimization.pdf).

# In[ ]:




