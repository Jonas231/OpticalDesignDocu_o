#!/usr/bin/env python
# coding: utf-8

# # Setup a Cooke triplet with python
# 
# The following python code creates a .mac file which is a macro that can be executed within the OpTaliX cli with the command "run Cooke_triplet.mac". This procedure is used for convenience in order to have a list of OpTaliX commands afterwards and to clearly separate between command syntax and text in this notebook. Once you have executed this notebook the file "Cooke_triplet.mac" will be located in the path "filename" (see below). Of course the system can also be built up using the gui.
# 
# At first a function is defined to write a string line into a file.

# In[1]:


def wl(file, L):
    """
    Function for writing a line in a file.
    """   
    file.writelines(L)
    file.write("\n") 


# ## Setup of the optical model
# Now the code to create the .mac file (with a sequence of OpTaliX commands) for the creation of an optical model of a Cooke triplet (as starting system) follows:

# In[2]:


import os
from datetime import date
today = date.today()
d2 = today.strftime("%B %d, %Y")

filename = "Cooke_triplet.mac"      # name of the .mac file to be written using python
f = open(os.path.join(r"C:\ProgramData\OpTaliX\macro", filename),"w")

wl(f, ['! execute in Optalix with: run '+str(filename)])
wl(f, ['! this file should be located in "C:\ProgramData\OpTaliX\macro"'])
wl(f, ['! generated with python: ', d2])
wl(f, [''])          # empty line

wl(f, ['! This macro sets up a Cooke triplet'])     # write our first commend
wl(f, ['len'])                 # create a new lens
wl(f, ['! dim m          ! standard is [mm]'])

wl(f, ['ins s'+str(2)+'         ! insert one surface'])
wl(f, ['ins s'+str(3)+'..s'+str(10)+'       ! insert multiple surfaces'])

#wl(f, ['SAY '+str(18.47)])     # = starting marginal reference height at surface 1 (semi-diameter of entrance pupil)
wl(f, ['EPD '+str(18.3*2)])    # = starting marginal reference height at surface 1 (entrance pupil)

#wl(f, ['SCY FANG 20.81'])      # define reference object height, important for FOB!, p. 66 of KDP-2 manual, express object by angle
#wl(f, ['YOB 20.81'])            # Object coordinates (Y) for finite object distances
#wl(f, ['TH 1.0E20'])           # set thickness of 1st surface to infinite (beam collimated)
wl(f, ['THI s0 1.0E20'])
#wl(f, ['AIR'])                 # the medium of between surface 0 is air

#wl(f, ['AIR'])                 # insert 2nd surface with medium air

wl(f, [''])          # empty line    
wl(f, ['sut s1..s10 s      ! set surface types (s = spherical)'])
wl(f, [''])          # empty line

wl(f, ['FHY s1 1           ! Sets the height of surfaces si..j to fixed '])    
wl(f, ['THI s1 0'])

#wl(f, ['FHY s2 1           ! Sets the height of surfaces si..j to fixed '])    
wl(f, ['RDY s2 40.94'])            # set the radius of the 2nd surface
wl(f, ['THI s2 8.74'])             # set the thickness between 2nd surface and 3rd surface
wl(f, ['CIR s2 p1 18.5'])           # set circular clear aperture to ...
wl(f, ['com s'+str(2)+' 1st lens 1st surface       ! surface comments'])   # give surface a surface comment
wl(f, ['GLA s2 K-SSK4'])          # set the medium to glass "SSK4"
wl(f, [''])          # empty line

#wl(f, ['FHY s3 1           ! Sets the height of surfaces si..j to fixed '])    
wl(f, ['THI s3 11.05'])
wl(f, ['CIR s3 p1 18.5'])
wl(f, ['com s3 1st lens 2nd surface'])  # give surface a label
wl(f, [''])          # empty line

