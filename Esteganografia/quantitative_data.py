# -*- coding: utf-8 -*-
"""
Created on Sun Oct  3 02:11:50 2021

@author: matheus.schenatto
"""

import os
import pydicom
import matplotlib.pylab as plt
import cv2
import numpy as np

def open_image(img_path):
    ds = pydicom.dcmread(img_path)
    img = ds.pixel_array 
    return img

def ssd(A, B):
    s = ((A-B)**2).sum()
    return s

def sad(A, B):
    vec1, vec2 = A.reshape(-1), B.reshape(-1)
    s = np.sum(np.abs (vec1-vec2))
    return s

def mad(A, B):
   s = np.max(np.abs(np.array(A) - np.array(B)))
   #print(np.abs(np.array(A) - np.array(B)))
   return s

def compare_images(original_path, path, arquivo_original, method):
    print('------------------------------------------------------------------')
    print('Comparando: ', arquivo_original, ' para o algoritmo ', method)
    print('------------------------------------------------------------------')
    A = open_image(original_path)
    B = open_image(path)
    
    print('SSD')
    result_ssd = ssd(A, B)
    print(result_ssd)
    print('------------------------------------------------------------------')
    print('SAD')
    result_sad = sad(A, B)
    print(result_sad)
    print('------------------------------------------------------------------')
    print('MADD')
    result_mad = mad(A, B)
    print(result_mad)
    print('------------------------------------------------------------------')
    
    return result_ssd, result_sad, result_mad


def find_equivalent_method(original_path, arquivo_original, method):
    pasta_02 = './steg_objects'
    
    soma_ssd = 0
    soma_sad = 0
    soma_mad = 0
    
    for diretorio, subpastas, arquivos in os.walk(pasta_02):
        for arquivo in arquivos:
            path = os.path.join(os.path.realpath(diretorio), arquivo)
            
            exame_part_original = arquivo_original.split('_')[0] + arquivo_original.split('_')[1]
            exame_part_method = arquivo.split('_')[1] + arquivo.split('_')[2]
            
            
            
            if arquivo.startswith(method) and exame_part_original == exame_part_method:
                print(exame_part_original, exame_part_method)
                a,b,c = compare_images(original_path, path, arquivo_original, method)
                soma_ssd += a
                soma_sad += b
                soma_mad += c
    
    return soma_ssd, soma_sad, soma_mad


pasta = './vessels_rgb'

soma_ssd_lsb = 0
soma_sad_lsb = 0
soma_mad_lsb = 0

soma_ssd_dct = 0
soma_sad_dct = 0
soma_mad_dct = 0

soma_ssd_bpcs = 0
soma_sad_bpcs = 0
soma_mad_bpcs = 0

for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        path = os.path.join(os.path.realpath(diretorio), arquivo)
        
        soma_ssd_lsb, soma_sad_lsb, soma_mad_lsb = find_equivalent_method(path, arquivo, 'lsb')
        soma_ssd_dct, soma_sad_dct, soma_mad_dct = find_equivalent_method(path, arquivo, 'dct')
        soma_ssd_bpcs, soma_sad_bpcs, soma_mad_bpcs = find_equivalent_method(path, arquivo, 'bpcs')
        print(arquivo)
        

print()
print('----------------------------------------------------------------------')
print('RESULTADOS FINAIS !!!!')
print('          ',  '  SSD   ', '   SAD   ', '    MAD    ')
print('  LSB     ',  soma_ssd_lsb/10,  soma_sad_lsb/10, soma_mad_lsb/10)
print('  DCT     ',  soma_ssd_dct/10,  soma_sad_dct/10, soma_mad_dct/10)
print('  BPCS    ',  soma_ssd_bpcs/10, soma_sad_bpcs/10,soma_mad_bpcs/10)
        
        