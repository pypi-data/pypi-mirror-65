"""
Library of SPAM functions for parsing inputs to the scripts
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

import argparse
import numpy
import os

# Nice str2bool suggestion from Maxim (https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse)

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

GLPv3descriptionHeader = "Copyright (C) 2020 SPAM developers\n"+\
                         "This program comes with ABSOLUTELY NO WARRANTY.\n"+\
                         "This is free software, and you are welcome to redistribute it under certain conditions\n\n\n"

def ldicParser(parser):
    parser.add_argument('-nompi',
                        action="store_false",
                        dest='MPI',
                        help='Force disactivate MPI? Only unse this if you cannot import mpi4py')

    parser.add_argument('inFiles',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help="A space-separated list of two 3D greyscale tiff files to correlate, in order")

    parser.add_argument('-mf1',
                        '--maskFile1',
                        dest='MASK1',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to tiff file containing the mask of image 1 -- masks zones not to correlate, which should be == 0")

    # parser.add_argument('-mf2',
    #                     '--maskFile2',
    #                     dest='MASK2',
    #                     default=None,
    #                     type=argparse.FileType('r'),
    #                     help="Path to tiff file containing the mask of image 2 -- masks correlation windows")

    parser.add_argument('-pf',
                        '-phiFile',
                        dest='PHIFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

    parser.add_argument('-pfb',
                        '--phiFile-bin-ratio',
                        type=int,
                        default=1,
                        dest='PHIFILE_BIN_RATIO',
                        help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    parser.add_argument('-glt',
                        '--grey-low-threshold',
                        type=float,
                        default=-numpy.inf,
                        dest='GREY_LOW_THRESH',
                        help="Grey threshold on mean of reference imagette BELOW which the correlation is not performed. Default = -infinity")

    parser.add_argument('-ght',
                        '--grey-high-threshold',
                        type=float,
                        default=numpy.inf,
                        dest='GREY_HIGH_THRESH',
                        help="Grey threshold on mean of reference imagette ABOVE which the correlation is not performed. Default = infinity")

    parser.add_argument('-reg',
                        '--registration',
                        action="store_true",
                        dest='REG',
                        help='Perform an initial registration? Default = False')

    parser.add_argument('-regb',
                        '--registration-binning',
                        type=int,
                        default=1,
                        dest='REG_BIN',
                        help='Binning to apply to input images for registration. Default = 1')

    parser.add_argument('-regm',
                        '--registration-margin',
                        type=float,
                        default=0.1,
                        dest='REG_MARGIN',
                        help='Registration margin in proportions of image size. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-regs',
                        '--subtract-registration',
                        action="store_true",
                        dest='REGSUB',
                        help='Subtract rigid part of initial registration from output displacements? Default = False')

    parser.add_argument('-ps',
                        '--pixel-search',
                        type=str,
                        default='auto',
                        dest='PS',
                        help="Pixel search option.Accepted values are:\n\t\"auto\": disactivate pixel search if registration works, or Ffile is given." +
                             "\n\t\"on\": Force a pixel search in any case (rounds initial guess and can lose initial F).\n\t\"off\": block pixel search. \"auto\" is default")

    parser.add_argument('-psr',
                        '--pixel-search-range',
                        nargs=6,
                        type=int,
                        default=[-3, 3, -3, 3, -3, 3],
                        dest='PSR',
                        help='Z- Z+ Y- Y+ X- X+ ranges (in pixels) for the pxiel search. Requires pixel search to be activated. Default = +-3px')

    parser.add_argument('-psf',
                        '--pixel-search-filter',
                        type=int,
                        default=0,
                        dest='PS_FILTER',
                        help='Median filter pixel search results. Default = 0')

    # Default: node spacing equal in all three directions
    parser.add_argument('-ns',
                        '--node-spacing',
                        nargs=1,
                        type=int,
                        default=None,
                        dest='NS',
                        help="Node spacing in pixels (assumed equal in all 3 directions -- see -ns3 for different setting). Default = 10px")

    # Possible: node spacing different in all three directions
    parser.add_argument('-ns3',
                        '--node-spacing-3',
                        nargs=3,
                        type=int,
                        default=None,
                        dest='NS',
                        help="Node spacing in pixels (different in 3 directions). Default = 10, 10, 10px")

    # Default: window size equal in all three directions
    parser.add_argument('-hws',
                        '--half-window-size',
                        nargs=1,
                        type=numpy.uint,
                        default=None,
                        dest='HWS',
                        help="Half correlation window size, measured each side of the node pixel (assumed equal in all 3 directions -- see -hws3 for different setting). Default = 10px")

    # Possible: node spacing different in all three directions
    parser.add_argument('-hws3',
                        '--half-window-size-3',
                        nargs=3,
                        type=int,
                        default=None,
                        dest='HWS',
                        help="Half correlation window size, measured each side of the node pixel (different in 3 directions). Default = 10, 10, 10px")

    parser.add_argument('-nogp',
                        '--no-grid-point',
                        action="store_false",
                        dest='GRID_POINT',
                        help='Disactivates grid-point registration')

    parser.add_argument('-gpm',
                        '--grid-point-margin',
                        nargs=1,
                        type=numpy.uint,
                        default=[3],
                        dest='GRID_POINT_MARGIN',
                        help="Margin in pixels for grid-point registration. Default = 3px")

    parser.add_argument('-gpm3',
                        '--grid-point-margin3',
                        nargs=3,
                        type=numpy.uint,
                        default=None,
                        dest='GRID_POINT_MARGIN',
                        help="Subpixel margin for grid-point registration. Default = 3px")

    parser.add_argument('-gpi',
                        '--grid-point-max-iterations',
                        type=numpy.uint,
                        default=50,
                        dest='GRID_POINT_MAX_ITERATIONS',
                        help="Maximum iterations for grid-point registration. Default = 50")

    parser.add_argument('-gpp',
                        '--grid-point-min-phi-change',
                        type=numpy.float,
                        default=0.001,
                        dest='GRID_POINT_MIN_PHI_CHANGE',
                        help="Minimum change in Phi to consider grid-point registration as converged. Default = 0.001")

    parser.add_argument('-gpo',
                        '--grid-point-interpolation-order',
                        type=numpy.uint,
                        default=1,
                        dest='GRID_POINT_INTERPOLATION_ORDER',
                        help="Interpolation order for grid-point registration. Default = 1")

    parser.add_argument('-sef',
                        '--series-Ffile',
                        action="store_true",
                        dest='SERIES_PHIFILE',
                        help='During a total analysis, activate use of previous Ffield for next correlation')

    parser.add_argument('-sei',
                        '--series-incremental',
                        action="store_true",
                        dest='SERIES_INCREMENTAL',
                        help='Perform incremental correlations between images')

    parser.add_argument('-cif',
                        '--correct-input-field',
                        action="store_true",
                        dest='CORRECT_FIELD',
                        help='Activates correction of the input F field')

    parser.add_argument('-cni',
                        '--correct-neighbours-for-field-interpolation',
                        type=numpy.uint,
                        default=12,
                        dest='CORRECT_NEIGHBOURS',
                        help="Number of neighbours for field interpolation. Default = 12")

    parser.add_argument('-cmf',
                        '--correct-median-filter',
                        action="store_true",
                        dest='CORRECT_MEDIAN_FILTER',
                        help="Activates an overall median filter on the input F field")

    parser.add_argument('-cmfr',
                        '--correct-median-filter-radius',
                        type=numpy.uint,
                        default=2,
                        dest='CORRECT_MEDIAN_FILTER_RADIUS',
                        help="Radius of median filter for correction of input F field. Default = 2")

    parser.add_argument('-cdp',
                        '--correct-delta-phi-norm',
                        type=numpy.float,
                        default=0.001,
                        dest='CORRECT_DELTA_F_NORM',
                        help="Delta F norm for a return status = 1 correlation window to consider the point good. Default = 0.001")

    parser.add_argument('-cpscc',
                        '--correct-pixel-search-cc',
                        type=numpy.float,
                        default=0.98,
                        dest='CORRECT_PIXEL_SEARCH_CC',
                        help="Pixel search correlation coefficient to consider the point good. Default = 0.98")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files (without extension). Default is basename of input file")

    parser.add_argument('-vtk',
                        '--VTKout',
                        action="store_true",
                        dest='VTK',
                        help='Activate VTK output format. Default = False')

    parser.add_argument('-tsv',
                        '--TSVout',
                        action="store_true",
                        dest='TSV',
                        help='Activate TSV output format. Default = False')

    parser.add_argument('-tif',
                        '-tiff',
                        '--TIFFout',
                        '--TIFout',
                        action="store_true",
                        dest='TIFF',
                        help='Activate TIFFoutput format. Default = False')

    args = parser.parse_args()

    # 2018-03-24 check for 2D without loading images
    # try:
    # except BaseException:
    #     print("DICregularGrid: Input TIFF files need to be writeable in order to guess their dimensionality")
    #     exit()
    # 2019-03-21 EA: better check for dimensions, doesn't depend on writability of files
    import tifffile
    tiff = tifffile.TiffFile(args.inFiles[0].name)
    imagejSingleSlice = True
    # if tiff.imagej_metadata is not None:
    #     if 'slices' in tiff.imagej_metadata:
    #         if tiff.imagej_metadata['slices'] > 1:
    #             imagejSingleSlice = False

    # 2019-04-05 EA: 2D image detection approved by Christophe Golke, update for shape 2019-08-29
    if len(tiff.pages) == 1 and len(tiff.series[0].shape) == 2:
        twoD = True
    else:
        twoD = False
    tiff.close()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFiles[0].name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.inFiles[0].name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    # 2018-11-15 EA: Setting this in the client in order not to overwrite files in a series
    # if args.PREFIX is None:
    #     args.PREFIX = os.path.splitext(os.path.basename(args.inFiles[0].name))[0]

    if args.PS != 'auto' and args.PS != 'on' and args.PS != 'off':
        print("\nInvalid option {} for pixel search. Setting \"auto\"".format(args.PS))
        args.PS = 'auto'

    # Catch interdependent node spacing and correlation window sizes
    if args.NS is None:
        print("\nUsing default node spacing: "),
        if args.HWS is None:
            print("2x default half window size"),
            args.HWS = [10]
            print("({}) which is".format(args.HWS[0])),
            args.NS = [args.HWS[0] * 2]
        else:
            print("2x user-set half window size"),
            if len(args.HWS) == 1:
                print("({}) which is".format(args.HWS[0])),
                args.NS = [int(args.HWS[0] * 2)]
            elif len(args.HWS) == 3:
                print("({} -- selecting smallest) which is".format(args.HWS)),
                args.NS = [int(min(args.HWS) * 2)]
        print(args.NS)

    # Catch 3D options
    if len(args.NS) == 1:
        args.NS = [args.NS[0], args.NS[0], args.NS[0]]
    if len(args.HWS) == 1:
        args.HWS = [args.HWS[0], args.HWS[0], args.HWS[0]]
    if len(args.GRID_POINT_MARGIN) == 1:
        args.GRID_POINT_MARGIN = [args.GRID_POINT_MARGIN[0], args.GRID_POINT_MARGIN[0], args.GRID_POINT_MARGIN[0]]

    if type(args.GRID_POINT_MAX_ITERATIONS) == list:
        args.GRID_POINT_MAX_ITERATIONS = args.GRID_POINT_MAX_ITERATIONS[0]

    # Catch and overwrite 2D options
    if twoD:
        args.NS[0] = 1
        args.HWS[0] = 0
        args.GRID_POINT_MARGIN[0] = 0
        args.PSR[0] = 0
        args.PSR[1] = 0

    # Behaviour undefined for series run and im1 mask since im1 will change, complain and continue
    if args.MASK1 is not None and args.SERIES_INCREMENTAL:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: You set an im1 mask and an incremental      ###")
        print("###  series correlation, meaning that im1 will change...  ###")
        print("#############################################################")
        print("#############################################################")

    # Make sure at least one output format has been asked for
    if args.VTK + args.TSV + args.TIFF== 0:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: No output type of VTK, TSV and TIFFoptions  ###")
        print("###  Are you sure this is right?!                         ###")
        print("#############################################################")
        print("#############################################################")

    if args.REG_MARGIN > 0.45:
        print("Registration margin cannot be bigger than 0.45 since 0.5 would contain no data!!")

    if args.SERIES_PHIFILE:
        args.TSV = True

    # just keep the name for this one
    if args.PHIFILE is not None:
        args.PHIFILE = args.PHIFILE.name

    return args


def ddicParser(parser):
    parser.add_argument('im1',
                        metavar='im1',
                        type=argparse.FileType('r'),
                        help="Greyscale image of reference state for correlation")

    parser.add_argument('lab1',
                        metavar='lab1',
                        type=argparse.FileType('r'),
                        help="Labelled image of reference state for correlation")

    parser.add_argument('im2',
                        metavar='im2',
                        type=argparse.FileType('r'),
                        help="Greyscale image of deformed state for correlation")

    parser.add_argument('-ps',
                        '--pixel-search',
                        type=str,
                        default='auto',
                        dest='PS',
                        help="Pixel search option.Accepted values are:\n\t\"auto\": disactivate pixel search if registration works, or Ffile is given." +
                             "\n\t\"on\": Force a pixel search in any case (rounds initial guess and can lose initial F).\n\t\"off\": block pixel search. \"auto\" is default")

    parser.add_argument('-nompi',
                        action="store_false",
                        dest='MPI',
                        help='Disactivate MPI parallelisation?')

    parser.add_argument('-psr',
                        '--pixel-search-range',
                        nargs=6,
                        type=int,
                        default=[-3, 3, -3, 3, -3, 3],
                        dest='PSR',
                        help='Z- Z+ Y- Y+ X- X+ ranges (in pixels) for the pxiel search. Requires pixel search to be activated. Default = +-3px')

    parser.add_argument('-nogp',
                        '--no-grid-point',
                        action="store_false",
                        dest='GRID_POINT',
                        help='Disactivate grid-point registration?')

    parser.add_argument('-ld',
                        '--label-dilate',
                        type=int,
                        default=1,
                        dest='LABEL_DILATE',
                        help="Number of times to dilate labels. Default = 1")

    parser.add_argument('-ldmax',
                        '--label-dilate-maximum',
                        type=int,
                        default=None,
                        dest='LABEL_DILATE_MAX',
                        help="Maximum dilation for label if they don't converge with -ld setting. Default = same as -ld setting")

    parser.add_argument('-vt',
                        '--volume-threshold',
                        type=numpy.uint,
                        default=100,
                        dest='VOLUME_THRESHOLD',
                        help="Volume threshold below which labels are ignored. Default = 100")

    parser.add_argument('-reg',
                        '--registration',
                        action="store_true",
                        dest='REG',
                        help='Perform an initial registration? Default = False')

    parser.add_argument('-regb',
                        '--registration-binning',
                        type=int,
                        default=1,
                        dest='REG_BIN',
                        help='Binning to apply to input images for registration. Default = 1')

    parser.add_argument('-regm',
                        '--registration-margin',
                        type=float,
                        default=0.1,
                        dest='REG_MARGIN',
                        help='Registration margin in proportions of image size. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-regs',
                        '--subtract-registration',
                        action="store_true",
                        dest='REGSUB',
                        help='Subtract rigid part of initial registration from output displacements? Default = False')

    parser.add_argument('-pf',
                        '-phiFile',
                        dest='PHIFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

    parser.add_argument('-pfb',
                        '--phiFile-bin-ratio',
                        type=int,
                        default=1,
                        dest='PHIFILE_BIN_RATIO',
                        help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")


    parser.add_argument('-pfd',
                        '--phiFile-direct',
                        action="store_true",
                        default=1,
                        dest='PHIFILE_DIRECT',
                        help="Trust the Phi file completely? This option ignores and overrides -cif and requires labels to be aligned between Phi file and labelled image")

    parser.add_argument('-cif',
                        '--correct-input-field',
                        action="store_true",
                        dest='CF',
                        help='Correction of the input F field. Default = True')

    parser.add_argument('-nfi',
                        '--neighbours-for-field-interpolation',
                        type=numpy.uint,
                        default=12,
                        dest='NEIGHBOURS',
                        help="Number of neighbours for field interpolation. Default = 12")

    parser.add_argument('-nomask',
                        '--no-mask',
                        action="store_false",
                        dest='MASK',
                        help='Don\'t mask each label\'s image')

    parser.add_argument('-gpm',
                        '--grid-point-margin',
                        type=numpy.uint,
                        default=2,
                        dest='GRID_POINT_MARGIN',
                        help="Margin in pixels for grid-point registration to be added to label dilate. Default = 2px")

    parser.add_argument('-gpi',
                        '--grid-point-max-iterations',
                        type=numpy.uint,
                        default=50,
                        dest='GRID_POINT_MAX_ITERATIONS',
                        help="Maximum iterations for grid-point registration. Default = 50")

    parser.add_argument('-gpp',
                        '--grid-point-min-phi-change',
                        type=numpy.float,
                        default=0.001,
                        dest='GRID_POINT_MIN_PHI_CHANGE',
                        help="Minimum change in Phi to consider grid-point registration as converged. Default = 0.001")

    parser.add_argument('-gpo',
                        '--grid-point-interpolation-order',
                        type=numpy.uint,
                        default=1,
                        dest='GRID_POINT_INTERPOLATION_ORDER',
                        help="Interpolation order for grid-point registration. Default = 3")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files (without extension). Default is basename of input file")

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.lab1.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0] + "-" + os.path.splitext(os.path.basename(args.im2.name))[0]

    # Set label dilate max as label dilate if it is none
    if args.LABEL_DILATE_MAX is None:
        args.LABEL_DILATE_MAX = args.LABEL_DILATE

    if args.LABEL_DILATE_MAX < args.LABEL_DILATE:
        print("spam-ddic: Warining \"label dilate max\" is less than \"label dilate\" setting them equal")
        args.LABEL_DILATE_MAX = args.LABEL_DILATE

    return args


def multiModalRegistrationParser(parser):
    import spam.DIC
    import numpy

    parser.add_argument('im1',
                        metavar='im1',
                        type=argparse.FileType('r'),
                        help="Greyscale image of reference state for correlation")

    parser.add_argument('im2',
                        metavar='im2',
                        type=argparse.FileType('r'),
                        help="Greyscale image of deformed state for correlation")

    parser.add_argument('-im1min',
                        type=float,
                        default=None,
                        dest='IM1_MIN',
                        help="Minimum of im1 for greylevel scaling. Default = im1.min()")

    parser.add_argument('-im1max',
                        type=float,
                        default=None,
                        dest='IM1_MAX',
                        help="Maximum of im1 for greylevel scaling. Default = im1.max()")

    parser.add_argument('-im2min',
                        type=float,
                        default=None,
                        dest='IM2_MIN',
                        help="Minimum of im2 for greylevel scaling. Default = im2.min()")

    parser.add_argument('-im2max',
                        type=float,
                        default=None,
                        dest='IM2_MAX',
                        help="Maximum of im2 for greylevel scaling. Default = im2.max()")

    parser.add_argument('-im1th',
                        '--im1-threshold',
                        type=int,
                        default=0,
                        dest='IM1_THRESHOLD',
                        help='Greylevel threshold for image 1. Below this threshold, peaks in the histogram are ignored.')

    parser.add_argument('-im2th',
                        '--im2-threshold',
                        type=int,
                        default=0,
                        dest='IM2_THRESHOLD',
                        help='Greylevel threshold for image 2. Below this threshold, peaks in the histogram are ignored.')

    parser.add_argument('-bin',
                        '--bin-levels',
                        type=int,
                        default=1,
                        dest='NBINS',
                        help='Number of binning levels to apply to the data (if given 3, the binning levels used will be 4 2 1). The -phase option is necessary and should define this many phases (i.e., 3 different numbers in this example)')

    parser.add_argument('-ph',
                        '--phases',
                        nargs='+',
                        type=int,
                        default=[2],
                        dest='PHASES',
                        help='Number of phases?')

    parser.add_argument('-jhb',
                        '--joint-histogram-bins',
                        # nargs=1,
                        type=int,
                        default=128,
                        dest='JOINT_HISTO_BINS',
                        help='The number of greylevel bins for both images in the joint histogram')

    parser.add_argument('-dst',
                        '--dist-between-max',
                        type=int,
                        default=None,
                        dest='DIST_BETWEEN_MAX',
                        help='Minimal distance between two maxima in the histogram')

    parser.add_argument('-fdi',
                        '--fit-distance',
                        type=float,
                        default=None,
                        dest='FIT_DISTANCE',
                        help='Distance considered around a peak for the Gaussian ellipsoid fitting')

    parser.add_argument('-voc',
                        '--voxel-coverage',
                        type=float,
                        default=1.0,
                        dest='VOXEL_COVERAGE',
                        help='Percentage (between 0 and 1) of voxel coverage of the phases in the joint histogram')

    parser.add_argument('-int',
                        '--interactive',
                        action="store_true",
                        dest='INTERACTIVE',
                        help='Present live-updating plots to the user')

    parser.add_argument('-gra',
                        '--graphs',
                        action="store_true",
                        dest='GRAPHS',
                        help='Save graphs to file')

    parser.add_argument('-ssl',
                        '--show-slice-axis',
                        type=int,
                        default=0,
                        dest='SHOW_SLICE_AXIS',
                        help='Axis of the cut used for the plots')

    parser.add_argument('-spp',
                        '--grid-point-min-phi-change',
                        type=numpy.float,
                        default=0.0005,
                        dest='GRID_POINT_MIN_PHI_CHANGE',
                        help="Subpixel min change in Phi to stop iterations. Default = 0.001")

    parser.add_argument('-spi',
                        '--grid-point-max-iterations',
                        type=numpy.uint,
                        default=50,
                        dest='GRID_POINT_MAX_ITERATIONS',
                        help="Max number of iterations to optimise Phi. Default = 50")

    # parser.add_argument('-tmp',
    #                     '--writeTemporaryFiles',
    #                     action="store_true",
    #                     dest='DATA',
    #                     help='Save temporary files (joint histogram) to \"dat\" file')

    parser.add_argument('-loadprev',
                        '--load-previous-iteration',
                        action="store_true",
                        dest='LOADPREV',
                        help='Load output pickle files from previous iterations (2* coarser binning)')

    parser.add_argument('-mar',
                        '--margin',
                        type=float,
                        default=0.1,
                        dest='MARGIN',
                        help='Margin of both images. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-cro',
                        '--crop',
                        type=float,
                        default=0.1,
                        dest='CROP',
                        help='Initial crop of both images. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-pif',
                        default=None,
                        type=argparse.FileType('rb'),
                        dest='FGUESS_PICKLE',
                        help="Pickle file name for initial guess. Should be in position 0 in the array and labeled as 'F' as for registration.")

    # Remove next two arguments for F input, and replace with displacement and rotation inputs on command line
    parser.add_argument('-pf',
                        '--phiFile',
                        dest='PHIFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to TSV file containing initial Phi guess, can be single-point registration or multiple point correlation. Default = None")

    # parser.add_argument('-Ffb',
    # '--Ffile-bin-ratio',
    # type=int,
    # default=1,
    # dest='PHIFILE_BIN_RATIO',
    # help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    # parser.add_argument('-tra',
    # '--translation',
    # nargs=3,
    # type=float,
    # default=None,
    # dest='TRA',
    # help="Z, Y, X initial displacements to apply at the bin 1 scale")

    # parser.add_argument('-rot',
    # '--rotation',
    # nargs=3,
    # type=float,
    # default=None,
    # dest='ROT',
    # help="Z, Y, X components of rotation vector to apply at the bin 1 scale")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files (without extension). Default is basename of input file")

    args = parser.parse_args()

    # The number of bin levels must be the same as the number of phases
    if (args.NBINS != len(args.PHASES)):
        print("\toptionsParser.multiModalRegistrationParser(): Number of bin levels and number of phases not the same, exiting")
        exit()

    # For back compatibility, generate list of bins
    args.BINS = []
    for i in range(args.NBINS)[::-1]:
        args.BINS.append(2**i)

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.im1.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.im1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Get initial guesses
    if args.PHIFILE is not None:
        import spam.helpers
        args.FGUESS = spam.helpers.readCorrelationTSV(args.PHIFILE.name, readConvergence=False, readEverything=False, readFs=True)['PhiField'][0]
    else:
        args.FGUESS = numpy.eye(4)

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.im1.name))[0] + "-" + os.path.splitext(os.path.basename(args.im2.name))[0]

    return args


def gdicParser(parser):
    parser.add_argument('inFiles',
                        nargs='+',
                        type=argparse.FileType('r'),
                        help="A space-separated list of two 3D greyscale tiff files to correlate, in order")

    parser.add_argument('-mf1',
                        '--maskFile1',
                        dest='MASK1',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to tiff file containing the mask of image 1 -- masks  zones not to correlate")

    parser.add_argument('-mf2',
                        '--maskFile2',
                        dest='MASK2',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to tiff file containing the mask of image 2 -- masks correlation windows")

    parser.add_argument('-pf',
                        '-phiFile',
                        dest='PHIFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to TSV file containing initial F guess, can be single-point registration or multiple point correlation. Default = None")

    parser.add_argument('-pfb',
                        '--phiFile-bin-ratio',
                        type=int,
                        default=1,
                        dest='PHIFILE_BIN_RATIO',
                        help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    # parser.add_argument('-glt',
    #                     '--grey-low-threshold',
    #                     type=float,
    #                     default=-numpy.inf,
    #                     dest='GREY_LOW_THRESH',
    #                     help="Grey threshold on mean of reference imagette BELOW which the correlation is not performed. Default = -infinity")
    #
    # parser.add_argument('-ght',
    #                     '--grey-high-threshold',
    #                     type=float,
    #                     default=numpy.inf,
    #                     dest='GREY_HIGH_THRESH',
    #                     help="Grey threshold on mean of reference imagette ABOVE which the correlation is not performed. Default = infinity")

    parser.add_argument('-d',
                        '--debug',
                        action="store_true",
                        dest='DEBUG_FILES',
                        help='Output debug files during iterations? Default = False')

    parser.add_argument('-reg',
                        '--registration',
                        action="store_true",
                        dest='REG',
                        help='Perform an initial registration? Default = False')

    parser.add_argument('-regb',
                        '--registration-binning',
                        type=int,
                        default=1,
                        dest='REG_BIN',
                        help='Binning to apply to input images for registration. Default = 1')

    parser.add_argument('-regm',
                        '--registration-margin',
                        type=float,
                        default=0.1,
                        dest='REG_MARGIN',
                        help='Registration margin in proportions of image size. Default = 0.1, which means 0.1 * image size from both sides')

    parser.add_argument('-mit',
                        '--max-iterations',
                        type=numpy.uint,
                        default=25,
                        dest='MAX_ITERATIONS',
                        help="Max iterations for global correlation. Default = 25")

    parser.add_argument('-cc',
                        '--convergence-criterion',
                        type=numpy.float,
                        default=0.01,
                        dest='CONVERGENCE_CRITERION',
                        help="Displacement convergence criterion in pixels (norm of incremental displacements). Default = 0.01")

    parser.add_argument('-str',
                        '--calculate-strain',
                        action="store_true",
                        dest='STRAIN',
                        help='Calculate strain? This is added to the VTK output files')

    parser.add_argument('-ss',
                        '--small--strains',
                        action="store_true",
                        dest='SMALL_STRAINS',
                        help='Strain field is computed under the hypothesis of small strain. Default = False')

    # parser.add_argument('-spo',
    #                     '--grid-point-interpolation-order',
    #                     type=numpy.uint,
    #                     default=1,
    #                     dest='GRID_POINT_INTERPOLATION_ORDER',
    #                     help="Subpixel interpolation order. Default = 1")

    # parser.add_argument('-cif',
    #                     '--correct-input-field',
    #                     action="store_true",
    #                     dest='CF',
    #                     help='Correction of the input F field. Default = True')

    # parser.add_argument('-nfi',
    #                     '--neighbours-for-field-interpolation',
    #                     type=numpy.uint,
    #                     default=12,
    #                     dest='NEIGHBOURS',
    #                     help="Neighbours for field interpolation. Default = 12")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help="Prefix for output files (without extension). Default is basename of input file")

    parser.add_argument('-Mfile',
                        dest='MESH_FILE',
                        default=None,
                        type=argparse.FileType('rb'),
                        help="Path to pickle file containing mesh information needed for the correlation (coordinates, connectivity, labels and padding). Default = None.")

    parser.add_argument('-Mcube',
                        '--mesh-cuboid',
                        nargs=7,
                        type=numpy.float,
                        default=None,
                        dest='MESH_CUBOID',
                        help='7 floats parameters to mesh a cuboid. first 3 are position of the bottom corner (Z, Y X), next 3 are the lenghts of the cube (Z, Y X) and the last one is the average length between two nodes.')

    args = parser.parse_args()

    if args.MESH_FILE is None and args.MESH_CUBOID is None:
        print("\tgdic: a mesh is needed. Use one of this option: -Mcube or -Mfile.")
        print("\tgdic: exiting.")
        exit()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFiles[0].name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.inFiles[0].name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = "GDIC_{}-{}".format(os.path.splitext(os.path.basename(args.inFiles[0].name))[0], os.path.splitext(os.path.basename(args.inFiles[1].name))[0])

    if type(args.MAX_ITERATIONS) == list:
        args.MAX_ITERATIONS = args.MAX_ITERATIONS[0]

    if args.REG_MARGIN > 0.45:
        print("Registration margin cannot be bigger than 0.45 since 0.5 would contain no data!!")

    return args


def regularStrainsCalcParser(parser):
    parser.add_argument('inFile',
                        metavar='inFile',
                        type=argparse.FileType('r'),
                        help='Path to TSV file containing the result of the correlation')

    parser.add_argument('-comp',
                        '--strain-components',
                        nargs='*',
                        type=str,
                        default=['vol', 'dev'],
                        dest='COMPONENTS',
                        help='Selection of which strain components to save, options are: vol (volumetric strain), dev (deviatoric strain), volss (volumetric strain in small strains), devss (deviatoric strain in small strains), r (rotation vector), z (zoom vector), U (right-hand stretch tensor), e (strain tensor in small strains)')

    parser.add_argument('-mask',
                        '--mask',
                        action="store_true",
                        dest='MASK',
                        help='Mask correlation points according to return status')

    parser.add_argument('-r',
                        '--neighbourhood-radius-for-strain-calculation',
                        type=float,
                        default=1.5,
                        dest='STRAIN_NEIGHBOUR_RADIUS',
                        help="Radius (in units of nodeSpacing) inside which to select neighbours for displacement gradient calculation. Ignored if -cub is set. Default = 1.5")

    parser.add_argument('-cub',
                        '--cubic-element',
                        '--Q8',
                        action="store_true",
                        dest='Q8',
                        help='Use Q8 element interpolation? More noisy and strain values not centred on displacement points')

    parser.add_argument('-cif',
                        '--correct-input-field',
                        action="store_true",
                        dest='CORRECT_FIELD',
                        help='Activates correction of the input displacement field')

    parser.add_argument('-cni',
                        '--correct-neighbours-for-field-interpolation',
                        type=numpy.uint,
                        default=12,
                        dest='CORRECT_NEIGHBOURS',
                        help="Neighbours for field interpolation. Default = 12")

    parser.add_argument('-cmf',
                        '--correct-median-filter',
                        action="store_true",
                        dest='CORRECT_MEDIAN_FILTER',
                        help="Activates an overall median filter on the input displacement field")

    parser.add_argument('-cmfr',
                        '--correct-median-filter-radius',
                        type=numpy.uint,
                        default=2,
                        dest='CORRECT_MEDIAN_FILTER_RADIUS',
                        help="Radius of median filter for correction of input displacement field. Default = 2")

    parser.add_argument('-cdp',
                        '--correct-delta-phi-norm',
                        type=numpy.float,
                        default=0.001,
                        dest='CORRECT_DELTA_PHI_NORM',
                        help="Delta Phi norm for a return status = 1 correlation window to consider the point good. Default = 0.001")

    parser.add_argument('-cpscc',
                        '--correct-pixel-search-cc',
                        type=numpy.float,
                        default=0,
                        dest='CORRECT_PIXEL_SEARCH_CC',
                        help="Pixel search correlation coefficient to consider the point good. Default = 0")

    #parser.add_argument('-ss',
                        #'--small--strains',
                        #action="store_true",
                        #dest='SMALL_STRAINS',
                        #help='Strain field is computed under the hypothesis of small strain. Default = False')

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help='Output directory, default is the dirname of input file')

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output files (without extension). Default is basename of input file')

    #parser.add_argument('-nos',
                        #'--not-only-strain',
                        #action="store_true",
                        #dest='NOT_ONLY_STRAIN',
                        #help='Return all the output matrices. Default = False')

    parser.add_argument('-tif',
                        '-tiff',
                        action="store_true",
                        dest='TIFF',
                        help='Activate TIFF output format. Default = False')

    parser.add_argument('-tsv',
                        '-TSV',
                        action="store_true",
                        dest='TSV',
                        help='Activate TSV output format. Default = False')

    parser.add_argument('-vtk',
                        '--VTKout',
                        action="store_true",
                        dest='VTK',
                        help='Activate VTK output format. Default = False')

    parser.add_argument('-vtkmn',
                        '--VTKmaskNANs',
                        action="store_true",
                        dest='VTKmaskNAN',
                        help='Mask NaNs in VTK output (replace them with 0.0). Default = False')

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFile.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise
    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.inFile.name))[0]+"-strain"

    # Make sure at least one output format has been asked for
    if args.VTK + args.TIFF + args.TSV == 0:
        print("#############################################################")
        print("#############################################################")
        print("###  WARNING: No output type of VTK, TSV or TIFF          ###")
        print("###  Are you sure this is right?!                         ###")
        print("#############################################################")
        print("#############################################################")

    return args


def discreteStrainsCalcParser(parser):
    parser.add_argument('inFile',
                        metavar='inFile',
                        type=argparse.FileType('r'),
                        help='Path to TSV file containing the result of the correlation')

    parser.add_argument('-comp',
                        '--strain-components',
                        nargs='*',
                        type=str,
                        default=['vol', 'dev'],
                        dest='COMPONENTS',
                        help='Selection of which strain components to save, options are: vol (volumetric strain), dev (deviatoric strain), volss (volumetric strain in small strains), devss (deviatoric strain in small strains), r (rotation vector), z (zoom vector), U (right-hand stretch tensor), e (strain tensor in small strains)')

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help='Output directory, default is the dirname of input file')

    parser.add_argument('-tri',
                        '--perform-triangulation',
                        action="store_true",
                        dest='TRI',
                        help='Perform triangulation of grain centres?')

    parser.add_argument('-a',
                        '-triangulation-alpha-value',
                        type=float,
                        default=0.0,
                        dest='TRI_ALPHA',
                        help='CGAL Alpha value for triangulation cleanup (negative = auto, zero = no cleanup, positive = userval). Default = 0')

    parser.add_argument('-tf',
                        '--triangulation-file',
                        type=str,
                        default=None,
                        dest='TRI_FILE',
                        help='Load a triangulation from file? This should be a TSV with just lines with three numbers corresponding to the connectivity matrix (e.g., output from numpy.savetxt())')

    parser.add_argument('-rf',
                        '--radius-file',
                        type=str,
                        default=None,
                        dest='RADII_TSV_FILE',
                        help='Load a series of particle radii from file? Only necessary if -tri is activated')

    parser.add_argument('-rl',
                        '--radii-from-labelled',
                        type=str,
                        default=None,
                        dest='RADII_LABELLED_FILE',
                        help='Load a labelled image and compute radii? Only necessary if -tri is activated')

    parser.add_argument('-rst',
                        '--return-stats-threshold',
                        type=int,
                        default=None,
                        dest='RETURN_STAT_THRESHOLD',
                        help='Lowest return status value to preserve in the triangulation. Default = 2')

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output files (without extension). Default is basename of input file')

    # parser.add_argument('-nos',
    # '--not-only-strain',
    # action="store_true",
    # dest='NOT_ONLY_STRAIN',
    # help='Return all the output matrices. Default = True')

    parser.add_argument('-pg',
                        '--project-to-grains',
                        action="store_true",
                        dest='PROJECT_TO_GRAINS',
                        help='Also project strain components to grains? This gives a neighbourhood average expressed at the grain (and not the deformation of the grain itself)')

    parser.add_argument('-kz',
                        '--keep-zero',
                        action="store_true",
                        dest='KEEP_ZERO',
                        help='Consider grain number zero? Only affects TSV files. Default = False')

    #parser.add_argument('-vtk',
                        #'--VTKout',
                        #action="store_false",
                        #dest='VTK',
                        #help='Activate VTK output format. Default = True')

    parser.add_argument('-vtkmn',
                        '--VTKmaskNANs',
                        action="store_true",
                        dest='VTKmaskNAN',
                        help='Mask NaNs in VTK output (replace them with 0.0). Default = False')

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFile.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise
    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.inFile.name))[0] + "-strains"

    # Make sure at least one output format has been asked for
    # if args.VTK + args.TIFF== 0:
    #     print("#############################################################")
    #     print("#############################################################")
    #     print("###  WARNING: No output type of VTK, TSV and TIFFoptions  ###")
    #     print("###  Are you sure this is right?!                         ###")
    #     print("#############################################################")
    #     print("#############################################################")

    return args


def BCFromDVCParser(parser):
    parser.add_argument('-gmshFile',
                        dest='GMSHFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help='Path to gmsh file containing the FE mesh. Default = None')

    parser.add_argument('-vtkFile',
                        dest='VTKFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help='Path to vtk file containing the FE mesh. Default = None')

    parser.add_argument('-tsvFile',
                        dest='TSVDVCFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to tsv file containing the result of a correlation. Default = None")

    parser.add_argument('-mask',
                        '--mask',
                        action="store_true",
                        dest='MASK',
                        help='Mask correlation points according to return status')

    parser.add_argument('-pixSize',
                        '--pixel-size',
                        type=numpy.float,
                        default=1.0,
                        dest='PIXEL_SIZE',
                        help="Physical size of a pixel (i.e. mm/px). Default = 1")

    parser.add_argument('-tol',
                        '--tolerance',
                        type=numpy.float,
                        default=1e-6,
                        dest='TOL',
                        help="Numerical tolerance for floats. Default = 1e-6")

    parser.add_argument('-meshType',
                        '--mesh-type',
                        type=str,
                        default="cube",
                        dest='MESHTYPE',
                        help="The type of the input mesh (i.e. cube, cylinder etc). Default = cube")

    parser.add_argument('-topBottom',
                        '--top-bottom',
                        action="store_true",
                        dest='TOP_BOTTOM',
                        help="Apply BC only on top-bottom surfaces (i.e. z=zmin, z=zmax)")

    parser.add_argument('-cylCentre',
                        '--cylinder-centre',
                        nargs=2,
                        type=numpy.float,
                        default=[0, 0],
                        dest='CYLCENTRE',
                        help="The cente of the cylinder [x, y]. Default =[0, 0]")

    parser.add_argument('-cylRadius',
                        '--cylinder-radius',
                        type=numpy.float,
                        default=1.0,
                        dest='CYLRADIUS',
                        help="The radius of the cylinder. Default = 1")

    parser.add_argument('-ni',
                        '--neighbours-for-interpolation',
                        type=numpy.uint,
                        default=4,
                        dest='NEIGHBOURS_INT',
                        help="Neighbours for field interpolation. Default = 4")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of gmsh file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output files (without extension). Default is basename of mesh file')

    parser.add_argument('-feapBC',
                        '--feap-boundary-conditions',
                        action="store_true",
                        dest='FEAPBC',
                        help='Write the boundary conditions in FEAP format. Default = True')

    parser.add_argument('-vtk',
                        '--VTKout',
                        action="store_false",
                        dest='SAVE_VTK',
                        help='Save the BC field as VTK. Default = True')

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        try:
            args.OUT_DIR = os.path.dirname(args.GMSHFILE.name)
        except BaseException:
            try:
                args.OUT_DIR = os.path.dirname(args.VTKFILE.name)
            except BaseException:
                print("\n***You need to input an unstructured mesh. Exiting...***")
                exit()
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                try:
                    args.DIR_out = os.path.dirname(args.GMSHFILE.name)
                except BaseException:
                    try:
                        args.DIR_out = os.path.dirname(args.VTKFILE.name)
                    except BaseException:
                        print("\n***You need to input an unstructured mesh. Exiting...***")

        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        try:
            args.PREFIX = os.path.splitext(os.path.basename(args.GMSHFILE.name))[0]
        except BaseException:
            try:
                args.DIR_out = os.path.dirname(args.VTKFILE.name)
            except BaseException:
                print("\n***You need to input an unstructured mesh. Exiting...***")
                exit()

    return args


def moveGrainsParser(parser):
    parser.add_argument('LabFile',
                        metavar='LabFile',
                        type=argparse.FileType('r'),
                        help='Path to the labelled TIFFfile to be moved')

    parser.add_argument('TSVFile',
                        metavar='TSVFile',
                        type=argparse.FileType('r'),
                        help='Path to TSV file containing the Phis to apply to each label')

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help='Output directory, default is the dirname of input file')

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output TIFF file (without extension). Default is basename of input file')

    parser.add_argument('-com',
                        '--apply-phi-centre-of-mass',
                        action="store_true",
                        dest='PHICOM',
                        help='Apply Phi to centre of mass of particle? Otherwise it will be applied in the middle of the particle\'s bounding box')

    parser.add_argument('-thr',
                        '--threshold',
                        type=float,
                        default=0.5,
                        dest='THRESH',
                        help='Partial volume threshold to keep interpolated voxels. Default = 0.5')

    parser.add_argument('-rst',
                        '--return-status-threshold',
                        type=int,
                        default=None,
                        dest='RETURN_STATUS_THRESHOLD',
                        help='Return status in spam-ddic to consider the grain. Default = None, but 2 (i.e., converged) is recommended ')

    parser.add_argument('-om',
                        '--overall-margin',
                        type=int,
                        default=10,
                        dest='OVERALL_MARGIN',
                        help="Overall image margin for particle movement, this is how much the labelled image is increased before calculating. Default = 10")

    parser.add_argument('-dm',
                        '--displacement-margin',
                        type=int,
                        default=3,
                        dest='DISPLACEMENT_MARGIN',
                        help="Displacement margin for particle movement, this the padding around the extraction of each objet and show allow for rotation. Default = 3")

    parser.add_argument('-md',
                        '--multipy-displacements',
                        type=float,
                        default=1.0,
                        dest='MULTIPLY_DISPLACEMENTS',
                        help="Displacement margin for particle movement, this must be AT LEAST equal to the mazimum displacement. Default = 1.0")

    parser.add_argument('-np',
                        '--number-parallel-process',
                        type=int,
                        default=1,
                        dest='NUMBER_OF_PROCESSES',
                        help='Number of parallel processes to use (shared mem parallelisation). Default = 1')

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.LabFile.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise
    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.LabFile.name))[0] + "-displaced"

    return args


def ITKwatershedParser(parser):
    parser.add_argument('inFile',
                        metavar='inFile',
                        type=argparse.FileType('r'),
                        help='Path to binary TIFF file to be watershedded')

    parser.add_argument('-ld',
                        '--label-dilate',
                        type=int,
                        default=0,
                        dest='LABEL_DILATE',
                        help="Number of times to dilate labels. Default = 0, Normally you want this to be negative")

    parser.add_argument('-mf',
                        '--marker-file',
                        type=str,
                        default=None,
                        dest='MARKER_FILE',
                        help='Path to labelled TIFF file to use as markers')

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output files (without extension). Default is basename of input file plus watershed at the end')

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of input file")

    parser.add_argument('-v',
                        type=int,
                        default=0,
                        dest='VERBOSE',
                        help="Print the evolution of the process (0 -> False, 1 -> True). Defalut is 0")

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFile.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise
    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.inFile.name))[0] + "-watershed"

    return args


def BCFromDVCParser(parser):
    parser.add_argument('-gmshFile',
                        dest='GMSHFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help='Path to gmsh file containing the FE mesh. Default = None')

    parser.add_argument('-vtkFile',
                        dest='VTKFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help='Path to vtk file containing the FE mesh. Default = None')

    parser.add_argument('-tsvFile',
                        dest='TSVDVCFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to tsv file containing the result of a correlation. Default = None")

    parser.add_argument('-mask',
                        '--mask',
                        action="store_true",
                        dest='MASK',
                        help='Mask correlation points according to return status')

    parser.add_argument('-pixSize',
                        '--pixel-size',
                        type=numpy.float,
                        default=1.0,
                        dest='PIXEL_SIZE',
                        help="Physical size of a pixel (i.e. mm/px). Default = 1")

    parser.add_argument('-tol',
                        '--tolerance',
                        type=numpy.float,
                        default=1e-6,
                        dest='TOL',
                        help="Numerical tolerance for floats. Default = 1e-6")

    parser.add_argument('-meshType',
                        '--mesh-type',
                        type=str,
                        default="cube",
                        dest='MESHTYPE',
                        help="The type of the input mesh (i.e. cube, cylinder etc). Default = cube")

    parser.add_argument('-topBottom',
                        '--top-bottom',
                        action="store_true",
                        dest='TOP_BOTTOM',
                        help="Apply BC only on top-bottom surfaces (i.e. z=zmin, z=zmax)")

    parser.add_argument('-cylCentre',
                        '--cylinder-centre',
                        nargs=2,
                        type=numpy.float,
                        default=[0, 0],
                        dest='CYLCENTRE',
                        help="The cente of the cylinder [x, y]. Default =[0, 0]")

    parser.add_argument('-cylRadius',
                        '--cylinder-radius',
                        type=numpy.float,
                        default=1.0,
                        dest='CYLRADIUS',
                        help="The radius of the cylinder. Default = 1")

    parser.add_argument('-ni',
                        '--neighbours-for-interpolation',
                        type=numpy.uint,
                        default=4,
                        dest='NEIGHBOURS_INT',
                        help="Neighbours for field interpolation. Default = 4")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of gmsh file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output files (without extension). Default is basename of mesh file')

    parser.add_argument('-feapBC',
                        '--feap-boundary-conditions',
                        action="store_true",
                        dest='FEAPBC',
                        help='Write the boundary conditions in FEAP format. Default = True')

    parser.add_argument('-saveVTK',
                        '--VTKout',
                        action="store_true",
                        dest='SAVE_VTK',
                        help='Save the BC field as VTK. Default = True')

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        try:
            args.OUT_DIR = os.path.dirname(args.GMSHFILE.name)
        except BaseException:
            try:
                args.OUT_DIR = os.path.dirname(args.VTKFILE.name)
            except BaseException:
                print("\n***You need to input an unstructured mesh. Exiting...***")
                exit()
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                try:
                    args.DIR_out = os.path.dirname(args.GMSHFILE.name)
                except BaseException:
                    try:
                        args.DIR_out = os.path.dirname(args.VTKFILE.name)
                    except BaseException:
                        print("\n***You need to input an unstructured mesh. Exiting...***")

        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise

    # Output file name prefix
    if args.PREFIX is None:
        try:
            args.PREFIX = os.path.splitext(os.path.basename(args.GMSHFILE.name))[0]
        except BaseException:
            try:
                args.DIR_out = os.path.dirname(args.VTKFILE.name)
            except BaseException:
                print("\n***You need to input an unstructured mesh. Exiting...***")
                exit()

    return args


def deformImageFromFieldParser(parser):
    parser.add_argument('inFile',
                        metavar='inFile',
                        type=argparse.FileType('r'),
                        help='Path to TIFF file containing the image to deform')

    parser.add_argument('-a',
                        '-triangulation-alpha-value',
                        type=float,
                        default=0.0,
                        dest='TRI_ALPHA',
                        help='CGAL Alpha value for triangulation cleanup (negative = auto, zero = no cleanup, positive = userval). Default = 0')

    parser.add_argument('-pf',
                        '-phiFile',
                        dest='PHIFILE',
                        default=None,
                        type=argparse.FileType('r'),
                        help="Path to TSV file containing the deformation function field (required)")

    parser.add_argument('-rad',
                        '--radius-limit',
                        type=float,
                        default=None,
                        dest='RADIUS',
                        help='Assume a sample which is a cylinder with the axis in the z-direction. Exclude points outside a given radius. Use Default = None')

    #parser.add_argument('-rl',
                        #'--radii-from-labelled',
                        #type=str,
                        #default=None,
                        #dest='RADII_LABELLED_FILE',
                        #help='Load a labelled image and compute radii? Only necessary if -tri is activated')

    parser.add_argument('-pfb',
                        '--phiFile-bin-ratio',
                        type=int,
                        default=1,
                        dest='PHIFILE_BIN_RATIO',
                        help="Ratio of binning level between loaded F file and current calculation. If the input F file has been obtained on a 500x500x500 image and now the calculation is on 1000x1000x1000, this should be 2. Default = 1")

    parser.add_argument('-od',
                        '--out-dir',
                        type=str,
                        default=None,
                        dest='OUT_DIR',
                        help="Output directory, default is the dirname of gmsh file")

    parser.add_argument('-pre',
                        '--prefix',
                        type=str,
                        default=None,
                        dest='PREFIX',
                        help='Prefix for output files (without extension). Default is basename of mesh file')

    args = parser.parse_args()

    # If we have no out dir specified, deliver on our default promise -- this can't be done inline before since parser.parse_args() has not been run at that stage.
    if args.OUT_DIR is None:
        args.OUT_DIR = os.path.dirname(args.inFile.name)
        # However if we have no dir, notice this and make it the current directory.
        if args.OUT_DIR == "":
            args.OUT_DIR = "./"
    else:
        # Check existence of output directory
        try:
            if args.OUT_DIR:
                os.makedirs(args.OUT_DIR)
            else:
                args.DIR_out = os.path.dirname(args.lab1.name)
        except OSError:
            if not os.path.isdir(args.OUT_DIR):
                raise
    # Output file name prefix
    if args.PREFIX is None:
        args.PREFIX = os.path.splitext(os.path.basename(args.inFile.name))[0] + "-def"


    return args
