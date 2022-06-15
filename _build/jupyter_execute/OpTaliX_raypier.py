#!/usr/bin/env python
# coding: utf-8

# # OpTalix to raypier
# 
# The OpTaliX file "Mobile_US20070024958A1.otx" is read with python, parsed and converted to a raypier model.

# In[1]:


filename = r"C:\Work\OpTaliX\Test\Mobile_US20070024958A1.otx"
filename = r"C:\Work\OpTaliX\Test\AFL12-15.otx"

# opten and read the .otx file
with open(filename) as f:
    data = f.readlines()


# In[2]:


#lines


# In[3]:


#import re
#p = re.compile(lines[0])
#print(p.match("VERS"))


# In[ ]:





# In[4]:


import numpy as np

def ret_value(line, f = 1, to_float=1, listf = 0):
    # function to return values
    if listf == []:
       a = listf
       a.append(line)
    else:
        if to_float:
            a=np.array(line.split()[f:]).astype(float)
        else:
            a=np.array(line.split()[f:])
    return a

def search_string_in_file(file_name, string_to_search):
    """Search for the given string in file and return lines containing that string,
    along with line numbers"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            # For each line, check if line contains the string
            line_number += 1
            if string_to_search in line:
                # If yes, then add the line number & line as a tuple in the list
                list_of_results.append((line_number, line.rstrip()))
    # Return list of tuples containing line numbers and lines where string is found
    return list_of_results

def search_multiple_strings_in_file(file_name, list_of_strings):
    """Get line from the file along with line numbers, which contains any string from the list"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    with open(file_name, 'r') as read_obj:
        # Read all lines in the file one by one
        for line in read_obj:
            line_number += 1
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line along with line number in list
                    list_of_results.append((string_to_search, line_number, line.rstrip()))
    # Return list of tuples containing matched string, line numbers and lines where string is found
    return list_of_results

def search_multiple_strings_in_file_mod(data, list_of_strings):
    """Get line from the file along with line numbers, which contains any string from the list"""
    line_number = 0
    list_of_results = []
    # Open the file in read only mode
    #with open(file_name, 'r') as read_obj:
    #    # Read all lines in the file one by one
    if 1:
        for line in data:
            line_number += 1
            # For each line, check if line contains any string from the list of strings
            for string_to_search in list_of_strings:
                if string_to_search in line:
                    # If any string is found in line, then append that line along with line number in list
                    list_of_results.append((string_to_search, line_number, line.rstrip()))
    # Return list of tuples containing matched string, line numbers and lines where string is found
    return list_of_results

# search in file
filen_L = []
rem_L = []
fld_L = []

for line in data:
    if 'VERS' in line:
        vers = line
    if 'FILE' in line:
        filen_L.append(line)
    if 'REM' in line:                # comment
        rem_L.append(line)
    if 'PPOS' in line:               # Plot zoom position'
        ppos = ret_value(line)
    if 'NRD' in line:                # 
        nrd = ret_value(line)
    if 'DVOM' in line:               # 
        dvom = ret_value(line)
    if 'RAIM' in line:               # 
        raim = ret_value(line)
    if 'RAIC' in line:               # 
        raic = ret_value(line)   
    if 'PIM' in line:               # 
        pim = ret_value(line) 
    if 'TRA' in line:               # 
        tra = ret_value(line) 
    if 'POL' in line:               # 
        pol = ret_value(line, f = 2) 
    if 'WRX' in line:               # 
        wrx = ret_value(line) 
    if 'WRY' in line:               # 
        wry = ret_value(line) 
    if 'ZWX' in line:               # 
        zwx = ret_value(line) 
    if 'ZWY' in line:               # 
        zwy = ret_value(line) 
    if 'RCX' in line:               # 
        dvom = ret_value(line) 
    if 'RCY' in line:               # 
        rcy = ret_value(line)
    if 'M2' in line:               # 
        m2 = ret_value(line)
    if 'TGR' in line:               # 
        tgr = ret_value(line)
    if 'MPRS' in line:               # 
        mprs = ret_value(line, to_float=0)
    if 'MPRR' in line:               # 
        mprr = ret_value(line, to_float=0)
    if 'FSR' in line:               # 
        fsr = ret_value(line)
    if 'FSD' in line:               # 
        fsd = ret_value(line)
    if 'FRR' in line:               # 
        frr = ret_value(line)
    if 'FRD' in line:               # 
        frd = ret_value(line)
    if 'FNO' in line:               # 
        fno = ret_value(line)
    if 'WL' in line:               # 
        wl = ret_value(line)
    if 'WTW' in line:               # 
        wtw = ret_value(line)
    if 'REF' in line:               # 
        ref = ret_value(line)
    if 'OSPF' in line:               # 
        ospf = ret_value(line)
    if 'IFR' in line:               # 
        ifr = ret_value(line)
    if 'FTYP' in line:               # 
        ftyp = ret_value(line)
    if 'MAXFLD' in line:               # 
        maxfld = ret_value(line)
    if 'NFLD' in line:               # 
        nfld = ret_value(line)
    if 'FLD' in line:               # 
        #fld = ret_value(line)
        fld_L.append(line.split())
    if 'MFR' in line:               # 
        mfr = ret_value(line)
    if 'MFRF' in line:               # 
        mfrf = ret_value(line)
    if 'MTFAVG' in line:               # 
        mtfavg = ret_value(line)
    if 'MTFIDEAL' in line:               # 
        mtfideal = ret_value(line)
    if 'AFR' in line:               # 
        afr = ret_value(line)
    if 'DEF' in line:               # 
        def_ = ret_value(line)
    if 'KLDR' in line:               # 
        kldr = ret_value(line)
    if 'PLSC ' in line:               # 
        plsc = ret_value(line)
    if 'PLSC2' in line:               # 
        plsc2 = ret_value(line)
    if 'DISTREF' in line:               # 
        distref = ret_value(line)
    #if 'AF' in line:               # 
    #    af = ret_value(line)
    if 'TRXLAM ' in line:               # 
        trxlam = ret_value(line)
    if 'TRXLAM2' in line:               # 
        trxlam2 = ret_value(line)
    if 'TRPLANE' in line:               # 
        trplane = ret_value(line)

        
list_data = search_multiple_strings_in_file_mod(data, list_of_strings = ["SUR", "! "])
list_data = np.array(list_data)
list_data_s = search_multiple_strings_in_file_mod(data, list_of_strings = ["SUR"])
list_data_s = np.array(list_data_s)
#print(list_data)
surend = int(list_data[list_data[:,0]=='! '][1][1])
#print("surend = ", surend)

list_data_s = list_data_s[list_data_s[:,1].astype(int)<surend]

# get information for every surface
list_L = []
list_data_sur_L = []
for i in range(0,len(list_data_s )):
    
    if i < len(list_data_s)-1:
        lineindex = int(list_data_s[i][1])
        lineindex2 = int(list_data_s[i+1][1])
    else:
        lineindex = int(list_data_s[i][1])
        lineindex2 = surend
    list_L.append((lineindex, lineindex2))
    
    list_data_sur = search_multiple_strings_in_file_mod(np.array(data)[lineindex: lineindex2], list_of_strings = ["SUT", "CUY", "THI", "APE", 
                                                                                 "STO", "GLA", "ASP", "VAR"])
    list_data_sur_L.append((list_data_s [i], np.array(list_data_sur)))
    


# In[5]:


#print(list_data_s)
#print(list_data_sur)
#print(list_L)
#print(surend)


# In[6]:


#print(len(list_data_sur_L))
#print(list_data_sur_L[2][0])
#print(list_data_sur_L[8][1])
#print((list_data_sur_L[8][1][list_data_sur_L[8][1][:,0] == "GLA"])[:,2])
#print(list_data_sur_L[0][1][list_data_sur_L[0][1][:,0] == "CUY"][:,2][0])
#print(list_data_sur_L[2][1].shape)
#print(list_data_sur_L[i][1][list_data_sur_L[i][1][:,0] == "SUT"])
sut_L = []
cuy_L = []
thi_L = []
sto_L = []
var_L = []
gla_L = []
ape_L = []
asp_L = []
for i in range(0,len(list_data_sur_L)):
    #print("i = ", i)
    sut = list_data_sur_L[i][1][list_data_sur_L[i][1][:,0] == "SUT"][:,2][-1][-1]
    cuy = float(list_data_sur_L[i][1][list_data_sur_L[i][1][:,0] == "CUY"][:,2][0][6:])
    thi = float(list_data_sur_L[i][1][list_data_sur_L[i][1][:,0] == "THI"][:,2][0][6:])

    sto = list_data_sur_L[i][1][list_data_sur_L[i][1][:,0] == "STO"][:,2]
    gla = list_data_sur_L[i][1][list_data_sur_L[i][1][:,0] == "GLA"][:,2]
    ape = list_data_sur_L[i][1][list_data_sur_L[i][1][:,0] == "APE"][:,2][0][6:]
    asp = list_data_sur_L[i][1][list_data_sur_L[i][1][:,0] == "ASP"][:,2]
    var = list_data_sur_L[i][1][list_data_sur_L[i][1][:,0] == "VAR"][:,2]

    sut_L.append(sut)
    cuy_L.append(cuy)
    thi_L.append(thi)
    sto_L.append(sto)
    gla_L.append(gla)
    ape_L.append(ape)
    asp_L.append(asp)
    var_L.append(var)
print(sut_L)
#print(cuy_L)
print(thi_L)
#print(sto_L)
print(gla_L)
#print(ape_L[-1][5:5+10])
print(asp_L)
#print(asp_L[2][0].split()[1])
#print(var_L)
#result = [i for i in (list_data_sur_L[2][1]) if i.startswith('SUT')]


# In[7]:


from raypier.api import RayTraceModel, GeneralLens, ParallelRaySource, SphericalFace, CircleShape, OpticalMaterial, AsphericFace


# check
from raypier import tracer
print(tracer.__file__)

if 1:
    ### Build a couple of lenses ###
    shape_L = []
    f_L = []
    for i in range(1,len(list_data_sur_L)):
        
        shape_L.append(CircleShape(radius=float(ape_L[i][5:5+10])))
        print("dia: ", float(ape_L[i][5:5+10]))
        if sut_L[i] == "S":
            print("i: ",i , " sphere")
            
            f_L.append(SphericalFace(curvature=cuy_L[i], z_height=thi_L[i]))
        if sut_L[i] == "A":
            print("i: ",i , " asphere")
            asp_coeffs = asp_L[i][0].split()
            asphere = AsphericFace(z_height=thi_L[i],
                                  curvature=cuy_L[i],            
                                  conic_const= float(asp_coeffs[1]),
                                  A4 = float(asp_coeffs[2]),  # A
                                  A6 = float(asp_coeffs[3]), #I'm not 100% sure if the signs of the polynomial terms are right.
                                  A8 = float(asp_coeffs[4]), # C
                                  A10 = float(asp_coeffs[5]), # D
                                  A12 = float(asp_coeffs[6]), # E
                                  A14 = float(asp_coeffs[7]), # F
                                  A16 = float(asp_coeffs[8])#, # G
                                  #A18 = asp_coeffs[9]  # H
                                  )
            f_L.append(asphere)
            
    print(shape_L)
    print(f_L)
    print(thi_L[0])
    #print(asphere)
            
    #f1 = SphericalFace(curvature=-50.0, z_height=0.0)
    #f2 = SphericalFace(curvature=50.0, z_height=5.0)

    #lens2 = GeneralLens(centre=(0,0,100.0),
    #                    direction=(0,0,1),
    #                    shape=shape,
    #                    surfaces=[f1,f2],
    #                    materials=[m])

    ### Add a source ###
   # src = ParallelRaySource(origin=(0,0,-50.0),
   #                         direction=(0,0,1),
   #                         rings=5,
   #                         show_normals=False,
   #                         display="wires",
   #                         opacity=0.1)
#
  #  model = RayTraceModel(optics=[lens1,lens2],
     #                       sources=[src])


# In[39]:


shape_L


# In[73]:


from raypier.api import GeneralLens, AxiconFace, PlanarFace, OpticalMaterial, CircleShape,            RayTraceModel, CollimatedGaussletSource, EFieldPlane, GaussletCapturePlane, IntensitySurface
            



m = OpticalMaterial(glass_name="N-BK7")
lens  = GeneralLens(centre=(0,0,0),
                    direction=(0,0,1),
                    shape=shape_L[1],
                    surfaces=[f_L[1], f_L[2]],
                    materials=[m])

### Add a source ###
src = ParallelRaySource(origin=(0,0,-5.0),
                        direction=(0,0,1),
                        rings=5,
                        show_normals=True,
                        display="wires",
                        opacity=0.1)

#src = CollimatedGaussletSource(origin=(0.001,0,-10.0),
#                               direction=(0,0,1),
#                               wavelength=0.5,
#                               radius=1.0,
#                               beam_waist=10.0,
#                               resolution=10,
#                               max_ray_len=50.0,
#                               display='wires',
#                               opacity=0.2
#                               )

model = RayTraceModel(optics=[lens],
                      sources=[src])
model.ipython_view(800,600)


# In[42]:


print(1/0.13537295248409)

glass = 'HPFS7980'
dir_path = r'C:\Program Files\OpTaliX-PRO\glasses'

# find glass in OpTaliX glass catalogues
# C:\Program Files\OpTaliX-PRO\glasses
def search_glass(dir_path):
    import os

    # iterate each file in a directory
    for file in os.listdir(dir_path):
        cur_path = os.path.join(dir_path, file)
        # check if it is a file
        if os.path.isfile(cur_path):
            with open(cur_path, 'r') as file:
                # read all content of a file and search string
                if glass in file.read():
                    print('string found in file: ', cur_path)
                    break
    return cur_path

cur_path =  search_glass(dir_path)  


with open(cur_path) as f:
    data_glass = f.readlines()

Legend = search_multiple_strings_in_file_mod(data_glass, list_of_strings = ["!Manufact"])
Legend = np.array(Legend[0])
list_data_glass = search_multiple_strings_in_file_mod(data_glass, list_of_strings = [glass])
list_data_glass = list_data_glass[0][2].split(',')



def filter_info(list_data_glass):
    list_data_glass = list_data_glass[0][2].split(',')
    
    listr_L = []
    for listr in list_data_glass:
        if len(listr) == 1:
            element = listr.replace(',', '')
        else:
            element = listr
        listr_L.append(element )
    

    listr_L = list(filter(None, listr_L))
    listr_L = listr_L[:-3] + listr_L[-3].split(",")
    listr_L = list(filter(None, listr_L))
    listr_L2 = []
    for listr in listr_L:
        element = listr.replace(',', '')
        listr_L2.append(element )
    return listr_L2

#list_data_glass = filter_info(list_data_glass)

#model.ipython_view(400,300)


# In[62]:


print(list_data_glass)
print(Legend[2].split(','))
print(len(list_data_glass))
print(len(Legend[2].split(',')))

Leg = Legend[2].split(',')


print("Leg = ", Leg[14])


# In[70]:


from raypier.api import OpticalMaterialFromFormula
#m1 = OpticalMaterial(from_database=False, refractive_index=1.5)

coeffs = np.array(list_data_glass[4:10]).astype(float).tolist()
print(coeffs)
Lmin =  float(list_data_glass[14])
Lmax =  float(list_data_glass[15])
print(Lmin)
m1 = OpticalMaterialFromFormula(formula_id = 2, coefs = coeffs, wavelen_min = Lmin, wavelen_max = Lmax)


# In[71]:


print(vers)
print(filen_L)
print(ppos)
print(nrd)
print(dvom)
print(pol)
print(wl)
print(fld_L)
print(mfr)
print(mfrf)
print(list_data)
print(surend)
print(lineindex)
print(lineindex2)
print(list_L)
print(list_L[0][1])
print(data[int(list_L[0][0])])
print(np.array(data)[list_L[0][0]:list_L[0][1]])


# In[ ]:


len(list_data)
#np.array(list_data[:])[:,0]
int(list_data[list_data[:,0]=='! Optimization constraints :'][0][1])



print(listc)

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




