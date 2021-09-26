# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 15:58:15 2021

@author: matheus.schenatto
"""

import os.path
import argparse

from bpcs_steg_decode import decode

parser = argparse.ArgumentParser()

def check_file_exists(filename):
    if not os.path.exists(filename):
        parser.error('The file "{0}" could not be found.'.format(filename))
        

alpha = 0.45
infile = 'some_secret.dcm'
outfile = 'decoded_secret.txt'
 
        
decode(infile, outfile, alpha)