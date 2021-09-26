# -*- coding: utf-8 -*-
"""
Created on Sun Sep 19 17:47:44 2021

@author: matheus.schenatto
"""

import cv2
import os
import pydicom

inputdir = 'images/'
outdir = './'
#os.mkdir(outdir)

test_list = [ f for f in  os.listdir(inputdir)]

for f in test_list[:10]:   # remove "[:10]" to convert all images 
    ds = pydicom.read_file(inputdir + f) # read dicom image
    img = ds.pixel_array # get image array
    cv2.imwrite(outdir + f.replace('.dcm','.png'),img) # write png image