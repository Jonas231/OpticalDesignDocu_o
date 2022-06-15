#!/usr/bin/env python
# coding: utf-8

# ## Comparison: Optimization for reduced tolerance sensitivity / maximum production yield

# ### KDP-2
# No built-in ways do reduce tolerance sensitivity during optimization are described in the manual.
# 
# ### OpTaliX
# "OpTaliX provides several commands to calculate tolerance sensitivity, TSF, TST, TSI, TSN, TSV, TSX, TSY, TSZ, TSA, TSB, TSG. " and minimize these sensitivities during optimization.

# ### CodeV
# Code V includes the "SAB - Sensitivity As Built" option within automatic design (AUT). See what is written in the Code V help:
# 
# "The Reduce Tolerance Sensitivity (SAB, for Sensitivity As Built) control can be used in AUT for improving the as-built performance by using wavefront differential coefficients, for each tolerance at each field and zoom, to reduce the tolerance sensitivity of the optimized design. The SAB command allows you to specify a zoom number or range, field number or range, and aberration weight. CODE V then constructs a set of appropriate aberrations that are used internally during optimization. You may optionally specify the number of rays across the diameter for evaluating the ray grid (otherwise, 32 rays are used by default).
# 
# This feature is generally applicable to any system for which the Wavefront Differential Tolerancing (TOR) option provides an accurate analysis of tolerance sensitivity. Prior to using the SAB error function in AUT, you should define tolerances and compensators for your optical system. As with other specialized optimization improvement features (such as MTF optimization), you generally should begin with a locally-optimized design. Some computational issues that you need to be aware of are discussed below.
# "

# ### ZEMAX
# ZEMAX provides two built-in ways to optimize for minimum sensitivity of performance with respect to fabrication tolerances (maximum production yield): 
# - [TOLR](https://support.zemax.com/hc/en-us/articles/1500005575222-How-to-optimize-for-as-built-performance) is a merit function operand which gives access to the estimated change of the RMS spot radius (a result of the sensitivity analysis). 
# 
#     "OpticStudio uses a Root Sum Square (RSS) assumption for computing the estimated changes in the performance. For each tolerance, the change in performance from the nominal is squared and then averaged between the min and max tolerance values. The resulting averaged squared values are then summed for all the tolerances, and the square root of the result is taken. The average of the min and max tolerances is taken because the min and the max tolerance cannot both occur simultaneously, and so summing the squares would result in an overly pessimistic prediction. The resulting RSS is the estimated change in performance."
# 
#     "TOLR with a data item of 1 computes the nominal performance, data item 0 the expected change and data item 2 the final performance (sum of these two)."
# - ["Improve Manufacturing Yield"](https://support.zemax.com/hc/en-us/articles/1500005575222-How-to-optimize-for-as-built-performance) is an option in the merit function wizard which inserts "HYLD operands", which minimize the angle of incidence in the design. 
# 
#     "The method applies a penalty term to the merit function discourages high angles of incidence or exitance at optical surfaces. 
# 
#     The penalty term acts as a surrogate for the induced aberrations in a design. Its value can be computed at every surface and can be optimized toward zero at every surface.
# 
#     The penalty term value is integrated into OpticStudio as the HYLD operand and easily added to the merit function using a simple "Improve Manufacturing Yield" option in the Optimization Wizard."

# A comparison of Code V (Sensitivity As Built (SAB) method) and ZEMAX (TOLR) is provided in this open-access publication, e.g.:
# - [Zhiyuan Gu, Yang Wang, and Changxiang Yan, "Optical system optimization method for as-built performance based on nodal aberration theory," Opt. Express 28, 7928-7942 (2020) ](https://opg.optica.org/oe/fulltext.cfm?uri=oe-28-6-7928&id=428713)

# In[ ]:




