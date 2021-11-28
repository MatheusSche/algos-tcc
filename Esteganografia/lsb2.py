# -*- coding: utf-8 -*-
"""
Created on Thu Oct 28 18:18:53 2021

@author: matheus.schenatto
"""

import numpy as np
import pydicom as dicom
from PIL import Image

def Encode(src, message, dest):

    ds = dicom.dcmread(src)
    array = ds.pixel_array    

    #img = Image.open(src, 'r')
    width, height, prof = array.shape
    array = np.array(list(array))

    #if img.mode == 'RGB':
    #    n = 3
    #elif img.mode == 'RGBA':
    #    n = 4
    n = 3
    total_pixels = array.size//n

    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        #enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        #enc_img.save(dest)
        print("Image Encoded Successfully")
        return array