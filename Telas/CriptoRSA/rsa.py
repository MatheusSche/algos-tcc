# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 17:39:06 2021

@author: matheus.schenatto
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii

class GeraChaves():
    def gera(self):
        # private_key = RSA.generate(3072)
        # public_key = private_key.publickey()
        
        # with open ("private.pem", "wb") as prv_file:
        #     #print("{}".format(private_key.exportKey()), file=prv_file)
        #     prv_file.write(private_key.exportKey('PEM'))

        # with open ("public.pem", "wb") as pub_file:
        #     pub_file.write(public_key.exportKey('PEM'))
        #     #print("{}".format(public_key.exportKey()), file=pub_file)
        private_key = RSA.generate(3072)
        public_key = private_key.publickey()

        with open("private_key.pem", "wb") as file:
            file.write(private_key.exportKey('PEM'))
            file.close()

        with open("public_key.pem", "wb") as file:
            file.write(public_key.exportKey('PEM'))
            file.close()

    def encripta(self, chave, texto):
        # Lê a chave
        public_key = None
        with open(chave, "rb") as file:
            public_key = RSA.importKey(file.read())
        #Criptografa
        encryptor = PKCS1_OAEP.new(public_key)
        encrypted = encryptor.encrypt(texto.encode())
        
        #retorna
        return encrypted

    def decripta(self, chave, encrypted):
        
        with open(chave, "rb") as file:
            private_key = RSA.importKey(file.read())

        decryptor = PKCS1_OAEP.new(private_key)
        decrypted = decryptor.decrypt(encrypted)
        print('Decrypted:', decrypted)    