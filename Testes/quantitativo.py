# -*- coding: utf-8 -*-
"""
Created on Sat Aug 14 17:10:17 2021

@author: mathe
"""

import numpy as np
import cv2
from sewar.full_ref import mse, rmse, psnr, uqi, ssim, ergas, scc, rase, sam, msssim, vifp


def open_image(img_path):
    img = cv2.imread(img_path)
    return img


def ssd(A, B):
    s = ((A-B)**2).sum()
    return s

'''

def ssd(A, B):
    s = ((A-B)**2).sum()
    return s

def sad(A, B):
    vec1, vec2 = A.reshape(-1), B.reshape(-1)
    s = np.sum(np.abs (vec1-vec2))
    return s

def mad(A, B):
   s = np.max(np.abs(np.array(A) - np.array(B)))
   print(np.abs(np.array(A) - np.array(B)))
   return s
'''

a_path = 'images/mri.jpg'
b_path = 'images/salt.jpg'
c_path = 'images/salt_rec.jpg'

A = open_image(a_path)
B = open_image(b_path)
C = open_image(c_path)

print("SSD: ",ssd(B, A))
print("MSE: ", mse(B,A))
print("RMSE: ", rmse(B, A))
print("PSNR: ", psnr(B, A))
print("SSIM: ", ssim(B, A))
print("UQI: ", uqi(B, A))
print("MSSSIM: ", msssim(B, A))
print("ERGAS: ", ergas(B, A))
print("SCC: ", scc(B, A))
print("RASE: ", rase(B, A))
print("SAM: ", sam(B, A))
print("VIF: ", vifp(B, A))

'''
result_ssd1 = ssd1(A, B)
result_ssd2 = ssd2(A, B)
result_ssd3 = calculate_ssd(A, B)
#result_sad = sad(A, B)
#result_mad = mad(A, B)

print(result_ssd1, result_ssd2, result_ssd3)
'''