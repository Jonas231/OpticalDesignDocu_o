#!/usr/bin/env python
# coding: utf-8

# ## Gaussian beam tracing in CodeV

# The Gaussian beam trace (BEA) implemented in CodeV appears to be similar to the OpTaliX "Bea", it is not however, because it allows for <u> Gaussian beams with general astigmatism </u>.

# ### Bea:
# See the note in the Code V manual: 
# 
# "Use the Gaussian Beam Trace (BEA) option when you want to determine the waist locations and sizes along chief rays in your optical system for unclipped Gaussian beams in the reference wavelength. Astigmatism and field curvature are included, but no other aberrations. This option <u> applies to any system regardless of symmetry </u>. It is most useful for systems containing narrow, slow beams where geometrical optics does not adequately predict the positions and sizes of the beam at the focus. In systems of this type, the focused spot is often similar in size to the beam diameter. A typical use would be to analyze a laser scanning system.
# 
# How is the computation performed?:
# 
# "Gaussian Beam Trace (BEA) propagates an untruncated Gaussian beam through the system. Since the only aberration accounted for is the local astigmatism of the beam, the beam profile remains Gaussian although the diameter, elliptical ratio and orientation may change from point to point. 
# The beam is propagated along the chief ray, using close skew rays to determine the local astigmatism. Tilts, decenters, and non-spherical surface shapes are all accounted for properly. The mathematical method used is a generalized 4 x 4 ABCD matrix described in “Gaussian Light Beams with General Astigmatism,” Arnaud and Kogelnik, Applied Optics, Vol. 8, No. 8, 1969 and “Matrix Theory of Light Beam Waveguides,” Suematsu and Fukinuki, Bull. Tokyo Inst. Tech, Number 88, 1968."
# 
# The applicability of this feature appears to be similar to Gaussian beam raytracing in KDP-2. 
#     "

# #### A simple example of a focused laser beam:
# All examples are taken from the CodeV help.

# In[1]:


import os

def wl(file, L):
    """
    Function for writing a line in a file.
    """   
    file.writelines(L)
    file.write("\n") 
    
filename = "simp_foc_lens.seq"      # name of the .seq file to be written using python
f = open(os.path.join(r"C:\Users\herbst\CVUSER", filename),"w")

# wl(f, [''])
wl(f, ['! execute in CodeV with: in '+str(filename)])
wl(f, ['! this file should be located in CVUSER folder or macro folder, then use: in cv_macro:'+str(filename)])
wl(f, [''])
wl(f, ['! lens is focusing collimated light. This is how one would normally set up a focusing lens if one were not concerned with the effects of slow f-numbers.'])
wl(f, [''])
wl(f, ['RDM                      !Radius input mode'])
wl(f, ['LENS'])
wl(f, ["TITLE 'FOCUSING LENS'"])
wl(f, ['dim m                    ! dimensions are in mm'])
wl(f, ['WL 632.8                 ! HeNe wavelength'])
wl(f, ['EPD 1                    ! laser beam diameter of 1 mm'])
wl(f, ['S 500 1 BK7              ! first surface of plane convex lens; radius of curvature: 0.5 m'])
wl(f, ['STO                      ! This surface is the aperture stop'])
wl(f, ['S 0 0                    ! Second surface of lens'])
wl(f, ['PIM                      ! Image at paraxial image distance'])
wl(f, ['GO'])

wl(f, [''])
wl(f, ['! now change the setup and perform BEA:'])
wl(f, [''])

wl(f, ['PIM  NO                  ! delete the PIM solve: Could be done with DEL PIM'])
wl(f, ['THI  S0  50              ! The laser is located 50 mm away from the lens'])
wl(f, ['BEA                      ! Enter the BEA option'])
wl(f, ['WRY  0.5                 ! The laser beam is 1.0 mm diameter'])
wl(f, ['GO'])


                              G A U S S I A N   B E A M   P R O P A G A T I O N

         FOCUSING LENS                                                                        POSITION  1

         WAVELENGTH  =      632.8 NM       DIMENSIONS = MILLIMETERS         FIELD POSITION = ( 0.00, 0.00)


                                  BEAM     WAVEFRONT RADIUS     PHASE      WAIST RADIUS
    PROPAGATION   BEAM RADIUS  ORIENTATION    OF CURVATURE   ORIENTATION      BEFORE         DISTANCE FROM
    DISTANCE TO   ON SURFACE    (DEGREES)  BEFORE REFRACTION  (DEGREES)     REFRACTION      WAIST TO SURFACE
SUR NEXT SURFACE   X        Y                  X         Y                  X        Y         X         Y

OBJ   50.0000   0.5000   0.5000    0.0        INF       INF     0.0      0.5000   0.5000   -0.0000   -0.0000
  1    1.0000   0.5004   0.5004    0.0   -30858.94 -30858.94    0.0      0.5000   0.5000   50.0000   50.0000
  2  970.0456   0.5001   0.5001    0.0   1518.1217 1518.1217    0.0      0.3141   0.3141 -919.3122 -919.3122
IMG             0.3911   0.3911    0.0   -1023.421 -1023.421    0.0      0.3141   0.3141  363.2746  363.2746

# In[2]:


wl(f, [''])
wl(f, ['! see the image size at this waist :'])
wl(f, [''])

wl(f, ['TIN SI-1 -363.2743       ! move image plane to waist location: TIN is Thickness INcrement '])
wl(f, ['BEA'])
wl(f, ['WRY 0.5'])
wl(f, ['GO'])

f.close()

G A U S S I A N   B E A M   P R O P A G A T I O N

         FOCUSING LENS                                                                        POSITION  1

         WAVELENGTH  =      632.8 NM       DIMENSIONS = MILLIMETERS         FIELD POSITION = ( 0.00, 0.00)


                                  BEAM     WAVEFRONT RADIUS     PHASE      WAIST RADIUS
    PROPAGATION   BEAM RADIUS  ORIENTATION    OF CURVATURE   ORIENTATION      BEFORE         DISTANCE FROM
    DISTANCE TO   ON SURFACE    (DEGREES)  BEFORE REFRACTION  (DEGREES)     REFRACTION      WAIST TO SURFACE
SUR NEXT SURFACE   X        Y                  X         Y                  X        Y         X         Y

OBJ   50.0000   0.5000   0.5000    0.0        INF       INF     0.0      0.5000   0.5000   -0.0000   -0.0000
  1    1.0000   0.5004   0.5004    0.0   -30858.94 -30858.94    0.0      0.5000   0.5000   50.0000   50.0000
  2  606.7713   0.5001   0.5001    0.0   1518.1217 1518.1217    0.0      0.3141   0.3141 -919.3122 -919.3122
IMG             0.3141   0.3141    0.0   -0.7869e9 -0.7869e9    0.0      0.3141   0.3141    0.0003    0.0003

# #### Example 3: Tilted anamorphic system
# --> shows general astigmatism in an optical system

# In[3]:


filename = "tilt_anamorph_sys.seq"      # name of the .seq file to be written using python
f = open(os.path.join(r"C:\Users\herbst\CVUSER", filename),"w")

# wl(f, [''])
wl(f, ['! execute in CodeV with: in '+str(filename)])
wl(f, ['! this file should be located in CVUSER folder or macro folder, then use: in cv_macro:'+str(filename)])
wl(f, [''])
wl(f, ['!  '])
wl(f, [''])

wl(f, ['LENS'])
wl(f, ["TITLE  'Rotated  Cylinders'"])
wl(f, ['dim m                    ! dimensions are in mm'])
wl(f, ['WL 632.8                 ! HeNe wavelength'])
wl(f, ['EPD 1                    ! laser beam diameter of 1 mm'])

wl(f, [''])

wl(f, ['SO   0.    500.'])
wl(f, ['S1  128.772   0.  BK7    ! fast input mode S: radius of curvature, thickness, glass']) 
wl(f, ['sto'])
wl(f, ['cyl                      ! cylinder lens'])
wl(f, ['S2   0.    500.'])
wl(f, ['S3  103.018   0.  BK7'])
wl(f, ['CYL'])
wl(f, ['CDE  45                  ! rotation by 45°'])
wl(f, ['DAR                      ! Decenter and Return (DAR) surface'])
wl(f, ['S4   0.  100.'])
wl(f, ['S5   0.  100.'])
wl(f, ['S6   0.  100.'])
wl(f, ['S7   0.  100.'])
wl(f, ['S8   0.  100.'])
wl(f, ['S9   0.  100.'])
wl(f, ['S4   0.  100.'])

wl(f, ["REX s1 100.            ! apply rectangular apertures to make the lenses visible in layout plot"])
wl(f, ["REY s1 100."])
wl(f, ["REX s3 100.            ! apply rectangular apertures to make the lenses visible in layout plot"])
wl(f, ["REY s3 100."])

wl(f, ['GO'])

wl(f, [''])

wl(f, ['BEA                      ! Enter the BEA option'])
wl(f, ['WRY  0.1                 ! The laser beam waist diameter is 0.2 mm '])
wl(f, ['GO'])


# The built up optical system looks like this in CodeV: ![image.png](attachment:image.png)
# ![image-2.png](attachment:image-2.png)
G A U S S I A N   B E A M   P R O P A G A T I O N

         Rotated  Cylinders                                                                   POSITION  1

         WAVELENGTH  =      632.8 NM       DIMENSIONS = MILLIMETERS         FIELD POSITION = ( 0.00, 0.00)


                                  BEAM     WAVEFRONT RADIUS     PHASE      WAIST RADIUS
    PROPAGATION   BEAM RADIUS  ORIENTATION    OF CURVATURE   ORIENTATION      BEFORE         DISTANCE FROM
    DISTANCE TO   ON SURFACE    (DEGREES)  BEFORE REFRACTION  (DEGREES)     REFRACTION      WAIST TO SURFACE
SUR NEXT SURFACE   X        Y                  X         Y                  X        Y         X         Y

OBJ  500.0000   0.1000   0.1000    0.0        INF       INF     0.0      0.1000   0.1000   -0.0000   -0.0000
  1    0.0000   1.0121   1.0121    0.0   -504.9294 -504.9294    0.0      0.1000   0.1000  500.0000  500.0000
  2  500.0000   1.0121   1.0121    0.0   -765.0131  750.2170    0.0      0.1000   0.0981  757.5446 -743.1709
  3    0.0000   2.0167   0.1000  -45.0   -249.9416 -1002.465   45.0      0.0981   0.1000    9.4870 1000.0000
  4  100.0000   2.0167   0.1000    0.0    519.3813 -519.6514  -29.5             *
  5  100.0000   1.7882   0.2189   16.7    505.3771 -125.4208   -3.5             *
  6  100.0000   1.7545   0.3331   37.2    439.6397 -211.4116   -1.5             *
  7  100.0000   0.3465   1.9462  -33.4    363.9548 -303.4831   -0.3             *
  8  100.0000   0.2875   2.3062  -19.4    297.7893 -394.3739    1.2             *
  9  100.0000   0.2116   2.7614   -9.9    279.8000 -477.0109    4.2             *
IMG             0.1681   3.2688   -3.4   1068.0864 -509.3459   17.1             *

                             * Waist not defined - beam has general astigmatism

# Why does the beam orientation change after 5? Can this be visualized within CodeV?

# In[4]:


wl(f, ['bea;wry 0.1;dis;go'])

f.close()


# ![image.png](attachment:image.png)

# Not really nice to see in yz-section.

# In[ ]:




