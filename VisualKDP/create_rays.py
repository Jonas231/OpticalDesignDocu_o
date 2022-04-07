import numpy as np

# doing a multi-raytrace and create ray history file
def multi_raytrace_mac(file, caobf = 0, fobx = 1, foby = 1, nfovs = 1, caobx = 1, caoby = 1, nrays = 2, swrite = 1):
    # created file.dat can be called within KDP-2
    # with command "input file file.dat"
    file = open(file, "w")

    def write_line(file, L):
        file.writelines(L)
        file.write("\n")

    # see manual, p. 217
    write_line(file, L=['mfobs, '+str(foby)+', '+str(fobx)+', ,'+str(nfovs)])
    if caobf:
        caob = 'caob'
    else:
        caob = ''
    write_line(file, L=['mrays ' + str(caob) + ', '+str(caoby)+', '+str(caobx)+', , ,' + str(nrays)])
    write_line(file, L=['rhist on'])
    write_line(file, L=['mtrace'])
    if swrite:
        w = 'swrite'
    else:
        w = 'write'
    write_line(file, L=['rhist '+str(w)])
    write_line(file, L=['rhist off'])

path_KDP_mac_multi_raytrace = r'C:\Work\Tools\KDP\create_rayhist.DAT'
multi_raytrace_mac(path_KDP_mac_multi_raytrace)
path_KDP_mac = r'C:\D\optical design software demos (other than Zemax)\free software\KDP-2\LIBMAC\MAC005.DAT'
path_KDP_mac = r'C:\D\optical design software demos (other than Zemax)\free software\KDP-2\create_rayhist.DAT'
multi_raytrace_mac(path_KDP_mac,fobx = 0, foby = 0)

# layout rays (like in KDP-2):
def layout_rays_mac(file, tracetype = 'gparaxial', n = 1, x_fob = 1, y_fob = 1, caobflag = 1):
    # created file.dat can be called within KDP-2
    # with command "input file file.dat"
    file = open(file, "w")

    def write_line(file, L):
        file.writelines(L)
        file.write("\n")

    filename = 'lrays.dat'
    write_line(file, L=['replace'])
    write_line(file, L=['output ed'])
    #write_line(file, L=['gpxtx ' + str(0) + ', ' + str(y_fob) + ', ' + str(x_fob)])
    #write_line(file, L=['output file ' + str(filename)])
    #write_line(file, L=['output tp'])
    if tracetype == 'paraxial':
        print("paraxial")
    if tracetype == 'gparaxial':
        # write to file:
        # 1. marginal ray heights
        # 2. marginal ray slopes
        # 3. chief ray heights
        # 4. chief ray slopes
        # in yz and xz plane ("gpxty", "ppxtx")
        print("generalized paraxial")
        for i in range(0, n):
            write_line(file, L=['gpxtx ' + str(i)+', '+str(y_fob)+', '+str(x_fob)])
            write_line(file, L=['gpxty ' + str(i)+', '+str(y_fob)+', '+str(x_fob)])
    write_line(file, L=['output tp']) # ensures that file is overwritten!

    write_line(file, L=['output pu'])

    write_line(file, L=['fob 0, 0'])
    N = 3
    Y = np.linspace(-y_fob,y_fob, num = N-1)
    X = np.linspace(-x_fob,x_fob, num = N-1)
    c = 0
    raystring = 'ray, '
    if caobflag:
        raystring = 'ray caob, '
    for y in Y:
        for x in X:
            print(c, y,x)
            if c > 0:
                write_line(file, L=['headings off'])
            write_line(file, L=[raystring+str(y)+', '+str(x)])
            write_line(file, L=['prxyz all'])
            c+=1
    #write_line(file, L=['ray -1, 0'])
    #write_line(file, L=['prxyz all'])
    #write_line(file, L=['ray 0, 1'])
    #write_line(file, L=['prxyz all'])
    #write_line(file, L=['ray 0, -1'])
    #write_line(file, L=['prxyz all'])

    #write_line(file, L=['prlmn all'])
    write_line(file, L=['output tp'])
    #write_line(file, L=['fob?'])
    file.close()

path_KDP_mac = r'C:\D\optical design software demos (other than Zemax)\free software\KDP-2\create_rays.DAT'
layout_rays_mac(path_KDP_mac, tracetype = 'gparaxial', n = 6, x_fob = 0.99, y_fob = 0)


