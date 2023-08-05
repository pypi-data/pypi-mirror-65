"""
Library of SPAM morphological functions.
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

import numpy
import spam.helpers
import multiprocessing
import progressbar
import spam.label.label
import scipy.ndimage
# operations on greyscale images

def greyDilation(im, nBytes=1):
    """
    This function apply a dilation on a grey scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        nBytes: int, default=1
            Number of bytes used to substitute the values on the border.

    Returns
    --------
        numpy array
            The dilated image
    """
    # Step 1: check type and dimension
    dim = len(im.shape)
    # Step 2: Determine substitution value
    sub = 2**(8 * nBytes) - 1
    # Step 3: apply dilation                                                          #  x  y  z
    outputIm = im                                                                     # +0  0  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, 1, 0, sub=sub))   # +1  0  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, -1, 0, sub=sub))  # -1  0  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, 1, 1, sub=sub))   # +0  1  0
    outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, -1, 1, sub=sub))  # +0 -1  0
    if dim == 3:
        outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, 1, 2, sub=sub))   # 0  0  1
        outputIm = numpy.maximum(outputIm, spam.helpers.singleShift(im, -1, 2, sub=sub))  # 0  0 -1
    return outputIm


def greyErosion(im, nBytes=1):
    """
    This function apply a erosion on a grey scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        nBytes: int, default=1
            Number of bytes used to substitute the values on the border.

    Returns
    --------
        numpy array
            The eroded image
    """
    # Step 1: check type and dimension
    dim = len(im.shape)
    # Step 2: Determine substitution value
    sub = 2**(8 * nBytes) - 1
    # Step 1: apply erosion                                                       #  x  y  z
    outputIm = im  # 0  0  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, 1, 0, sub=sub))  # 1  0  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, -1, 0, sub=sub))  # -1  0  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, 1, 1, sub=sub))  # 0  1  0
    outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, -1, 1, sub=sub))  # 0 -1  0
    if dim == 3:
        outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, 1, 2, sub=sub))  # 0  0  1
        outputIm = numpy.minimum(outputIm, spam.helpers.singleShift(im, -1, 2, sub=sub))  # 0  0 -1
    return outputIm


def greyMorphologicalGradient(im, nBytes=1):
    """
    This function apply a morphological gradient on a grey scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        nBytes: int, default=1
            Number of bytes used to substitute the values on the border.

    Returns
    --------
        numpy array
            The morphologycal gradient of the image
    """
    return (greyDilation(im, nBytes=nBytes) - im)


# operation on binary images

def binaryDilation(im, sub=False):
    """
    This function apply a dilation on a binary scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        sub: bool, default=False
            Subtitute value.

    Returns
    --------
        numpy array
            The dilated image
    """
    # Step 0: import as bool
    im = im.astype(bool)
    # Step 1: check type and dimension
    dim = len(im.shape)
    # Step 1: apply dilation                             #  x  y  z
    outputIm = im  # 0  0  0
    outputIm = outputIm | spam.helpers.singleShift(im, 1, 0, sub=sub)  # 1  0  0
    outputIm = outputIm | spam.helpers.singleShift(im, -1, 0, sub=sub)   # -1  0  0
    outputIm = outputIm | spam.helpers.singleShift(im, 1, 1, sub=sub)  # 0  1  0
    outputIm = outputIm | spam.helpers.singleShift(im, -1, 1, sub=sub)  # 0 -1  0
    if dim == 3:
        outputIm = outputIm | spam.helpers.singleShift(im, 1, 2, sub=sub)  # 0  0  1
        outputIm = outputIm | spam.helpers.singleShift(im, -1, 2, sub=sub)  # 0  0 -1
    return numpy.array(outputIm).astype('<u1')


def binaryErosion(im, sub=False):
    """
    This function apply a erosion on a binary scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        sub: bool, default=False
            Subtitute value.

    Returns
    --------
        numpy array
            The eroded image
    """
    # Step 1: apply erosion with dilation --> erosion = ! dilation( ! image )
    return numpy.logical_not(binaryDilation(numpy.logical_not(im), sub=sub)).astype('<u1')


def binaryMorphologicalGradient(im, sub=False):
    """
    This function apply a morphological gradient on a binary scale image

    Parameters
    -----------
        im: numpy array
            The input image (greyscale)
        nBytes: int, default=False
            Number of bytes used to substitute the values on the border.

    Returns
    --------
        numpy array
            The morphologycal gradient of the image
    """
    return (numpy.logical_xor(binaryDilation(im, sub=sub), im)).astype('<u1')


# def _binary_reconstruction_from_edges(im, dmax=0):
#     """
#     Calculate the morphological reconstruction of an image (binary) with the edges of a CUBE as a marker!
#     PARAMETERS:
#     - im (3D numpy.array): The input image (binary)
#     - dmax (int): the maximum geodesic distance. If zero, the reconstruction is complete.
#     RETURNS:
#     - (3D numpy.array): The reconstructed image
#     TODO:
#     - Consider mask for other geometry than cube
#     #- Consider different marker than the edges (for example, two opposite faces for percolation test)
#     HISTORY:
#     2016-04-21 (Sun Yue): First version of the function
#     """
#     # Step 1: compute marker
#     size = im.shape[0]
#     bord = numpy.zeros((size, size, size), dtype=bool)
#     bord[0, :, :] = im[0, :, :]
#     bord[-1, :, :] = im[-1, :, :]
#     bord[:, 0, :] = im[:, 0, :]
#     bord[:, -1, :] = im[:, -1, :]
#     bord[:, :, 0] = im[:, :, 0]
#     bord[:, :, -1] = im[:, :, -1]
#
#     # Step 2: first dilation and intersection
#     temp1 = (binaryDilation(bord)) & (im)
#     temp2 = temp1
#     temp1 = (binaryDilation(temp2)) & (im)
#     distance = 1
#
#     if dmax == 0:
#         dmax = 1e99  # perform complete reconstruction
#     while ((not(numpy.array_equal(temp1, temp2))) & (distance < dmax)):
#         temp2 = temp1
#         temp1 = (binaryDilation(temp2)) & (im)
#         distance += 1
#         print('distance =', distance)
#
#     return temp1  # send the reconstructed image


