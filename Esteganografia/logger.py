# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 21:35:02 2021

@author: mathe
"""

import logging

def get_log():
    log = logging.getLogger('bpcs-steg')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    log.addHandler(ch)
    return log

log = get_log()