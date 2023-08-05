"""
Library of SPAM functions for generating partial volume balls, see Tengattini et al. 2015
Copyright (C) 2020 SPAM Contributors

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the Free
Software Foundation, either version 3 of the License, or (at your option)
any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
more details.

You should have received a copy of the GNU General Public License along with
this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from __future__ import print_function
import numpy

from . import kalispheraToolkit

real_t = '<f8'
# also need to select double or float in kalisphera C call


def makeSphere(vol, centre, radius):
    """
    This function creates a sphere in a given 3D volume,
    with analytically-calculated partial-volume effects.
    Background is assumed to have a greyvalue of zero,
    and a fully-occupied sphere voxel is considered to
    have a greyvalue of 1.

    Greyvalues are added to the volume, so spheres can be
    added to an existing background.

    Parameters
    ----------
        vol : 3D numpy array of doubles
            A 3D image of greylevels (typically zeros) into which sphere(s) should be added

        centre : 1D or 2D numpy array
            Either a 3-component vector, or an Nx3 matrix of sphere centres to draw with respect to 0,0,0 in `vol`

        radius : float or 1D numpy array
            Raduis(ii) of spheres to draw in `vol`


    Returns
    -------
        None : function updates vol
    """

    if len(vol.shape) != 3:
        print("\tkalisphera.makeSphere(), need 3D vol array")
        return -1

    centre = numpy.array(centre, dtype=real_t)

    # Turn centre into a numpy array in case it is passed as a list-of-lists
    if len(centre.shape) == 1:
        centre = numpy.array([centre])

    if len(centre.shape) == 2:
        if type(radius) == float or type(radius) == int:
            # print("\tkalisphera.makeSphere.run(), Got single radius for multiple spheres... fine")
            radius = [radius] * centre.shape[0]

        if len(radius) == centre.shape[0]:
            for centre, radius in zip(centre, radius):
                volTemp = numpy.zeros_like(vol, dtype=real_t)
                # For compatibility with scipy centre of mass
                # centre+=0.5
                # print centre, radius
                # print vol.sum()
                kalispheraToolkit.kalisphera(volTemp, numpy.array(centre).astype(real_t), float(radius))
                # print vol.sum()
                vol += volTemp  # .copy()
            return 0

        else:
            print("\tkalisphera.makeSphere(), Got multiple radii, but different number from number of centres")
            return -1
