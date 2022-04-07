import numpy as np

filename = r"C:\D\optical design software demos (other than Zemax)\free software\KDP-2\RAYHIST.dat"
def load_multitrace(filename):
    """
    Reads the ray history file produced with the KDP commands
    ("mrays", "rhist on", "mtrace", "rhist swrite/write")
    # see function multi_raytrace_mac in create_rays.py
    :param filename:
    :return:
    """
    # ray_info contains: number of rays, surfaces, fields
    ray_info = np.loadtxt(filename, skiprows=0, max_rows = 1)
    ray_info = ray_info.astype(np.float)
    ray_info = np.array(ray_info)
    n_rays = ray_info[0]
    n_sur = ray_info[1]
    n_flds = ray_info[2]
    # read surface, sequential ray, rayhist data items
    # columns: surface, ray, items (see p. 218,219)
    rayhist = np.loadtxt(filename, skiprows=1, dtype='str')
    rayhist = np.char.replace(rayhist, 'D', 'E').astype(np.float)
    if rayhist.shape[1] == 15:
        print("short ray history file (swrite)")
        L_legend = [
        "Surface  #",
        "Sequential Ray  #",
        "Local X - coordinate",
        "Local Y - coordinate",
        "Local Z - coordinate",
        "Angle of Incidence",
        "Ray Energy Term",
        "X - component of the Angle of Incidence",
        "Y - component of the Angle of Incidence",
        "X - coordinate of cheif ray at object surface",
        "Y - coordinate of cheif ray at object surface",
        "XZ - slope angle, in radians, of the chief ray at the object surface",
        "YZ - slope",
        "Sequential number of the chief ray(from 1 to the maximum number of chief rays)",
        "RAYCOD(1)(Ray failure code, 0 = no fail)",
        "RAYCOD(2)(Surface where ray stopped)"]
        L_legend = np.array(L_legend)
    else:
        L_legend = np.array([])
    return ray_info, rayhist, L_legend


ray_info, rayhist, L_legend = load_multitrace(filename)