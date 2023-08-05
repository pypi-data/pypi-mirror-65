from pyibex import IntervalVector, SepCtcPair, Function, SepFwdBwd
from pyibex.image import CtcRaster
import numpy as np

from vibes import vibes
import gdal
import os

def drawGeotiff(filename, figurename=''):
    try:
        gtiff = gdal.Open(filename)
    except:
        print("ERROR unable to open %s" % filename)
        exit(-1)
    # self.gtiff = gdal.Open( filename )
    geotransform = gtiff.GetGeoTransform()
    basename = os.path.dirname(filename)
    figname, ext = os.path.splitext(os.path.basename(filename))
    if figurename == '':
        print(figname)
        vibes.newFigure(figname)
        vibes.setFigureSize(500, 500)
        vibes.setFigurePos(0, 0)
    rasterName = os.path.abspath(os.path.join(basename, figname+".png"))
    print(rasterName)
    vibes.drawRaster(rasterName, geotransform[0], geotransform[3], geotransform[1], geotransform[5])
    vibes.axisEqual()


def loadGeoImage(filename, fliplr=False, transpose=True):
    basename, ext = os.path.splitext(filename)
    if ext in [".tiff" , ".tif"]:
        try:
            gtiff = gdal.Open(filename)
        except:
            print("ERROR unable to open %s" % filename)

        img = (gtiff.GetRasterBand(1).ReadAsArray())  # .astype(np.uint64)
        geoTranform = list(gtiff.GetGeoTransform())
        # geoTranform[0] -= 0.5*geoTranform[1]
        # geoTranform[3] -= 0.5*geoTranform[5]
    elif ext in [".png"]:
        img = imageio.imread(filename, as_gray=True).astype(np.uint8)

        with open(basename+".pgw", "r") as f:
            gt = [float(l.strip()) for l in f if l.strip() != '']
        geoTranform = [gt[4], gt[0], gt[1], gt[5], gt[2], gt[3] ]
        print(geoTranform)

    if fliplr is True:
        print('fliplr')
        img = np.fliplr(img)
    if transpose is True:
        img = img.T
    return img, geoTranform



class ShapeImage:
    """Shape from images

    This class load a georeferenced image (geotiff or png+pgw) 

    The image is loaded using gdal or imageio.
    Then based 
    Args:
        filename (string): filename .tiff or .png
        fliplr (bool): inverse left and right axis
        tranpose (bool): transpose image

    """
    def __init__(self, filename, fliplr=False, transpose=True):    
        print("load {}".format(filename))
        try:
            gtiff = gdal.Open(filename)
        except:
            print("ERROR unable to open %s" % filename)
        img = (gtiff.GetRasterBand(1).ReadAsArray())  # .astype(np.uint64)
        if fliplr is True:
            print('fliplr')
            img = np.fliplr(img)
        if transpose is True:
            img = img.T
        self.filename = filename

        img_subset = np.zeros(img.shape, dtype=np.uint64)
        img_supset = np.zeros(img.shape, dtype=np.uint64)
        img_subset[img == 1] = 1

        img_subset_in = (1 - img_subset).cumsum(0).cumsum(1)
        img_subset = img_subset.cumsum(0).cumsum(1)

        img_supset[img >= 1] = 1
        img_supset_in = (1 - img_supset).cumsum(0).cumsum(1)
        img_supset = img_supset.cumsum(0).cumsum(1)

        metaData = gtiff.GetMetadata()
        self.t = float(metaData['TIMESTAMP'])
        self.x0 = float(metaData['X'])
        self.y0 = float(metaData['Y'])

        geoTranform = list(gtiff.GetGeoTransform())
        geoTranform[0] -= self.x0
        geoTranform[3] -= self.y0
        # print(geoTranform)


        # print(self.Sp.ctc_in.boundingBox())
        xmax = geoTranform[0] + img.shape[0]*geoTranform[1]
        ymax = geoTranform[3] + img.shape[1]*geoTranform[5]
        xmin = geoTranform[0]
        ymin = geoTranform[3]
        bbox = IntervalVector([xmin, ymin]) | IntervalVector([xmax, ymax])
        sepMask = SepFwdBwd(Function("x", "y", "(x,y)"), bbox)
        self.bbox = bbox

        self.Sp = SepCtcPair(
            CtcRaster(img_supset_in, geoTranform[0], geoTranform[3], geoTranform[1], geoTranform[5], inner=True),
            CtcRaster(img_supset, geoTranform[0], geoTranform[3], geoTranform[1], geoTranform[5])
        )| ~sepMask
        self.Sm = SepCtcPair(
                    CtcRaster(img_subset_in, geoTranform[0], geoTranform[3], geoTranform[1], geoTranform[5], inner=True),
                    CtcRaster(img_subset, geoTranform[0], geoTranform[3], geoTranform[1], geoTranform[5])
        )


    def __repr__(self):
        return "Shape : t={}, (x, y) = ({}, {}) ".format(self.t, self.x0, self.y0)

    def updatePos(self, X, Y):
        self.pos = IntervalVector([X[self.t], Y[self.t]])
