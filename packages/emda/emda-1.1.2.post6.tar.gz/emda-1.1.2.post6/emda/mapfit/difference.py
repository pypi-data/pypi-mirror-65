# difference map 
from emda import iotools
from emda.mapfit import mapaverage
import numpy as np
import fcodes_fast
from emda.config import *

def difference_map(f1, f2, cell, origin=None, res_arr=None, bin_idx=None, nbin=None, s_grid=None):
    from emda import fsc, restools
    nx, ny, nz = f1.shape
    if s_grid is None:
        maxbin = np.amax(np.array([nx//2,ny//2,nz//2]))
        _, s_grid, _ = fcodes_fast.resolution_grid_full(cell,0.0,1,maxbin,nx,ny,nz)
    if bin_idx is None:
        nbin,res_arr,bin_idx = restools.get_resolution_array(cell,f1)
    # estimating covariance between current map vs. static map
    f1f2_fsc,_ = fsc.anytwomaps_fsc_covariance(f1,f2,bin_idx,nbin)
    '''_,f1f2_fsc = fcodes_fast.calc_covar_and_fsc_betwn_anytwomaps(
                            f1,f2,bin_idx,nbin,0,nx,ny,nz)'''
    # find the relative B-factor between static and frt_full
    resol = mapaverage.get_resol(f1f2_fsc,res_arr)
    scale, bfac_relative = mapaverage.estimate_scale_and_relativebfac([f1,f2],cell,resol)
    #fobj.write('Relative B-factor between static map and moving(full) map: '+ str(bfac_relative)+'\n')
    # apply B-factor and scale to 2nd map
    f2_scaled = scale * f2 * np.exp(bfac_relative * (s_grid**2)/4.0)
    # calculating maps
    dm1_dm2 = np.real(np.fft.ifftshift(
                         np.fft.ifftn(
                         np.fft.ifftshift(f1 - f2_scaled))))
    dm2_dm1 = np.real(np.fft.ifftshift(
                         np.fft.ifftn(
                         np.fft.ifftshift(f2_scaled - f1))))
    iotools.write_mrc(dm1_dm2,
                      'diffmap_m1-m2.mrc',
                      cell, origin)
    iotools.write_mrc(dm2_dm1,
                      'diffmap_m2-m1.mrc',
                      cell, origin)