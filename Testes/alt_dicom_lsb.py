# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 18:44:33 2021

@author: mathe
"""

import pydicom as dicom
import matplotlib.pylab as plt
import numpy as np
from PIL import Image

DELIM = ";;;"
encoding = "none"
MSG = 'Matheus Schenatto'

def Encode(src, message, dest):
    
    ds = dicom.dcmread(src)
    img = ds.pixel_array
    width, height, bits_layers = img.shape

    array = np.array(img.ravel())
    array = array.reshape(-1, 3)
 

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
                    print(array[p][q])
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

        array=array.reshape(height, width, n)
        plt.imshow(array)
        
        ds.PixelData = array.tobytes()
        ds.save_as(dest)
        
        #enc_img = Image.fromarray(array.astype('uint8'), img.mode)
        #enc_img.save(dest)
        print("Image Encoded Successfully")
        

def Decode(src):

    ds = dicom.dcmread(src)
    img = ds.pixel_array
    width, height, bits_layers = img.shape

    array = np.array(img.ravel())
    array = array.reshape(-1, 3)

    n = 3    

    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += (bin(array[p][q])[2:][-1])

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    for i in range(len(hidden_bits)):
        if message[-5:] == "$t3g0":
            break
        else:
            message += chr(int(hidden_bits[i], 2))
    if "$t3g0" in message:
        print("Hidden Message:", message[:-5])
    else:
        print("No Hidden Message Found")
        

image_path = 'other1.dcm'



image_encode = Encode(image_path, MSG, 'TEST.dcm')
        
src = 'TEST.dcm'


Decode(src)