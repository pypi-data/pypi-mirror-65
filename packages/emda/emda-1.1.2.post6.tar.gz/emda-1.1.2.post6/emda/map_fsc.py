# This module calculates FSC between maps and model
# Author: Rangana Warshamanage
# Created: 2019.06.11

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
from timeit import default_timer as timer
import sys
from emda.iotools import read_mrc
from emda.plotter import *
import argparse
from emda.config import *

#debug_mode = 1 # 0: no debug info, 1: debug

cmdl_parser = argparse.ArgumentParser(description='Computes FSC between model and map\n')
cmdl_parser.add_argument('-h1', '--half1_map', required=True, help='Input filename for hfmap1')
cmdl_parser.add_argument('-h2', '--half2_map', required=True, help='Input filename for hfmap2')
cmdl_parser.add_argument('-af', '--modelf_pdb', required=True, help='Input full atomic model')
cmdl_parser.add_argument('-a1', '--model1_pdb', required=True, help='Input halfmap1 atomic model')
cmdl_parser.add_argument('-r', '--model_resol', type=np.float32, required=False, help='Resolution in Angstrom')
cmdl_parser.add_argument('-s', '--map_size', nargs='+', type=np.int, required=False, help='Map size ')
cmdl_parser.add_argument('-f1', '--hff1_map', required=False, help='Input filename for hfmap1')
cmdl_parser.add_argument('-f2', '--hff2_map', required=False, help='Input filename for hfmap2')
cmdl_parser.add_argument('-v', '--verbose', default=False,
                         help='Verbose output')

def calc_fsc_mrc(hf1,hf2,bin_idx,nbin):
    from emda import fsc
    '''import fcodes_fast
    assert hf1.shape == hf2.shape
    nx,ny,nz = hf1.shape
    _,_,_,_,_,bin_fsc = fcodes_fast.calc_fsc_using_halfmaps(
                hf1,hf2,bin_idx,nbin,1,nx,ny,nz)'''
    bin_fsc,_,_,_,_,_ = fsc.halfmaps_fsc_variance(hf1,hf2,bin_idx,nbin)
    return bin_fsc

'''def calculate_modelmap(model_pdb,dim,map_resol):
    model_bfac = 20 # FSC does not depend on the B factor.
    run_refmac_sfcalc(model_pdb,map_resol,model_bfac)
    modelname = 'sfcalc_from_crd.mtz'
    uc2,df = read_mtz_gemmi(modelname)
    f,h,k,l = get_f_gemmi(df)
    f3d,_ = mtz2mrc(uc2,h,k,l,f,dim[0],dim[1],dim[2])
    _,f_model,_ = read_mrc('mtz2mrc.mrc')
    return f_model

def pass_mtz(mtzfile,dim):
    uc,df = read_mtz_gemmi(mtzfile)
    f,h,k,l = get_f_gemmi(df)
    f3d,_ = mtz2mrc(uc,h,k,l,f,dim[0],dim[1],dim[2])
    _,f_map,_ = read_mrc('mtz2mrc.mrc')
    return uc, f_map'''

def calculate_modelmap(model_pdb,dim,map_resol):
    import emda.iotools
    model_bfac = 0 # FSC does not depend on the B factor.
    emda.iotools.run_refmac_sfcalc(model_pdb,map_resol,model_bfac)
    f_model = pass_mtz('sfcalc_from_crd.mtz',dim)
    return f_model

def pass_mtz(mtzfile,dim):
    from emda.maptools import mtz2map
    import numpy as np
    arr = mtz2map(mtzfile,dim)
    f_map = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr)))
    return f_map

