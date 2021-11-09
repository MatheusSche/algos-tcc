# -*- coding: utf-8 -*-
"""
Created on Sat Aug 21 17:26:23 2021
@author: mathe
"""

import pydicom as dicom
import numpy as np
import cv2

DELIM = ";;;"
encoding = "none"
MSG = 'Matheus Schenatto'
encCount = 0

class LSB():

    def text2uint8mask(self, msg):
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

    def apply_LSB(self, data, mask):
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

    def lsb_encode(self, data, message):
        enc_msg = message + DELIM    
        enc_mask = self.text2uint8mask(enc_msg)   
        enc_data = self.apply_LSB(data, enc_mask)
        
        return enc_data
    

    def encode(self, image, message):
        dim = image.shape
        data = image.ravel()    
        data = self.lsb_encode(data, message)  
        data.shape = (dim)
        image.data = data.tobytes()
        
        return image


    def uint8mask2text(self, maskarr):
        msg = ""
        destchar = np.zeros(1, np.uint8)

        for char in range(0, maskarr.size, 8):
            destchar[0] = 0
            for shift in range(8):
                if(maskarr[char + shift] == 1):
                    destchar[0] = destchar[0] | (0x1 << (7 - shift))
            
            if(destchar[0] != 0):    
                
                if len(str(destchar.tobytes()).strip()) % 4 == 0:
                    msg += destchar.tobytes().decode() 
            
        return msg


    def lsb_decode(self, data):
        ext_mask = (data & 1).astype(np.uint8)
        ext_msg = self.uint8mask2text(ext_mask)
        
        # Find the last occurrence of the delimiter
        last_pos = ext_msg.rfind(DELIM)
        if last_pos == -1:
            print("Could not find any message delimiters")
        
        ext_msg = ext_msg[:last_pos]

        return ext_msg
    

    def decode(self, image):
        data = image.data
        data = image.ravel()
        
        msg_list = self.lsb_decode(data)
        
        return msg_list


    def main_lsb(self, image_path_from, msg):  
        image_path = image_path_from
        ds = dicom.dcmread(image_path)
        message = msg
        image_array = ds.pixel_array
        
        image = self.encode(image_array, message)
        ds.PixelData = image.tobytes()
        
        return ds

    def encode_image(self, path_image, text):
        ds = self.open_dicom(path_image)
        image_array = ds.pixel_array

        image = self.encode(image_array, text)
        ds.PixelData = image.tobytes()

        # salva dicom esteganografado
        name = path_image.split('\\')[-1].split('.')[0] + '_stego' + '.dcm'
        print(name)
        ds.save_as('./Images/dcm/' + name)

        # salva png apenas para exibição
        esteg_ds = self.open_dicom('./Images/dcm/'+ name)
        name_png = name.replace('.dcm', '.png')

        cv2.imwrite('./Images/png/' + name_png, esteg_ds.pixel_array)
        #retorna só o path da imagem
        return './Images/png/' + name_png 

    def decode_image(self, path_image):
        ds = self.open_dicom(path_image)
        image_array = ds.pixel_array

        mensagem_extraida = self.decode(image_array)
        print(mensagem_extraida)
        #retorna só o path da imagem
        return mensagem_extraida

    def save_png(self):
        pass

    def open_dicom(self, path_image):
        return dicom.dcmread(path_image)