def binaryReconstructionFromEdges(im, dmax=None, verbose=False):
    """
    Calculate the morphological reconstruction of an binary image with the edges of a cube as a marker

    Parameters
    -----------
        im: numpy array
            The input image
        dmax: int, default=None
            The maximum geodesic distance. If None, the reconstruction is complete.
        verbose: bool, default=False
            Verbose mode

    Returns
    --------
        numpy.array
            The reconstructed image
    """
    size = im.shape[0]
    bord = numpy.zeros((size, size, size), dtype=bool)
    bord[0, :, :] = im[0, :, :]
    bord[-1, :, :] = im[-1, :, :]
    bord[:, 0, :] = im[:, 0, :]
    bord[:, -1, :] = im[:, -1, :]
    bord[:, :, 0] = im[:, :, 0]
    bord[:, :, -1] = im[:, :, -1]

    # Step 2: first dilation and intersection
    rec1 = (binaryDilation(bord)) & (im)
    rec2 = rec1
    rec1 = (binaryDilation(rec2)) & (im)
    distance = 1

    if dmax is None:
        dmax = numpy.inf  # perform complete reconstruction
    while ((not(numpy.array_equal(rec1, rec2))) & (distance < dmax)):
        rec2 = rec1
        rec1 = (binaryDilation(rec2)) & (im)
        distance += 1
        if verbose:
            print('Distance = {}'.format(distance))

    return rec1  # send the reconstructed image


