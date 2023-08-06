"""
Author: "Rangana Warshamanage, Garib N. Murshudov"
MRC Laboratory of Molecular Biology
    
This software is released under the
Mozilla Public License, version 2.0; see LICENSE.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import os
from timeit import default_timer as timer
import numpy as np
import fcodes_fast
from emda.iotools import read_map,write_mrc,resample2staticmap
from emda.mapfit.utils import remove_unwanted_corners
import emda.plotter
from emda.config import *
import emda.mapfit.utils as utils
from emda import fsc

#debug_mode = 1 # 0: no debug info, 1: debug

class EmmapOverlay:
    
    def __init__(self,hfmap_list, mask_list=None):
        self.hfmap_list         = hfmap_list
        self.mask_list          = mask_list
        self.map_unit_cell      = None
        self.map_origin         = None
        self.map_dim            = None
        self.arr_lst            = []
        #
        self.ceo_lst            = None
        self.cfo_lst            = None
        self.cbin_idx           = None
        self.cdim               = None
        self.cbin               = None

    def load_maps(self, fobj):
        from scipy import ndimage
        from scipy.ndimage.interpolation import shift
        #import fcodes_fast
        # read mask and map
        fhf_lst = []
        if self.mask_list is not None:
            if len(self.hfmap_list) != len(self.mask_list):
                print('map_list and mask_list must have the same size!')
                print('exiting program...')
                exit()
            for i in range(len(self.mask_list)):
                _,mask,_ = read_map(self.mask_list[i])
                mask = utils.set_dim_even(mask)
                uc,arr,origin = read_map(self.hfmap_list[i])
                arr = utils.set_dim_even(arr)
                if i == 0: 
                    temp = arr * mask
                    com1 = ndimage.measurements.center_of_mass(temp * temp)
                    print('COM: ', com1)
                    nx, ny, nz = arr.shape
                    box_centr = (nx//2, ny//2, nz//2)
                    print(box_centr)
                    self.com1 = com1
                    self.box_centr = box_centr
                    map_origin = origin
                    uc_target = uc
                    target_dim = arr.shape
                    target_pix_size = uc_target[0]/target_dim[0]
                    corner_mask = remove_unwanted_corners(uc,target_dim)
                    arr_mask = shift(arr * mask, np.subtract(box_centr,com1))

                    fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_mask * corner_mask))))
                else:
                    mask = resample2staticmap(target_pix_size,target_dim,uc,mask)
                    arr = resample2staticmap(target_pix_size,target_dim,uc,arr) 
                    temp = arr * mask               
                    com1 = ndimage.measurements.center_of_mass(temp * temp) 
                    print('COM: ', com1)            
                    arr_mask = shift(arr * mask, np.subtract(box_centr,com1))                  
                    fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_mask * corner_mask))))

            # free memory
            del arr, arr_mask, mask
            del corner_mask
            #
            self.map_origin     = map_origin
            self.map_unit_cell  = uc_target
            self.map_dim        = target_dim 
            self.fhf_lst        = fhf_lst 

        if self.mask_list is None: 
            for i in range(len(self.hfmap_list)):
                uc,arr,origin = read_map(self.hfmap_list[i])
                arr = utils.set_dim_even(arr)
                print('origin: ', origin)
                if i == 0:
                    #write_mrc(arr,'static.mrc',uc)
                    #uc,arr,origin = read_map('static.mrc')
                    com1 = ndimage.measurements.center_of_mass(arr * (arr >= 0.)) # to remove effect from negative values
                    print('COM: ', com1)
                    nx, ny, nz = arr.shape
                    box_centr = (nx//2, ny//2, nz//2)
                    print('BOX center: ', box_centr)
                    self.com1 = com1
                    self.box_centr = box_centr
                    map_origin = origin
                    uc_target = uc
                    target_dim = arr.shape
                    target_pix_size = uc_target[0]/target_dim[0]
                    arr = shift(arr, np.subtract(box_centr,com1)) 
                    self.arr_lst.append(arr)
                    write_mrc(arr,'static_centered.mrc',uc_target,map_origin)
                    print('COM after centering: ', ndimage.measurements.center_of_mass(arr * (arr >= 0.)))
                    fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr))))
                else:
                    arr = resample2staticmap(target_pix_size,target_dim,uc,arr)
                    com1 = ndimage.measurements.center_of_mass(arr * (arr >= 0.)) # to remove effect from negative values
                    #com1 = ndimage.measurements.center_of_mass(arr * arr )
                    print('COM: ', com1)
                    arr = shift(arr, np.subtract(box_centr,com1))
                    self.arr_lst.append(arr)
                    write_mrc(arr,'moving_centered.mrc',uc_target,map_origin) 
                    print('COM after centering: ', ndimage.measurements.center_of_mass(arr * (arr >= 0.)))
                    fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr))))
                
            # free memory
            del arr
            #            
            self.map_origin     = map_origin
            self.map_unit_cell  = uc_target
            self.map_dim        = target_dim 
            self.fhf_lst        = fhf_lst 

    def calc_fsc_from_maps(self, fobj):  
        # function for only two maps fitting
        import fcodes_fast
        from emda import restools
        nmaps = len(self.fhf_lst) 
        fFo_lst = []
        fEo_lst = []
        fBTV_lst = []
        #
        nx,ny,nz = self.fhf_lst[0].shape
        self.nbin,self.res_arr,self.bin_idx = restools.get_resolution_array(self.map_unit_cell,
                                                                       self.fhf_lst[0])
        #
        for i in range(nmaps):  
            _,_,_,totalvar,fo,eo = fsc.halfmaps_fsc_variance(self.fhf_lst[i],
                                                             self.fhf_lst[i],
                                                             self.bin_idx,
                                                             self.nbin)
            #fo,eo,_,_,totalvar,_ = fcodes_fast.calc_fsc_using_halfmaps(
            #    self.fhf_lst[i],self.fhf_lst[i],self.bin_idx,self.nbin,debug_mode,nx,ny,nz)  
            fFo_lst.append(fo)
            fEo_lst.append(eo)
            fBTV_lst.append(totalvar)
        #
        self.fo_lst            = fFo_lst
        self.eo_lst            = fEo_lst
        self.totalvar_lst      = fBTV_lst



class EmmapAverage:
    
    def __init__(self,hfmap_list,mask_list=None):
        self.hfmap_list         = hfmap_list
        self.mask_list          = mask_list
        self.map_unit_cell      = None
        self.map_origin         = None
        self.map_dim            = None
        self.com_lst            = None
        self.resol_rand         = 10.0 # resolution (A) for phase randomisation
        #
        self.ceo_lst            = None
        self.cbin_idx           = None
        self.cdim               = None
        self.cbin               = None

    def load_maps(self, fobj):
        from scipy import ndimage
        from scipy.ndimage.interpolation import shift
        from emda.fsc_true_from_phase_randomize import get_randomized_sf
        import fcodes_fast
        # read masks
        fhf_lst = []
        unmask_fhf_lst = []
        phrand_fhf_lst = []
        com_lst = []
        if self.mask_list is not None:
            if len(self.hfmap_list) != len(self.mask_list):
                print('hfmap_list and mask_list must have the same size!')
                print('exiting program...')
                exit()
            '''mask_lst = []
            fobj.write('\n Masks files:\n')
            for i in range(0,len(self.mask_list),2):
                fobj.write('%s\n' %os.path.abspath(self.mask_list[i]))
                _,mask,_ = read_map(self.mask_list[i])
                mask_lst.append(mask) # for hfmap1 & hfmap2
            fobj.write('\n Input files (static map):\n') '''
            for i in range(0,len(self.hfmap_list),2):
                '''fobj.write('\n Masks files:\n')
                fobj.write('%s\n' %os.path.abspath(self.mask_list[i]))
                _,mask,_ = read_map(self.mask_list[i])
                mask_lst.append(mask) # for hfmap1 & hfmap2
                fobj.write('\n Input files (static map):\n')
                uc,arr1,origin = read_map(self.hfmap_list[i])
                fobj.write('%s\n' %os.path.abspath(self.hfmap_list[i]))
                uc,arr2,origin = read_map(self.hfmap_list[i+1])
                fobj.write('%s\n' %os.path.abspath(self.hfmap_list[i+1]))'''
                if i == 0: 
                    fobj.write('Static map:\n')
                    fobj.write('Mask file: %s\n' %os.path.abspath(self.mask_list[i]))
                    _,mask,_ = read_map(self.mask_list[i]) # for hfmap1 & hfmap2
                    fobj.write('Input files (static map):\n')
                    uc,arr1,origin = read_map(self.hfmap_list[i])
                    fobj.write('%s\n' %os.path.abspath(self.hfmap_list[i]))
                    uc,arr2,origin = read_map(self.hfmap_list[i+1])
                    fobj.write('%s\n' %os.path.abspath(self.hfmap_list[i+1]))
                    com1 = ndimage.measurements.center_of_mass(arr1 * mask)#mask_lst[0])
                    com_lst.append(com1)
                    nx, ny, nz = arr1.shape
                    box_centr = (nx//2, ny//2, nz//2)
                    print(box_centr)
                    fobj.write('Center_of_mass coordinates: ' + str(com1) + ' \n')
                    self.box_centr = box_centr
                    fobj.write('Center_of_box coordinates: ' + str(box_centr) + '\n')
                    map_origin = origin
                    fobj.write('Map origin coordinates: ' + str(map_origin) + ' \n')
                    uc_target = uc
                    fobj.write('Unit cell: ' + str(uc_target) + ' \n')
                    target_dim = arr1.shape
                    fobj.write('Map dimensions: ' + str(target_dim) + ' \n')
                    target_pix_size = uc_target[0]/target_dim[0]
                    fobj.write('Map pixel size: ' + str(target_pix_size) + ' \n')
                    corner_mask = remove_unwanted_corners(uc,target_dim)
                    # get resolution grid
                    maxbin = np.amax(np.array([nx//2,ny//2,nz//2]))
                    fobj.write('Creating resolution grid... \n')
                    resol_grid, self.s_grid, _ = fcodes_fast.resolution_grid_full(uc,0.0,1,maxbin,nx,ny,nz)
                    #
                    fobj.write('Phase randomization using static half maps. \n')
                    fobj.write('Phase randomize resolution:'+str(self.resol_rand)+' \n')
                    #test_hflist = []
                    for arr in [arr1, arr2]:
                        arr_unmask = arr
                        fhf1_randomized = get_randomized_sf(resol_grid,arr_unmask,self.resol_rand)
                        arr_rand = np.real(np.fft.ifftn(np.fft.ifftshift(fhf1_randomized))) * mask
                        arr_mask = shift(arr * mask, np.subtract(box_centr,com1))
                        # test
                        #write_mrc(arr_mask,'test.mrc',uc_target,map_origin)
                        #fmask = np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_mask * corner_mask)))
                        #test_hflist.append(fmask)
                        #data2write = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(fmask))))
                        #data2write = shift(data2write, np.subtract(com_lst[0],self.box_centr))
                        #write_mrc(data2write,'test2.mrc',uc_target,map_origin)
                        #exit()
                        #
                        arr_unmask = shift(arr_unmask, np.subtract(box_centr,com1)) 
                        arr_rand = shift(arr_rand, np.subtract(box_centr,com1))
                        fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_mask * corner_mask))))
                        unmask_fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_unmask * 
                                                                                          corner_mask))))
                        phrand_fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_rand * 
                                                                                          corner_mask))))
                    '''fullmap_stat = (test_hflist[0] + test_hflist[0])/2.0
                    data2write = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(fullmap_stat))))
                    data2write = shift(data2write, np.subtract(com_lst[0],self.box_centr))
                    write_mrc(data2write,'test3.mrc',uc_target,map_origin)
                    exit()'''
                else:
                    fobj.write('Moving map:\n')
                    fobj.write('Mask file: %s\n' %os.path.abspath(self.mask_list[i]))
                    #fobj.write('%s\n' %os.path.abspath(self.mask_list[i]))
                    _,mask,_ = read_map(self.mask_list[i]) # for hfmap1 & hfmap2
                    fobj.write('Resampling mask...\n')
                    mask = resample2staticmap(target_pix_size,target_dim,uc,mask,fobj=fobj)
                    #mask_lst.append(mask) # for hfmap1 & hfmap2
                    fobj.write('Input files (moving map):\n')
                    uc,arr1,origin = read_map(self.hfmap_list[i])
                    fobj.write('%s\n' %os.path.abspath(self.hfmap_list[i]))
                    uc,arr2,origin = read_map(self.hfmap_list[i+1])
                    fobj.write('%s\n' %os.path.abspath(self.hfmap_list[i+1]))
                    run_once = True
                    #mask = resample2staticmap(target_pix_size,target_dim,uc,mask) #mask_lst[i//2])
                    fobj.write('Phase randomization using half maps. \n')
                    fobj.write('Phase randomize resolution:'+str(self.resol_rand)+' \n')
                    for arr in [arr1, arr2]:
                        fobj.write('Resampling halfmaps...\n')
                        arr = resample2staticmap(target_pix_size,target_dim,uc,arr,fobj=fobj)
                        arr_unmask = arr
                        fobj.write('Phase randomization...\n')
                        fhf1_randomized = get_randomized_sf(resol_grid,arr_unmask,self.resol_rand)
                        arr_rand = np.real(np.fft.ifftn(np.fft.ifftshift(fhf1_randomized))) * mask
                        if run_once: 
                            com1 = ndimage.measurements.center_of_mass(arr * mask)
                            com_lst.append(com1)
                        run_once = False
                        arr_mask = shift(arr * mask, np.subtract(box_centr,com1))
                        arr_unmask = shift(arr_unmask, np.subtract(box_centr,com1)) 
                        arr_rand = shift(arr_rand, np.subtract(box_centr,com1))
                        fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_mask * corner_mask))))
                        unmask_fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_unmask * 
                                                                                          corner_mask))))
                        phrand_fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_rand * 
                                                                                          corner_mask))))

            # free memory
            #del mask_lst
            del arr, arr1, arr2
            del corner_mask
            #
            self.map_origin     = map_origin
            self.map_unit_cell  = uc_target
            self.map_dim        = target_dim 
            self.fhf_lst        = fhf_lst 
            self.com_lst        = com_lst
            self.unmask_fhf_lst = unmask_fhf_lst
            self.phrand_fhf_lst = phrand_fhf_lst

        if self.mask_list is None: 
            print('Correlation based masks will be generated and used for fitting!')
            from emda import maskmap_class
            obj_maskmap = maskmap_class.MaskedMaps()
            for i in range(0,len(self.hfmap_list),2):
                uc,arr1,origin = read_map(self.hfmap_list[i])
                uc,arr2,origin = read_map(self.hfmap_list[i+1])
                # calculate the mask
                obj_maskmap.generate_mask(arr1, arr2)
                mask = obj_maskmap.mask
                write_mrc(mask,"{0}_{1}.{2}".format('mask',str(i),'mrc'),uc,origin)
                if i == 0:
                    com1 = ndimage.measurements.center_of_mass(arr1 * mask)
                    nx, ny, nz = arr1.shape
                    box_centr = (nx//2, ny//2, nz//2)
                    print(box_centr)
                    self.com1 = com1
                    self.box_centr = box_centr
                    map_origin = origin
                    uc_target = uc
                    target_dim = arr1.shape
                    target_pix_size = uc_target[0]/target_dim[0]
                    # get resolution grid
                    maxbin = np.amax(np.array([nx//2,ny//2,nz//2]))
                    resol_grid, self.s_grid, _ = fcodes_fast.resolution_grid_full(uc,0.0,1,maxbin,nx,ny,nz)
                    #
                    for arr in [arr1, arr2]:
                        arr_unmask = arr
                        fhf1_randomized = get_randomized_sf(resol_grid,arr_unmask,self.resol_rand)
                        arr_rand = np.real(np.fft.ifftn(np.fft.ifftshift(fhf1_randomized))) * mask
                        arr_mask = shift(arr * mask, np.subtract(box_centr,com1))
                        arr_unmask = shift(arr_unmask, np.subtract(box_centr,com1)) 
                        arr_rand = shift(arr_rand, np.subtract(box_centr,com1))
                        fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_mask))))
                        unmask_fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_unmask))))
                        phrand_fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_rand))))
                else:
                    run_once = True
                    for arr in [arr1, arr2]:
                        mask = resample2staticmap(target_pix_size,target_dim,uc,mask)
                        arr = resample2staticmap(target_pix_size,target_dim,uc,arr)
                        arr_unmask = arr
                        fhf1_randomized = get_randomized_sf(resol_grid,arr_unmask,self.resol_rand)
                        arr_rand = np.real(np.fft.ifftn(np.fft.ifftshift(fhf1_randomized))) * mask
                        if run_once: com1 = ndimage.measurements.center_of_mass(arr * mask)
                        run_once = False
                        arr_mask = shift(arr * mask, np.subtract(box_centr,com1))
                        arr_unmask = shift(arr_unmask, np.subtract(box_centr,com1)) 
                        arr_rand = shift(arr_rand, np.subtract(box_centr,com1))
                        fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_mask))))
                        unmask_fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_unmask))))
                        phrand_fhf_lst.append(np.fft.fftshift(np.fft.fftn(np.fft.fftshift(arr_rand))))
                
            # free memory
            del arr, arr1, arr2
            #            
            self.map_origin     = map_origin
            self.map_unit_cell  = uc_target
            self.map_dim        = target_dim 
            self.fhf_lst        = fhf_lst 
            self.unmask_fhf_lst = unmask_fhf_lst 
            self.phrand_fhf_lst = phrand_fhf_lst

    def calc_fsc_variance_from_halfdata(self, fobj): 
        import fcodes_fast 
        from emda import restools
        from scipy.ndimage.interpolation import shift
        nmaps = len(self.fhf_lst) 
        fFo_lst = []
        fEo_lst = []
        fBNV_lst = []
        fBSV_lst = []
        fBTV_lst = []
        fBFsc_lst = []
        umfFo_lst = []
        umfEo_lst = []
        umfBNV_lst = []
        umfBSV_lst = []
        umfBTV_lst = []
        umfBFsc_lst = []
        #
        fobj.write('\n Calculating Fourier Shell Correlation using half data \n')
        fobj.write('   ----------------------------------------------------- \n')
        fobj.write('\n')
        nx,ny,nz = self.fhf_lst[0].shape
        self.nbin,self.res_arr,self.bin_idx = restools.get_resolution_array(self.map_unit_cell,
                                                                       self.fhf_lst[0])
        idx = np.argmin((self.res_arr - self.resol_rand)**2)
        #
        for i in range(0,nmaps,2): 
            # unmasked data
            fobj.write('Unmasked maps %s\n' %os.path.abspath(self.hfmap_list[i]))
            fobj.write('              %s\n' %os.path.abspath(self.hfmap_list[i+1]))
            fobj.write('\n')
            umbin_fsc,umnoisevar,umsignalvar,umtotalvar,umfo,umeo = fsc.halfmaps_fsc_variance(
                                                             self.unmask_fhf_lst[i],
                                                             self.unmask_fhf_lst[i+1],
                                                             self.bin_idx,
                                                             self.nbin)
            #umfo,umeo,umnoisevar,umsignalvar,umtotalvar,umbin_fsc = fcodes_fast.calc_fsc_using_halfmaps(
            #    self.unmask_fhf_lst[i],self.unmask_fhf_lst[i+1],self.bin_idx,self.nbin,debug_mode,nx,ny,nz)
            data2write = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(umfo))))
            data2write = shift(data2write, np.subtract(self.com_lst[0],self.box_centr))
            write_mrc(data2write,'test4.mrc',self.map_unit_cell,self.map_origin)
            fobj.write(' bin# \n')
            fobj.write(' bin resolution (A) \n')
            fobj.write(' Signal Variance \n')
            fobj.write(' Noise variance \n')
            fobj.write(' Total variance \n')
            fobj.write(' Halfmap FSC \n')
            fobj.write('\n')
            for j in range(len(self.res_arr)):
                fobj.write("{:5d} {:6.2f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}\n".format(
                            j,
                            self.res_arr[j],
                            umsignalvar[j],
                            umnoisevar[j],
                            umtotalvar[j],
                            umbin_fsc[j]))
            full_fsc_unmasked = 2.0 * umbin_fsc / (1.0 + umbin_fsc)
            # masked data
            fobj.write('\n')
            fobj.write('Masked maps %s\n' %os.path.abspath(self.hfmap_list[i]))
            fobj.write('            %s\n' %os.path.abspath(self.hfmap_list[i+1]))
            fobj.write('\n')
            bin_fsc,noisevar,signalvar,totalvar,fo,eo = fsc.halfmaps_fsc_variance(self.fhf_lst[i],
                                                             self.fhf_lst[i+1],
                                                             self.bin_idx,
                                                             self.nbin)
            #fo,eo,noisevar,signalvar,totalvar,bin_fsc = fcodes_fast.calc_fsc_using_halfmaps(
            #    self.fhf_lst[i],self.fhf_lst[i+1],self.bin_idx,self.nbin,debug_mode,nx,ny,nz) 
            # test
            data2write = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(fo))))
            data2write = shift(data2write, np.subtract(self.com_lst[0],self.box_centr))
            write_mrc(data2write,'test5.mrc',self.map_unit_cell,self.map_origin)
            exit()
            #
            fobj.write(' bin# \n')
            fobj.write(' bin resolution (A) \n')
            fobj.write(' Signal Variance \n')
            fobj.write(' Noise variance \n')
            fobj.write(' Total variance \n')
            fobj.write(' Halfmap FSC \n')
            fobj.write('\n')
            for j in range(len(self.res_arr)):
                fobj.write("{:5d} {:6.2f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}\n".format(
                            j,
                            self.res_arr[j],
                            signalvar[j],
                            noisevar[j],
                            totalvar[j],
                            bin_fsc[j]))
            full_fsc_total = 2.0 * bin_fsc / (1.0 + bin_fsc)
            #weighted_grid = fcodes_fast.read_into_grid(self.bin_idx,bin_fsc,self.nbin,nx,ny,nz)
            #data2write = np.real(np.fft.ifftshift(np.fft.ifftn(np.fft.ifftshift(eo * weighted_grid))))
            #write_mrc(data2write,'weightedmap.mrc',self.map_unit_cell)
            #exit()
            # randomised data
            rbin_fsc,_,_,_,_,_ = fsc.halfmaps_fsc_variance(self.phrand_fhf_lst[i],
                                                             self.phrand_fhf_lst[i+1],
                                                             self.bin_idx,
                                                             self.nbin)
            #_,_,_,_,_,rbin_fsc = fcodes_fast.calc_fsc_using_halfmaps(
            #    self.phrand_fhf_lst[i],self.phrand_fhf_lst[i+1],self.bin_idx,self.nbin,debug_mode,nx,ny,nz)
            full_fsc_noise = 2.0 * rbin_fsc / (1.0 + rbin_fsc)

            # fsc_true from Richard's formular
            fsc_true = (full_fsc_total - full_fsc_noise) / (1 - full_fsc_noise)
            # replace fsc_true with fsc_masked_full upto resol_rand_idx + 2 (RELION uses 2)
            fsc_true[:idx+2] = full_fsc_total[:idx+2] 

            # override fec_true with fsc_unmasked
            #fsc_true = full_fsc_unmasked
            fobj.write('\n')
            fobj.write(' All halfmap FSCs have been converted into fullmap FSC \n')
            fobj.write('\n')
            fobj.write(' bin# \n')
            fobj.write(' bin resolution (A) \n')
            fobj.write(' Unmasked FSC \n')
            fobj.write(' Masked FSC \n')
            fobj.write(' Randomized FSC \n')
            fobj.write(' True FSC \n')
            fobj.write('\n')
            for j in range(len(self.res_arr)):
                fobj.write("{:5d} {:6.2f} {:8.4f} {:8.4f} {:8.4f} {:8.4f}\n".format(
                            j,
                            self.res_arr[j],
                            full_fsc_unmasked[j],
                            full_fsc_total[j],
                            full_fsc_noise[j],
                            fsc_true[j]))

            # plot various FSCs
            fobj.write('\n FSC were plotted into fsc_%d.eps \n' %i)
            emda.plotter.plot_nlines(self.res_arr,
                                [full_fsc_unmasked,full_fsc_total,full_fsc_noise,fsc_true],
                                "{0}_{1}.{2}".format('fsc',str(i),'eps'),
                                ["unmasked","fsc_t","fsc_n","fsc_true"])
            
            fFo_lst.append(fo)
            fEo_lst.append(eo)
            fBNV_lst.append(noisevar)
            fBSV_lst.append(signalvar)
            fBTV_lst.append(totalvar)
            fBFsc_lst.append(fsc_true)
            #umfFo_lst.append(umfo)
            #umfEo_lst.append(umeo)
            #umfBNV_lst.append(umnoisevar)
            #umfBSV_lst.append(umsignalvar)
            #umfBTV_lst.append(umtotalvar)
            #umfBFsc_lst.append(umbin_fsc)
        #
        self.fo_lst            = fFo_lst
        self.eo_lst            = fEo_lst
        self.signalvar_lst     = fBSV_lst
        self.totalvar_lst      = fBTV_lst
        self.hffsc_lst         = fBFsc_lst
        #self.umfo_lst            = umfFo_lst
        #self.umeo_lst            = umfEo_lst
        #self.umsignalvar_lst     = umfBSV_lst
        #self.umtotalvar_lst      = umfBTV_lst
        #self.umhffsc_lst         = umfBFsc_lst