#wl(f, ['FHY s4 1           ! Sets the height of surfaces si..j to fixed '])    
wl(f, ['RDY s4 -55.65'])
wl(f, ['THI s4 2.78'])
wl(f, ['CIR s4 p1 14.9'])
wl(f, ['GLA s4 SF2'])
wl(f, [''])          # empty line

#wl(f, ['FHY s5 1           ! Sets the height of surfaces si..j to fixed '])   
wl(f, ['RDY s5 39.75'])
wl(f, ['THI s5 1'])
wl(f, ['CIR s5 p1 14.4'])
#wl(f, ['AIR'])
wl(f, [''])          # empty line

#wl(f, ['FHY s6 1           ! Sets the height of surfaces si..j to fixed ']) 
wl(f, ['THI s6 6.63'])
#wl(f, ['REFS'])                # reference surface
#wl(f, ['ASTOP'])               # aperture stop
wl(f, ['sto s6           ! set stop surface'])
wl(f, ['com s6 aperture stop'])  # give surface a label
#wl(f, ['AIR'])
wl(f, [''])          # empty line

#wl(f, ['FHY s7 1           ! Sets the height of surfaces si..j to fixed ']) 
wl(f, ['RDY s7 107.9'])
wl(f, ['THI s7 9.54'])
wl(f, ['CIR s7 p1 15.5'])
wl(f, ['GLA s7 K-SSK4'])
wl(f, [''])          # empty line

wl(f, ['FHY s8 1           ! Sets the height of surfaces si..j to fixed '])   
wl(f, ['RDY s8 -43.33'])
wl(f, ['THI s8 78'])
wl(f, ['CIR s8 p1 15.5'])
#wl(f, ['AIR'])
wl(f, [''])          # empty line

#wl(f, ['AIR'])
#wl(f, ['AIR'])
#wl(f, ['EOS'])
wl(f, [''])          # empty line

wl(f, ['nfld '+str(5)])
wl(f, ['xan f1 '+str(20.81)+   '!      set set x field angle of field 1'])
wl(f, ['yan f1 '+str(0)])

wl(f, ['xan f2 '+str(-20.81)+   '!      set set x field angle of field 1'])
wl(f, ['yan f2 '+str(0)])

wl(f, ['xan f3 '+str(0)+   '!      set set x field angle of field 1'])
wl(f, ['yan f3 '+str(0)])

wl(f, ['xan f4 '+str(0)+   '!      set set x field angle of field 1'])
wl(f, ['yan f4 '+str(20.81)])

wl(f, ['xan f5 '+str(0)+   '!      set set x field angle of field 1'])
wl(f, ['yan f5 '+str(-20.81)])

#wl(f, ['VIEVIG YES'])         # automatic vignetting in VIE
#wl(f, ['set vig'])
#wl(f, ['SET MHT s1..8 f1..5 z1'])

wl(f, ['vie'])                # show lens layout

f.close()


# You then go to KDP-2 folder start the application and input "input file Cooke_triplet.dat" in the command line. This will execute all the commands written with the function "wl" in this section. You will obtain this plot:

# In[3]:


PATH = r'C:\Users\herbst\OpticalDesignDocu'
from IPython.display import Image
Image(filename = PATH + "\OpTaliX_Cooke_triplet.png", width=1000, height=800)


# Or view in orthographic projection:

# In[4]:


Image(filename = PATH + "\OpTaliX_Cooke_triplet_ortho.png", width=1000, height=800)


# Or use POV ray to render the lens in 3D. This is no interactive plot, however.
# 

# In[5]:


Image(filename = PATH + "\OpTaliX_Cooke_triplet_povray.png", width=600, height=600)


# A fully interactive 3D rendered plot can be generated with python, i.e. pyvista (see: [OpTaliX: Interactive 3D layout with Python](./OpTaliX_interactive_3DLayout.ipynb)).

# The lens can be updated and its specifications can be changed:

# In[ ]:





# ## Analysis
# The aberrations of this Cooke triplet can be analyzed with the following commands:

# In[6]:


# display YZ-plane paraxial ray data


# The 3rd order aberration values calculated. To calculate and display the 3rd spherical aberrations, issue the command:

# In[7]:


# the 3rd, 5th and 7th order spherical aberrations


# In[8]:


#Image(filename = PATH + "\KDP-2_Cooke_triplet_SA.png", width=300, height=300)


# Chromatic differences:

# In[9]:


#wl(f, ['PCW?'])        # query primary and secondary wavelength pairs
#wl(f, ['SCW?'])
#wl(f, ['PCDSA ALL'])   # calculate the primary chromatic differences for 3rd, 5th and 7th order spherical aberrations


# ABERRATION FANS AND THEIR PLOTS - To generate transverse fan data at a specific point in the field of view, issue an "FOB" command which specifies that fractional field of view location. In our example lens, the SCY FANG value was 20.81 degrees. To use "FOB" to specify that analysis is to be performed at a Y-object angle of 2.5 degrees and an X-object angle of 1.25 degrees, issue:
#     

# In[10]:


#wl(f, ['FOB 0.1201 0.060067'])
#wl(f, ['YFAN, -1, 1, 1, 11'])
#wl(f, ['FAN'])


# One obtains this table of values which can also be written to a text file (and plotted with matplotlib, e.g.) or it can be directly plotted with KDP-2 (see below).

# In[11]:


#Image(filename = PATH + "\KDP-2_Cooke_triplet_yfan_preopt.png", width=900, height=800)


# The "FAN" command can be used to generate more complex ray fan aberration graphics. The next two commands generate YZ and XZ-plane, transverse ray aberration plots for all five defined fields.

# In[12]:


Image(filename = PATH + "\OpTaliX\OpTaliX_fan.png", width=900, height=800)


# Plotting of spot diagrams in OpTaliX and with python (see: [Create spot diagram and plot with python](./OpTaliX_plotly_spot_diagram.ipynb)), using:

# In[13]:



#wl(f, ['SPO'])         # create spot diagram data


# In[14]:


Image(filename = PATH + "\OpTaliX\OpTaliX_spot.png", width=900, height=800)


# Geometrical and Diffraction MTF generation and plotting is done with these commands for all defined fields: 

# In[15]:


#wl(f, ['MTF FRE GEO'])   # generate and plot geometric MTF vs. frequency
#wl(f, ['MTF FRE'])       # generate and plot diffraction MTF vs. frequency


# In[16]:


Image(filename = PATH + "\OpTaliX\OpTaliX_mtf.png", width=900, height=800)


# ## Optimization with predefined operands:
# 
# The aim is to vary the last surface curvature and its conic constant of the current lens so as to change the system focal length to 100 mm while at the same time driving the 3rd order spherical aberration to 0.0. 
# 
# Lists of predefined target operands in KDP-2 are here: 
# [**Operands**](./KDP-2_markdown.md)
# 
# Just type the following lines in the KDP-2 cli:
# 
# Do a PY solve:
# 

# In[ ]:





# Next, set up the operands (targets) with the following commands:

# In[ ]:





# Next, set up the variables with the following commands:

# In[ ]:





# In[ ]:





# This optimization problem can be solved with damped least squares (ITER) or directly (PFIND) since we have two variables and two operands which happen to be linearly independent. We will do a combination of the two techniques. Type:

# In[ ]:





# After these optimization cycles, the FMT (Figure of Merit) will be much smaller than it was. Before we started, it was 0.13095. The new focal length and SA3 values will be very near their target values. Further cycles could drive the values closer to their targets. The new curvature and conic values can be seen by issuing another VB command or by issuing an RTG ALL or an RTG 8 command. The thickness of surface 9 has now changed to 0.474615 mm in order to maintain paraxial focus. There are other optimization methods described in the reference manual which you should try.

# In[ ]:





# In[ ]:




