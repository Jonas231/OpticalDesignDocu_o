# Author: Jonas Herbst

import numpy as np
import pyvista as pv
from pyvistaqt import BackgroundPlotter

#from pyrateoptics import raytracer
from pyrateoptics.raytracer.localcoordinates import LocalCoordinates
from pyrateoptics.raytracer.aperture import BaseAperture, create_aperture
from pyrateoptics.raytracer.globalconstants import standard_wavelength, canonical_ex, canonical_ey

# add method to class "RayBundle"
from pyrateoptics.raytracer.ray import RayBundle
def draw3d(self, plotter, color="blue", plane_normal=canonical_ex,
           up=canonical_ey, **kwargs):
    # normalizing plane_normal, up direction
    plane_normal = plane_normal / np.linalg.norm(plane_normal)
    up = up / np.linalg.norm(up)

    ez = np.cross(plane_normal, up)

    (num_points, num_dims, num_rays) = np.shape(self.x)

    if num_rays == 0:
        return

    # arrange num_ray copies of simple vectors in appropriate form
    plane_normal = np.repeat(plane_normal[:, np.newaxis], num_rays, axis=1)
    ez = np.repeat(ez[:, np.newaxis], num_rays, axis=1)
    up = np.repeat(up[:, np.newaxis], num_rays, axis=1)

    ptlist = [self.x[i] for i in np.arange(num_points)]
    validity = [self.valid[i] for i in np.arange(num_points)]

    #just for debugging
    #print("len(ptlist)", len(ptlist))
    #print("ptlist", ptlist[0].shape, ptlist[1].shape)
    #print("ptlist", ptlist[0][:,0], ptlist[1][:,0])
    #print("a", ptlist[1:][0].shape, ptlist[:-1][0].shape)
    #print("ptlist", ptlist[1:], ptlist[:-1])
    
    Line_LL = []
    for (pt1, pt2, todraw) in zip(ptlist[1:], ptlist[:-1], validity[1:]):
        # perform in-plane projection
        pt1inplane = pt1 - np.sum(pt1 * plane_normal, axis=0) * plane_normal
        pt2inplane = pt2 - np.sum(pt2 * plane_normal, axis=0) * plane_normal

        # calculate y-components
        ypt1 = np.sum(pt1inplane * up, axis=0)
        ypt2 = np.sum(pt2inplane * up, axis=0)

        # calculate z-components
        zpt1 = np.sum(pt1inplane * ez, axis=0)
        zpt2 = np.sum(pt2inplane * ez, axis=0)

        y = np.vstack((ypt1, ypt2))[:, todraw]
        z = np.vstack((zpt1, zpt2))[:, todraw]
        #ax.plot(z, y, color=color, **kwargs)
        #print("pt-shape", pt1.shape, pt2.shape)
        #print("pt", pt1[:,0], pt2[:,0])
        Line_L = []
        for i in range(0, len(pt1[0])):

            line = pv.Line(pointa=np.array(pt1[:,i].real),pointb=np.array(pt2[:,i].real))
            Line_L.append(line)
            if i == 0:
                Mesh = Line_L[0]
            Mesh += Line_L[i]
        Line_L = np.array(Line_L)
        
        # for i in range(0, len(pt1[0])):
        #     plotter.add_mesh(Line_L[i], color=color, opacity = 0.75)
        plotter.add_mesh(Mesh, color=color, opacity = 0.75)

RayBundle.draw3d = draw3d

from pyrateoptics.raytracer.ray import RayPath
def draw3d(self, plotter, color="blue",
           plane_normal=canonical_ex, up=canonical_ey,
           do_not_draw_raybundles=[], **kwargs):
    """
    Draw raybundles.
    """
    # TODO: exclude different raybundles from drawing

    """
    print(self.raybundles)
    xdraw_list = []
    kdraw_list = []
    edraw_list = []
    valid_list = []
    for (ind, r) in enumerate(self.raybundles):
        if ind not in do_not_draw_raybundles:
            (numpts, numdims, numrays) = r.x.shape
            xdraw_list += [r.x[i] for i in np.arange(numpts)]
            kdraw_list += [r.k[i] for i in np.arange(numpts)]
            edraw_list += [r.Efield[i] for i in np.arange(numpts)]
            valid_list += [r.valid[i] for i in np.arange(numpts)]
            # r.draw2d(ax, color=color,
            #          plane_normal=plane_normal, up=up, **kwargs)
    # ugly construction to perform a nice drawing of the raybundle
    r_draw = RayBundle(x0=xdraw_list[0],
                       k0=kdraw_list[0],
                       Efield0=edraw_list[0])
    r_draw.x = np.array(xdraw_list)
    r_draw.k = np.array(kdraw_list)
    r_draw.Efield = np.array(edraw_list)
    r_draw.valid = np.array(valid_list)
    r_draw.draw2d(ax, color=color,
                  plane_normal=plane_normal, up=up, **kwargs)
    """
    for r in self.raybundles:
        r.draw3d(plotter, color=color, plane_normal=plane_normal,
                 up=up, **kwargs)

