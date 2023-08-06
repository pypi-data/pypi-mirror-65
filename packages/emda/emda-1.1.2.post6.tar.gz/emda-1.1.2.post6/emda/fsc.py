"""
Author: "Rangana Warshamanage, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import fcodes_fast
from .config import *

#debug_mode = 1 # 0: no debug info, 1: debug

def halfmaps_fsc_variance(hf1,hf2,bin_idx,nbin):
    assert hf1.shape == hf2.shape
    nx,ny,nz = hf1.shape
    fo,eo,noisevar,signalvar,totalvar,bin_fsc,bincount = fcodes_fast.calc_fsc_using_halfmaps(hf1,
                                                    hf2,
                                                    bin_idx,
                                                    nbin,
                                                    debug_mode,
                                                    nx,
                                                    ny,
                                                    nz)
    return bin_fsc,noisevar,signalvar,totalvar,fo,eo

def anytwomaps_fsc_covariance(f1,f2,bin_idx,nbin):
    assert f1.shape == f2.shape
    nx,ny,nz = f1.shape
    f1f2_covar,bin_fsc,bincount = fcodes_fast.calc_covar_and_fsc_betwn_anytwomaps(f1,
                                                                f2,
                                                                bin_idx,
                                                                nbin,
                                                                debug_mode,
                                                                nx,ny,nz)
    return bin_fsc,f1f2_covar

def predict_fsc(hf1,hf2,bin_idx,nbin,nparticles):
    fsc,noise,signal,total,_,_ = halfmaps_fsc_variance(hf1,hf2,bin_idx,nbin)
    factors = nparticles
    print(factors)
    predicted_fsc_lst = []
    for i in range(len(nparticles)):
        predicted_fsc_lst.append(signal / (signal + noise * factors[i]))
    predicted_fsc_lst.append(2 * fsc/(1.0 + fsc))
    return predicted_fsc_lst

    
    


