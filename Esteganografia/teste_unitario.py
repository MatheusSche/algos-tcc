# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 20:09:51 2021

@author: matheus.schenatto
"""

import os
import pydicom
import matplotlib.pylab as plt
import cv2
import numpy as np
import imutils

def open_image(img_path):
    ds = pydicom.dcmread(img_path)
    img = ds.pixel_array 
    return img

def ssd(A, B):
    grayA = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    #s = np.sum((np.array(grayA, dtype=np.float)**2 - np.array(grayB, dtype=np.float)**2))
    #s = np.sum(np.abs(np.subtract(grayA,grayB,dtype=np.float))**2)
    s = np.sum(np.abs(grayA-grayB)**2)
    #s = np.sum(np.square(grayA - grayB))
    #s = np.sum((grayA[:,:,0:3]-grayB[:,:,0:3])**2)
    
    return s

def sad(A, B):
    grayA = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    
    #vec1, vec2 = grayA.reshape(-1), grayB.reshape(-1)
    #s = np.sum(np.abs(grayA-grayB))
    #s = np.sum(np.abs(np.subtract(grayA,grayB,dtype=np.float)))
    s = np.sum(np.abs(grayA - grayB))
  
    return s

def ssd2(A,B):
    grayA = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    
    dif = grayA.ravel() - grayB.ravel()
    return np.dot( dif, dif )


original_path = './vessels_rgb/coracao_02.dcm'
path = './steg_objects/lsb_coracao_02.dcm'

A = open_image(original_path)
B = open_image(path)

y = sad(A, B)
x = ssd(A, B)

z = ssd2(A, B)

print(x, y, z)    
















def ssd(A, B):
    s = np.sum(np.abs(A-B)**2)    
    return s

def sad(A, B):
    s = np.sum(np.abs(A - B))
    return s

def mad(A, B):
    s = np.max(np.abs(np.array(A) - np.array(B)))
    return s