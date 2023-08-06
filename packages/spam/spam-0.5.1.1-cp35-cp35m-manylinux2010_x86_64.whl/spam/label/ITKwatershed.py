"""
Library of wrapper functions for Simple ITK
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
import tifffile
import sys
import os
import SimpleITK
import spam.label


#if sys.version_info >= (3, 0):
    #def xrange(*args, **kwargs):
        #return iter(range(*args, **kwargs))

"""
Classes binding ITK morphological watershed algorithm implementation

Note:
Author is Olumide Okubadejo
"""

class _MWatershed(object):
    def __init__(self, data, level=1, watershedLineOn=False, fullyConnected=True, fromMarkers=False, markerImage=None):
        self._level = level
        self._watershedLineOn = watershedLineOn
        self._fullyConnected = fullyConnected
        self._data = SimpleITK.GetImageFromArray(data)
        self._fromMarkers = fromMarkers
        if fromMarkers:
            self._markerImage = SimpleITK.GetImageFromArray(markerImage)

    #def _CalculateGradient(self):
        #gradient = SimpleITK.GradientMagnitudeImageFilter()
        #self._gradient = gradient.Execute(self._bdata)

    def _Binarize(self):
        threshold = SimpleITK.OtsuThresholdImageFilter()
        self._bdata = threshold.Execute(self._data)
        self._bdata = self._Rescale(self._bdata)
        self._threshold = threshold.GetThreshold()

    def _Rescale(self, data):
        rescale = SimpleITK.RescaleIntensityImageFilter()
        return rescale.Execute(data, 0, 65535)

    def _DistanceMap(self):
        distanceMap = SimpleITK.DanielssonDistanceMapImageFilter()
        self._distance = distanceMap.Execute(self._bdata)
        pass

    def _InvertImage(self, data):
        invert = SimpleITK.InvertIntensityImageFilter()
        inverted = invert.Execute(data)
        return inverted

    def _MaskImage(self):
        mask = SimpleITK.MaskImageFilter()
        self._mask = mask.Execute(self._labelImage, self._bdata)

    def _FillHoles(self):
        fill = SimpleITK.BinaryFillholeImageFilter()
        self._bdata = fill.Execute(self._bdata)

    def _LabelOverlay(self):
        overlay = SimpleITK.LabelOverlayImageFilter()
        self._overlay = overlay.Execute(self._bdata, self._mask)

    def _Watershed(self):
        if (self._fromMarkers):
            watershed = SimpleITK.MorphologicalWatershedFromMarkersImageFilter()
        else:
            watershed = SimpleITK.MorphologicalWatershedImageFilter()
        watershed.SetFullyConnected(self._fullyConnected)
        watershed.SetMarkWatershedLine(self._watershedLineOn)

        if (self._fromMarkers):
            self._labelImage = watershed.Execute(
                self._distance, self._markerImage)
        else:
            watershed.SetLevel(self._level)
            self._labelImage = watershed.Execute(self._distance)

    #def GetThreshold(self):
        #return self._threshold

    #def GetLabeledImage(self):
        #return SimpleITK.GetArrayFromImage(self._mask)

    #def GetITKLabeledImage(self):
        #return self._labelImage

    #def GetColorMap(self):
        #return SimpleITK.GetArrayFromImage(self._overlay)

    #def GetBinaryImage(self):
        #return SimpleITK.GetArrayFromImage(self._bdata)

    #def GetDistanceMapImage(self):
        #return SimpleITK.GetArrayFromImage(self._distance)

    def GetMaskImage(self):
        return SimpleITK.GetArrayFromImage(self._mask)

    #def GetLabelParams(self):
        #return self._labelParams.GetLabels()

    #def GetLabelObject(self):
        #return self._labelParams

    #def GetRadiusArray(self):
        #return self._labelParams.GetRadiusArray()

    def run(self):
        self._Binarize()
        # self._bdata = self._InvertImage(self._bdata)
        self._FillHoles()
        self._DistanceMap()
        self._distance = self._InvertImage(self._distance)
        self._Watershed()
        self._bdata = self._InvertImage(self._bdata)
        self._MaskImage()
        self._LabelOverlay()
        #self._labelParams = _Labels(self._data, self._labelImage)
        return SimpleITK.GetArrayFromImage(self._overlay)


def watershed(binary, markers=None, verbose = False):
    """
    This function runs an ITK watershed on a binary image and returns a labelled image.
    This function uses an interpixel watershed.

    Parameters
    -----------
        binary : 3D numpy array
            This image which is non-zero in the areas which should be split by the watershed algorithm

        markers : 3D numpy array (optional, default = None)
            Not implemented yet, but try!

	verbose : boolean (optional, default = False)
	        True for printing the evolution of process
	        False for not printing the evolution of process

    Returns
    --------
        labelled : 3D numpy array of ints
            3D array where each object is numbered
    """
    binary = binary > 0

    # Let's convert it 8-bit
    binary = binary.astype('<u1') * 255

    if markers is not None:
        if verbose:
            print("\tITKwatershed.watershed(): Running watershed with your markers...", end='')
        if markers.max() > 65535: markers = markers.astype('<u4')
        else:                     markers = markers.astype('<u2')

        mWatershed = _MWatershed(binary, markerImage=markers.astype(spam.label.labelType), fromMarkers=True,
                                 level=1, watershedLineOn=False, fullyConnected=True)
    else:
        if verbose:
            print("\tITKwatershed.watershed(): Running watershed...", end='')
        mWatershed = _MWatershed(
            binary, level=1, watershedLineOn=False, fullyConnected=True)
    labels = mWatershed.run()
    if verbose:
        print("done.")
    if verbose:
        print("\tITKwatershed.watershed(): Collecting labelled image...", end='')
    lab = mWatershed.GetMaskImage().astype('<u4')
    if verbose:
        print("done.")

    return lab
