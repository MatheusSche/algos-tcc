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
        private_key = RSA.generate(3072)
        public_key = private_key.publickey()

        with open("./Chaves/private_key.pem", "wb") as file:
            file.write(private_key.exportKey('PEM'))
            file.close()

        with open("./Chaves/public_key.pem", "wb") as file:
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
       
        return decrypted.decode()    