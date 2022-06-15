# -*- coding: utf-8 -*-
"""
Created on Wed Apr  6 15:52:19 2022

Anleitung: 
Lasse das Makro "export_spots.mac" in OpTaliX laufen und führe anschließend dieses Skript aus

@author: herbst
"""
import numpy as np
import matplotlib.pylab as plt
from matplotlib import cm
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors
import time 
import os

t0 = time.perf_counter()


def centeroidnp(arr):
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return np.array([sum_x/length, sum_y/length])

# settings ====================================================================
color_by_field = 0                  # 1: colors spots by field number, 0: color spots by wavelength
p_every = 10                        # plot every "p_every"th spot only
# =============================================================================


# execute "spo file C:\Work\OpTaliX\Test\spot.txt" in OpTaliX
# execute "psf file C:\Work\OpTaliX\Test\diff_psf.txt" in OpTaliX
# execute "psf file C:\Work\OpTaliX\Test\diff_psf.txt" in OpTaliX
filename = r'C:\Work\OpTaliX\Test\spot.txt'

filename_diff_psf = r'C:\Work\OpTaliX\Test\diff_psf.txt'
filename_diff_psf_info = r'C:\Work\OpTaliX\Test\PSF_PATCH.txt'
filename_spots_info = r'C:\Work\OpTaliX\Test\spots_info.txt'
spotdata = np.loadtxt(filename)

diff_psfdata = np.loadtxt(filename_diff_psf,skiprows = 3 )[:,1:]
diff_psfdata_info = np.loadtxt(filename_diff_psf_info,skiprows = 1 )
wavl = diff_psfdata_info[0]
NA = diff_psfdata_info[1]
N_diff = diff_psfdata_info[2]
d = diff_psfdata_info[3]*N_diff
x = np.linspace(-d/2, d/2, num = int(N_diff))
X, Y = np.meshgrid(x,x)

r0 = 0.61*wavl*1e-3/(1*np.sin(NA))

if 0:
    plt.close("all")
    fig_diff = plt.figure("diffraction psf")
    #ax = plt.subplot(111)
    ax = fig_diff.add_subplot(111, projection='3d')
    #ax.plot(x, diff_psfdata[0,:])
    if 1:
        ax.plot_wireframe(X, Y, diff_psfdata)
    else:
        Z = diff_psfdata
        norm = plt.Normalize(Z.min(), Z.max())
        colors = cm.viridis(norm(Z))
        rcount, ccount, _ = colors.shape
        surf = ax.plot_surface(X, Y, Z, rcount=rcount, ccount=ccount,
                               facecolors=colors, shade=False)
        surf.set_facecolor((0,0,0,0))
        plt.show()
#else:
    
#ax.imshow(diff_psfdata )
# plot Airy disc

if 1:
    spotdata_pos1 = spotdata[spotdata[:,0]==1]    # select first position (config)
    
    # read extra information spot info
    diff_psfdata = np.loadtxt(filename_diff_psf,skiprows = 3 )[:,1:]
    diff_psfdata_info = np.loadtxt(filename_diff_psf_info,skiprows = 1 )
    
    spots_info = np.loadtxt(filename_spots_info,skiprows = 1, max_rows=1 )
    
    
    n_fields = int(spots_info[1])
    n_wavl = int(spots_info[0])
    
    wavl = np.loadtxt(filename_spots_info,skiprows = 2, max_rows=n_wavl )
    flds = np.loadtxt(filename_spots_info,skiprows = 2+n_wavl, max_rows=n_fields )
    
    r0 = 0.61*wavl*1e-3/(1*np.sin(NA))
    
    n_colors = n_fields
    n_colors2 = n_wavl
    
    L_wavl = np.linspace(1, n_wavl, n_wavl).astype(np.int)-1
    
    spotdata_pos_L =[]
    centroid_L = []
    rms_spot_size_L = []
    for i in range(0, n_colors):    # select by field
        spot_data_w_L = []
        centroid_w_L = []
        rms_spot_size_w_L = []
        for w in range(0, n_wavl):
            sp = spotdata_pos1[spotdata_pos1[:,1]==i+1]
            spw = sp[sp[:,2]==w+1]
            spot_data_w_L.append(spw)
        spot_data_w_L = np.array(spot_data_w_L)
        #spotdata_pos_L.append(spotdata_pos1[spotdata_pos1[:,1]==i+1])
        spotdata_pos_L.append(spot_data_w_L)
        for w in range(0, n_wavl):
            centroid_w_L.append(centeroidnp(spotdata_pos_L[i][w][:,-2:]))
            rms_spot_size_w_L.append(np.sqrt(np.sum((np.linalg.norm(centroid_w_L[w] - spotdata_pos_L[i][w][:,-2:], axis=1))**2)/len(spotdata_pos_L[i][w][:,-2:])))
        centroid_L.append(np.array(centroid_w_L))
        rms_spot_size_L.append(np.array(rms_spot_size_w_L))
        
    spotdata_pos1_f1 = spotdata_pos1[spotdata_pos1[:,1]==1]
    spotdata_pos1_f2 = spotdata_pos1[spotdata_pos1[:,1]==2]
    
    Lim = np.round(np.abs(np.min(spotdata))*2, decimals = 2)     # in [mm]
    Limit = (-Lim,Lim)
    dtick = Lim / 2
    marker=dict(
                color='LightSkyBlue',
                size=6,
                line=dict(
                    color='Black',
                    width=0.5
                ))
    
    if not color_by_field:
        marker=dict(
                    color='LightSkyBlue',
                    size=1,
                    line=dict(
                        color='Black',
                        width=0.0
                    ))
              
    Titles = ['Field 1','Field 2','Field 3', 'Field 4', 'Field 5', 'Field 6', 'Field 7', 'Field 8', 'Field 9']
    Titles2 = wavl.astype(str)
    for i in range(0,len(flds)):
        Titles[i] += "  ("+str(flds[i][0])+" , "+str(flds[i][1])+ ") °"
    
    # with some colormap "turbo"
    colors = px.colors.sample_colorscale("turbo", [n/(n_colors -1) for n in range(n_colors)])
    #colors2 = px.colors.sample_colorscale("turbo", [n/(n_colors2 -1) for n in range(n_colors2)])
    
    def to_rgb(name):
        from matplotlib import colors
        import matplotlib.cm
        C = colors.to_rgba(name)
        c = 'rgb'+str((C[0], C[1], C[2]))
        return c
    # with OpTaliX Field colors:
    colors = (to_rgb('red'),to_rgb('green'),to_rgb('blue'), to_rgb('magenta'), to_rgb('cyan'),to_rgb('yellow'), to_rgb('orange'), to_rgb('mediumpurple'), to_rgb('lightseagreen'))
    colors2 = (to_rgb('red'),to_rgb('green'),to_rgb('blue'), to_rgb('magenta'), to_rgb('cyan'))
    
    fig = make_subplots(rows=3,cols=3, vertical_spacing=0.1,
                      horizontal_spacing=0.1,shared_xaxes='all',
                      shared_yaxes='all', subplot_titles=Titles,
                      x_title='x / mm',
                      y_title='y / mm')
    #fig.add_scatter(x=spotdata_pos1_f1[:,-2], y=spotdata_pos1_f1[:,-1], mode='markers', row = 1, col=1, marker = marker)
    #fig.add_scatter(x=spotdata_pos1_f2[:,-2], y=spotdata_pos1_f2[:,-1], mode='markers', row = 1, col=2, marker = marker)
    row_L = np.array([1,1,1,2,2,2,3,3,3])
    col_L = np.array([1,2,3,1,2,3,1,2,3])
    for ww in range(0, len(L_wavl)):
        w = L_wavl[ww]
        for i in range(0, n_fields):
            if color_by_field:
                Co = colors[i]
            else:
                Co = colors2[w]
            if color_by_field:
                if ww == 0:
                    fig.add_scatter(x=spotdata_pos_L[i][w][::p_every,-2], y=spotdata_pos_L[i][w][::p_every,-1], mode='markers', row = row_L[i], col=col_L[i], marker = marker, marker_color = Co,
                                    name=Titles[i])
                else:
                    fig.add_scatter(x=spotdata_pos_L[i][w][::p_every,-2], y=spotdata_pos_L[i][w][::p_every,-1], mode='markers', row = row_L[i], col=col_L[i], marker = marker, marker_color = Co,
                                    name=Titles[i], showlegend = False)
            else:
                if i == 0:
                    fig.add_scatter(x=spotdata_pos_L[i][w][::p_every,-2], y=spotdata_pos_L[i][w][::p_every,-1], mode='markers', row = row_L[i], col=col_L[i], marker = marker, marker_color = Co,
                                    name=Titles2[ww])

                else:
                    fig.add_scatter(x=spotdata_pos_L[i][w][::p_every,-2], y=spotdata_pos_L[i][w][::p_every,-1], mode='markers', row = row_L[i], col=col_L[i], marker = marker, marker_color = Co, showlegend = False)
            
            if ww == 0:
                fig.add_annotation(x=0, y=Limit[1]*0.75,
                            text="centroid: "+str(np.round(centroid_L[i][0],decimals=3))+ ", "+str(np.round(centroid_L[i][0],decimals=3)),
                            showarrow=False,
                            arrowhead=0,
                            row = row_L[i],
                            col=col_L[i])
                
                fig.add_annotation(x=0, y=Limit[1]/4,
                            text="RMS ss: "+str(np.round(rms_spot_size_L[i],decimals=3))+"",
                            showarrow=True,
                            arrowhead=1,
                            row = row_L[i],
                            col=col_L[i],
                            font=dict(color="black"))
            
                fig.add_annotation(x=0, y=-Limit[1]*0.75,
                            text="Airy d: "+str(np.round(r0*2,decimals=3))+"",
                            showarrow=False,
                            arrowhead=1,
                            row = row_L[i],
                            col=col_L[i],
                            font=dict(color="black"))
            
            # fig.add_shape(type="circle",
            # xref="x", yref="y",
            # x0=centroid_L[i][w][0]-rms_spot_size_L[i], y0=centroid_L[i][w][1]-rms_spot_size_L[i] , x1=centroid_L[i][w][0]+rms_spot_size_L[i], y1=centroid_L[i][w][1]+rms_spot_size_L[i],
            # line_color='black', row = row_L[i], col=col_L[i]
            # )
            
            if 1:
                if color_by_field:
                    Co2 = "white"
                else:
                    Co2 = Co
                fig.add_shape(type="circle",
                xref="x", yref="y",
                x0=centroid_L[i][ww][0]-r0[ww], y0=centroid_L[i][ww][1]-r0[ww] , x1=centroid_L[i][ww][0]+r0[ww], y1=centroid_L[i][ww][1]+r0[ww],
                line_color=Co2, row = row_L[i], col=col_L[i]
                )
                
                fig.update_layout(title_font_color=colors[i])
        
    
    fig.update_xaxes(range=[Limit[0], Limit[1]], dtick=dtick)
    fig.update_yaxes(range=[Limit[0], Limit[1]], dtick=dtick)
    fig.update_yaxes(
        scaleanchor = "x",
        scaleratio = 1,
      )
    fig.update_layout(height=900, width=900)#, template='plotly_white')
    
    
    fig.show(renderer="browser")
    fig.write_html(os.path.join(os.path.dirname(filename), "spots.html"))
    
    
    print("Elapsed time: ", np.round(time.perf_counter()-t0, decimals = 4), " s")