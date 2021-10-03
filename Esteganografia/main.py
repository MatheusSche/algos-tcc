# -*- coding: utf-8 -*-
"""
Created on Sat Oct  2 21:39:48 2021

@author: matheus.schenatto
"""
import os
import pydicom
import matplotlib.pylab as plt
from lsb import main_lsb
from bpcs import main_bpcs
from dct import main_dct

pasta = './vessels_rgb'

index = 0

for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        path = os.path.join(os.path.realpath(diretorio), arquivo)
        
        ###################################################################
        # BPCS PART
        
        image = main_bpcs(path, 'HI!')
        output_file = "./steg_objects/" + "" + "bpcs_" + arquivo
        
        image.save_as(output_file)
        
        index_plot = index + 10
        
        plt.figure(index_plot)
        plt.imshow(image.pixel_array)
        
        ###################################################################
        
        ###################################################################
        # LSB PART
        
        image = main_lsb(path, 'HI!')
        output_file = "./steg_objects/" + "" + "lsb_" + arquivo
        
        image.save_as(output_file)
        
        index_plot = index + 20
        
        plt.figure(index_plot)
        plt.imshow(image.pixel_array)
        
        ###################################################################
        
        ###################################################################
        # DCT PART
        try:
            image = main_dct(path, 'HI!')
            output_file = "./steg_objects/" + "" + "dct_" + arquivo
            
            image.save_as(output_file)
            
            index_plot = index + 30
    
            plt.figure(index_plot)
            plt.imshow(image.pixel_array)
        
        except Exception as e:
            print(e)
            print()
            print(arquivo)
            print()
      
        
    
        ###################################################################
        
        index += 1
       


'''
image = main_lsb('other.dcm', 'HI!', 'SAD')

plt.figure(1)
plt.imshow(image.pixel_array)


image = main_bpcs('other.dcm', 'HI!')

plt.figure(2)
plt.imshow(image.pixel_array)

image = main_dct('other.dcm', 'HI!')

plt.figure(3)
plt.imshow(image.pixel_array)
'''