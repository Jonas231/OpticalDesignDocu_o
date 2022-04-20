#!/usr/bin/env/python
"""
Pyrate - Optical raytracing based on Python

Copyright (C) 2014-2020
               by     Moritz Esslinger moritz.esslinger@web.de
               and    Johannes Hartung j.hartung@gmx.net
               and    Uwe Lippmann  uwe.lippmann@web.de
               and    Thomas Heinze t.heinze@uni-jena.de
               and    others

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""

import math
import numpy as np

from pyrateoptics.core.base import ClassWithOptimizableVariables

from pyrateoptics.raytracer.aperture import BaseAperture

# class BaseAperture(ClassWithOptimizableVariables):
#     # for optimizable aperture it would be good to
#     # derive from optimizable class, but I think
#     # apertures will be inserted after optimization
#
#     # comment 20200217: class has to be derived from
#     # ClassWithOptimizableVariables anyway, for following
#     # reasons:
#     # * localcoordinate system is still optimizable
#     # * it is saved by serializer
#     """
#     Base class representing the aperture of a surface.
#     Subclasses may define the actual shapes (circular,
#     elliptic, rectangular, etc.)
#
#     Decentering of apertures do not make any sense, since
#     the local coordinate system can be redefined if desired.
#
#     The base class does not limit the beam diameter.
#     """
#     @classmethod
#     def p(cls, lc, name="", *_):
#         return cls({"typicaldimension": 1e16}, {"lc": lc},
#                    name=name)
#
#     def setKind(self):
#         self.kind = "aperture"
#
#     def get_typical_dimension(self):
#         """
#         Returns typical dimension of aperture
#
#         :return self.typicaldimension: float
#         """
#
#         return self.annotations["typicaldimension"]
#
#     def are_points_in_aperture(self, x_intersection, y_intersection):
#         """
#
#         Returns of points given by numpy arrays x, y are within aperture
#
#         :param x_intersection: x in local coordinates (1xn npy array of floats)
#         :param y_intersection: y in local coordinates (1xn npy array of floats)
#
#         :return True (1d numpy array of n bools)
#         """
#
#         bool_func = self.get_boolean_function()
#         return bool_func(x_intersection, y_intersection)  # return true always
#
#     def get_boolean_function(self):
#         """
#
#         Returns boolean function of aperture
#
#         :return anonymous function for 2 arguments x, y
#
#         """
#
#         return (lambda x, y: np.ones_like(x, dtype=bool))
#
#

### add here some new sub classes (J, Herbst, VisualOpticsPy)
class EllipticAperture(BaseAperture):
    """
    Elliptic aperture of a surface.
    # see: CLAP ELIP , cay , cax , Yd , Xd
    # in KDP-2: manual, p. 100
    cay ... y-semi-height, cax ... x-semi-dimension, Yd, Xd (centered)
    """

    def setKind(self):
        self.kind = "aperture_Elliptic"

    @classmethod
    def p(cls, lc, cay=1.0, cax=0.0, Yd = 0.0, Xd = 0.0, name="", *_):
        return cls({"cay": cay,
                    "cax": cax,
                    "Yd": Yd,
                    "Xd": Xd,
                    "typicaldimension": max(cay,cax)},
                   {"lc": lc}, name=name)

    def get_boolean_function(self):
        return (lambda x, y:
                ((((x-self.annotations["Xd"])**2)/((1e-10)**2) + ((y-self.annotations["Yd"])**2)/((1e-10)**2)) >= 1) *
                (((x-self.annotations["Xd"])**2)/(self.annotations["cax"]**2) + ((y-self.annotations["Yd"])**2)/(self.annotations["cay"]**2)) <= 1)


# Needed for convenience functions in pyrateoptics

ACCESSIBLE_APERTURES = {None: BaseAperture,
                        "EllipticAperture": EllipticAperture}


def create_aperture(localcoordinates, ap_dict):
    """
    Creates aperture object from dictionary
    """
    ap_type = ap_dict.pop("type", None)
    return ACCESSIBLE_APERTURES[ap_type].p(localcoordinates, **ap_dict)
