import numpy as np
def built_spd_mac(file, a, b):
    macroname = 'buildSPD'
    file = open(file, "w")
    def write_line(file, L):
        file.writelines(L)
        file.write("\n")


    #write_line(file, L=['MACRO ' + str(macroname)])
    # FOB ... object point specification, manual p. 159
    # This command defines the object point from which subsequent rays will be traced
    # FOB (qualifier word) , Y, X, Z, n, m

    if isinstance(a, list) and isinstance(b, list):
        #filename = "multi_fob_"+str(a[0])+"_to_"+str(a[-1])+"__"+str(b[0])+"_to_"+str(b[-1])
        for i in range(0, len(a)):
            filename = str(a[i]) + '_' + str(b[i])
            # for one object point specification (field)
            write_line(file, L=['FOB, ' + str(a[i]) + ' ' + str(b[i])])
            write_line(file, L=['SPD'])
            # create an ascii file with the current spd
            write_line(file, L=['AWRTSPOT spd_' + filename])
    else:
        filename = str(a)+'_'+str(b)
        # for one object point specification (field)
        write_line(file, L=['FOB, ' + str(a) + ' '+ str(b)])
        write_line(file, L=['SPD'])
        # create an ascii file with the current spd
        write_line(file, L=['AWRTSPOT spd_'+filename])

    #write_line(file, L=['EOM'])
    file.close()

path_KDP_mac_spd = r'C:\Work\Tools\KDP\create_spd.DAT'
path_KDP_mac_spd_multi = r'C:\Work\Tools\KDP\create_spd_multi.DAT'
built_spd_mac(path_KDP_mac_spd, a = 0.1, b = 0.1)

a = np.linspace(0, 0.1, num = 11)
b = np.linspace(0, 0.1, num = 11)
A,B = np.meshgrid(a,b)
built_spd_mac(path_KDP_mac_spd_multi, a = A.flatten().tolist(), b = B.flatten().tolist())