# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 17:26:23 2021

@author: mathe
"""

import pydicom as dicom
import matplotlib.pylab as plt
import numpy as np

DELIM = ";;;"
encoding = "none"
MSG = 'Matheus Schenatto'
encCount = 0

def text2uint8mask(msg):
    msgarr = np.frombuffer(msg.encode(), dtype=np.uint8)
    msglen = msgarr.size
    maskarr = np.zeros(msglen * 8, dtype=np.uint8)

    arrind = 0
    for char in msgarr:
        for shift in range(8):
            if(arrind == maskarr.size):
                break
            if(char & (0x1 << (7 - shift))):
                maskarr[arrind] = 1
            else:
                maskarr[arrind] = 0
            arrind += 1

     
    return maskarr



def apply_LSB(data, mask):
    global encCount
   
    numMasks = 1
    newmask = mask

    for i in range(0, newmask.size):
        if(newmask[i] == 0):
            data[i] &= (~newmask[i] - 1)
        else:
            data[i] |= newmask[i]

    encCount += numMasks

    return data   

def lsb_encode(data):
    enc_msg = MSG + DELIM
    
    enc_mask = text2uint8mask(enc_msg)
    
    enc_data = apply_LSB(data, enc_mask)
    
    return enc_data
    

def encode(image):
    dim = image.shape
    data = image.ravel()
    print(data)
    
    data = lsb_encode(data)
    
    data.shape = (dim)
    image.data = data.tobytes()
    return image


def uint8mask2text(maskarr):
    msg = ""
    destchar = np.zeros(1, np.uint8)
    #if(True != isinstance(maskarr[0], np.uint8)):
    #    raise Exception("uint8mask2text: array is not of type numpy.uint8")

    for char in range(0, maskarr.size, 8):
        destchar[0] = 0
        for shift in range(8):
            if(maskarr[char + shift] == 1):
                destchar[0] = destchar[0] | (0x1 << (7 - shift))

        
        if(destchar[0] != 0):
            #print(msg, type(destchar.tobytes()))        
            
            if len(str(destchar.tobytes()).strip()) % 4 == 0:
                msg += destchar.tobytes().decode() 
            
            
                   
    return msg


def lsb_decode(data):
    ext_mask = (data & 1).astype(np.uint8)
    ext_msg = uint8mask2text(ext_mask)
    
    # Find the last occurrence of the delimiter
    last_pos = ext_msg.rfind(DELIM)
    print(last_pos)
    if last_pos == -1:
        print("Could not find any message delimiters")
    
    ext_msg = ext_msg[:last_pos]
    print(ext_msg)
    return ext_msg
    

def decode(image):
    #data = image.data
    data = image.ravel()
    
    msg_list = lsb_decode(data)
    
    print(msg_list)



# specify your image path
image_path = 'images/cranio01.dcm'
ds = dicom.dcmread(image_path)
image_array = ds.pixel_array

image = encode(image_array)

plt.imshow(image)

image_decoded = decode(image)

plt.imshow(image_decoded)


