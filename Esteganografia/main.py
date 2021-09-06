# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 21:34:05 2021

@author: mathe
"""
"""
BPCS Steganography: encoding/decoding messages hidden in a vessel image
Source: http://web.eece.maine.edu/~eason/steg/SPIE98.pdf
BEHAVIORS:
    encoding
        * expects a vessel image file, message file, and alpha value
        * hides the contents of a file inside a vessel image
    decoding
        * expects a vessel image file, and alpha value
        * recovers the message stored inside a vessel image
    capacity
        * expects a vessel image file and alpha value
        * assesses the maximum size of a message that could be encoded within the vessel image
    test
        * runs the unit tests
"""
import os.path
import argparse

#from .bpcs_steg_decode import decode
from bpcs_steg_encode import encode
from bpcs_steg_capacity import capacity
#from .bpcs_steg_test import test_all


alpha = 0.45
vslfile = 'other.dcm'
#vslfile = 'vessel.png'
msgfile = 'message.txt' # can be any type of file
encfile = 'encoded.png'
msgfile_decoded = 'tmp.txt'

capacity(vslfile, alpha) # check max size of message you can embed in vslfile
encode(vslfile, msgfile, encfile, alpha) # embed msgfile in vslfile, write to encfile