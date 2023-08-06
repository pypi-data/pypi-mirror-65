"""
Library of SPAM functions for dealing with labelled images
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

import sys
import os

from . import labelToolkit
import spam.plotting

import scipy.ndimage
import scipy.spatial
import matplotlib
import math
import progressbar
import spam.filters.morphologicalOperations as morph

# Define a random colourmap for showing labels
#   This is taken from https://gist.github.com/jgomezdans/402500
randomCmapVals = numpy.random.rand(256, 3)
randomCmapVals[0, :] = numpy.array([1.0, 1.0, 1.0])
randomCmapVals[-1, :] = numpy.array([0.0, 0.0, 0.0])
randomCmap = matplotlib.colors.ListedColormap(randomCmapVals)
del randomCmapVals


# If you change this, remember to change the typedef in tools/labelToolkit/labelToolkitC.hpp
labelType = '<u4'


def boundingBoxes(lab):
    """
    Returns bounding boxes for labelled objects using fast C-code which runs a single time through lab

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

    Returns
    -------
        boundingBoxes : lab.max()x6 array of ints
            This array contains, for each label, 6 integers:

            - Zmin, Zmax
            - Ymin, Ymax
            - Xmin, Xmax

    Note
    ----
        Bounding boxes `are not slices` and so to extract the correct bounding box from a numpy array you should use:
            lab[ Zmin:Zmax+1, Ymin:Ymax+1, Xmin:Xmax+1 ]
        Otherwise said, the bounding box of a single-voxel object at 1,1,1 will be:
            1,1,1,1,1,1

        Also note: for labelled images where some labels are missing, the bounding box returned for this case will be obviously wrong: `e.g.`, Zmin = (z dimension-1) and Zmax = 0

    """
    lab = lab.astype(labelType)

    boundingBoxes = numpy.zeros((lab.max() + 1, 6), dtype='<u2')

    labelToolkit.boundingBoxes(lab, boundingBoxes)

    return boundingBoxes


def centresOfMass(lab, boundingBoxes=None, minVol=None):
    """
    Calculates (binary) centres of mass of each label in labelled image

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        minVol : int, optional
            The minimum volume in vx to be treated, any object below this threshold is returned as 0

    Returns
    -------
        centresOfMass : lab.max()x3 array of floats
            This array contains, for each label, 3 floats, describing the centre of mass of each label in Z, Y, X order
    """
    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)
    if minVol is None:
        minVol = 0

    lab = lab.astype(labelType)

    centresOfMass = numpy.zeros((lab.max() + 1, 3), dtype='<f4')

    labelToolkit.centresOfMass(lab, boundingBoxes, centresOfMass, minVol)

    return centresOfMass


def volumes(lab, boundingBoxes=None):
    """
    Calculates (binary) volumes each label in labelled image, using potentially slow numpy.where

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

    Returns
    -------
        volumes : lab.max()x1 array of ints
            This array contains the volume in voxels of each label
    """
    # print "label.toolkit.volumes(): Warning this is a crappy python implementation"

    lab = lab.astype(labelType)

    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)

    volumes = numpy.zeros((lab.max() + 1), dtype='<u4')

    labelToolkit.volumes(lab, boundingBoxes, volumes)

    return volumes


def equivalentRadii(lab, boundingBoxes=None, volumes=None):
    """
    Calculates (binary) equivalent sphere radii of each label in labelled image

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        volumes : lab.max()x1 array of ints
            Vector contining volumes, if this is passed, the others are ignored

    Returns
    -------
        equivRadii : lab.max()x1 array of floats
            This array contains the equivalent sphere radius in pixels of each label
    """
    def vol2rad(volumes):
        return ((3.0 * volumes) / (4.0 * numpy.pi))**(1.0 / 3.0)

    # If we have volumes, just go for it
    if volumes is not None:
        return vol2rad(volumes)

    # If we don't have bounding boxes, recalculate them
    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)

    return vol2rad(spam.label.volumes(lab, boundingBoxes=boundingBoxes))


def momentOfInertia(lab, boundingBoxes=None, minVol=None, centresOfMass=None):
    """
    Calculates (binary) moments of inertia of each label in labelled image

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        centresOfMass : lab.max()x3 array of floats, optional
            Centres of mass in format returned by ``centresOfMass``.
            If not defined (Default = None), it is recomputed by running ``centresOfMass``

        minVol : int, optional
            The minimum volume in vx to be treated, any object below this threshold is returned as 0
            Default = default for spam.label.centresOfMass

    Returns
    -------
        eigenValues : lab.max()x3 array of floats
            The values of the three eigenValues of the moment of inertia of each labelled shape

        eigenVectors : lab.max()x9 array of floats
            3 x Z,Y,X components of the three eigenValues in the order of the eigenValues
    """
    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)
    if centresOfMass is None:
        centresOfMass = spam.label.centresOfMass(lab, boundingBoxes=boundingBoxes, minVol=minVol)

    lab = lab.astype(labelType)

    eigenValues = numpy.zeros((lab.max() + 1, 3), dtype='<f4')
    eigenVectors = numpy.zeros((lab.max() + 1, 9), dtype='<f4')

    labelToolkit.momentOfInertia(lab, boundingBoxes, centresOfMass, eigenValues, eigenVectors)

    return [eigenValues, eigenVectors]


def ellipseAxes(lab, volumes=None, MOIeigenValues=None, enforceVolume=True, twoD=False):
    """
    Calculates length of half-axes a,b,c of the ellipitic fit of the particle.
    These are half-axes and so are comparable to the radius -- and not the diameter -- of the particle.

    See appendix of for inital work:
        "Three-dimensional study on the interconnection and shape of crystals in a graphic granite by X-ray CT and image analysis.", Ikeda, S., Nakano, T., & Nakashima, Y. (2000). 

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels
            Note: This is not strictly necessary if volumes and MOI is given

        volumes : 1D array of particle volumes (optional, default = None)
            Volumes of particles (length of array = lab.max())

        MOIeigenValues : lab.max()x3 array of floats, (optional, default = None)
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        enforceVolume = bool (default = True)
            Should a, b and c be scaled to enforce the fitted ellipse volume to be
            the same as the particle?
            This causes eigenValues are no longer completely consistent with fitted ellipse

        twoD : bool (default = False)
            Are these in fact 2D ellipses?
            Not implemented!!

    Returns
    -------
        ABCaxes : lab.max()x3 array of floats
            a, b, c lengths of particle in pixels

    Note
    -----
        Our elliptic fit is not necessarily of the same volume as the original particle,
        although by default we scale all axes linearly with `enforceVolumes` to enforce this condition.

        Reminder: volume of an ellipse is (4/3)*pi*a*b*c

        Useful check from TM: Ia = (4/15)*pi*a*b*c*(b**2+c**2)

        Function contributed by Takashi Matsushima (University of Tsukuba)
    """
    # Full ref:
    # @misc{ikeda2000three,
    #         title={Three-dimensional study on the interconnection and shape of crystals in a graphic granite by X-ray CT and image analysis},
    #         author={Ikeda, S and Nakano, T and Nakashima, Y},
    #         year={2000},
    #         publisher={De Gruyter}
    #      }

    if volumes is None:
        volumes = spam.label.volumes(lab)
    if MOIeigenValues is None:
        MOIeigenValues = spam.label.momentOfInertia(lab)[0]

    ABCaxes = numpy.zeros((volumes.shape[0], 3))

    Ia = MOIeigenValues[:, 0]
    Ib = MOIeigenValues[:, 1]
    Ic = MOIeigenValues[:, 2]

    # Initial derivation -- has quite a different volume from the original particle
    # Use the particle's V. This is a source of inconsistency,
    # since the condition V = (4/3) * pi * a * b * c is not necessarily respected
    # ABCaxes[:,2] = numpy.sqrt( numpy.multiply((5.0/(2.0*volumes.ravel())),( Ib + Ia - Ic ) ) )
    # ABCaxes[:,1] = numpy.sqrt( numpy.multiply((5.0/(2.0*volumes.ravel())),( Ia + Ic - Ib ) ) )
    # ABCaxes[:,0] = numpy.sqrt( numpy.multiply((5.0/(2.0*volumes.ravel())),( Ic + Ib - Ia ) ) )

    mask = numpy.logical_and(Ia != 0, numpy.isfinite(Ia))
    # Calculate a, b and c: TM calculation 2018-03-30
    # 2018-04-30 EA and MW: swap A and C so that A is the biggest
    ABCaxes[mask, 2] = ((15.0 / (8.0 * numpy.pi)) * numpy.square((Ib[mask] + Ic[mask] - Ia[mask])) / numpy.sqrt(((Ia[mask] - Ib[mask] + Ic[mask]) * (Ia[mask] + Ib[mask] - Ic[mask])))) ** (1.0 / 5.0)
    ABCaxes[mask, 1] = ((15.0 / (8.0 * numpy.pi)) * numpy.square((Ic[mask] + Ia[mask] - Ib[mask])) / numpy.sqrt(((Ib[mask] - Ic[mask] + Ia[mask]) * (Ib[mask] + Ic[mask] - Ia[mask])))) ** (1.0 / 5.0)
    ABCaxes[mask, 0] = ((15.0 / (8.0 * numpy.pi)) * numpy.square((Ia[mask] + Ib[mask] - Ic[mask])) / numpy.sqrt(((Ic[mask] - Ia[mask] + Ib[mask]) * (Ic[mask] + Ia[mask] - Ib[mask])))) ** (1.0 / 5.0)

    if enforceVolume:
        # Compute volume of ellipse:
        ellipseVol = (4.0 / 3.0) * numpy.pi * ABCaxes[:, 0] * ABCaxes[:, 1] * ABCaxes[:, 2]
        # filter zeros and infs
        # print volumes.shape
        # print ellipseVol.shape
        volRatio = (volumes[mask] / ellipseVol[mask])**(1.0 / 3.0)
        # print volRatio
        ABCaxes[mask, 0] = ABCaxes[mask, 0] * volRatio
        ABCaxes[mask, 1] = ABCaxes[mask, 1] * volRatio
        ABCaxes[mask, 2] = ABCaxes[mask, 2] * volRatio

    return ABCaxes


def convertLabelToFloat(lab, vector):
    """
    Replaces all values of a labelled array with a given value.
    Useful for visualising properties attached to labels, `e.g.`, sand grain displacements.

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        vector : a lab.max()x1 vector with values to replace each label with

    Returns
    -------
        relabelled : 3D array of converted floats
    """
    lab = lab.astype(labelType)

    relabelled = numpy.zeros_like(lab, dtype='<f4')

    vector = vector.ravel().astype('<f4')

    labelToolkit.labelToFloat(lab, vector, relabelled)

    return relabelled


def makeLabelsSequential(lab):
    """
    This function fills gaps in labelled images,
    by relabelling them to be sequential integers.
    Don't forget to recompute all your grain properties since the label numbers will change

    Parameters
    -----------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background

    Returns
    --------
        lab : 3D numpy array of ints ( of type spam.label.toolkit.labelType)
            An array of labels with 0 as the background
    """
    maxLabel = int(lab.max())
    lab = lab.astype(labelType)

    uniqueLabels = numpy.unique(lab)
    # print uniqueLabels

    relabelMap = numpy.zeros((maxLabel + 1), dtype=labelType)
    relabelMap[uniqueLabels] = range(len(uniqueLabels))

    labelToolkit.relabel(lab, relabelMap)

    return lab


def _checkSlice(topOfSlice, botOfSlice, topLimit, botLimit):
    # Do we have any negative positions? Set all negative numbers to zero and see if there was any difference
    topOfSliceLimited = topOfSlice.copy()
    if topOfSliceLimited[0] < topLimit[0]:
       topOfSliceLimited[0] = topLimit[0]
    if topOfSliceLimited[1] < topLimit[1]:
       topOfSliceLimited[1] = topLimit[1]
    if topOfSliceLimited[2] < topLimit[2]:
       topOfSliceLimited[2] = topLimit[2]
    topOfSliceOffset = topOfSliceLimited - topOfSlice

    botOfSliceLimited = botOfSlice.copy()
    if botOfSliceLimited[0] > botLimit[0]:
       botOfSliceLimited[0] = botLimit[0]
    if botOfSliceLimited[1] > botLimit[1]:
       botOfSliceLimited[1] = botLimit[1]
    if botOfSliceLimited[2] > botLimit[2]:
       botOfSliceLimited[2] = botLimit[2]
    botOfSliceOffset = botOfSliceLimited - botOfSlice

    returnSliceLimited = (slice(int(topOfSliceLimited[0]), int(botOfSliceLimited[0])),
                          slice(int(topOfSliceLimited[1]), int(botOfSliceLimited[1])),
                          slice(int(topOfSliceLimited[2]), int(botOfSliceLimited[2])))

    returnSliceOffset = (slice(int(topOfSliceOffset[0]), int(topOfSliceOffset[0] + botOfSliceLimited[0] - topOfSliceLimited[0])),
                         slice(int(topOfSliceOffset[1]), int(topOfSliceOffset[1] + botOfSliceLimited[1] - topOfSliceLimited[1])),
                         slice(int(topOfSliceOffset[2]), int(topOfSliceOffset[2] + botOfSliceLimited[2] - topOfSliceLimited[2])))

    return returnSliceLimited, returnSliceOffset


def getLabel(labelledVolume, label, boundingBoxes=None, centresOfMass=None, margin=None, extractCube=False, extractCubeSize=None, maskOtherLabels=True, labelDilate=0):
    """
    Helper function to return well-formatted information about labels to
    help with iterations over labels

    Parameters
    ----------
        labelVolume : 3D array of ints
            3D Labelled volume

        label : int
            Label that we want information about

        boundingBoxes : nLabels*2 array of ints, optional
            Bounding boxes as returned by ``boundingBoxes``.
            Optional but highly recommended.
            If unset, bounding boxes are recalculated for every call.

        centresOfMass : nLabels*3 array of floats, optional
            Centres of mass as returned by ``centresOfMass``.
            Optional but highly recommended.
            If unset, centres of mass are recalculated for every call.

        extractCube : bool, optional
            Whether returned label subvolume should be in the middle of a cube or its bounding box.
            Should handle edges.
            Default = no

        extractCubeSize : int, optional
            half-size of cube to exctract.
            Default = calculate minimum cube

        margin : int, optional
            Extract a ``margin`` pixel margin around bounding box or cube.
            Default = 0

        maskOtherLabels : bool, optional
            In the returned subvolume, should other labels be masked?
            If true, the mask is directly returned.
            Default = True

        labelDilate : int, optional
            Number of times label should be dilated before returning it?
            This can be useful for catching the outside/edge of an image.
            ``margin`` should at least be equal to this value.
            Requires ``maskOtherLabels``.
            Default = 0

    Returns
    -------
        Dictionary containing:

            Keys:
                subvol : 3D array of ints
                    subvolume from labelled image

                slice : tuple of 3*slices
                    Slice used to extract subvol -- however edge management complicates this a bit, perhaps an offset should also be returned

                centreOfMassABS : 3*float
                    Centre of mass with respect to ``labelVolume``

                centreOfMassREL : 3*float
                    Centre of mass with respect to ``subvol``

                volume: int
                    Volume of label (before dilating)

    """
    import spam.mesh
    if boundingBoxes is None:
        print("\tlabel.toolkit.getLabel(): Bounding boxes not passed.")
        print("\tThey will be recalculated for each label, highly recommend calculating outside this function")
        boundingBoxes = spam.label.boundingBoxes(labelledVolume)

    if centresOfMass is None:
        print("\tlabel.toolkit.getLabel(): Centres of mass not passed.")
        print("\tThey will be recalculated for each label, highly recommend calculating outside this function")
        centresOfMass = spam.label.centresOfMass(labelledVolume)

    # Check if there is a bounding box for this label:
    if label >= boundingBoxes.shape[0]:
        return
        raise "No bounding boxes for this grain"

    bbo = boundingBoxes[label]
    com = centresOfMass[label]
    comRound = numpy.floor(centresOfMass[label])

    # 1. Check if boundingBoxes are correct:
    if (bbo[0] == labelledVolume.shape[0] - 1) and \
       (bbo[1] == 0) and \
       (bbo[2] == labelledVolume.shape[1] - 1) and \
       (bbo[3] == 0) and \
       (bbo[4] == labelledVolume.shape[2] - 1) and \
       (bbo[5] == 0):
        pass
        #print("\tlabel.toolkit.getLabel(): Label {} does not exist".format(label))

    else:
        # We have a bounding box, let's extract it.
        if extractCube:
            # Calculate offsets between centre of mass and bounding box
            offsetTop = numpy.ceil(com - bbo[0::2])
            offsetBot = numpy.ceil(com - bbo[0::2])
            offset = numpy.max(numpy.hstack([offsetTop, offsetBot]))

            # If is none, assume closest fitting cube.
            if extractCubeSize is not None:
                if extractCubeSize < offset:
                    print("\tlabel.toolkit.getLabel(): size of desired cube is smaller than minimum to contain label. Continuing anyway.")
                offset = int(extractCubeSize)

            # if a margin is set, add it to offset
            if margin is not None:
                offset += margin

            offset = int(offset)

            # we may go outside the volume. Let's check this
            labSubVol = numpy.zeros((3 * [2 * offset + 1]))

            topOfSlice = numpy.array([int(comRound[0] - offset),
                                      int(comRound[1] - offset),
                                      int(comRound[2] - offset)])
            botOfSlice = numpy.array([int(comRound[0] + offset + 1),
                                      int(comRound[1] + offset + 1),
                                      int(comRound[2] + offset + 1)])

            sliceLimited, sliceOffset = _checkSlice(topOfSlice, botOfSlice, [0, 0, 0], numpy.array(labelledVolume.shape))

            labSubVol[sliceOffset] = labelledVolume[sliceLimited].copy()

        # We have a bounding box, let's extract it.
        else:
            if margin is None:
                margin = 0

            topOfSlice = numpy.array([int(bbo[0] - margin),
                                      int(bbo[2] - margin),
                                      int(bbo[4] - margin)])
            botOfSlice = numpy.array([int(bbo[1] + 1 + margin),
                                      int(bbo[3] + 1 + margin),
                                      int(bbo[5] + 1 + margin)])

            labSubVol = numpy.zeros((botOfSlice[0] - topOfSlice[0],
                                     botOfSlice[1] - topOfSlice[1],
                                     botOfSlice[2] - topOfSlice[2]))

            sliceLimited, sliceOffset = _checkSlice(topOfSlice, botOfSlice, [0, 0, 0], numpy.array(labelledVolume.shape))

            labSubVol[sliceOffset] = labelledVolume[sliceLimited].copy()

        # Get mask for this label
        maskLab = labSubVol == label
        volume = numpy.sum(maskLab)

        # if we should mask, just return the mask.
        if maskOtherLabels:
            # labSubVol[ numpy.logical_not( maskLab ) ] = 0
            # Just overwrite "labSubVol"
            labSubVol = maskLab

            # 2019-09-07 EA: changing dilation/erosion into a single pass by a spherical element, rather than repeated
            # iterations of the standard.
            if labelDilate > 0:
                if labelDilate >= margin:
                    print("\tlabel.toolkit.getLabel(): labelDilate requested with a margin smaller than or equal to the number of times to dilate. I hope you know what you're doing!")
                strucuringElement = spam.mesh.structuringElement(radius=labelDilate, order=2, dim=3)
                labSubVol = scipy.ndimage.morphology.binary_dilation(labSubVol, structure=strucuringElement, iterations=1)
            if labelDilate < 0:
                strucuringElement = spam.mesh.structuringElement(radius=-1*labelDilate, order=2, dim=3)
                labSubVol = scipy.ndimage.morphology.binary_erosion( labSubVol, structure=strucuringElement, iterations=1)

        return {'subvol': labSubVol,
                'slice': sliceLimited,
                'centreOfMassABS': com,
                'centreOfMassREL': com - [sliceLimited[0].start - sliceOffset[0].start,
                                          sliceLimited[1].start - sliceOffset[1].start,
                                          sliceLimited[2].start - sliceOffset[2].start],
                'volume': volume}


def labelsOnEdges(lab):
    """
    Return labels on edges of volume

    Parameters
    ----------
        lab : 3D numpy array of ints
            Labelled volume

    Returns
    -------
        uniqueLabels : list of ints
            List of labels on edges
    """

    labelsVector = numpy.arange(lab.max() + 1)

    uniqueLabels = []

    uniqueLabels.append(numpy.unique(lab[:, :, 0]))
    uniqueLabels.append(numpy.unique(lab[:, :, -1]))
    uniqueLabels.append(numpy.unique(lab[:, 0, :]))
    uniqueLabels.append(numpy.unique(lab[:, -1, :]))
    uniqueLabels.append(numpy.unique(lab[0, :, :]))
    uniqueLabels.append(numpy.unique(lab[-1, :, :]))

    # Flatten list of lists:
    # https://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python?utm_medium=organic&utm_source=google_rich_qa&utm_campaign=google_rich_qa
    uniqueLabels = [item for sublist in uniqueLabels for item in sublist]

    # There might well be labels that appears on multiple faces of the cube, remove them
    uniqueLabels = numpy.unique(numpy.array(uniqueLabels))

    return uniqueLabels.astype(labelType)


def removeLabels(lab, listOfLabelsToRemove):
    """
    Resets a list of labels to zero in a labelled volume.

    Parameters
    ----------
        lab : 3D numpy array of ints
            Labelled volume

        listOfLabelsToRemove : list-like of ints
            Labels to remove

    Returns
    -------
        lab : 3D numpy array of ints
            Labelled volume with desired labels blanked

    Note
    ----
        You might want to use `makeLabelsSequential` after using this function,
        but don't forget to recompute all your grain properties since the label numbers will change
    """
    lab = lab.astype(labelType)

    # define a vector with sequential ints
    arrayOfLabels = numpy.arange(lab.max() + 1, dtype=labelType)

    # Remove the ones that have been asked for
    for l in listOfLabelsToRemove:
        arrayOfLabels[l] = 0

    labelToolkit.relabel(lab, arrayOfLabels)

    return lab


def setVoronoi(lab, poreEDT=None, maxPoreRadius=10):
    """
    This function computes an approximate set Voronoi for a given labelled image.
    This is a voronoi which does not have straight edges, and which necessarily
    passes through each contact point, so it is respectful of non-spherical grains.

    See:
    Schaller, F. M., Kapfer, S. C., Evans, M. E., Hoffmann, M. J., Aste, T., Saadatfar, M., ... & Schroder-Turk, G. E. (2013). Set Voronoi diagrams of 3D assemblies of aspherical particles. Philosophical Magazine, 93(31-33), 3993-4017.
    https://doi.org/10.1080/14786435.2013.834389

    and

    Weis, S., Schonhofer, P. W., Schaller, F. M., Schroter, M., & Schroder-Turk, G. E. (2017). Pomelo, a tool for computing Generic Set Voronoi Diagrams of Aspherical Particles of Arbitrary Shape. In EPJ Web of Conferences (Vol. 140, p. 06007). EDP Sciences.

    Parameters
    -----------
        lab: 3D numpy array of labelTypes
            Labelled image

        poreEDT: 3D numpy array of floats (optional, default = None)
            Euclidean distance map of the pores.
            If not given, it is computed by scipy.ndimage.morphology.distance_transform_edt

        maxPoreRadius: int (optional, default = 10)
            Maximum pore radius to be considered (this threshold is for speed optimisation)

    Returns
    --------
        lab: 3D numpy array of labelTypes
            Image labelled with set voronoi labels
    """
    if poreEDT is None:
        # print( "\tlabel.toolkit.setVoronoi(): Calculating the Euclidean Distance Transform of the pore with" )
        # print  "\t\tscipy.ndimage.morphology.distance_transform_edt, this takes a lot of memory"
        poreEDT = scipy.ndimage.morphology.distance_transform_edt(lab == 0).astype('<f4')

    lab = lab.astype(labelType)
    labOut = numpy.zeros_like(lab)
    maxPoreRadius = int(maxPoreRadius)

    # Prepare sorted distances in a cube to fit a maxPoreRadius.
    # This precomutation saves a lot of time
    # Local grid of values, centred at zero
    gridD = numpy.mgrid[-maxPoreRadius:maxPoreRadius + 1,
                        -maxPoreRadius:maxPoreRadius + 1,
                        -maxPoreRadius:maxPoreRadius + 1]

    # Compute distances from centre
    Rarray = numpy.sqrt(numpy.square(gridD[0]) + numpy.square(gridD[1]) + numpy.square(gridD[2])).ravel()
    sortedIndices = numpy.argsort(Rarray)

    # Array to hold sorted points
    coords = numpy.zeros((len(Rarray), 3), dtype='<i4')
    # Fill in with Z, Y, X points in order of distance to centre
    coords[:, 0] = gridD[0].ravel()[sortedIndices]
    coords[:, 1] = gridD[1].ravel()[sortedIndices]
    coords[:, 2] = gridD[2].ravel()[sortedIndices]
    del gridD

    # Now define a simple array (by building a list) that gives the linear
    #   entry point into coords at the nearest integer values
    sortedDistances = Rarray[sortedIndices]
    indices = []
    n = 0
    i = 0
    while i <= maxPoreRadius + 1:
        if sortedDistances[n] >= i:
            # indices.append( [ i, n ] )
            indices.append(n)
            i += 1
        n += 1
    indices = numpy.array(indices).astype('<i4')

    # Call C++ code
    labelToolkit.setVoronoi(lab, poreEDT.astype('<f4'), labOut, coords, indices)

    return labOut


def labelTetrahedra(dims, points, connectivity):
    """
    Labels voxels corresponding to tetrahedra according to a connectivity matrix and node points

    Parameters
    ----------
        dims: tuple representing z,y,x dimensions of the desired labelled output

        points: 3 x number of points array of floats
            List of points that define the vertices of the tetrahedra in Z,Y,X format.
            These points are referred to by line number in the connectivity array

        connectivity: 4 x number of tetrahedra array of integers
            Connectivity matrix between points that define tetrahedra.
            Each line defines a tetrahedron whose number is the line number + 1.
            Each line contains 4 integers that indicate the 4 points in the nodePos array.

    Returns
    -------
        3D array of ints, shape = dims
            Labelled 3D volume where voxels are numbered according to the tetrahedron number they fall inside of
    """

    dims = numpy.array(dims).astype('<u2')
    lab = numpy.ones(tuple(dims), dtype=labelType)*connectivity.shape[0]+1

    connectivity = connectivity.astype('<u4')
    points = points.astype('<f4')

    labelToolkit.tetPixelLabel(lab, connectivity, points)

    return lab


def labelTetrahedraForScipyDelaunay(dims, delaunay):
    """
    Labels voxels corresponding to tetrahedra coming from scipy.spatial.Delaunay
    Apparently the cells are not well-numbered, which causes a number of zeros
    when using `labelledTetrahedra`

    Parameters
    ----------
        dims: tuple
            represents z,y,x dimensions of the desired labelled output

        delaunay: "delaunay" object
            Object returned by scipy.spatial.Delaunay( centres )
            Hint: If using label.toolkit.centresOfMass( ), do centres[1:] to remove
            the position of zero.

    Returns
    -------
        lab: 3D array of ints, shape = dims
            Labelled 3D volume where voxels are numbered according to the tetrahedron number they fall inside of
    """

    # Big matrix of points poisitions
    points = numpy.zeros((dims[0] * dims[1] * dims[2], 3))

    mgrid = numpy.mgrid[0:dims[0], 0:dims[1], 0:dims[2]]
    for i in [0, 1, 2]:
        points[:, i] = mgrid[i].ravel()

    del mgrid

    lab = numpy.ones(tuple(dims), dtype=labelType)*delaunay.nsimplex+1
    lab = delaunay.find_simplex(points).reshape(dims)

    return lab


def fabricTensor(orientations):
    """
    Calculation of a second order fabric tensor from orientations

    Parameters
    ----------
        orientations: Nx3 array of floats
            Z, Y and X components of direction vectors
            Non-unit vectors are normalised.

    Returns
    -------
        N: 3x3 array of floats
            normalised second order fabric tensor
            with N[0,0] corresponding to z-z, N[1,1] to y-y and N[2,2] x-x

        F: 3x3 array of floats
            fabric tensor of the third kind (deviatoric part)
            with F[0,0] corresponding to z-z, F[1,1] to y-y and F[2,2] x-x

        a: float
            scalar anisotropy factor based on the deviatoric part F

    Note
    ----
        see [Kanatani, 1984] for more information on the fabric tensor
        and [Gu et al, 2017] for the scalar anisotropy factor

        Function contibuted by Max Wiebicke (Dresden University)
    """
    # from http://stackoverflow.com/questions/2850743/numpy-how-to-quickly-normalize-many-vectors
    norms = numpy.apply_along_axis(numpy.linalg.norm, 1, orientations)
    orientations = orientations / norms.reshape(-1, 1)

    # create an empty array
    N = numpy.zeros((3, 3))
    size = len(orientations)

    for i in range(size):
        orientation = orientations[i]
        tensProd = numpy.outer(orientation, orientation)
        N[:, :] = N[:, :] + tensProd

    # fabric tensor of the first kind
    N = N / size
    # fabric tensor of third kind
    F = (N - (numpy.trace(N) * (1. / 3.)) * numpy.eye(3, 3)) * (15. / 2.)

    # scalar anisotropy factor
    a = math.sqrt(3. / 2. * numpy.tensordot(F, F, axes=2))

    return N, F, a


def filterIsolatedCells(array, struct, size):
    """
    Return array with completely isolated single cells removed

    Parameters
    ----------
        array: 3-D (labelled or binary) array
            Array with completely isolated single cells

        struct: 3-D binary array
            Structure array for generating unique regions

        size: integer
            Size of the isolated cells to exclude
            (Number of Voxels)

    Returns
    -------
        filteredArray: 3-D (labelled or binary) array
            Array with minimum region size > size

    Notes
    -----
        function from: http://stackoverflow.com/questions/28274091/removing-completely-isolated-cells-from-python-array
    """

    filteredArray = ((array > 0) * 1).astype('uint8')
    idRegions, numIDs = scipy.ndimage.label(filteredArray, structure=struct)
    idSizes = numpy.array(scipy.ndimage.sum(filteredArray, idRegions, range(numIDs + 1)))
    areaMask = (idSizes <= size)
    filteredArray[areaMask[idRegions]] = 0

    filteredArray = ((filteredArray > 0) * 1).astype('uint8')
    array = filteredArray * array

    return array


def trueSphericity(lab, boundingBoxes=None, centresOfMass=None, gaussianFilterSigma=0.75, minVol=256):
    """
    Calculates the degree of True Sphericity (psi) for all labels, as per:
    "Sphericity measures of sand grains" Rorato et al., Engineering Geology, 2019
    and originlly proposed in: "Volume, shape, and roundness of rock particles", Waddell, The Journal of Geology, 1932.

    True Sphericity (psi) = Surface area of equivalent sphere / Actual surface area

    The actual surface area is computed by extracting each particle with getLabel, a Gaussian smooth of 0.75 is applied
    and the marching cubes algorithm from skimage is used to mesh the surface and compute the surface area.

    Parameters
    ----------
        lab : 3D array of integers
            Labelled volume, with lab.max() labels

        boundingBoxes : lab.max()x6 array of ints, optional
            Bounding boxes in format returned by ``boundingBoxes``.
            If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        centresOfMass : lab.max()x3 array of floats, optional
            Centres of mass in format returned by ``centresOfMass``.
            If not defined (Default = None), it is recomputed by running ``centresOfMass``

        gaussianFilterSigma : float, optional
            Sigma of the Gaussian filter used to smooth the binarised shape
            Default = 0.75

        minVol : int, optional
            The minimum volume in vx to be treated, any object below this threshold is returned as 0
            Default = 256 voxels

    Returns
    -------
        trueSphericity : lab.max() array of floats
            The values of the degree of true sphericity for each particle

    Notes
    -----
        Function contributed by Riccardo Rorato (UPC Barcelona)

        Due to numerical errors, this value can be >1, it should be clipped at 1.0
    """
    import skimage.measure

    lab = lab.astype(labelType)

    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(lab)
    if centresOfMass is None:
        centresOfMass = spam.label.centresOfMass(lab, boundingBoxes=boundingBoxes, minVol=minVol)


    trueSphericity = numpy.zeros((lab.max() + 1), dtype='<f4')

    sphereSurfaceArea = 4.0*numpy.pi*(equivalentRadii(lab, boundingBoxes=boundingBoxes)**2)

    for label in range(1, lab.max()+1):
        if not (centresOfMass[label]==numpy.array([0.0, 0.0, 0.0])).all():
            # Extract grain
            GL = getLabel(lab, label, boundingBoxes=boundingBoxes, centresOfMass=centresOfMass, extractCube=True, margin=2, maskOtherLabels=True)
            # Gaussian smooth
            grainCubeFiltered = scipy.ndimage.filters.gaussian_filter(GL['subvol'].astype('<f4'), sigma=gaussianFilterSigma)
            # mesh edge
            verts, faces, _, _ = skimage.measure.marching_cubes_lewiner(grainCubeFiltered, level=0.5)
            # compute surface
            surfaceArea  = skimage.measure.mesh_surface_area(verts, faces)
            # compute psi
            trueSphericity[label] = sphereSurfaceArea[label]/surfaceArea
    return trueSphericity


#def _feretDiameters(lab, labelList=None, boundingBoxes=None, centresOfMass=None, numberOfOrientations=100, margin=0, interpolationOrder=0):
    #"""
    #Calculates (binary) feret diameters (caliper lengths) over a number of equally-spaced orientations
    #and returns the maximum and minimum values, as well as the orientation they were found in.

    #Parameters
    #----------
        #lab : 3D array of integers
            #Labelled volume, with lab.max() labels

        #labelList: list of ints, optional
            #List of labels for which to calculate feret diameters and orientations. Labels not in lab are ignored. Outputs are given in order of labelList.
            #If not defined (Default = None), a list is created from label 0 to lab.max()

        #boundingBoxes : lab.max()x6 array of ints, optional
            #Bounding boxes in format returned by ``boundingBoxes``.
            #If not defined (Default = None), it is recomputed by running ``boundingBoxes``

        #centresOfMass : lab.max()x3 array of floats, optional
            #Centres of mass in format returned by ``centresOfMass``.
            #If not defined (Default = None), it is recomputed by running ``centresOfMass``

        #numberOfOrientations : int, optional
            #Number of trial orientations in 3D to measure the caliper lengths in.
            #These are defined with a Saff and Kuijlaars Spiral.
            #Default = 100

        #margin : int, optional
            #Number of pixels by which to pad the bounding box length to apply as the margin in spam.label.getLabel().
            #Default = 0

        #interpolationOrder = int, optional
            #Interpolation order for rotating the object.
            #Default = 0

    #Returns
    #-------
        #feretDiameters : lab.max()x2 (or len(labelList)x2 if labelList is not None) array of integers
            #The max and min values of the caliper lengths of each labelled shape.
            #Expected accuracy is +- 1 pixel

        #feretOrientations : lab.max()x6 (or len(labelList)x6 if labelList is not None) array of floats
            #2 x Z,Y,X components of orientations of the max and min caliper lengths

    #Notes
    #-----
        #Function contributed by Estefan Garcia (Caltech, previously at Berkeley)
    #"""

    ##Notes
    ##-------
        ##Must import spam.DIC to use this function because it utilizes the computePhi and applyPhi functions.
        ##This function currently runs in serial but can be improved to run in parallel.
    #import spam.DIC

    #lab = lab.astype(labelType)

    #if labelList is None:
        #labelList = list(range(0,lab.max()+1))
        #feretDiameters = numpy.zeros((lab.max() + 1, 2))
        #feretOrientations = numpy.zeros((lab.max()+1,6))
    #elif type(labelList) is not list and type(labelList) is not numpy.ndarray:
        ## Allow inputs to be ints or of type numpy.ndarray
        #labelList = [labelList]
        #feretDiameters = numpy.zeros((len(labelList),2))
        #feretOrientations = numpy.zeros((len(labelList),6))
    #else:
        #feretDiameters = numpy.zeros((len(labelList),2))
        #feretOrientations = numpy.zeros((len(labelList),6))

    ##print('Calculating Feret diameters for '+str(len(labelList))+' label(s).')

    #if boundingBoxes is None:
        #boundingBoxes = spam.label.boundingBoxes(lab)
    #if centresOfMass is None:
        #centresOfMass = spam.label.centresOfMass(lab, boundingBoxes=boundingBoxes)

    ## Define test orientations
    #testOrientations = spam.plotting.orientationPlotter.SaffAndKuijlaarsSpiral(4*numberOfOrientations)

    #i=0
    #while i < len(testOrientations):
        #if (testOrientations[i] < 0).any():
            #testOrientations = numpy.delete(testOrientations,i,axis=0)
        #else:
            #i+=1

    ## Compute rotation of trial orientations onto z-axis
    #rot_axes = numpy.cross(testOrientations,[1.,0.,0.])
    #rot_axes/=numpy.linalg.norm(rot_axes,axis=1,keepdims=True)
    #theta=numpy.reshape(numpy.rad2deg(numpy.arccos(numpy.dot(testOrientations,[1.,0.,0.]))),[len(testOrientations),1])

    ## Compute Phi and its inverse for all trial orientations
    #Phi = numpy.zeros((len(testOrientations),4,4))
    #transf_R = rot_axes*theta
    #for r in range(0,len(transf_R)):
        #transformation = {'r': transf_R[r]}
        #Phi[r] = spam.DIC.computePhi(transformation)
    #Phi_inv = numpy.linalg.inv(Phi)

    ## Loop through all labels provided in labelList. Note that labels might not be in order.    
    #for labelIndex in range(0,len(labelList)):
        #label = labelList[labelIndex]
        #if label in lab and label > 0: #skip if label does not exist or if zero
            ##print('spam.label.feretDiameters: Working on Label '+str(label))
            ##margin = numpy.uint16(numpy.round(marginFactor*numpy.min([boundingBoxes[label,1]-boundingBoxes[label,0]+1,
                                                                      ##boundingBoxes[label,3]-boundingBoxes[label,2]+1,
                                                                      ##boundingBoxes[label,5]-boundingBoxes[label,4]+1])))
            #particle = getLabel(lab,
                                #label,
                                #boundingBoxes   = boundingBoxes,
                                #centresOfMass   = centresOfMass,
                                #extractCube     = True,
                                #margin          = margin,
                                #maskOtherLabels = True)
            #subvol = particle['subvol']

            ## Initialize DMin and DMax using the untransformed orientation
            #subvol_transformed_BB = spam.label.boundingBoxes(subvol > 0.5)
            #zWidth = subvol_transformed_BB[1,1] - subvol_transformed_BB[1,0] + 1
            #yWidth = subvol_transformed_BB[1,3] - subvol_transformed_BB[1,2] + 1
            #xWidth = subvol_transformed_BB[1,5] - subvol_transformed_BB[1,4] + 1

            #index_max = numpy.argmax([zWidth,yWidth,xWidth])
            #index_min = numpy.argmin([zWidth,yWidth,xWidth])

            #DMax = max([zWidth, yWidth, xWidth])
            #DMin = min([zWidth, yWidth, xWidth])
            #maxOrientation = [numpy.array([1.,0.,0.]),
                              #numpy.array([0.,1.,0.]),
                              #numpy.array([0.,0.,1.])][index_max]
            #minOrientation = [numpy.array([1.,0.,0.]),
                              #numpy.array([0.,1.,0.]),
                              #numpy.array([0.,0.,1.])][index_min]

            #for orientationIndex in range(0,len(testOrientations)):
                ## Apply rotation matrix about centre of mass of particle
                #subvol_centreOfMass = spam.label.centresOfMass(subvol)
                #subvol_transformed = spam.DIC.applyPhi(subvol,
                                                       #Phi = Phi[orientationIndex],
                                                       #PhiPoint = subvol_centreOfMass[1],
                                                       #interpolationOrder=interpolationOrder)

                ## Use bounding box of transformed subvolume to calculate particle widths in 3 directions
                #subvol_transformed_BB = spam.label.boundingBoxes(subvol_transformed > 0.5)
                #zWidth = subvol_transformed_BB[1,1] - subvol_transformed_BB[1,0] + 1
                #yWidth = subvol_transformed_BB[1,3] - subvol_transformed_BB[1,2] + 1
                #xWidth = subvol_transformed_BB[1,5] - subvol_transformed_BB[1,4] + 1

                ## Check if higher than previous DMax or lower than previous DMin
                #index_max = numpy.argmax([DMax,zWidth,yWidth,xWidth])
                #index_min = numpy.argmin([DMin,zWidth,yWidth,xWidth])
                #DMax = max([DMax,zWidth,yWidth,xWidth])
                #DMin = min([DMin,zWidth,yWidth,xWidth])

                ## Update orientations for DMax and DMin
                #maxOrientation = [maxOrientation,
                                #testOrientations[orientationIndex],
                                #numpy.matmul(Phi_inv[orientationIndex,:3,:3],numpy.array([0,1,0])),
                                #numpy.matmul(Phi_inv[orientationIndex,:3,:3],numpy.array([0,0,1]))][index_max]
                #minOrientation = [minOrientation,
                                #testOrientations[orientationIndex],
                                #numpy.matmul(Phi_inv[orientationIndex,:3,:3],numpy.array([0,1,0])),
                                #numpy.matmul(Phi_inv[orientationIndex,:3,:3],numpy.array([0,0,1]))][index_min]


            #feretDiameters[labelIndex,:] = [DMax,DMin]
            #feretOrientations[labelIndex,:] = numpy.concatenate([maxOrientation,minOrientation])

    #return feretDiameters,feretOrientations
def meanOrientation(orientations):
    """
    This function performs a Principal Component Analysis over a group of vectors in order to find the main direction of the set. Once the main direction is found, all the vectors are projected to the new basis. 
    

    Parameters
    -----------

        orientations : Nx3 numpy array of floats
                        Z, Y and X components of direction vectors.
                        Non-unit vectors are normalised.

    Returns
    --------
        
        orientations_proj : Nx3 numpy array of floats with the [z,y,x] components of the projected vectors over the basis obtained in the Principal Component Analysis. All the projected vectors are normalized.
    
        main_axis : [z,y,x] components of the main axis of the data set.
        
        intermediate_axis : [z,y,x] components of the intermediate axis of the data set.
        
        minor_axis : [z,y,x] components of the minor axis of the data set.
        
    Notes
    -----
        PCA analysis taken from https://machinelearningmastery.com/calculate-principal-component-analysis-scratch-python/
        
    """
    
    # Read Number of Points
    numberOfPoints = orientations.shape[0]
    #Normalize all the vectors from http://stackoverflow.com/questions/2850743/numpy-how-to-quickly-normalize-many-vectors
    norms = numpy.apply_along_axis( numpy.linalg.norm, 1, orientations )
    orientations = orientations / norms.reshape( -1, 1 )
    #Flip if the z-component is located at z < 0
    for vector_i in range(numberOfPoints):
        z,y,x=orientations[vector_i]
        if z < 0: z = -z; y = -y; x = -x
        orientations[vector_i] = [z,y,x]
    #Run PCA
    orientationsPCA = numpy.concatenate((orientations, -1*orientations), axis=0) #COMENT
    #Compute mean of each column
    meanVal = numpy.mean(orientationsPCA, axis=0)
    #Center array
    orientationsPCA = orientationsPCA - meanVal
    #Compute covariance matrix of centered matrix
    covMat = numpy.cov(orientationsPCA.T)
    #Eigendecomposition of covariance matrix
    values, vectors = numpy.linalg.eig(covMat)
    #Decompose axis
    main_axis = vectors[:,numpy.argmax(values)]
    if main_axis[0]<0: main_axis[:]=-1*main_axis[:]
    intermediate_axis = vectors[:,3 - numpy.argmin(values) - numpy.argmax(values)]
    minor_axis = vectors[:,numpy.argmin(values)]
    
    #Project all vectors
    orientations_proj = numpy.zeros((numberOfPoints,3))
    for vector_i in range(numberOfPoints):
        orientations_proj[vector_i,0] = numpy.dot(orientations[vector_i,:],main_axis) / numpy.linalg.norm(main_axis)
        orientations_proj[vector_i,1] = numpy.dot(orientations[vector_i,:],intermediate_axis) / numpy.linalg.norm(intermediate_axis)
        orientations_proj[vector_i,2] = numpy.dot(orientations[vector_i,:],minor_axis) / numpy.linalg.norm(minor_axis)
    
    
   
    return orientations_proj, main_axis, intermediate_axis, minor_axis

