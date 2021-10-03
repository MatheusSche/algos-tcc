# -*- coding: utf-8 -*-
"""
Created on Sun Sep 26 16:01:18 2021

@author: matheus.schenatto
"""

import numpy as np

from bpcs_codes.logger import log
from bpcs_codes.array_grid import get_next_grid_dims
from bpcs_codes.act_on_image import ActOnImage
from bpcs_codes.array_message import write_conjugated_message_grids
from bpcs_codes.bpcs_steg import arr_bpcs_complexity

def remove_message_from_vessel(arr, alpha, grid_size):
    messages = []
    nfound, nkept, nleft = 0, 0, 0
    complexities = []
    for dims in get_next_grid_dims(arr, grid_size):
        nfound += 1
        grid = arr[tuple(dims)]
        cmplx = arr_bpcs_complexity(grid)
        if cmplx < alpha:
            nleft += 1
            continue
        complexities.append(cmplx)
        nkept += 1
        messages.append(grid)
    assert nfound == nkept + nleft
    log.critical('Found {0} out of {1} grids with complexity above {2}'.format(nkept, nfound, alpha))
    return messages

class BPCSDecodeImage(ActOnImage):
    def modify(self, alpha):
        return remove_message_from_vessel(self.arr, alpha, (8,8))

def decode(infile, outfile, alpha=0.45):
    x = BPCSDecodeImage(infile, as_rgb=True, bitplane=True, gray=True, nbits_per_layer=8)
    grids = x.modify(alpha)
    write_conjugated_message_grids(outfile, grids, alpha)