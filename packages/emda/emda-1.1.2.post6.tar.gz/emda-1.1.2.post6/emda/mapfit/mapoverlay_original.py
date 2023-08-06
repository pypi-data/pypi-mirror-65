"""
Author: "Rangana Warshamanage, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from emda.mapfit import map_Class
from emda.mapfit import emfit_Class

def output_rotated_maps(emmap1, r_lst, t_lst, Bf_arr=[0.0]):
    import numpy as np
    import fcodes_fast
    from emda.mapfit import utils
    from emda.plotter import plot_nlines,plot_nlines_log
    from scipy.ndimage.interpolation import shift
    from emda import iotools 
    import numpy.ma as ma

    com = emmap1.com1  
    fo_lst = emmap1.fo_lst   
    bin_idx = emmap1.bin_idx  
    nbin = emmap1.nbin     
    res_arr = emmap1.res_arr  
    cell = emmap1.map_unit_cell 
    origin = emmap1.map_origin
    #assert len(fo_lst) == len(t_lst) == len(r_lst)
    nx,ny,nz = fo_lst[0].shape
    frt_lst = []
    frt_lst.append(fo_lst[0])  
    cov_lst = []
    fsc12_lst = []
    fsc12_lst_unaligned = []
    imap_f = 0
    # static map
    data2write = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(fo_lst[0]))))
    data2write = shift(data2write, np.subtract(com,emmap1.box_centr))
    iotools.write_mrc(data2write,'static_map.mrc',cell,origin)
    del data2write
    for fo, t, rotmat in zip(fo_lst[1:], t_lst, r_lst):
        _,f1f2_fsc_unaligned = fcodes_fast.calc_covar_and_fsc_betwn_anytwomaps(
                    fo_lst[0],fo,bin_idx,nbin,0,nx,ny,nz)
        fsc12_lst_unaligned.append(f1f2_fsc_unaligned)            
        imap_f = imap_f + 1
        st,_,_,_ = fcodes_fast.get_st(nx,ny,nz,t)
        frt_full = utils.get_FRS(cell,rotmat,fo * st)[:,:,:,0]
        frt_lst.append(frt_full)
        data2write = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(frt_full))))
        data2write = shift(data2write, np.subtract(com,emmap1.box_centr))
        iotools.write_mrc(data2write,"{0}_{1}.{2}".format('fitted_map',str(imap_f),'mrc'),cell,origin)
        # estimating covaraince between current map vs. static map
        f1f2_covar,f1f2_fsc = fcodes_fast.calc_covar_and_fsc_betwn_anytwomaps(
                    fo_lst[0],frt_full,bin_idx,nbin,0,nx,ny,nz)
        cov_lst.append(f1f2_covar)
        fsc12_lst.append(f1f2_fsc)

        plot_nlines(res_arr,
                    fsc12_lst_unaligned + fsc12_lst,
                    'fsc.eps',
                    ["s-u1","s-a1"])

def main(maplist, ncycles=10, t_init=[0.0, 0.0, 0.0], theta_init=[(1,0,0),0.0], smax=6, masklist=None, mapavg=False):
    if len(maplist) < 2: 
        print(" At least 2 maps required!")
        exit()
    try:
        emmap1 = map_Class.EmmapOverlay(maplist,masklist)
    except NameError:
        emmap1 = map_Class.EmmapOverlay(maplist)
    emmap1.load_maps()
    emmap1.calc_fsc_from_maps()
    # converting theta_init to rotmat for initial iteration
    from quaternions import get_quaternion, get_RM
    import numpy as np
    q = get_quaternion(theta_init)
    q = q/np.sqrt(np.dot(q,q))
    print(q)
    rotmat = get_RM(q)
    t = t_init
    rotmat_lst = []
    transl_lst = []
    # frequency marching test
    from frequency_marching import frequency_marching
    static_bin_lst = []
    #for ibin in [40, 50, 55, 60]: # Takanori ATPase 31-34
    #for ibin in [30, 40, 50, 60, 65]: # Bianka data
    #for ibin in [50,100]: # vinoth-full map
    for ibin in [44,66]: # vinoth-reboxed
        cutmap,cBIdx, cbin = frequency_marching(emmap1.eo_lst[0],
                                        emmap1.bin_idx,
                                        emmap1.res_arr,
                                        bmax=ibin)
        static_bin_lst.append(cutmap)

    for ifit in range(1, len(emmap1.eo_lst)):
        i = -1
        #for ibin in [40, 50, 55, 60]:
        #for ibin in [30, 40, 50, 60, 65]:
        #for ibin in [50,100]:
        for ibin in [44,66]: # vinoth-reboxed
            i = i + 1
            #ceo_lst = []
            cutmap,cBIdx, cbin = frequency_marching(emmap1.eo_lst[ifit],
                                                emmap1.bin_idx,
                                                emmap1.res_arr,
                                                bmax=ibin)
            assert static_bin_lst[i].shape == cutmap.shape
            emmap1.ceo_lst = [static_bin_lst[i],cutmap]
            emmap1.cbin_idx = cBIdx
            emmap1.cdim = cutmap.shape
            emmap1.cbin = cbin
            fit = emfit_Class.EmFit(emmap1)
            fit.minimizer(ncycles, t, rotmat)
            ncycles = 5
            t = fit.t_accum
            rotmat = fit.rotmat
        
        rotmat_lst.append(fit.rotmat)
        transl_lst.append(fit.t_accum)
        # free memory
        del fit

    output_rotated_maps(emmap1,
                        rotmat_lst,
                        transl_lst)


if (__name__ == "__main__"):
    maplist = ['/Users/ranganaw/MRC/REFMAC/Vinoth/reboxed_maps/nat_hf2.mrc',
           '/Users/ranganaw/MRC/REFMAC/Vinoth/reboxed_maps/lig_hf2.mrc']
    masklist = ['/Users/ranganaw/MRC/REFMAC/Vinoth/reboxed_maps/nat_msk.mrc',
            '/Users/ranganaw/MRC/REFMAC/Vinoth/reboxed_maps/lig_msk.mrc']
    main(maplist)