RayPath.draw3d = draw3d


# add a method draw3D to the class Surface
from pyrateoptics.raytracer.surface import Surface
def draw3d(self, plotter, vertices=50,
           inyzplane=True,
           color="white",
           style="points", style_swapped_lines=False, c = np.array([0,0,255]), **kwargs):
    """
    :param plotter (plotter object)
    :param vertices (int), vertices in xy for aperture sampling
    :param inyzplane (bool), cuts globalpts in yz plane before projection
    on plane_normal
    :param color (string), "red", "blue", "grey", "green", ...
    :param plane_normal (1D numpy array of float), new x projection axis
    :param up (1D numpy array), invariant y axis, z = x x y
    :param style (string), "points", "meander"
    """

    sizelimit = 1000.0
    failsafevalue = 11.0

    if self.aperture is None:
        effsemidia = failsafevalue
        # TODO: choose max ray height of all bundles instead
        # (cosmetic but absolutely necessary for beauty)
    else:
        if self.aperture.get_typical_dimension() <= sizelimit:
            # TODO: aperture types Object and Image to distuingish
            # from very large normal apertures
            effsemidia = self.aperture.get_typical_dimension()
        else:
            effsemidia = failsafevalue

    xl = effsemidia * np.linspace(-1, 1, num=vertices)
    yl = effsemidia * np.linspace(-1, 1, num=vertices)

    X, Y = np.meshgrid(xl, yl)
    if style_swapped_lines:
        X[::2, :] = X[::2, ::-1]
    x = X.flatten()
    y = Y.flatten()

    isinap = self.aperture.are_points_in_aperture(x, y)
    xinap = x[isinap]
    yinap = y[isinap]
    zinap = np.zeros_like(xinap)

    localpts_aperture = np.row_stack((xinap, yinap, zinap))
    localpts_shape =\
        self.shape.lc.returnOtherToActualPoints(localpts_aperture,
                                                self.aperture.lc)

    xinap_shape = localpts_shape[0, :]
    yinap_shape = localpts_shape[1, :]
    zinap_shape = self.shape.getSag(xinap_shape, yinap_shape)

    localpts_shape = np.row_stack((xinap_shape, yinap_shape, zinap_shape))
    localpts_surf =\
        self.rootcoordinatesystem.returnOtherToActualPoints(localpts_shape,
                                                            self.shape.lc)

    # plane projection: here!

    globalpts =\
        self.rootcoordinatesystem.returnLocalToGlobalPoints(localpts_surf)
    print("shape: ", globalpts.shape)
    globalpts2 = globalpts.T
    print(globalpts[:,0:10])
    if globalpts.shape == (3,int(vertices*vertices)):
        globalpts = globalpts.reshape(3,vertices,vertices)
        
    #globalpts = globalpts.T
    #globalpts_mesh = globalpts.reshape(vertices*vertices,3)
    #print(globalpts_mesh.shape)
    # draw in pyvista
    #mesh = pv.PolyData(globalpts[0], globalpts[1], globalpts[2])  # x,y,z

    # see: https://docs.pyvista.org/examples/00-load/create-structured-surface.html
    #globalpts = np.c_[globalpts[0].reshape(-1), globalpts[1].reshape(-1), globalpts[2].reshape(-1)]
    mesh_2 = pv.PolyData(globalpts2)  # x,y,z
    surf = mesh_2.delaunay_2d()
    #print(globalpts.shape)
    #c = np.random.random(3)
    #mesh = pv.StructuredGrid(globalpts[0], globalpts[1], globalpts[2])
    #plotter.add_mesh(mesh, opacity=0.85, color=tuple(c))
    #plotter.add_mesh(mesh_2, opacity=0.85, color=tuple(np.random.random(3)))
    plotter.add_mesh(surf, opacity=0.15, color=tuple(c))

