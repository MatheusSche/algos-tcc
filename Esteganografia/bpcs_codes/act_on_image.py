# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 21:35:49 2021

@author: mathe
"""

import numpy as np
from PIL import Image 
import pydicom as dicom
import matplotlib.pylab as plt
import cv2

from bpcs_codes.logger import log
from bpcs_codes.array_bit_plane import BitPlane

def load_image(infile, as_rgb):
    
    ds = dicom.dcmread(infile)
    img = ds.pixel_array
   
    return img, ds

def write_image(outfile, im, ds):
    # save pixel data and dicom file
    ds.PixelData = im.tobytes()
    
    ds.save_as(outfile)
    
    return ds


def image_to_array(im):
    return np.array(im)

def array_to_image(arr):
    return Image.fromarray(np.uint8(arr))

class ActOnImage(object):
    def __init__(self, infile, as_rgb, bitplane, gray, nbits_per_layer):
        self.infile = infile
        self.as_rgb = as_rgb
        self.bitplane  = bitplane
        self.gray = gray
        self.nbits_per_layer = nbits_per_layer
        self.ds = None
        self.arr = self.read(infile)
        log.critical('Loaded image as array with shape {0}'.format(self.arr.shape))

    def read(self, infile):
        im, self.ds = load_image(infile, self.as_rgb)
        arr = image_to_array(im)
        
        if self.bitplane:
            arr = BitPlane(arr, self.gray).slice(self.nbits_per_layer)
        return arr

    def modify(self):
        raise NotImplementedError()

    def write(self, outfile, arr):
        if self.bitplane:
            arr = BitPlane(arr, self.gray).stack()
        im = array_to_image(arr)
        log.critical('Loaded new array as image')
        ds_return = write_image(outfile, im, self.ds)
        
        return ds_return