def reconstructionFromOppositeFaces(im, dmax=None, verbose=False):
    """
    Calculate the morphological reconstruction of an binary image with two opposite faces of a cube as a marker

    Parameters
    -----------
        im: numpy array
            The input image
        dmax: int, default=None
            The maximum geodesic distance. If None, the reconstruction is complete.
        verbose: bool, default=False
            Verbose mode

    Returns
    --------
        numpy.array
            The reconstructed image
    """
    # Step 1: compute marker
    size = im.shape[0]
    bord = numpy.zeros((size, size, size), dtype=bool)
    bord[0, :, :] = im[0, :, :]
    bord[-1, :, :] = im[-1, :, :]

    # Step 2: first dilation and intersection
    rec1 = (binaryDilation(bord)) & (im)
    rec2 = rec1
    rec1 = (binaryDilation(rec2)) & (im)
    distance = 1

    if dmax is None:
        dmax = numpy.inf  # perform complete reconstruction
    while ((not(numpy.array_equal(rec1, rec2))) & (distance < dmax)):
        rec2 = rec1
        rec1 = (binaryDilation(rec2)) & (im)
        distance += 1
        if verbose:
            print('Distance =', distance)

    return rec1  # send the reconstructed image

def directionalErosion(bwIm, vect, a, c, NumberOfThreads=1, verbose = False):
    """
    This functions performs direction erosion over the binarized image using
    an ellipsoidal structuring element over a range of directions. It is 
    recommended that the structuring element is slightly smaller than the expected particle
    
    Parameters
    -----------
        bwIm : 3D numpy array
            Binarized image to perform the erosion
            
        vect : list of n elements, each element correspond to a 1X3 array of floats
            List of directional vectors for the structuring element
        
        a : int or float
            Length of the secondary semi-axis of the structuring element in px
            
        c : int or float
            Lenght of the principal semi-axis of the structuring element in px
            
        NumberOfThreads : integer, optional
            Number of Threads for multiprocessing.
            Default = 1

        verbose : boolean, optional (Default = False)
            True for printing the evolution of the process
            False for not printing the evolution of process

    Returns
    --------
        imEroded : 3D boolean array
            Booean array with the result of the erosion

    Note
    -----
        Taken from https://sbrisard.github.io/posts/20150930-orientation_correlations_among_rice_grains-06.html
        
    """
    
    
    #Check if the directional vector input is a list
    if isinstance(vect,list) == False:
        print("spam.contacts.directionalErosion: The directional vector must be a list")
        return
        
    numberOfJobs = len( vect )
    imEroded = numpy.zeros(bwIm.shape)
    
    def worker( workerNumber, qJobs, qResults ):
        while True:
            job = qJobs.get()

            if job == "STOP":
                qResults.put("STOP")
                break
            
            spheroid = spam.label.label.Spheroid(a, c, numpy.asarray(vect[job])).digitize()
            imEroded_i = scipy.ndimage.binary_erosion(bwIm, structure = spheroid)
            
            qResults.put( [imEroded_i])
            
            
    qJobs = multiprocessing.Queue()
    qResults = multiprocessing.Queue()
    
    # print "Master: Adding jobs to queues"
    for x in range(numberOfJobs):
        # qJobs.put( contactList[x,0] )
        qJobs.put(x)
    
    for i in range(NumberOfThreads):
        qJobs.put("STOP")
        
    # print "Master: Launching workers"
    for i in range(NumberOfThreads):
        p = multiprocessing.Process(target=worker, args=(i, qJobs, qResults, ))
        p.start()
        
    if verbose:
        pbar = progressbar.ProgressBar(maxval=numberOfJobs).start()
    finishedThreads = 0
    finishedJobs = 0
    # print "Master: Waiting for results"
    while finishedThreads < NumberOfThreads:
        result = qResults.get()

        if result == "STOP":
            finishedThreads += 1
            #print("\tNumber of finished threads = ", finishedThreads)

        else:
            # print "Master: got {}".format( result )
            
            imEroded = imEroded + result[0]
            finishedJobs += 1
            if verbose:
                pbar.update(finishedJobs)
    if verbose:
        pbar.finish()

    return imEroded
