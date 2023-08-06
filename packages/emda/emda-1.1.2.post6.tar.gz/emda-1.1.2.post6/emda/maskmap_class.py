# this code generates the mask if not supplied. 
# then ally that mask to arr.
from __future__ import absolute_import, division, print_function, unicode_literals

from emda.config import *

class MaskedMaps:
    def __init__(self,hfmap_list=None):
        self.hfmap_list = hfmap_list

    def read_halfmaps(self):
        from emda import iotools
        for n in range(0,len(self.hfmap_list),2):
            uc,arr1,origin = iotools.read_map(self.hfmap_list[n])
            uc,arr2,origin = iotools.read_map(self.hfmap_list[n+1])
        self.uc = uc
        self.arr1 = arr1
        self.arr2 = arr2
        self.origin = origin

    def generate_mask(self, arr1, arr2):
        from emda import realsp_corr_3d
        from emda.restools import create_soft_edged_kernel_pxl
        kern = create_soft_edged_kernel_pxl(10) # sphere with radius of n pixles
        _,fullcc3d = realsp_corr_3d.get_3d_realspcorrelation(arr1,arr2,kern)
        #iotools.write_mrc(fullcc3d,'fullcc3d.mrc',self.uc,self.origin)
        cc_mask, threshold = self.histogram(fullcc3d)
        mask = fullcc3d * (fullcc3d >= threshold)
        #iotools.write_mrc(mask*cc_mask,'mask.mrc',self.uc,self.origin)
        self.mask = mask*cc_mask
        #self.fullcc3d = fullcc3d
        self.arr1 = arr1 * self.mask
        self.arr2 = arr2 * self.mask        

    def create_edgemask(self, radius):
        import numpy as np
        # Remove everything outside radius
        box_radius = radius + 1
        box_size = radius * 2 + 1
        # Creating a sphere mask
        center = [box_radius, box_radius, box_radius]
        print('boxsize: ',box_size,'boxradius: ',box_radius,'center:',center)
        radius = box_radius
        X, Y, Z = np.ogrid[:box_size, :box_size, :box_size]
        dist_from_center = np.sqrt((X - center[0])**2 + (Y-center[1])**2 + (Z-center[2])**2)
        mask = dist_from_center <= radius
        return mask

    def histogram(self, arr1):
        import numpy as np
        from scipy import stats
        nx, ny, nz = arr1.shape
        maxbin = np.amax(np.array([nx//2,ny//2,nz//2]))
        counts = stats.binned_statistic(arr1.flatten(),
                                        arr1.flatten(),
                                        statistic='count',
                                        bins=maxbin,
                                        range=(0,1))[0]
        sc = counts - np.roll(counts,1)
        ulim = len(sc) - 11 + np.argmax(sc[-10:])
        cc_arr = np.linspace(0,1,maxbin)
        xc = cc_arr[:ulim] * counts[:ulim]
        xc_sum = np.sum(xc)
        isum = 0.0
        cc_arr = cc_arr[:ulim]
        for i in range(len(xc)):
            isum = isum + xc[i]
            if isum >= xc_sum/2:
                threshold = cc_arr[i]
                break
        edge_mask = self.create_edgemask(ulim)
        cc_mask = np.zeros(shape=(nx,ny,nz),dtype='bool')
        cx, cy, cz = edge_mask.shape
        dx = (nx - cx)//2
        dy = (ny - cy)//2
        dz = (nz - cz)//2
        print(dx,dy,dz)
        cc_mask[dx:dx+cx, dy:dy+cy, dz:dz+cz] = edge_mask
        return cc_mask,threshold

    def get_radial_sum(self, arr1):
        # this function not used
        import numpy as np
        from emda import iotools, restools
        import fcodes_fast
        from matplotlib import pyplot as plt
        nx,ny,nz = arr1.shape
        nbin,res_arr,bin_idx = restools.get_resolution_array(self.uc,arr1)
        sum_lst = []
        ibin_lst = []
        isum = 0.0
        isum_old = 0.0
        for ibin in range(nbin):
            ibin_sum = np.sum(arr1 * (bin_idx==ibin))
            ibin_lst.append(ibin_sum)
            isum_old = isum
            isum = isum + ibin_sum
            #if ibin_sum < 0.0 and ibin > 10: 
            if isum <= isum_old and ibin > 10:
                break
            print(ibin,ibin_sum)
            sum_lst.append(isum)
        edge_mask = self.create_edgemask(ibin)
        cc_mask = np.zeros(shape=(nx,ny,nz),dtype='bool')
        cx, cy, cz = edge_mask.shape
        dx = (nx - cx)//2
        dy = (ny - cy)//2
        dz = (nz - cz)//2
        print(dx,dy,dz)
        cc_mask[dx:dx+cx, dy:dy+cy, dz:dz+cz] = edge_mask  
        iotools.write_mrc(arr1*cc_mask,'maskedcc_map.mrc',self.uc,self.origin)    
        #plt.plot(sum_lst,"r")
        plt.plot(ibin_lst,"r")
        plt.show()



if(__name__ == "__main__"):    
    maplist = [
            '/Users/ranganaw/MRC/REFMAC/Bianka/EMD-4572/other/run_half1_class001_unfil.mrc',
            '/Users/ranganaw/MRC/REFMAC/Bianka/EMD-4572/other/run_half2_class001_unfil.mrc'
            ]       
    obj = MaskedMaps(maplist)
    obj.read_halfmaps()
    obj.generate_mask(obj.arr1, obj.arr2)