def map_model_fsc(half1_map, half2_map, modelf_pdb, model1_pdb, mask_map=None, map_size=None, model_resol=None):
    import fcodes_fast
    from emda.iotools import read_mrc,read_map
    from emda.plotter import plot_nlines,plot_nlines2
    from emda import restools
    import emda.maskmap_class
    import numpy as np
    fsc_list = []
    ########## FSC between half maps ##########
    # if maps are in MRC format
    if half1_map.endswith(('.mrc','.mrcs','.map')):
        #uc,f_hf1, _ = read_mrc(half1_map)
        uc,arr1, _ = read_map(half1_map)
        #f_hf1 = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr1)))
    if half2_map.endswith(('.mrc','.mrcs','.map')):
        #uc,f_hf2, _ = read_mrc(half2_map)
        uc,arr2, _ = read_map(half2_map)
        #f_hf2 = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr2)))
    #f_ful = (f_hf1 + f_hf2)/2.0 
    # mask taking into account
    if mask_map is not None:
         uc,msk, _ = read_map(mask_map)
    if mask_map is None:
        # creating ccmask from half data
        obj_maskmap = emda.maskmap_class.MaskedMaps()
        obj_maskmap.generate_mask(arr1, arr2)
        msk = obj_maskmap.mask

    f_hf1 = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr1 * msk)))
    f_hf2 = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr2 * msk)))
    f_ful = (f_hf1 + f_hf2)/2.0 
    # if maps are in MTZ format
    if half1_map.endswith(('.mtz')):
        if map_size is None:
            print('Need map dimensions.')
            exit()
        dim = map_size
        if len(dim) < 3: 
            print('Need three values space delimited')
            exit()
        if len(dim) > 3:
            dim = dim[:3]
        f_hf1 = pass_mtz(half1_map, dim)
    if half2_map.endswith(('.mtz')):
        f_hf2 = pass_mtz(half2_map, dim)  
    # making resolution grid
    dim = f_hf1.shape
    nx,ny,nz = f_hf1.shape
    nbin,res_arr,bin_idx = restools.get_resolution_array(uc,f_hf1)
    # FSC between halfmaps
    bin_fsc = calc_fsc_mrc(f_hf1,f_hf2,bin_idx,nbin)
    fsc_list.append(bin_fsc)
    ##########################################
    if model_resol is None:
        # determine map resolution using hfmap FSC
        dist = np.sqrt((bin_fsc - 0.143)**2)
        map_resol = res_arr[np.argmin(dist)]
    else:
        map_resol = model_resol

    ########## Calculate maps from models ##########
    # if model is suppied as coordinates
    dim = [nx, ny, nz]
    if modelf_pdb.endswith(('.pdb','.ent')):
        f_modelf = calculate_modelmap(modelf_pdb,dim,map_resol)
    if model1_pdb.endswith(('.pdb','.ent')):
        f_model1 = calculate_modelmap(model1_pdb,dim,map_resol)
    # if model is suppied as maps (for whatever crazy reason)
    if modelf_pdb.endswith(('.mrc','.mrcs','.map')):
        _,f_modelf,_ = read_mrc(modelf_pdb)
    if model1_pdb.endswith(('.mrc','.mrcs','.map')):
        _,f_model1,_ = read_mrc(model1_pdb)
    # if model is suppied as mtz (for whatever crazy reason)
    if modelf_pdb.endswith(('.mtz')):
        f_modelf = pass_mtz(modelf_pdb, dim)
    if model1_pdb.endswith(('.mtz')):
        f_model1 = pass_mtz(model1_pdb, dim)
    ################################################

    ########## FSC between maps and models #########
    # FSC between halfmaps and model1
    for imap in [f_hf1,f_hf2]:
        bin_fsc = calc_fsc_mrc(imap,f_model1,bin_idx,nbin)
        fsc_list.append(bin_fsc)
    # FSC between fullmap and modelfull
    bin_fsc = calc_fsc_mrc(f_ful,f_modelf,bin_idx,nbin)
    fsc_list.append(bin_fsc)
    ################################################
    # output plots
    plot_nlines(res_arr,fsc_list,
                'allmap_fsc_modelvsmap.eps',
                ["hf1-hf2","half1-model1","half2-model1","fullmap-model"])
    plot_nlines2(1/res_arr,fsc_list,
                 'allmap_fsc_modelvsmap-2.eps',
                 ["hf1-hf2","half1-model1","half2-model1","fullmap-model"])



