# -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 18:11:55 2021

@author: matheus.schenatto
"""

import os
import pydicom


pasta = './vessels_rgb'

index = 0


for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        path = os.path.join(os.path.realpath(diretorio), arquivo)
        
        INPUT_DICOM_PATH = path
        OUTPUT_DICOM_PATH = "./vessels_rgb/" + arquivo
  
        ds = pydicom.dcmread(INPUT_DICOM_PATH)
        
        print(arquivo, ds.pixel_array.shape, ds.pixel_array.nbytes)
        