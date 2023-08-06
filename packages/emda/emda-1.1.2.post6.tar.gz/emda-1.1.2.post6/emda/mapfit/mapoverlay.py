"""
Author: "Rangana Warshamanage, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from timeit import default_timer as timer
from emda.mapfit import map_Class
from emda.mapfit import emfit_Class
from emda.mapfit import linefit_class
from emda.config import *

def output_rotated_maps(emmap1, r_lst, t_lst, Bf_arr=[0.0]):
    import numpy as np
    import fcodes_fast
    from emda.mapfit import utils
    from emda.plotter import plot_nlines,plot_nlines_log
    from scipy.ndimage.interpolation import shift
    from emda import iotools 
    import numpy.ma as ma
    from emda import fsc

    com = emmap1.com1  
    arr_lst = emmap1.arr_lst
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
    #data2write = shift(data2write, np.subtract(com,emmap1.box_centr))
    iotools.write_mrc(data2write,'static_map.mrc',cell,origin)
    iotools.write_mrc(arr_lst[0],'static_map_realsp.mrc',cell,origin)
    del data2write
    for fo, t, rotmat in zip(fo_lst[1:], t_lst, r_lst):
        f1f2_fsc_unaligned,_ = fsc.anytwomaps_fsc_covariance(fo_lst[0],fo,bin_idx,nbin)
        fsc12_lst_unaligned.append(f1f2_fsc_unaligned)            
        imap_f = imap_f + 1
        '''# rotate original map
        st,_,_,_ = fcodes_fast.get_st(nx,ny,nz,t)
        arr = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(fo * st))))
        #arr = np.fft.fftshift(arr)
        print('before triliner map')
        nx, ny, nz = arr.shape
        data2write = fcodes_fast.trilinear_map(rotmat,arr,nx,ny,nz)
        print('after triliner map')'''
        #
        st,_,_,_ = fcodes_fast.get_st(nx,ny,nz,t)
        frt_full = utils.get_FRS(rotmat,fo * st, interp='cubic')[:,:,:,0]
        frt_lst.append(frt_full)
        data2write = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(frt_full))))
        #data2write = shift(data2write, np.subtract(com,emmap1.box_centr))
        iotools.write_mrc(data2write,"{0}_{1}.{2}".format('fitted_map',str(imap_f),'mrc'),cell,origin)
        #exit()
        # estimating covaraince between current map vs. static map
        f1f2_fsc,f1f2_covar = fsc.anytwomaps_fsc_covariance(fo_lst[0],frt_full,bin_idx,nbin)
        cov_lst.append(f1f2_covar)
        fsc12_lst.append(f1f2_fsc)

    plot_nlines(res_arr,
                fsc12_lst_unaligned + fsc12_lst,
                'fsc.eps',
                ["start FSC","end FSC"])

'''def fsc_between_static_and_transfomed_map(staticmap,movingmap,bin_idx,rm,t,cell,nbin):
    import fcodes_fast
    from emda.mapfit import utils
    from emda import fsc
    nx, ny, nz = staticmap.shape
    st,_,_,_ = fcodes_fast.get_st(nx,ny,nz,t)
    frt_full = utils.get_FRS(rm,movingmap * st, interp='cubic')[:,:,:,0]
    f1f2_fsc,_ = fsc.anytwomaps_fsc_covariance(staticmap,
                                               frt_full,
                                               bin_idx,
                                               nbin)
    return f1f2_fsc

def get_ibin(bin_fsc):
    import numpy as np
    bin_fsc = bin_fsc[bin_fsc > 0.1]
    #dist = np.sqrt((bin_fsc - 0.143)**2)
    dist = np.sqrt((bin_fsc - 0.4)**2)
    ibin = np.argmin(dist) + 1 # adding 1 because zero indexing
    if ibin % 2 != 0: ibin = ibin - 1
    ibin = min([len(dist), ibin])
    return ibin'''

def main(maplist, ncycles, t_init, theta_init, smax, masklist, fobj, interp):
    from emda.quaternions import get_quaternion, get_RM
    import numpy as np
    from emda.mapfit.frequency_marching import frequency_marching
    from emda.mapfit.utils import get_FRS,create_xyz_grid,get_xyz_sum
    from emda.mapfit import interp_derivatives
    from emda import scale_maps
    from emda.iotools import write_mrc
    from emda.mapfit import run_fit
    if len(maplist) < 2: 
        print(" At least 2 maps required!")
        exit()
    try:
        emmap1 = map_Class.EmmapOverlay(maplist,masklist)
        fobj.write('Map overlay\n')
    except NameError:
        emmap1 = map_Class.EmmapOverlay(maplist)
        fobj.write('Map overlay\n')
    emmap1.load_maps(fobj)
    emmap1.calc_fsc_from_maps(fobj)
    # converting theta_init to rotmat for initial iteration
    fobj.write('\n')
    fobj.write('Initial fitting parameters:\n')
    fobj.write('    Translation: '+ str(t_init)+' \n')
    fobj.write('    Rotation: '+ str(theta_init)+' \n')
    q = get_quaternion(theta_init)
    q = q/np.sqrt(np.dot(q,q))
    print('Initial quaternion: ', q)
    rotmat = get_RM(q)
    fobj.write('    Rotation matrix: '+ str(rotmat)+' \n')
    fobj.write('\n')
    fobj.write('    # fitting cycles: '+ str(ncycles)+' \n')
    t = t_init
    rotmat_lst = []
    transl_lst = []
    # resolution estimate for line-fit
    dist = np.sqrt((emmap1.res_arr - smax)**2) # smax can be a reasonable value
    slf = np.argmin(dist) + 1 
    if slf % 2 != 0: slf = slf - 1
    slf = min([len(dist), slf])
    #
    dfs_interp = False
    # preparing parameters for minimization
    if dfs_interp:
        cell = emmap1.map_unit_cell
        xyz = create_xyz_grid(cell, emmap1.map_dim)
        vol = cell[0] * cell[1] * cell[2]
    #
    for ifit in range(1, len(emmap1.eo_lst)):
        fobj.write('Fitting set#: ' + str(ifit)+' \n')
        # scale moving map to static map
        '''f0 = emmap1.fo_lst[0]
        f1 = emmap1.fo_lst[ifit]
        scale_grid = scale_maps.transfer_power(emmap1.bin_idx,
                                  emmap1.res_arr,
                                  scale_maps.scale_twomaps_by_power(f0,
                                  f1,
                                  bin_idx=emmap1.bin_idx,
                                  res_arr=emmap1.res_arr))
        f1 = f1 * scale_grid
        write_mrc(np.fft.ifftshift(np.real(np.fft.ifftn(
                                     np.fft.ifftshift(f1)))),
                                     'test_f1.mrc',
                                     emmap1.map_unit_cell,
                                     emmap1.map_origin)'''
        #
        start_fit = timer()
        if dfs_interp:
            #dfs_full = interp_derivatives.dfs_fullmap(emmap1.arr_lst[ifit],xyz,vol)
            dfs_full = interp_derivatives.dfs_fullmap(
                                     np.fft.ifftshift(
                                     np.real(np.fft.ifftn(
                                     #np.fft.ifftshift(f1)))),
                                     np.fft.ifftshift(emmap1.eo_lst[ifit])))),
                                                      xyz,vol)
        rotmat, t = run_fit.run_fit(emmap1,smax,rotmat,t,slf,ncycles,ifit,fobj,interp)
        '''for i in range(5):
            if i==0:
                smax = smax # A
                if emmap1.res_arr[0] < smax: 
                    ibin = 2
                    print('Fitting starts at ',emmap1.res_arr[ibin],' (A) instead!' )
                else:
                    dist = np.sqrt((emmap1.res_arr - smax)**2)
                    ibin = np.argmin(dist) + 1 # adding 1 because fResArr starts with zero
                    if ibin % 2 != 0: ibin = ibin - 1
                    ibin = min([len(dist), ibin])
                    print('Fitting starts at ',emmap1.res_arr[ibin],' (A)' )
                ibin_old = ibin
                f1f2_fsc = fsc_between_static_and_transfomed_map(
                                            emmap1.fo_lst[0],
                                            emmap1.fo_lst[ifit],
                                            emmap1.bin_idx,
                                            rotmat,
                                            t,
                                            emmap1.map_unit_cell,
                                            emmap1.nbin)
                fsc_lst.append(f1f2_fsc)
            else:
                # Apply initial rotation and translation to calculate fsc
                f1f2_fsc = fsc_between_static_and_transfomed_map(
                                            emmap1.fo_lst[0],
                                            emmap1.fo_lst[ifit],
                                            emmap1.bin_idx,
                                            rotmat,
                                            t,
                                            emmap1.map_unit_cell,
                                            emmap1.nbin)
                ibin = get_ibin(f1f2_fsc)
                if ibin_old == ibin: 
                    fsc_lst.append(f1f2_fsc)
                    fobj.write('\n')
                    fobj.write('FSC between static and moving maps\n')
                    fobj.write('\n')
                    fobj.write('bin#\n')
                    fobj.write('resolution (A)\n')
                    fobj.write('start FSC\n')
                    fobj.write('end FSC\n')
                    fobj.write('\n')
                    for j in range(len(emmap1.res_arr)):
                        print(emmap1.res_arr[j], fsc_lst[0][j], fsc_lst[1][j])
                        fobj.write("{:5d} {:6.2f} {:8.4f} {:8.4f}\n".format(
                            j,
                            emmap1.res_arr[j],
                            fsc_lst[0][j],
                            fsc_lst[1][j]))
                    break
                else: 
                    ibin_old = ibin
            if ibin == 0:
                print('Cannot find a solution! Stopping now...')
                exit()

            static_cutmap,cBIdx, cbin = frequency_marching(emmap1.eo_lst[0],
                                            emmap1.bin_idx,
                                            emmap1.res_arr,
                                            bmax=ibin)  
            moving_cutmap,_, _ = frequency_marching(emmap1.eo_lst[ifit],
                                                emmap1.bin_idx,
                                                emmap1.res_arr,
                                                bmax=ibin)
            moving_cutmap_f1,_, _ = frequency_marching(emmap1.fo_lst[ifit],
                                                emmap1.bin_idx,
                                                emmap1.res_arr,
                                                bmax=ibin)
            if dfs_interp:
                # cut dfs_full for current size
                dfs = interp_derivatives.cut_dfs4interp(dfs_full,cbin)
                #
            else: 
                dfs = None
            assert static_cutmap.shape == moving_cutmap.shape
            emmap1.cfo_lst = [moving_cutmap_f1]
            emmap1.ceo_lst = [static_cutmap,moving_cutmap]
            emmap1.cbin_idx = cBIdx
            emmap1.cdim = moving_cutmap.shape
            emmap1.cbin = cbin
            fit = emfit_Class.EmFit(emmap1,interp=interp,dfs=dfs)
            if ibin < slf or slf == 0: slf = ibin
            slf = min([ibin, slf])
            fit.minimizer(ncycles, t, rotmat, smax_lf=slf, fobj=fobj)
            ncycles = ncycles # tweaking this you can change later # cycles
            t = fit.t_accum
            rotmat = fit.rotmat'''

        #rotmat_lst.append(fit.rotmat)
        #transl_lst.append(fit.t_accum)
        rotmat_lst.append(rotmat)
        transl_lst.append(t)
        end_fit = timer()
        print('time for fitting: ', end_fit-start_fit)

    output_rotated_maps(emmap1,
                        rotmat_lst,
                        transl_lst)


if (__name__ == "__main__"):
    maplist = ['/Users/ranganaw/MRC/REFMAC/Vinoth/reboxed_maps/nat_hf2.mrc',
           '/Users/ranganaw/MRC/REFMAC/Vinoth/reboxed_maps/lig_hf2.mrc']
    masklist = ['/Users/ranganaw/MRC/REFMAC/Vinoth/reboxed_maps/nat_msk.mrc',
            '/Users/ranganaw/MRC/REFMAC/Vinoth/reboxed_maps/lig_msk.mrc']
    main(maplist)


