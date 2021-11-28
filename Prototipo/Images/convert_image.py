# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 17:39:06 2021

@author: matheus.schenatto
"""

import cv2
import os
import pydicom

class ConvertDicomToPNG():
    def convert(self, image_path = None):
        INPUT_DICOM_PATH = image_path
        OUTPUT_DICOM_PATH = "./Images/png/"
        
        path = os.path.normpath(image_path)
        name = path.split('\\')[-1].split('.')[0]
        
        ds = pydicom.dcmread(INPUT_DICOM_PATH)
        img = ds.pixel_array    
       
        cv2.imwrite(OUTPUT_DICOM_PATH + name + '.png', img)

        return OUTPUT_DICOM_PATH + name + '.png'