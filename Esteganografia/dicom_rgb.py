# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 16:39:53 2021

@author: mathe
"""
import os
import numpy as np
import pydicom
from PIL import Image, ImageDraw
import matplotlib.pylab as plt

# your file paths
#INPUT_DICOM_PATH = 'images/cranio01.dcm'
MASK_PATH = ''
OUTPUT_DICOM_PATH = 'vessels_rgb/'

def apply_ct_window(img, window):
    # window = (window width, window level)
    R = (img-window[1]+0.5*window[0])/window[0]
    R[R<0] = 0
    R[R>1] = 1
    return R


pasta = 'vessels'
index = 0

for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        path = os.path.join(os.path.realpath(diretorio), arquivo)
     
        INPUT_DICOM_PATH = path
        OUTPUT_DICOM_PATH = "./vessels_rgb/" + arquivo
        print(arquivo)
        ds = pydicom.dcmread(INPUT_DICOM_PATH)
        img = ds.pixel_array # dtype = uint16
        img = img.astype(float)
        img = img*ds.RescaleSlope + ds.RescaleIntercept
        
        display_img = apply_ct_window(img, [400,50])
        
        plt.figure(index)
        plt.imshow(display_img)
        
        img_bbox = Image.fromarray((255*display_img).astype('uint8'))
        
        img_bbox = img_bbox.convert('RGB')
        
        img_bbox = np.asarray(img_bbox)
        
        
        # modify DICOM tags
        ds.PhotometricInterpretation = 'RGB'
        ds.SamplesPerPixel = 3
        ds.BitsAllocated = 8
        ds.BitsStored = 8
        ds.HighBit = 7
        ds.PixelRepresentation = 0
        ds.add_new(0x00280006, 'US', 0)
        ds.is_little_endian = True
        ds.fix_meta_info()
        
        plt.figure(3)
        plt.imshow(img_bbox)
        
        
        # save pixel data and dicom file
        ds.PixelData = img_bbox.tobytes()
        
        plt.figure(2)
        plt.imshow(ds.pixel_array)
        
        
        ds.save_as(OUTPUT_DICOM_PATH)
        
        print(index)
        
        index += 1








