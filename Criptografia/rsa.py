# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 17:39:06 2021

@author: matheus.schenatto
"""

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
##############################################################################
# Gera as chaves
##############################################################################

keyPair = RSA.generate(3072)

pubKey = keyPair.publickey()
print(f"Public key:  (n={hex(pubKey.n)}, e={hex(pubKey.e)})")
pubKeyPEM = pubKey.exportKey()
print(pubKeyPEM.decode('ascii'))

print(f"Private key: (n={hex(pubKey.n)}, d={hex(keyPair.d)})")
privKeyPEM = keyPair.exportKey()
print(privKeyPEM.decode('ascii'))
##############################################################################

##############################################################################
# Encripta
##############################################################################

msg = b'#0010-0010#PatientName#PN#Diego Alcoforado Aires#;#0010-0020#PatientID#LO#010101B4#;#0010-0030#PatientBirthDate#DA#20000318#;#0010-0040#PatientSex#CS#M#;#0010-1000#OtherPatientIDs#LO#1987365293747#;#0010-1030#PatientWeight#DS#70#;#0010-21C0#PregnancyStatus#US#4#;'
encryptor = PKCS1_OAEP.new(pubKey)
encrypted = encryptor.encrypt(msg)
print("Encrypted:", binascii(encrypted))
##############################################################################

##############################################################################
# DEncripta
##############################################################################
decryptor = PKCS1_OAEP.new(keyPair)
decrypted = decryptor.decrypt(encrypted)
print('Decrypted:', decrypted)

##############################################################################



