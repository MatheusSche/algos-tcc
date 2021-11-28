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
import imutils

from skimage.metrics import structural_similarity as ssim

from sewar.full_ref import mse, rmse

INDEX = 0

individual_values = []

def open_image(img_path):
    ds = pydicom.dcmread(img_path)
    img = ds.pixel_array 
    return img

def test_mse(B, A):
    
    return mse(B,A)

def test_rmse(B, A):
    
    return rmse(B,A)


def test_ssim(A, B, method, original):
    grayA = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    (score, diff) = ssim(grayA, grayB, full=True)

    #plt.figure(1)    
    #plt.imshow(diff)
    destaca_diferencas(A, B, diff, method, original)
    
    return score
'''
def ssd(A, B):
    grayA = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    s = ((grayA-grayB)**2).sum()
    return s
'''
def ssd(A, B):
    grayA = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    #s = np.sum((np.array(grayA, dtype=np.float) - np.array(grayB, dtype=np.float))**2)
    #s = np.sum(np.abs(np.subtract(grayA,grayB,dtype=np.float))**2)
    #s = np.sum(np.abs(grayA-grayB)**2)
    s = np.sum(np.square(grayA - grayB))
    print(np.square(grayA - grayB))
    return s

def sad(A, B):
    grayA = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    
    #vec1, vec2 = grayA.reshape(-1), grayB.reshape(-1)
    #s = np.sum(np.abs(grayA-grayB))
    #s = np.sum(np.abs(np.subtract(grayA,grayB,dtype=np.float)))
    s = np.sum(np.abs(grayA - grayB))
    print(np.abs(grayA - grayB))
    return s

