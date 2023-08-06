"""
Library of SPAM functions for dealing with fields of Phi or fields of F
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

# 2020-02-24 Olga Stamati and Edward Ando
from __future__ import print_function
import numpy

def FfieldRegularQ8(displacementField, nodeSpacing):
    """
    This function computes the transformation gradient field F from a given displacement field.
    Please note: the transformation gradient tensor: F = I + du/dx.

    This function computes du/dx in the centre of an 8-node cell (Q8 in Finite Elements terminology) using order one (linear) shape functions.

    Parameters
    ----------
        displacementField : 4D array of floats
            The vector field to compute the derivatives.
            #Its shape is (nz, ny, nx, 3)

        nodeSpacing : 3-component list of floats
            Length between two nodes in every direction (*i.e.,* size of a cell)

    Returns
    -------
        F : (nz-1) x (ny-1) x (nx-1) x 3x3 array of n cells
            The field of the transformation gradient tensors
    """
    import numpy
    import progressbar
    # import spam.DIC.deformationFunction
    #import spam.mesh.strain

    # Define dimensions
    dims = list(displacementField.shape[0:3])
    nCells = [n - 1 for n in dims]

    # Check if a 2D field is passed
    if dims[0] == 1:
        # Add a ficticious layer of nodes and cells in Z direction
        dims[0] += 1
        nCells[0] += 1
        nodeSpacing[0] += 1

        # Add a ficticious layer of equal displacements so that the strain in z is null
        displacementField = numpy.concatenate((displacementField, displacementField))

    # Transformation gradient tensor F = du/dx +I
    Ffield = numpy.zeros((nCells[0], nCells[1], nCells[2], 3, 3))

    # Define the coordinates of the Parent Element
    # we're using isoparametric Q8 elements
    lid = numpy.zeros((8, 3)).astype('<u1')  # local index
    lid[0] = [0, 0, 0]
    lid[1] = [0, 0, 1]
    lid[2] = [0, 1, 0]
    lid[3] = [0, 1, 1]
    lid[4] = [1, 0, 0]
    lid[5] = [1, 0, 1]
    lid[6] = [1, 1, 0]
    lid[7] = [1, 1, 1]

    # Calculate the derivatives of the shape functions
    # Since the center is equidistant from all 8 nodes, each one gets equal weighting
    SFderivative = numpy.zeros((8, 3))
    for node in range(8):
        # (local nodes coordinates) / weighting of each node
        SFderivative[node, 0] = (2.0 * (float(lid[node, 0]) - 0.5)) / 8.0
        SFderivative[node, 1] = (2.0 * (float(lid[node, 1]) - 0.5)) / 8.0
        SFderivative[node, 2] = (2.0 * (float(lid[node, 2]) - 0.5)) / 8.0

    # Compute the jacobian to go from local(Parent Element) to global base
    jacZ = 2.0 / float(nodeSpacing[0])
    jacY = 2.0 / float(nodeSpacing[1])
    jacX = 2.0 / float(nodeSpacing[2])

    bar = progressbar.ProgressBar(maxval=nCells[0]*nCells[1]*nCells[2]).start()
    nodesDone = 0

    # Loop over the cells
    for kCell in range(nCells[0]):
        for jCell in range(nCells[1]):
            for iCell in range(nCells[2]):
                # Check for nans in one of the 8 nodes of the cell
                dCell = displacementField[kCell:kCell + 2, jCell:jCell + 2, iCell:iCell + 2]
                if not numpy.all(numpy.isfinite(dCell)):
                    Ffield[kCell, jCell, iCell, :, :] = numpy.zeros((3, 3)) * numpy.nan

                # If no nans start the strain calculation
                else:
                    # Initialise the gradient of the displacement tensor
                    dudx = numpy.zeros((3, 3))

                    # Loop over each node of the cell
                    for node in range(8):
                        # Get the displacement value
                        d = displacementField[int(kCell + lid[node, 0]), int(jCell + lid[node, 1]), int(iCell + lid[node, 2]), :]

                        # Compute the influence of each node to the displacement gradient tensor
                        dudx[0, 0] += jacZ * SFderivative[node, 0] * d[0]
                        dudx[1, 1] += jacY * SFderivative[node, 1] * d[1]
                        dudx[2, 2] += jacX * SFderivative[node, 2] * d[2]
                        dudx[1, 0] += jacY * SFderivative[node, 1] * d[0]
                        dudx[0, 1] += jacZ * SFderivative[node, 0] * d[1]
                        dudx[2, 1] += jacX * SFderivative[node, 2] * d[1]
                        dudx[1, 2] += jacY * SFderivative[node, 1] * d[2]
                        dudx[2, 0] += jacX * SFderivative[node, 2] * d[0]
                        dudx[0, 2] += jacZ * SFderivative[node, 0] * d[2]

                    Ffield[kCell, jCell, iCell, :, :] = numpy.eye(3)+dudx
                bar.update(nodesDone)
                nodesDone += 1
    bar.finish()
    return Ffield

def FfieldRegularGeers(displacementField, nodeSpacing, neighbourRadius=1.5, mask=True, bruteForceDistance=False):
    """
    This function computes the transformation gradient field F from a given displacement field.
    Please note: the transformation gradient tensor: F = I + du/dx.

    This function computes du/dx as a weighted function of neighbouring points.
    Here is implemented the linear model proposed in:
        "Computing strain fields from discrete displacement fields in 2D-solids", Geers et al., 1996

    Parameters
    ----------
        displacementField : 4D array of floats
            The vector field to compute the derivatives.
            Its shape is (nz, ny, nx, 3).

        nodeSpacing : 3-component list of floats
            Length between two nodes in every direction (*i.e.,* size of a cell)

        neighbourRadius : float, optional
            Distance in nodeSpacings to include neighbours in the strain calcuation.
            Default = 1.5*nodeSpacing which will give radius = 1.5*min(nodeSpacing)

        mask : bool, optional
            Avoid non-correlated NaN points in the displacement field?
            Default = True

        bruteForceDistance : bool, optional
            Use scipy.spatial.KDtree.query_ball_point to obtain neighbours (bruteForceDistance=False),
            or explicitly compute distance to each point (bruteForceDistance=True).
            Default = False

    Returns
    -------
        Ffield: nz x ny x nx x 3x3 array of n cells
            The field of the transformation gradient tensors

    Note
    ----
        Taken from the implementation in "TomoWarp2: A local digital volume correlation code", Tudisco et al., 2017
    """
    import numpy
    import progressbar
    import scipy.spatial
    pbar = progressbar.ProgressBar()

    #Define dimensions
    dims = displacementField.shape[0:3]
    nNodes = dims[0]*dims[1]*dims[2]
    displacementFieldFlat = displacementField.reshape(nNodes, 3)

    #Deformation gradient tensor F = du/dx +I
    Ffield = numpy.zeros((dims[0], dims[1], dims[2], 3, 3))
    FfieldFlat = numpy.zeros((nNodes, 3, 3))

    #Define field coordinates for KD-tree distance calculation, warning, the top point is at zero
    fieldCoordsFlat = numpy.mgrid[0:dims[0],0:dims[1],0:dims[2]].reshape(3, nNodes).T*nodeSpacing
    fieldCoordsFlat = numpy.mgrid[nodeSpacing[0]:dims[0]*nodeSpacing[0]+nodeSpacing[0]:nodeSpacing[0],
                                  nodeSpacing[1]:dims[1]*nodeSpacing[1]+nodeSpacing[1]:nodeSpacing[1],
                                  nodeSpacing[2]:dims[2]*nodeSpacing[2]+nodeSpacing[2]:nodeSpacing[2]].reshape(3, nNodes).T

    #Get non-nan displacements
    if mask:
        goodPointsMask = numpy.isfinite(displacementField[:,:,:,0].reshape(nNodes))
        badPointsMask  = numpy.isnan(   displacementField[:,:,:,0].reshape(nNodes))
        #Flattened variables
        fieldCoordsFlatGood       = fieldCoordsFlat[goodPointsMask]
        displacementFieldFlatGood = displacementFieldFlat[goodPointsMask]
        #set bad points to nan
        FfieldFlat[badPointsMask] = numpy.eye(3) * numpy.nan
    else:
        #Flattened variables
        fieldCoordsFlatGood       = fieldCoordsFlat
        displacementFieldFlatGood = displacementFieldFlat

    #build KD-tree for neighbour identification
    treeCoord = scipy.spatial.KDTree(fieldCoordsFlatGood)

    FfieldFlatGood = numpy.zeros_like(FfieldFlat[goodPointsMask])
    #for n in pbar(range(nNodes)):
    for goodPoint in pbar(range(fieldCoordsFlatGood.shape[0])):
        #This is for the linear model, equation 15 in Geers
        centralNodePosition       = fieldCoordsFlatGood[goodPoint]
        centralNodeDisplacement   = displacementFieldFlatGood[goodPoint]
        sX0X0 = numpy.zeros((3,3))
        sX0Xt = numpy.zeros((3,3))
        m0    = numpy.zeros((3))
        mt    = numpy.zeros((3))

        if bruteForceDistance:
            ## Option 1: Manual calculation of distance
            ## superslow alternative to KDtree
            distances = numpy.sqrt(numpy.sum(numpy.square(fieldCoordsFlatGood - centralNodePosition), axis=1))
            ind = numpy.where(distances < neighbourRadius*max(nodeSpacing))[0]

        else:
            ## Option 2: KDTree on distance
            # KD-tree will always give the current point as zero-distance
            ind = treeCoord.query_ball_point(centralNodePosition, neighbourRadius*max(nodeSpacing))

        # We know that the current point will also be included, so remove it from the index list.
        ind = numpy.array(ind)
        ind = ind[ind != goodPoint]
        nNeighbours = len(ind)
        nodalRelativePositionsRef = numpy.zeros((nNeighbours, 3)) # Delta_X_0 in paper
        nodalRelativePositionsDef = numpy.zeros((nNeighbours, 3)) # Delta_X_t in paper

        for neighbour, i in enumerate(ind):
            # Relative position in reference configuration
            #                                         absolute position of this neighbour node
            #                                                                  minus abs position of central node
            nodalRelativePositionsRef[neighbour, :] = fieldCoordsFlatGood[i] - centralNodePosition

            # Relative position in deformed configuration (i.e., plus displacements)
            #                                         absolute position of this neighbour node
            #                                                                  plus displacement of this neighbour node
            #                                                                                                minus abs position of central node
            #                                                                                                                       minus displacement of central node
            nodalRelativePositionsDef[neighbour, :] = fieldCoordsFlatGood[i] + displacementFieldFlatGood[i] - centralNodePosition - centralNodeDisplacement

            for u in range(3):
                for v in range(3):
                    sX0X0[u, v] += nodalRelativePositionsRef[neighbour, u] * nodalRelativePositionsRef[neighbour, v]
                    sX0Xt[u, v] += nodalRelativePositionsRef[neighbour, u] * nodalRelativePositionsDef[neighbour, v]

            m0 += nodalRelativePositionsRef[neighbour, :]
            mt += nodalRelativePositionsDef[neighbour, :]

        sX0X0 = nNeighbours*sX0X0
        sX0Xt = nNeighbours*sX0Xt

        A = sX0X0 - numpy.dot(m0, m0)
        C = sX0Xt - numpy.dot(m0, mt)

        try:
            FfieldFlatGood[goodPoint] = numpy.dot(numpy.linalg.inv(A), C)

        except numpy.linalg.linalg.LinAlgError:
            pass
            #print("spam.deformation.deformationField.FfieldRegularGeers(): LinAlgError: A", A)

    FfieldFlat[goodPointsMask] = FfieldFlatGood
    return FfieldFlat.reshape(dims[0], dims[1], dims[2], 3, 3)

def FfieldBagi(points, connectivity, displacements):
    """
    Calculates transformation gradient function using Bagi's 1996 paper, especially equation 3 on page 174.
    Required inputs are connectivity matrix for tetrahedra (for example from spam.mesh.triangulate) and
    nodal positions in reference and deformed configurations.

    Parameters
    ----------
        points : m x 3 numpy array
            M Particles' points in reference configuration

        connectivity : n x 4 numpy array
            Delaunay triangulation connectivity generated by spam.mesh.triangulate for example

        displacements : m x 3 numpy array
            M Particles' displacement

    Returns
    -------
        Ffield: nx3x3 array of n cells
            The field of the transformation gradient tensors
    """
    from progressbar import ProgressBar
    import spam.mesh
    pbar = ProgressBar()

    Ffield = numpy.zeros([connectivity.shape[0], 3, 3], dtype='<f4')

    connectivity = connectivity.astype(numpy.uint)

    # define dimension
    D = 3.0

    # Import modules

    # Construct 4-list of 3-lists of combinations constituting a face of the tet
    combs = [[0, 1, 2],
             [1, 2, 3],
             [2, 3, 0],
             [0, 1, 3]]
    unode = [3, 0, 1, 2]

    # Precompute tetrahedron Volumes
    tetVolumes = spam.mesh.tetVolumes(points, connectivity)

    # Initialize arrays for tet strains
    # print("spam.mesh.bagiStrain(): Constructing strain from Delaunay and Displacements")

    # Loop through tetrahdra to get avec1, uPos1
    # for tet in range(connectivity.shape[0]):
    for tet in pbar(range(connectivity.shape[0])):
        # Get the list of IDs, centroids, center of tet
        tet_ids = connectivity[tet, :]
        # 2019-10-07 EA: Skip references to missing particles
        if max(tet_ids) >= points.shape[0]:
            print("spam.mesh.unstructured.bagiStrain(): this tet has node > points.shape[0], skipping")
            pass
        else:
            tetCoords = points[tet_ids, :]
            tetDisp = displacements[tet_ids, :]
            tetCen = numpy.average(tetCoords, axis=0)
            if numpy.isfinite(tetCoords).sum() + numpy.isfinite(tetDisp).sum() != 3*4*2:
                print("spam.mesh.unstructured.bagiStrain(): nans in position or displacement, skipping")
                # Compute strains
                Ffield[tet] = numpy.zeros((3,3))*numpy.nan
            else:
                # Loop through each face of tet to get avec, upos (Bagi, 1996, pg. 172)
                # aVec1 = numpy.zeros([4, 3], dtype='<f4')
                # uPos1 = numpy.zeros([4, 3], dtype='<f4')
                # uPos2 = numpy.zeros([4, 3], dtype='<f4')
                dudx = numpy.zeros((3, 3), dtype='<f4')

                for face in range(4):
                    faceNorm = numpy.cross(tetCoords[combs[face][0]] - tetCoords[combs[face][1]],
                                           tetCoords[combs[face][0]] - tetCoords[combs[face][2]])

                    # Get a norm vector to face point towards center of tet
                    faceCen = numpy.average(tetCoords[combs[face]], axis=0)
                    tmpnorm = faceNorm / (numpy.linalg.norm(faceNorm))
                    facetocen = tetCen - faceCen
                    if (numpy.dot(facetocen, tmpnorm) < 0):
                        tmpnorm = -tmpnorm

                    # Divide by 6 (1/3 for 1/Dimension; 1/2 for area from cross product)
                    # See first eqn., Bagi, 1996, pg. 172.
                    # aVec1[face] = tmpnorm*numpy.linalg.norm(faceNorm)/6

                    # Undeformed positions
                    # uPos1[face] = tetCoords[unode[face]]
                    # Deformed positions
                    # uPos2[face] = tetComs2[unode[face]]

                    dudx += numpy.tensordot(tetDisp[unode[face]], tmpnorm * numpy.linalg.norm(faceNorm) / 6, axes=0)

                dudx /= float(tetVolumes[tet])

                Ffield[tet] = numpy.eye(3) + dudx
    return Ffield


def decomposeFfield(Ffield, components, twoD=False):
    """
    This function takes in an F field (from either FfieldRegularQ8, FfieldRegularGeers, FfieldBagi) and
    returns fields of desired transformation components.

    Parameters
    ----------
        Ffield : multidimensional x 3 x 3 numpy array
            Spatial field of Fs

        components : list of strings
            These indicate the desired components consistent with spam.deformation.decomposeF or decomposePhi

        twoD : bool, optional
            Is the Ffield in 2D? This changes the strain calculation.
            Default = False

    Returns
    -------
        Dictionary containing appropriately reshaped fields of the transformation components requested.

        Keys:
            vol, dev, volss, devss are scalars
            r and z are 3-component vectors
            e and U are 3x3 tensors
    """
    import spam.deformation
    import progressbar
    pbar = progressbar.ProgressBar()
    # The last two are for the 3x3 F field
    fieldDimensions = Ffield.shape[0:-2]
    fieldRavelLength = numpy.prod(numpy.array(fieldDimensions))
    FfieldFlat = Ffield.reshape(fieldRavelLength, 3, 3)

    output = {}
    for component in components:
        output[component] = []

    # Iterate through flat field of Fs
    for n in pbar(range(FfieldFlat.shape[0])):
        F = FfieldFlat[n]
        decomposedF = spam.deformation.decomposeF(F, twoD=twoD)
        for component in components:
            output[component].append(decomposedF[component])

    # Reshape on the output
    for component in components:
        if component == 'vol' or component == 'dev' or component == 'volss' or component == 'devss':
            output[component] = numpy.array(output[component]).reshape(fieldDimensions)

        if component == 'r' or component == 'z':
            output[component] = numpy.array(output[component]).reshape(Ffield.shape[0:-1])

        if component == 'U' or component == 'e':
            output[component] = numpy.array(output[component]).reshape(Ffield.shape)

    return output


def correctPhiField(fileName=None, fieldCoords=None, fieldValues=None, fieldRS=None, fieldDPhi=None, fieldPSCC=None, fieldIT=None, fieldBinRatio=1.0, ignoreBadPoints=False, ignoreBackGround=False, correctBadPoints=False, deltaPhiNormMin=0.001, pixelSearchCCmin=0.98, nNeighbours=12, filterPoints=False, filterPointsRadius=3, verbose=False, saveFile=False, saveFileName=None):
    """
    This function corrects a field of deformation functions **Phi** calculated at a number of points.
    This is typically the output of the DICdiscrete and DICregularGrid clients.
    The correction is done based on the `returnStatus` and `deltaPhiNorm` of the correlated points.
    It takes as an input either a tsv file containing the result of the correlation or
    6 separate arrays:

        1 the coordinates of the points

        2 the PhiField

        3 the `returnStatus`

        4 the `deltaPhiNorm`

        5 the `PSCC`

        6 the `iterations`


    Parameters
    ----------
        fileName : string, optional
            name of the file

        fieldCoords : 2D array, optional
            nx3 array of n points coordinates (ZYX)
            centre where each deformation function **Phi** has been calculated

        fieldValues : 3D array, optional
            nx4x4 array of n points deformation functions

        fieldRS : 1D array, optional
            nx1 array of n points `returnStatus` from the correlation

        fieldDf : 1D array, optional
            nx1 array of n points `deltaPhiNorm` from the correlation

        fieldIT : 1D array, optional
            nx1 array of n points `iterations` from the correlation

        fieldPSCC : 1D array, optional
            nx1 array of n points `PScorrelationCoefficient` from the correlation

        fieldBinRatio : int, optional
            if the input field is referred to a binned version of the image
            *e.g.*, if `fieldBinRatio = 2` the fileName values have been calculated for an image half the size of what the returned PhiField is referring to.
            Default = 1.0

        ignoreBadPoints : bool, optional
            if True it will replace the **Phi** matrices of the badly correlated points with nans.
            Bad points are set according to `returnStatus` and `deltaPhiNorm` or `PSCC` of the correlation.
            Default = False

         ignoreBackGround : bool, optional
            if True it will replace the **Phi** matrices of the back ground points with nans.
            Back ground points are set according to `returnStatus` (<-4) of the correlation.
            Default = False

        correctBadPoints : bool, optional
            if True it will replace the **Phi** matrices of the badly correlated points with the weighted function of the k nearest good points.
            Bad points are set according to `returnStatus` and `deltaPhiNorm` or `PSCC` of the correlation
            The number of the nearest good neighbours can be defined (see `nNeighbours` below).
            Default = False

        deltaPhiNormMin: float, optional
            minimum value of subpixel change in Phi to consider a point with `returnStatus` = 1 as good or bad.
            Default = 0.001

        picelSearchCCmin: float, optional
            minimum value of pixel search correlation coefficient to consider a point as good or bad.
            Default = 0.98

        nNeighbours : int, optional
            if `correctBadPoints` is activated, it specifies the number of the nearest neighbours to consider.
            If == 1, the nearest neighbour is used, if >1 neighbours are weighted according to distance.
            Default = 12

        filterPoints : bool, optional
            if True: a median filter will be applied on the **Phi** of each point.
            Default = False

        filterPointsRadius : int, optional
            Radius of median filter.
            Size of cubic structuring element is 2*filterPointsRadius+1.
            Default = 3

        verbose : bool, optional
            follow the progress of the function.
            Default = False

        saveFile : bool, optional
            save the corrected file into a tsv
            Default = False

        saveFileName : string, optional
            The file name for output.
            Default = 'spam'

    Returns
    -------
        PhiField : nx4x4 array
            n points deformation functions **Phi** after the correction

    """
    import os
    # read the input arguments
    if fileName:
        if not os.path.isfile(fileName):
            print("\n\tdeformationFunction.correctPhiField():{} is not a file. Exiting.".format(fileName))
            return
        else:
            import spam.helpers.tsvio
            fi = spam.helpers.tsvio.readCorrelationTSV(fileName, fieldBinRatio=fieldBinRatio, readDisplacements=True, readFs=False, readConvergence=True, readPSCC=True)
            PhiField     = fi["PhiField"]
            fieldCoords  = fi["fieldCoords"]
            fieldDims    = fi["fieldDims"]
            RS           = fi["returnStatus"]
            deltaPhiNorm = fi["deltaPhiNorm"]
            iterations   = fi["iterations"]
            PSCC         = fi["PSCC"]
    elif fieldCoords is not None and fieldValues is not None and fieldRS is not None and fieldDPhi is not None and fieldPSCC is not None and fieldIT is not None:
        fieldCoords = fieldCoords
        fieldDims = numpy.array([len(numpy.unique(fieldCoords[:, 0])), len(numpy.unique(fieldCoords[:, 1])), len(numpy.unique(fieldCoords[:, 2]))])
        PhiField = fieldValues
        RS = fieldRS
        deltaPhiNorm = fieldDPhi
        PSCC = fieldPSCC
        iterations = fieldIT
    else:
        print("\tdeformationFunction.correctPhiField(): Not enough arguments given. Exiting.")
        return

    # check if it is a subPixel field or a pixel search field
    if numpy.nansum(PSCC) > 0 and iterations.sum() == 0:
        pixelSearch = True
        subPixel = False
    else:
        pixelSearch = False
        subPixel = True

    # define good and bad correlation points according to `returnStatus` and `deltaPhiNorm` or `PSCC`conditions
    if ignoreBackGround is False:
        if subPixel:
            goodPoints = numpy.where(numpy.logical_or(RS == 2, numpy.logical_and(RS == 1, deltaPhiNorm <= deltaPhiNormMin)))
            badPoints = numpy.where(numpy.logical_or(RS <= 0, numpy.logical_and(RS == 1, deltaPhiNorm > deltaPhiNormMin)))
        if pixelSearch:
            goodPoints = numpy.where(PSCC >= pixelSearchCCmin)
            badPoints = numpy.where(PSCC < pixelSearchCCmin)
    else:
        if subPixel:
            goodPoints = numpy.where(numpy.logical_or(RS == 2, numpy.logical_and(RS == 1, deltaPhiNorm <= deltaPhiNormMin)))
            badPoints = numpy.where(numpy.logical_or(numpy.logical_and(RS <= 0, RS >= -4), numpy.logical_and(RS == 1, deltaPhiNorm > deltaPhiNormMin)))
            backGroundPoints = numpy.where(RS < -4)
        if pixelSearch:
            goodPoints = numpy.where(numpy.logical_and(RS >= -4, PSCC >= pixelSearchCCmin))
            badPoints = numpy.where(numpy.logical_and(RS >= -4, PSCC < pixelSearchCCmin))
        backGroundPoints = numpy.where(RS < -4)
        PhiField[backGroundPoints] = numpy.nan

    # if asked, ignore the bad correlation points by setting their Phi to identity matrix
    if ignoreBadPoints:
        PhiField[badPoints] = numpy.eye(4) * numpy.nan

    # if asked, replace the bad correlation points with the weighted influence of the k nearest good neighbours
    if correctBadPoints:
        # create the k-d tree of the coordinates of good points, we need this to search for the k nearest neighbours easily
        #   for details see: https://en.wikipedia.org/wiki/K-d_tree &
        #   https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.spatial.KDTree.query.html

        from scipy.spatial import KDTree
        treeCoord = KDTree(fieldCoords[goodPoints])

        # extract the Phi matrices of the bad points
        fieldBad = numpy.zeros_like(PhiField[badPoints])
        fieldBad[:, -1, :] = numpy.array([0, 0, 0, 1])

        # check if we have asked only for the closest neighbour
        if nNeighbours == 1:

            # loop over each bad point
            for badPoint in range(badPoints[0].shape[0]):
                if verbose:
                    print("\rWorking on bad point: {} of {}".format(badPoint + 1, badPoints[0].shape[0]), end='')
                # call tree.query to calculate:
                #   {ind}: the index of the nearest neighbour (as neighbours we consider only good points)
                #   {distnace}: distance (Minkowski norm 2, which is  the usual Euclidean distance) of the bad point to the nearest neighbour
                distance, ind = treeCoord.query(fieldCoords[badPoints][badPoint], k=nNeighbours)

                # replace bad point's Phi with the Phi of the nearest good point
                fieldBad[badPoint][:-1] = PhiField[goodPoints][ind][:-1].copy()

            # replace the corrected Phi field
            PhiField[badPoints] = fieldBad

        # if we have asked for more neighbours
        else:

            # loop over each bad point
            for badPoint in range(badPoints[0].shape[0]):
                if verbose:
                    print("\rWorking on bad point: {} of {}".format(badPoint + 1, badPoints[0].shape[0]), end='')
                # call tree.query to calculate:
                #   {ind}: k nearest neighbours (as neighbours we consider only good points)
                #   {distnace}: distance (Minkowski norm 2, which is  the usual Euclidean distance) of the bad point to each of the ith nearest neighbour
                distance, ind = treeCoord.query(fieldCoords[badPoints][badPoint], k=nNeighbours)

                # compute the "Inverse Distance Weighting" since the nearest points should have the major influence
                weightSumInv = sum(1 / distance)

                # loop over each good neighbour point:
                for neighbour in range(nNeighbours):
                    # calculate its weight
                    weightInv = (1 / distance[neighbour]) / float(weightSumInv)

                    # replace the Phi components of the bad point with the weighted Phi components of the ith nearest good neighbour
                    fieldBad[badPoint][:-1] += PhiField[goodPoints][ind[neighbour]][:-1] * weightInv

            # replace the corrected Phi field
            PhiField[badPoints] = fieldBad
        # overwrite RS to the corrected
        RS[badPoints] = 2

    # if asked, apply a median filter of a specific size in the Phi field
    if filterPoints:
        if verbose:
            print("\nFiltering...")
        import scipy.ndimage
        filterPointsRadius = int(filterPointsRadius)

        PhiField[:, 0, 0] = scipy.ndimage.generic_filter(PhiField[:, 0, 0].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()
        PhiField[:, 1, 0] = scipy.ndimage.generic_filter(PhiField[:, 1, 0].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()
        PhiField[:, 2, 0] = scipy.ndimage.generic_filter(PhiField[:, 2, 0].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()

        PhiField[:, 0, 1] = scipy.ndimage.generic_filter(PhiField[:, 0, 1].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()
        PhiField[:, 1, 1] = scipy.ndimage.generic_filter(PhiField[:, 1, 1].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()
        PhiField[:, 2, 1] = scipy.ndimage.generic_filter(PhiField[:, 2, 1].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()

        PhiField[:, 0, 2] = scipy.ndimage.generic_filter(PhiField[:, 0, 2].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()
        PhiField[:, 1, 2] = scipy.ndimage.generic_filter(PhiField[:, 1, 2].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()
        PhiField[:, 2, 2] = scipy.ndimage.generic_filter(PhiField[:, 2, 2].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()

        PhiField[:, 0, -1] = scipy.ndimage.generic_filter(PhiField[:, 0, -1].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()
        PhiField[:, 1, -1] = scipy.ndimage.generic_filter(PhiField[:, 1, -1].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()
        PhiField[:, 2, -1] = scipy.ndimage.generic_filter(PhiField[:, 2, -1].reshape(fieldDims), numpy.nanmedian, size=(2 * filterPointsRadius + 1)).ravel()

        if ignoreBackGround:
            PhiField[backGroundPoints] = numpy.nan

    if saveFile:
        # if asked, write the corrected PhiField into a TSV
        if fileName:
            outDir = os.path.dirname(fileName)
            prefix = os.path.splitext(os.path.basename(fileName))[0]
            saveFileName = outDir+"/"+prefix
        elif saveFileName is None and fileName is None:
            saveFileName = "spam"

        TSVheader = "NodeNumber\tZpos\tYpos\tXpos\tF11\tF12\tF13\tZdisp\tF21\tF22\tF23\tYdisp\tF31\tF32\tF33\tXdisp\treturnStatus\tdeltaPhiNorm\titerations\tPSCC"
        outMatrix = numpy.array([numpy.array(range(PhiField.shape[0])),
                                 fieldCoords[:, 0], fieldCoords[:, 1], fieldCoords[:, 2],
                                 PhiField[:, 0, 0], PhiField[:, 0, 1], PhiField[:, 0, 2], PhiField[:, 0, 3],
                                 PhiField[:, 1, 0], PhiField[:, 1, 1], PhiField[:, 1, 2], PhiField[:, 1, 3],
                                 PhiField[:, 2, 0], PhiField[:, 2, 1], PhiField[:, 2, 2], PhiField[:, 2, 3],
                                 RS, deltaPhiNorm, iterations, PSCC]).T

        if filterPoints:
            title = "{}-corrected-N{}-filteredRad{}.tsv".format(saveFileName, nNeighbours, filterPointsRadius)
        else:
            title = "{}-corrected-N{}.tsv".format(saveFileName, nNeighbours)
        numpy.savetxt(title,
                      outMatrix,
                      fmt='%.7f',
                      delimiter='\t',
                      newline='\n',
                      comments='',
                      header=TSVheader)

    return PhiField


def mergeRegularGridAndDiscrete(fileNameRegularGrid=None, fileNameDiscrete=None, labelled=None, binningLabelled=1, alwaysLabel=True, saveFileName=None):
    """
    This function merges displacement fields from the DICregularGrid script and
    the DICdiscrete script.
    This can be useful where there are large flat zones in the image that cannot
    be correlated with small correlation windows, but can be identified and
    tracked with a DICdiscrete computation.

    Parameters
    -----------
        fileNameRegularGrid : string
            File name of TSV from DICregularGrid client.
            Default = None

        fileNameDiscrete : string
            File name of TSV from DICdiscrete client, or list of filenames
            Default = None

        labelled : 3D numpy array of ints, or list of numpy arrays
            Labelled volume used for discrete computation
            Default = None

        alwaysLabel : bool
            If regularGrid point falls inside the label, should we use the
            label displacement automatically?
            Otherwise if the reggularGrid point has converged should we use that?
            Default = True (always use Label displacement)

        saveFileName : string
            Output filename
            Default = None

    Returns
    --------
        Output matrix, with number of rows equal to DICregularGrid with columns:
            "NodeNumber", "Zpos", "Ypos", "Xpos", "Zdisp", "Ydisp", "Xdisp", "deltaPhiNorm", "returnStatus", "iterations"
    """
    import spam.helpers

    regGrid = spam.helpers.readCorrelationTSV(fileNameRegularGrid)

    # If we have a list of input discrete files, we also need a list of labelled images
    if type(fileNameDiscrete) == list:
        if type(labelled) != list:
            print("spam.DIC.deformationFunction.mergeRegularGridAndDiscrete(): if you pass a list of discreteTSV you must also pass a list of labelled images")
            return 0
        if len(fileNameDiscrete) != len(labelled):
            print("spam.DIC.deformationFunction.mergeRegularGridAndDiscrete(): len(fileNameDiscrete) must be equal to len(labelled)")
            return 0

        # OK we have lists of both, let's load the series of discrete TSVs
        discrete = []
        for fn in fileNameDiscrete:
            discrete.append(spam.helpers.readCorrelationTSV(fn))
        nDiscrete = len(fileNameDiscrete)

    # We have only one TSV and labelled image, it should be a number array
    else:
        if type(labelled) != numpy.ndarray:
            print("spam.DIC.deformationFunction.mergeRegularGridAndDiscrete(): with a single discrete TSV file, labelled must be a numpy array")
            return 0
        discrete = [spam.helpers.readCorrelationTSV(fileNameDiscrete)]
        labelled = [labelled]
        nDiscrete = 1

    # 2019-11-11 EA: Add extra column for which field it came from
    output = numpy.zeros([regGrid['fieldCoords'].shape[0], 11])

    # from progressbar import ProgressBar
    # pbar = ProgressBar()

    # For each point on the regular grid...
    # for n, gridPoint in pbar(enumerate(regGrid['fieldCoords'].astype(int))):
    for n, gridPoint in enumerate(regGrid['fieldCoords'].astype(int)):
        # Find labels corresponding to this grid position for the labelled images
        labels = []
        for m in range(nDiscrete):
            labels.append(int(labelled[m][int(gridPoint[0] / float(binningLabelled)), int(gridPoint[1] / float(binningLabelled)), int(gridPoint[2] / (binningLabelled))]))
        labels = numpy.array(labels)

        # First column is point number
        output[n, 0] = n

        # Next three columns are the position of the regular grid point
        output[n, 1:4] = gridPoint

        # Is the point inside a discrete label?
        if (labels == 0).all() or (not alwaysLabel and regGrid['returnStatus'][n] == 2):
            # If we're not in a label, copy the results from DICregularGrid
            output[n, 4:7] = regGrid['PhiField'][n][0:3, -1]
            output[n, 7] = regGrid['deltaPhiNorm'][n]
            output[n, 8] = regGrid['returnStatus'][n]
            output[n, 9] = regGrid['iterations'][n]
        else:
            # Give precedence to earliest non-zero-labelled discrete field, conflicts not handled
            m = numpy.where(labels != 0)[0][0]
            label = labels[m]
            #print("m,label = ", m, label)
            phi = discrete[m]['PhiField'][label].copy()
            phi[0:3, -1] *= float(binningLabelled)
            output[n, 4:7] = spam.DIC.decomposePhi(phi, PhiCentre=discrete[m]['fieldCoords'][label] * float(binningLabelled), PhiPoint=gridPoint)['t']
            output[n, 7] = discrete[m]['deltaPhiNorm'][label]
            output[n, 8] = discrete[m]['returnStatus'][label]
            output[n, 9] = discrete[m]['iterations'][label]
            output[n, 10] = m

    # displacements = output[:,4:7].reshape([regGrid['fieldDims'][0],
                # regGrid['fieldDims'][1],
                # regGrid['fieldDims'][2],
                # 3])

    # plt.imshow( displacements[:,24,:,0], vmin=0, vmax=3, cmap='plasma'); plt.show()

    if saveFileName is not None:
        numpy.savetxt(saveFileName,
                      output,
                      header="NodeNumber\tZpos\tYpos\tXpos\tZdisp\tYdisp\tXdisp\tdeltaPhiNorm\treturnStatus\titerations\tmergeSource",
                      delimiter="\t")

    return output, regGrid['fieldDims']


def interpolateFfield(fieldCoords, fieldValues, interpCoords, fieldInterpBinRatio=1):
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

        dims = [int(1 + (zUnique[-1] - zUnique[0]) / zSpacing),
                  int(1 + (yUnique[-1] - yUnique[0]) / ySpacing),
                  int(1 + (xUnique[-1] - xUnique[0]) / xSpacing)]
    else:
        print("Not all node spacings are the same, help! {} {} {} ".format(
            zSpacing, ySpacing, xSpacing))
        return "moinsUn"

    # 2. reshape fieldValues into an Z*Y*X*Phiy*Phix array for map_coordinates
    fieldValues = fieldValues.reshape([dims[0], dims[1], dims[2], 4, 4])

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

