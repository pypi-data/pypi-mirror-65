"""
Library of SPAM functions for deforming images.
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
import scipy.ndimage
#numpy.set_printoptions(precision=3, suppress=True)

###########################################################
# Take an Phi and apply it (C++) to an image
###########################################################
def applyPhi(im, Phi=None, PhiPoint=None, interpolationOrder=1):
    """
    Deform a 3D image using a deformation function "Phi", applied using spam's C++ interpolator.
    Only interpolation order = 1 is implemented.

    Parameters
    ----------
        im : 3D numpy array
            3D numpy array of grey levels to be deformed

        Phi : 4x4 array, optional
            "Phi" deformation function.
            Highly recommended additional argument (why are you calling this function otherwise?)

        PhiPoint : 3x1 array of floats, optional
            Centre of application of Phi.
            Default = (numpy.array(im1.shape)-1)/2.0
            i.e., the centre of the image

        interpolationOrder : int, optional
            Order of image interpolation to use. This value is passed directly to ``scipy.ndimage.map_coordinates`` as "order".
            Default = 1

    Returns
    -------
        imDef : 3D array
            Deformed greyscales by Phi
    """
    # import sys
    # import os
    from . import DICToolkit

    # Detect 2D images, and bail, doesn't work with our interpolator
    if len(im.shape) == 2 or (numpy.array(im.shape) == 1).any():
        print("DIC.deformationFunction.applyPhi(): looks like a 2D image which cannot be handled. Please use DIC.deformationFunction.applyPhiPython")
        return

    # Sort out Phi and calculate inverse
    if Phi is None:
        PhiInv = numpy.eye(4, dtype='<f4')
    else:
        try:
            PhiInv = numpy.linalg.inv(Phi).astype('<f4')
        except numpy.linalg.linalg.LinAlgError:
            # print( "\tapplyPhi(): Can't inverse Phi, setting it to identity matrix. Phi is:\n{}".format( Phi ) )
            PhiInv = numpy.eye(4, dtype='<f4')

    if PhiPoint is None:
        PhiPoint = (numpy.array(im.shape) - 1) / 2.0

    if interpolationOrder > 1:
        print("DIC.deformationFunction.applyPhi(): interpolation Order > 1 not implemented")
        return

    im = im.astype('<f4')
    PhiPoint = numpy.array(PhiPoint).astype('<f4')
    # We need to inverse Phi for question of direction
    imDef = numpy.zeros_like(im, dtype='<f4')
    DICToolkit.applyPhi(im.astype('<f4'),
                        imDef,
                        PhiInv.astype('<f4'),
                        PhiPoint.astype('<f4'),
                        int(interpolationOrder))

    return imDef

###########################################################
# Take an Phi and apply it to an image
###########################################################
def applyPhiPython(im, Phi=None, PhiPoint=None, interpolationOrder=3):
    """
    Deform a 3D image using a deformation function "Phi", applied using scipy.ndimage.map_coordinates
    Can have orders > 1 but is hungry in memory.

    Parameters
    ----------
        im : 3D numpy array
            3D numpy array of grey levels to be deformed

        Phi : 4x4 array, optional
            "Phi" linear deformation function.
            Highly recommended additional argument (why are you calling this function otherwise?)

        PhiPoint : 3x1 array of floats, optional
            Centre of application of Phi.
            Default = (numpy.array(im1.shape)-1)/2.0
            i.e., the centre of the image

        interpolationOrder : int, optional
            Order of image interpolation to use. This value is passed directly to ``scipy.ndimage.map_coordinates`` as "order".
            Default = 3

    Returns
    -------
        imSub : 3D array
            Deformed greyscales by Phi
    """

    if Phi is None:
        PhiInv = numpy.eye(4, dtype='<f4')
    else:
        try:
            PhiInv = numpy.linalg.inv(Phi).astype('<f4')
        except numpy.linalg.linalg.LinAlgError:
            # print( "\tapplyPhiPython(): Can't inverse Phi, setting it to identity matrix. Phi is:\n{}".format( Phi ) )
            PhiInv = numpy.eye(4)

    if PhiPoint is None:
        PhiPoint = (numpy.array(im.shape) - 1) / 2.0

    imDef = numpy.zeros_like(im, dtype='<f4')

    coordinatesInitial = numpy.ones((4, im.shape[0] * im.shape[1] * im.shape[2]), dtype='<f4')

    coordinates_mgrid = numpy.mgrid[0:im.shape[0],
                                    0:im.shape[1],
                                    0:im.shape[2]]

    # Copy into coordinatesInitial
    coordinatesInitial[0, :] = coordinates_mgrid[0].ravel() - PhiPoint[0]
    coordinatesInitial[1, :] = coordinates_mgrid[1].ravel() - PhiPoint[1]
    coordinatesInitial[2, :] = coordinates_mgrid[2].ravel() - PhiPoint[2]

    # Apply Phi to coordinates
    coordinatesDef = numpy.dot(PhiInv, coordinatesInitial)

    coordinatesDef[0, :] += PhiPoint[0]
    coordinatesDef[1, :] += PhiPoint[1]
    coordinatesDef[2, :] += PhiPoint[2]

    imDef += scipy.ndimage.map_coordinates(im,
                                           coordinatesDef[0:3],
                                           order=interpolationOrder).reshape(imDef.shape).astype('<f4')
    return imDef

###############################################################
# Take a field of Phi and apply it (quite slowly) to an image
###############################################################
def applyPhiField(im, fieldName=None, fieldCoords=None, fieldValues=None, fieldBinRatio=1.0, neighbours=8, interpolationOrder=3, verbose=False):
    """
    Deform a 3D image using a field of deformation functions "Phi" coming from a regularGrid,
    applied using scipy.ndimage.map_coordinates.

    Parameters
    ----------
        im : 3D array
            3D array of grey levels to be deformed

        fieldName : string, optional
            Name of the file containing the deformation functions field

        fieldCoords: 2D array, optional
            nx3 array of n points coordinates (ZYX)
            centre where each deformation function "Phi" has been calculated

        fieldValues: 3D array, optional
            nx4x4 array of n points deformation functions

        fieldBinRatio : int, optional
            If the input field refers to a binned version of the image
            `e.g.`, if ``fieldBinRatio = 2`` the ``fieldName`` values have been calculated
            for an image half the size of the input image ``im``
            Default = 1

        neighbours : int, optional
            Neighbours for field interpolation
            If == 1, the nearest neighbour is used, if >1 neighbours are weighted according to distance.
            Default = 8

        interpolationOrder : int, optional
            Order of image interpolation to use. This value is passed directly to ``scipy.ndimage.map_coordinates`` as "order".
            Default = 1

    Returns
    -------
        imDef : 3D array
            deformed greylevels by a field of deformation functions "Phi"
    """
    import spam.deformation

    # Create the grid of the input image
    imSize = im.shape
    coordinates_mgrid = numpy.mgrid[0:imSize[0],
                                    0:imSize[1],
                                    0:imSize[2]]

    coordIn = numpy.ones((imSize[0] * imSize[1] * imSize[2], 4))

    coordIn[:, 0] = coordinates_mgrid[0].ravel()
    coordIn[:, 1] = coordinates_mgrid[1].ravel()
    coordIn[:, 2] = coordinates_mgrid[2].ravel()

    numberofPoints = imSize[0] * imSize[1] * imSize[2]

    # Copy initial coordinates to the deformed coordinates
    coordDef = coordIn.copy()

    # Read input PhiField, usually the result of a regularGrid correlation
    if fieldName:
        import spam.helpers.tsvio
        PhiFromFile = spam.helpers.tsvio.readCorrelationTSV(fieldName, fieldBinRatio=fieldBinRatio)
        fieldCoords = PhiFromFile["fieldCoords"]
        fieldValues = PhiFromFile["PhiField"]
    else:
        fieldCoords = fieldCoords
        fieldValues = fieldValues

    # Create the k-d tree of the coordinates of the input Phi field
    from scipy.spatial import KDTree
    tree = KDTree(fieldCoords)

    # Loop over each point of the grid of the input image
    for point in range(coordIn.shape[0]):
        if verbose:
            print("\rWorking on point {} {}%".format(point, (point / float(numberofPoints)) * 100), end='')

        # Calculate the distance of the current point to the points of the input Phi field
        distance, indices = tree.query(coordIn[point][0:3], k=neighbours)

        # Check if we've hit the same point
        if numpy.any(distance == 0):

            # Deform the coordinates of the current point
            # by subtracting the translation part of the deformation function Phi
            coordDef[point][:3] -= fieldValues[indices][numpy.where(distance == 0)][0][0:3, -1].copy()

        # Check if we have asked only for the closest neighbour
        elif neighbours == 1:

            # Deform the coordinates of the current point
            # by subtracting the translation part of the deformation function Phi
            # applied on the current point
            coordDef[point][:3] -= spam.deformation.decomposePhi(fieldValues[indices].copy(),
                                                                 PhiCentre=fieldCoords[indices],
                                                                 PhiPoint=coordIn[point][:3])["t"]

        # Consider the k closest neighbours
        else:
            # Compute the `Inverse Distance Weighting` since the closest points should have the major influence
            weightSumInv = sum(1 / distance)

            # Loop over each neighbour
            for neighbour in range(neighbours):
                # Calculate its weight
                weightInv = (1 / distance[neighbour]) / float(weightSumInv)

                # Deform the coordinates of the current point
                # by subtracting the translation part of the deformation function Phi
                # applied on the current point
                # multiplied by the weight of each neighbour
                coordDef[point][:3] -= numpy.dot(spam.deformation.decomposePhi(fieldValues[indices][neighbour].copy(),
                                                                                PhiCentre=fieldCoords[indices][neighbour],
                                                                                PhiPoint=coordIn[point][:3])["t"],
                                                    weightInv)

    # Deform the image
    imDef = numpy.zeros_like(im)

    imDef += scipy.ndimage.map_coordinates(im,
                                           coordDef[:, 0:3].T,
                                           mode="constant",
                                           order=interpolationOrder).reshape(imDef.shape).astype('<f4')

    return imDef


def interpolateField(fieldCoords, fieldValues, interpCoords, fieldInterpBinRatio=1):
    """
    Interpolate a field of deformation functions (Phi).

    Parameters
    ----------
        fieldCoords : nPointsField x 3 array
            Z Y X coordinates of points where ``fieldValues`` are defined

        fieldValues : nPointsField x 4 x 4 array
            Phi defined at ``fieldCoords``

        interpCoords : nPointsInterpolate x 3
            Z Y X coordinates of points to interpolate Phi for

        fieldInterpBinRatio : int, optional
            If the ``fieldCoords`` and ``fieldValues`` matrices refer to a binned version of the new coordintes.
            `e.g.`, if ``fieldInterpBinRatio = 2`` then ``fieldCoords`` and ``fieldValues`` have been calculated on an
            image half the size of what ``interpCoords`` are referring to.

    Returns
    -------
        interpValues : nPointsInterpolate x 4 x 4 array of Phis
    """

    # This version of the function will use scipy.ndimage.interpolation.map_coordinates().
    # It takes in a field, which means that our fieldValues Phi field MUST be regularly spaced.
    # Furthermore it takes points at integer values (voxels), so we have to convert from
    # positions in the Phi field, and the "real" voxel coordinates.
    # e.g., Our first measurement point is 12,12,12 and the node spacing is 20 pixels.
    # map_coordinates will access this first Phi 12,12,12 at a position [0,0,0] in the matrix of Phi values in space
    # The next Phi 32,12,12 at a position [1,0,0]
    # Define the output array
    output = numpy.zeros((interpCoords.shape[0], 4, 4))

    # 1. calculate node spacing and position of first point
    # Measure node spacing in all three directions:
    zUnique = numpy.unique(fieldCoords[:, 0])
    yUnique = numpy.unique(fieldCoords[:, 1])
    xUnique = numpy.unique(fieldCoords[:, 2])

    zSpacing = zUnique[1] - zUnique[0]
    ySpacing = yUnique[1] - yUnique[0]
    xSpacing = xUnique[1] - xUnique[0]

    if zSpacing == ySpacing and zSpacing == xSpacing:
        nodeSpacing = zSpacing

        # TopPoint -- Ask ER -- Elizabeth Regina -- Honni soit qui mal y pense
        taupPoihunt = [zUnique[0], yUnique[0], xUnique[0]]
        # print "Top point:", taupPoihunt

        nNodes = [int(1 + (zUnique[-1] - zUnique[0]) / zSpacing),
                  int(1 + (yUnique[-1] - yUnique[0]) / ySpacing),
                  int(1 + (xUnique[-1] - xUnique[0]) / xSpacing)]
    else:
        print("Not all node spacings are the same, help! {} {} {} ".format(
            zSpacing, ySpacing, xSpacing))
        return "moinsUn"

    # 2. reshape fieldValues into an Z*Y*X*Phiy*Phix array for map_coordinates
    fieldValues = fieldValues.reshape([nNodes[0], nNodes[1], nNodes[2], 4, 4])

    # 3. Convert interpCoords into positions in reshaped Phi array
    # If we have a non-zero bin, scale coordinates
    interpCoords /= fieldInterpBinRatio

    # Remove top corner coords...
    interpCoords -= taupPoihunt
    # And divide by node spacing, now coords are in 0->1 format
    interpCoords /= float(nodeSpacing)

    # 4. Call map_coordinates and return
    # Loop over each component of Phi, so they are not interpolated together.
    for Fy in range(4):
        for Fx in range(4):
            output[:, Fy, Fx] = scipy.ndimage.interpolation.map_coordinates(
                fieldValues[:, :, :, Fy, Fx], interpCoords.T, order=1)

    # 5. Scale transformation by binning value
    output[:, 0:3, 3] *= fieldInterpBinRatio
    return output


def binning(im, binning, returnCropAndCentre=False):
    """
    This function downscales images by averaging NxNxN voxels together in 3D and NxN pixels in 2D.
    This is useful for reducing data volumes, and denoising data (due to averaging procedure).

    Parameters
    ----------
        im : 2D/3D numpy array
            Input measurement field

        binning : int
            The number of pixels/voxels to average together

        returnCropAndCentre: bool (optional)
            Return the position of the centre of the binned image
            in the coordinates of the original image, and the crop
            Default = False

    Returns
    -------
        imBin : 2/3D numpy array
            `binning`-binned array

        (otherwise if returnCropAndCentre): list containing:
            imBin,
            topCrop, bottomCrop
            centre of imBin in im coordinates (useful for re-stitching)
    Notes
    -----
        Here we will only bin pixels/voxels if they is a sufficient number of
        neighbours to perform the binning. This means that the number of pixels that
        will be rejected is the dimensions of the image, modulo the binning amount.

        The returned volume is computed with only fully binned voxels, meaning that some voxels on the edges
        may be excluded.
        This means that the output volume size is the input volume size / binning or less (in fact the crop
        in the input volume is the input volume size % binning
    """
    twoD = False
    from . import DICToolkit

    if im.dtype == 'f8':
        im = im.astype('<f4')

    binning = int(binning)
    #print("binning = ", binning)

    dimsOrig = numpy.array(im.shape)
    #print("dimsOrig = ", dimsOrig)

    # Note: // is a floor-divide
    imBin = numpy.zeros(dimsOrig // binning, dtype=im.dtype)
    #print("imBin.shape = ", imBin.shape)

    # Calculate number of pixels to throw away
    offset = dimsOrig % binning
    #print("offset = ", offset)

    # Take less off the top corner than the bottom corner
    topCrop = offset // 2
    #print("topCrop = ", topCrop)
    topCrop = topCrop.astype('<i2')

    if len(im.shape) == 2:
        # pad them
        im = im[numpy.newaxis, ...]
        imBin = imBin[numpy.newaxis, ...]
        topCrop = numpy.array([0, topCrop[0], topCrop[1]]).astype('<i2')
        offset = numpy.array([0, offset[0], offset[1]]).astype('<i2')
        twoD = True

    # Call C++
    if im.dtype == 'f4':
        #print("Float binning")
        DICToolkit.binningFloat(im.astype('<f4'),
                                imBin,
                                topCrop.astype('<i4'),
                                int(binning))
    elif im.dtype == 'u2':
        #print("Uint 2 binning")
        DICToolkit.binningUInt(im.astype('<u2'),
                               imBin,
                               topCrop.astype('<i4'),
                               int(binning))
    elif im.dtype == 'u1':
        #print("Char binning")
        DICToolkit.binningChar(im.astype('<u1'),
                               imBin,
                               topCrop.astype('<i4'),
                               int(binning))

    if twoD:
        imBin = imBin[0]

    if returnCropAndCentre:
        centreBinned = (numpy.array(imBin.shape) - 1) / 2.0
        relCentOrig = offset + binning * centreBinned
        return [imBin, [topCrop, offset - topCrop], relCentOrig]
    else:
        return imBin

###############################################################
# Take a tetrahedral mesh (defined by coords and conn) and use
#   it to deform an image
###############################################################
def applyMeshTransformation(im, coordinates, connectivity, displacements, tetLabel=None):
    """
    This function deforms an image based on a tetrahedral mesh and
    nodal displacements (normally from Global DVC),
    using the mesh's shape functions to interpolate.

    Parameters
    ----------
        im : 3D numpy array of greyvalues
            Input image to be deformed

        coordinates : m x 3 numpy array
            M nodal coordinates in reference configuration

        connectivity : n x 4 numpy array
            Tetrahedral connectivity generated by spam.mesh.triangulate() for example

        displacements : m x 3 numpy array
            M displacements defined at the nodes


        tetLabel : 3D numpy array of ints (optional)
            Pixels labelled with the tetrahedron (i.e., line number in connectivity matrix) they belong to.
            This is in the deformed configuration.
            If this is not passed, it's calculated in this function (can be slow).

    Returns
    -------
        imDef : 3D numpy array of greyvalues
            Deformed image

    """
    import spam.label

    if tetLabel is None:
        #print("spam.DIC.applyMeshTransformation(): tetLabel not passed, recomputing it.")
        tetLabel = spam.label.labelTetrahedra(im.shape, coordinates+displacements, connectivity)

    # Allocate output array that will be painted in by C++
    imDef = numpy.zeros_like(im, dtype='<f4')


    spam.DIC.DICToolkit.applyMeshTransformation(im.astype('<f4'),
                                                tetLabel.astype("<u4"),
                                                imDef,
                                                connectivity.astype("<u4"),
                                                (coordinates+displacements).astype("<f8"),
                                                displacements.astype("<f8"))
    return imDef