def mad(A, B):
    grayA = cv2.cvtColor(A, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(B, cv2.COLOR_BGR2GRAY)
    
    s = np.max(np.abs(np.array(grayA) - np.array(grayB)))
    #print(np.abs(np.array(A) - np.array(B)))
    return s

def destaca_diferencas(imageA, imageB, diff, method, original):
    cv2.imwrite("./diferencas/" + method + "/" + method + "_" + "a_" + original.split('.')[0] + ".png", imageA)
    cv2.imwrite("./diferencas/" + method + "/" + method + "_" + "b_" + original.split('.')[0]  + ".png", imageB)
    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    diff = (diff * 255).astype("uint8")
    thresh = cv2.threshold(diff, 0, 255,
    	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    
    for c in cnts:
    	# compute the bounding box of the contour and then draw the
    	# bounding box on both input images to represent where the two
    	# images differ
    	(x, y, w, h) = cv2.boundingRect(c)
    	cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
    	cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
    # show the output images
    #cv2.imshow("Original", imageA)
    #cv2.imshow("Modified", imageB)
    #cv2.imshow("Diff", diff)
    #cv2.imshow("Thresh", thresh)
    #cv2.waitKey(0)
    
    print("./diferencas/" + method + "/" + method + "_" + original.split('.')[0]  + ".png")
    
    cv2.imwrite("./diferencas/" + method + "/" + method + "_" + original.split('.')[0] + ".png", imageA)
    cv2.imwrite("./diferencas/" + method + "/" + method + "_" + "imageB_" + original.split('.')[0]  + ".png", imageB)
    cv2.imwrite("./diferencas/" + method + "/" + method + "_" + "diff_" + original.split('.')[0]  + ".png", diff)
    cv2.imwrite("./diferencas/" + method + "/" + method + "_" + "thresh_" + original.split('.')[0]  + ".png", thresh)


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
    print('SSIM')
    result_ssim = test_ssim(A, B, method, arquivo_original)
    print(result_ssim)
    print('------------------------------------------------------------------')
    print('------------------------------------------------------------------')
    print('MSE')
    result_mse = test_mse(B, A)
    print(result_mse)
    print('------------------------------------------------------------------')
    print('------------------------------------------------------------------')
    print('RMSE')
    result_rmse = test_rmse(B, A)
    print(result_rmse)
    print('------------------------------------------------------------------')
    
    
    individual_values.append( (arquivo_original, 
                               method, 
                               result_ssd, 
                               result_sad, 
                               result_mad, 
                               result_ssim,
                               result_mse,
                               result_rmse)
                             )
    
    return result_ssd, result_sad, result_mad, result_ssim, result_mse, result_rmse


def find_equivalent_method(original_path, arquivo_original, method):
    pasta_02 = './steg_objects/'
    
    soma_ssd = 0
    soma_sad = 0
    soma_mad = 0
    soma_ssim = 0
    soma_mse = 0
    soma_rmse = 0
    
    for diretorio, subpastas, arquivos in os.walk(pasta_02):
        for arquivo in arquivos:
            path = os.path.join(os.path.realpath(diretorio), arquivo)
            
            exame_part_original = arquivo_original.split('_')[0] + arquivo_original.split('_')[1]
            exame_part_method = arquivo.split('_')[1] + arquivo.split('_')[2]
            
            
            
            if arquivo.startswith(method) and exame_part_original == exame_part_method:
                print(exame_part_original, exame_part_method)
                a,b,c,d, e, f = compare_images(original_path, path, arquivo_original, method)
                soma_ssd += a
                soma_sad += b
                soma_mad += c
                soma_ssim += d
                soma_mse += e
                soma_rmse += f
    
                return soma_ssd, soma_sad, soma_mad, soma_ssim, soma_mse, soma_rmse


pasta = './vessels_rgb'

soma_ssd_lsb = 0
soma_sad_lsb = 0
soma_mad_lsb = 0
soma_ssim_lsb = 0
soma_mse_lsb = 0
soma_rmse_lsb = 0

soma_ssd_dct = 0
soma_sad_dct = 0
soma_mad_dct = 0
soma_ssim_dct = 0
soma_mse_dct = 0
soma_rmse_dct = 0

soma_ssd_bpcs = 0
soma_sad_bpcs = 0
soma_mad_bpcs = 0
soma_ssim_bpcs = 0
soma_mse_bpcs = 0
soma_rmse_bpcs = 0

for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        path = os.path.join(os.path.realpath(diretorio), arquivo)
        
        (
            ssd_lsb, 
            sad_lsb, 
            mad_lsb, 
            ssim_lsb,
            soma_mse_lsb,
            soma_rmse_lsb
        ) = find_equivalent_method(path, arquivo, 'lsb')
        
        (
            ssd_dct, 
            sad_dct, 
            mad_dct, 
            ssim_dct,
            soma_mse_dct,
            soma_rmse_dct
        ) = find_equivalent_method(path, arquivo, 'dct')
        
        (
            ssd_bpcs, 
            sad_bpcs, 
            mad_bpcs, 
            ssim_bpcs,
            soma_mse_bpcs,
            soma_rmse_bpcs
        ) = find_equivalent_method(path, arquivo, 'bpcs')
        print(arquivo)
        
        soma_ssd_lsb += ssd_lsb
        soma_sad_lsb += sad_lsb
        soma_mad_lsb += mad_lsb
        soma_ssim_lsb += ssim_lsb
        
        soma_ssd_dct += ssd_dct
        soma_sad_dct += sad_dct
        soma_mad_dct += mad_dct
        soma_ssim_dct += ssim_dct
        
        soma_ssd_bpcs += ssd_bpcs
        soma_sad_bpcs += sad_bpcs
        soma_mad_bpcs += mad_bpcs
        soma_ssim_bpcs += ssim_bpcs
        

print()
print('----------------------------------------------------------------------')
print('RESULTADOS FINAIS !!!!')
print('          ',  '  SSD   ', '   SAD   ', '    MAD    ', 'SSIM', 'MSE', 'RMSE')
print('  LSB     ',  soma_ssd_lsb/10,  soma_sad_lsb/10, soma_mad_lsb/10, soma_ssim_lsb/10, soma_mse_lsb/10, soma_rmse_lsb/10)
print('  DCT     ',  soma_ssd_dct/10,  soma_sad_dct/10, soma_mad_dct/10, soma_ssim_dct/10,  soma_mse_dct/10, soma_rmse_dct/10)
print('  BPCS    ',  soma_ssd_bpcs/10, soma_sad_bpcs/10,soma_mad_bpcs/10, soma_ssim_bpcs/10,  soma_mse_bpcs/10, soma_rmse_bpcs/10)


print()


for imagem in individual_values:
    if  imagem[0] == 'coracao_01.dcm':
        print(imagem)
        
        