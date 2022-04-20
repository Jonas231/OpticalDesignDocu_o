# sphinx_gallery_thumbnail_number = 2
import pyvista as pv
from pyvista import examples
import numpy as np

#From NumPy Meshgrid

#Create a simple meshgrid using NumPy

# Make data
d = 50
x = np.arange(-d, d, 0.25)
y = np.arange(-d, d, 0.25)
x, y = np.meshgrid(x, y)
r = np.sqrt(x ** 2 + y ** 2)
z = np.sin(r)

from VisualOpticsPy import draw3D
from pyrateoptics.raytracer.optical_element import OpticalElement
from pyrateoptics.raytracer.optical_system import OpticalSystem
s = OpticalSystem.p()
from pyrateoptics.raytracer.surface_shape import Conic
import pyrateoptics.raytracer.surface_shape as Shapelib
from pyrateoptics.raytracer.localcoordinates import LocalCoordinates
L = s.addLocalCoordinateSystem(LocalCoordinates.p(name='t', decz=0, tiltx = 0, tilty=0, tiltz = 0, tiltThenDecenter = 0),refname = 'global')
radius = 20 # [mm]
Curv = 1/radius
Shape_ob = Shapelib.Conic.p(L, curv=Curv)
#z = Shape_ob.getSag(x, y)

from pyrateoptics.raytracer.surface import Surface
from pyrateoptics.raytracer.aperture import CircularAperture
from pyrateoptics.raytracer.aperture import RectangularAperture

Radius = 10
Radius_min = 3
aptype = 'circ'

width = 10
height = 10
aptype = 'rect'

if aptype == 'circ':
    Aperture = CircularAperture.p(L, maxradius=Radius, minradius = Radius_min)
if aptype == 'rect':
    Aperture = RectangularAperture.p(L, width=width*2, height = height*2)

S2 = Surface.p(L, shape = Shape_ob, aperture = Aperture)
#S = Surface.p(L, shape = Shape_ob)
#coord2 = S2.draw3d(L, plot = 0)
coord = S2.draw3d(L, plot = 0)
#coord[2][coord[2]== 0] = np.nan
#Now pass the NumPy meshgrid to PyVista

# Create and plot structured grid
#grid = pv.StructuredGrid(x, y, z)
grid = pv.StructuredGrid(coord[0], coord[1], coord[2])
grid = pv.PolyData(coord.T)
#grid.plot(render_points_as_spheres=True)
#grid2 = pv.StructuredGrid(coord2[0], coord2[1], coord2[2])
#grid2.plot()

#Create a dataset to plot
Max = coord[2].max()
def make_points(r1 = 1, r2 = 1, Max = 0, aptype = 'circ'):
    """Helper to make XYZ points"""
    z = np.ones(100) * Max  # np.linspace(-2, 2, 100)
    if aptype == 'circ':
        theta = np.linspace(- np.pi, np.pi, 100)
        r = r1
        x = r * np.sin(theta)
        y = r * np.cos(theta)
    if aptype == 'rect':
        #rx = np.linspace(- r1, r1, 100)
        #ry = np.linspace(- r2, r2, 100)
        z = np.max(z)
        Linex1 = pv.Line(pointa=(- r1, -r2, z), pointb=(r1, -r2, z), resolution=1)
        Linex2 = pv.Line(pointa=(- r1, r2, z), pointb=(r1, r2, z), resolution=1)
        Liney1 = pv.Line(pointa=(- r1, -r2, z), pointb=(-r1, r2, z), resolution=1)
        Liney2 = pv.Line(pointa=(r1, -r2, z), pointb=(r1, r2, z), resolution=1)
        lines = Linex1 + Linex2 + Liney1 +Liney2
        spline = pv.PolyData(lines)

    if aptype == 'circ':
        points = np.column_stack((x, y, z))
        spline = pv.Spline(points, 1000)
    return spline
if aptype == 'circ':
    spline = make_points(r1 = Radius, Max = Max, aptype = aptype)
    spline_m = make_points(r1 = Radius_min, Max = 0)
if aptype == 'rect':
    spline = make_points(r1 = width, r2 = height, Max = Max, aptype = aptype)
    spline_m = spline
#Poinst = points[0:5, :]

# Create spline with 1000 interpolation points


#Plot spline as a tube

# add scalars to spline and plot it
#spline["scalars"] = np.arange(spline.n_points)
#tube = spline.tube(radius= 0.1)
#tube.plot(smooth_shading=True)
# plot without scalars
#spline.plot(line_width=4, color="r")

pl = pv.Plotter()
actor = pl.add_mesh(spline, line_width=4, color="r")
actor_m = pl.add_mesh(spline_m, line_width=4, color="r")
grid = grid.delaunay_2d()       #
grid_mesh = pv.PolyData(grid)
actor2 = pl.add_mesh(grid_mesh, smooth_shading=True, show_edges = True,opacity=0.5)

# pl.add_background_image(examples.mapfile)
pl.show()