class Spheroid:
    """
    This class creates at 3D binarised ellipsoid characterised by two semi-axis and 
    an orientation vector as: 
            - c, Main semi-axis of rotational symmetry. 
            - a, Secondary semi-axis (contains as well the third semi-axis)
            - v, Orientation vector.
            
    The binarised ellipsoid can be used as an structuring element for morphological 
    operations.
    
    Parameters
    -----------
        a : int or float
            Length of the secondary semi-axis, contains as well the third semi-axis
            
        c : int or float
            Lenght of the principal semi-axis
            
        v : 1x3 array
            Orientation vector of the ellipsoid

    Returns
    --------
        Spheroid : 3D boolean array
            Boolean array with the spheroid

    Note
    -----
        If c>a, a prolate is generated; while a>c yields an oblate.
        
        Taken from https://sbrisard.github.io/posts/20150930-orientation_correlations_among_rice_grains-06.html
        
    """
    def __init__(self, a, c, d=None, dim=None):
        if ((d is None) + (dim is None)) != 1:
            raise ValueError('d and dim cannot be specified simultaneously')
        self.a = a
        self.c = c
        if d is None:
            self.d = numpy.zeros((dim,), dtype=numpy.float64)
            self.d[-1] = 1.
        else:
            self.d = numpy.asarray(d)
            dim = len(d)
        p = numpy.outer(self.d, self.d)
        q = numpy.eye(dim, dtype=numpy.float64) - p
        self.Q = c**2*p+a**2*q
        self.invQ = p/c**2+q/a**2

    def __str__(self):
        return ('spheroid: a = {}, c = {3}, d = {}, ').format(tuple(self.d),
                                                              self.a,
                                                              self.c)

    def bounding_box(self):
        return numpy.sqrt(numpy.diag(self.Q))

    def criterion(self, x):
        """Ordering of points: ``x[i, ...]`` is the i-th coordinate"""
        y = numpy.tensordot(self.invQ, x, axes=([-1], [0]))
        numpy.multiply(x, y, y)
        return numpy.sum(y, axis=0)

    def digitize(self, h=1.0):
        bb = self.bounding_box()
        i_max = numpy.ceil(bb/h-0.5)
        bb = i_max*h
        shape = 2*i_max+1

        slices = [slice(-x, x, i*1j) for (x, i) in zip(bb, shape)]
        x = numpy.mgrid[slices]
        return self.criterion(x)<=1.0