Surface.draw3d = draw3d

# add a method draw3D to the class "OpticalElement"
from pyrateoptics.raytracer.optical_element import OpticalElement
def draw3d(self, plotter, color="grey", vertices=50, inyzplane=True,
           do_not_draw_surfaces=[], **kwargs):
    for surfs in self.surfaces.values():
        if surfs.name not in do_not_draw_surfaces:
            surfs.draw3d(plotter, color=color, vertices=vertices,
                         inyzplane=inyzplane, **kwargs)
OpticalElement.draw3d = draw3d

# add a method draw3D to the class "OpticalSystem"
from pyrateoptics.raytracer.optical_system import OpticalSystem
def draw3d(self, plotter, vertices=50, color="grey", inyzplane=True,
           do_not_draw_surfaces=[], **kwargs):
    for e in self.elements.values():
        e.draw3d(plotter, vertices=vertices,
                 color=color,
                 inyzplane=inyzplane,
                 do_not_draw_surfaces=do_not_draw_surfaces,
                 **kwargs)
OpticalSystem.draw3d = draw3d


def draw_rays_3D(plotter, rays, do_not_draw_raybundles=[], **kwargs):
    if rays is not None:
        if isinstance(rays, list):
            for rpl in rays:
                ray_color = tuple(np.random.random(3))
                if isinstance(rpl, list):
                    for rp in rpl:
                        ray_color = tuple(np.random.random(3))
                        rp.draw3d(plotter, color=ray_color,
                                  do_not_draw_raybundles=do_not_draw_raybundles,
                                  **kwargs)
                elif isinstance(rpl, tuple):
                    (rl, ray_color) = rpl
                    if isinstance(rl, list):
                        # draw(s, [([rp1, ..], color1), (....)])
                        for r in rl:
                            r.draw3d(plotter, color=ray_color, **kwargs)
                    else:
                        # draw(s, [(rp1, color1), (....)])
                        rl.draw3d(plotter, color=ray_color, **kwargs)
                else:
                    rpl.draw3d(plotter, color=ray_color,
                               do_not_draw_raybundles=do_not_draw_raybundles,
                               **kwargs)
        elif isinstance(rays, RayPath):
            # draw(s, raypath)
            ray_color = tuple(np.random.random(3))
            rays.draw3d(plotter, color=ray_color,
                        do_not_draw_raybundles=do_not_draw_raybundles,
                        **kwargs)
        elif isinstance(rays, RayBundle):
            # draw(s, raybundle)
            ray_color = tuple(np.random.random(3))
            rays.draw3d(plotter, color=ray_color, **kwargs)
        elif isinstance(rays, tuple):
            (rl, ray_color) = rays
            if isinstance(rl, list):
                # draw(s, ([raypath1, ...], color))
                for r in rl:
                    r.draw3d(plotter, color=ray_color, **kwargs)
            else:
                # draw(s, (raypath, color))
                rl.draw3d(plotter, color=ray_color,
                          do_not_draw_raybundles=do_not_draw_raybundles,
                          **kwargs)

def draw3D_pyvista(os, rays=None,
         hold_on=False,
         do_not_draw_surfaces=[],
         do_not_draw_raybundles=[],
         interactive=False,
         show_box=True,
         linewidth=1.0,
         export_type="pdf",
         export=None, **kwargs):
    pv.set_plot_theme("document")
    plotter = BackgroundPlotter()
    plotter.set_background("gray", top="white")

    # draw surfaces of optical systems
    os.draw3d(plotter, color="grey", linewidth=linewidth,
              do_not_draw_surfaces=do_not_draw_surfaces, **kwargs)
    # draw rays
    draw_rays_3D(plotter, rays, linewidth=linewidth,
              do_not_draw_raybundles=do_not_draw_raybundles, **kwargs)

    #plotter.add_axes_at_origin(x_color=None, y_color=None, z_color=None, xlabel='X', ylabel='Y', zlabel='Z', line_width=2, labels_off=False)
    plotter.add_bounding_box(color='red', corner_factor=0.5, line_width=None, opacity=1.0, render_lines_as_tubes=False, lighting=None, reset_camera=None, outline=True, culling='front')
    #plotter.add_bounds_axes()
    plotter.show_bounds(font_size = 20, color='red')
    plotter.show_axes()
    plotter.add_axes()
    plotter.show()