def main():
    import fcodes_fast
    from emda import restools
    args = cmdl_parser.parse_args()
    # Onetime manipulation for Wenjuan maps.
    # we supply unfiltered half maps and use them for
    # hf1-hf2 fsc calculation
    calc_hf_fsc = True
    if args.hff1_map is not None:
        uc,f_hff1, _ = read_mrc(args.hff1_map)
        uc,f_hff2, _ = read_mrc(args.hff2_map)
        # making resolution grid
        nx,ny,nz = f_hff1.shape
        nbin,res_arr,bin_idx = restools.get_resolution_array(uc,f_hff1)
        # FSC between halfmaps
        fsc_list = []
        bin_fsc = calc_fsc_mrc(f_hff1,f_hff2,bin_idx,nbin)
        fsc_list.append(bin_fsc)
        calc_hf_fsc = False

    # if maps are in MTZ format
    if args.half1_map.endswith(('.mtz')):
        if args.map_size is None:
            print('Need map dimensions.')
            exit()
        dim = args.map_size
        if len(dim) < 3: 
            print('Need three values space delimited')
            exit()
        if len(dim) > 3:
            dim = dim[:3]
        f_hf1 = pass_mtz(args.half1_map, dim)
    if args.half2_map.endswith(('.mtz')):
        f_hf2 = pass_mtz(args.half2_map, dim)

    # if maps are in MRC format
    if args.half1_map.endswith(('.mrc','.mrcs','.map')):
        uc,f_hf1, _ = read_mrc(args.half1_map)
    if args.half1_map.endswith(('.mrc','.mrcs','.map')):
        uc,f_hf2, _ = read_mrc(args.half2_map)
    f_ful = (f_hf1 + f_hf2)/2.0

    if calc_hf_fsc:
        # making resolution grid
        nx,ny,nz = f_hf1.shape
        nbin,res_arr,bin_idx = restools.get_resolution_array(uc,f_hf1)
        # FSC between halfmaps
        fsc_list = []
        bin_fsc = calc_fsc_mrc(f_hf1,f_hf2,bin_idx,nbin)
        fsc_list.append(bin_fsc)
    # determine map resolution using hfmap FSC
    dist = np.sqrt((bin_fsc - 0.143)**2)
    map_resol = res_arr[np.argmin(dist)]
    if args.model_resol is not None: map_resol = args.map_resol

    # Calculate maps from models
    # if model is suppied as maps
    modelf_pdb = args.modelf_pdb
    model1_pdb = args.model1_pdb
    if modelf_pdb.endswith(('.mrc','.mrcs','.map')):
        _,f_modelf,_ = read_mrc(args.modelf_pdb)
    if model1_pdb.endswith(('.mrc','.mrcs','.map')):
        _,f_model1,_ = read_mrc(args.modelf_pdb)
    # if model is suppied as coordinates
    dim = [nx, ny, nz]
    if modelf_pdb.endswith(('.pdb','.ent')):
        #pdb2mmcif(args.modelf_pdb)
        f_modelf = calculate_modelmap(args.modelf_pdb,dim,map_resol)
    if model1_pdb.endswith(('.pdb','.ent')):
        #pdb2mmcif(args.model1_pdb)
        f_model1 = calculate_modelmap(args.model1_pdb,dim,map_resol)

    # FSC between halfmaps and model1
    for imap in [f_hf1,f_hf2]:
        bin_fsc = calc_fsc_mrc(imap,f_model1,bin_idx,nbin)
        fsc_list.append(bin_fsc)
    # FSC between fullmap and modelfull
    bin_fsc = calc_fsc_mrc(f_ful,f_modelf,bin_idx,nbin)
    fsc_list.append(bin_fsc)

    # output plots
    plot_nlines(res_arr,fsc_list,'allmap_fsc_modelvsmap.eps',["hf1-hf2","half1-model1","half2-model1","fullmap-model"])
    plot_nlines2(1/res_arr,fsc_list,'allmap_fsc_modelvsmap-2.eps',["hf1-hf2","half1-model1","half2-model1","fullmap-model"])

if (__name__ == "__main__"):
    main()



    
    