def fixUndersegmentation(labelIm, greyIm, vol_Expected, tVol1, tVol2, vect, a, c, boundingBoxes=None, centresOfMass=None, NumberOfThreads = 1, verbose = False):
    """
    This functions fix the undersegmentation for a labelled image, making use of directional 
    erosion to get the seed for the watershed. 
    
    Parameters
    -----------
        labelIm : 3D numpy array
            Labelled image
            
        greyIm : 3D numpy array
            Greyscale of the labelled image
            
        vol_Expected : float
            Expected volume of a single particle
            
        tVol1 : float between 0 and 1
            Volume threshold for oversegmentation. A particle is oversegmented
            if its volume is less than tVol1.
            
        tVol2 : float greater than 1
            Volume threshold for undersegmentation. A particle is undersegmented
            if its volume is greater than tVol2.
            
        vect : nX3 array of floats
            Array of directional vectors for the structuring element
        
        a : int or float
            Length of the secondary semi-axis of the structuring element
            
        c : int or float
            Lenght of the principal semi-axis of the structuring element
            
        NumberOfThreads : integer (optional, default = 1)
            Number of Threads for multiprocessing of the directional erosion.
            Default = 1

        verbose : boolean (optional, default = False)
            True for printing the evolution of the process
            False for not printing the evolution of process

    Returns
    --------
        labelIm : 3D numpy array
            New labelled image

    Note
    -----
        This algorithm requires a prior knowledge of the particle shape,
        described as an ellipsoid with semi axis a and c. 
       
        
    """
    
    #Compute boundingBixes if needed
    if boundingBoxes is None:
        boundingBoxes = spam.label.boundingBoxes(labelIm)
    if centresOfMass is None:
        centresOfMass = spam.label.centresOfMass(labelIm)
    #Compute volumes of particles and normalize    
    volumesLab = spam.label.volumes(labelIm[1:])
    volumesLab = volumesLab / vol_Expected
    #Get undersegmented subset
    underSeg = numpy.where(volumesLab >= tVol2, volumesLab, 0)
    listLabels = numpy.nonzero(underSeg)[0]
    labelCounter = numpy.max(labelIm)
    labelDummy = numpy.zeros(labelIm.shape)
    pbar = progressbar.ProgressBar(maxval=len(listLabels)).start()
    finishedCounter = 0
    for i in range(len(listLabels)):
        #Get Label
        label_i = listLabels[i]
        #Get BW subset
        labelData = spam.label.getLabel(labelIm, label_i, boundingBoxes = boundingBoxes, centresOfMass = centresOfMass)
        bwIm = labelData['subvol']
        Continue = False
        itCounter = 1
        while Continue == False:
            #Directional Erosion
            imEroded = morph.directionalErosion(bwIm, vect, a, c, NumberOfThreads = NumberOfThreads, verbose = verbose)
            #Label the markers
            markers, num_seeds =  scipy.ndimage.label(imEroded)
            #New Segmentation
            if verbose:
                print('Processing label '+str(i)+' of '+str(len(listLabels))+'. Iteration #'+str(itCounter))
            newSeg = spam.label.watershed(bwIm, markers=markers, verbose = verbose)
            #Check Number of Labels
            if numpy.max(newSeg) > 1:
                volNewSeg = spam.label.volumes(newSeg) / vol_Expected
                if any([a and b for a, b in zip(volNewSeg > tVol1, volNewSeg < tVol2)]) == True:
                    Continue = True
                    finishedCounter += 1
                    pbar.update(finishedCounter)
                    for lab in numpy.unique(newSeg[newSeg != 0]):
                        if volNewSeg[lab] >= tVol1: #Only check for mini-particles, Greater particles can be used to run the code again?
                            newSeg = numpy.where( newSeg == lab, labelCounter + 1 , newSeg)
                            labelCounter += 1           
                    labelDummyUnit = numpy.zeros(labelDummy.shape) 
                    labelDummyUnit[boundingBoxes[label_i][0] : boundingBoxes[label_i][1]+1, boundingBoxes[label_i][2] : boundingBoxes[label_i][3]+1, boundingBoxes[label_i][4] : boundingBoxes[label_i][5]+1] = newSeg
                    labelDummy = labelDummy + labelDummyUnit
                    labelIm = spam.label.removeLabels(labelIm, [label_i])
                else:
                    if itCounter != 4:
                        itCounter+= 1
                        labelData = spam.label.getLabel(labelIm, label_i, boundingBoxes = boundingBoxes, centresOfMass = centresOfMass)
                        bwImOr = labelData['subvol']
                        greyIm_i = greyIm[boundingBoxes[label_i,0] : boundingBoxes[label_i,1]+1, boundingBoxes[label_i,2] : boundingBoxes[label_i,3]+1, boundingBoxes[label_i,4] : boundingBoxes[label_i,5]+1]
                        greyIm_i = greyIm_i * bwImOr
                        bwIm = greyIm_i>= 0.5+itCounter*0.05
                    else:
                        Continue = True
                        finishedCounter += 1
                        pbar.update(finishedCounter)
                
            else:
                if itCounter != 4:
                    itCounter+= 1
                    labelData = spam.label.getLabel(labelIm, label_i, boundingBoxes = boundingBoxes, centresOfMass = centresOfMass)
                    bwImOr = labelData['subvol']
                    greyIm_i = greyIm[boundingBoxes[label_i,0]:boundingBoxes[label_i,1]+1, boundingBoxes[label_i,2]:boundingBoxes[label_i,3]+1, boundingBoxes[label_i,4]:boundingBoxes[label_i,5]+1]
                    greyIm_i = greyIm_i * bwImOr
                    bwIm = greyIm_i>= 0.5+itCounter*0.05
                else:
                    Continue = True 
                    finishedCounter += 1
                    pbar.update(finishedCounter)             
    labelIm = labelIm + labelDummy
    labelIm = spam.label.makeLabelsSequential(labelIm)
    pbar.finish()      
    
    return labelIm

