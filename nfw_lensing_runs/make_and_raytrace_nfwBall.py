import os
import sys
import pdb
sys.path.append('/home/hollowed/repos/mpwl-raytrace/NFW_test_cases') # cooley
sys.path.append('/Users/joe/repos/mpwl-raytrace/NFW_test_cases') # miniroomba
from make_simple_halo import NFW
from raytrace_simple_halo import raytracer


# ======================================================================================================


def make_halo(zl=0.3, zs=1.0, N=10000, rfrac=6, rfrac_los=6, 
              nsrcs=10000, lenspix=1024, out_dir='./output', vis=False,
              density_estimator='dtfe', seed=606):
    '''
    Generate an NFW particle distribution and place it at a redshift z via the methods in mpwl_raytrace

    Parameters
    ----------
    zl : float, optional
        redshift of lens; defaults to 0.2
    zs : float, optional
        redshift of sources; defaults to 1.0
    N : int, optional
        number of particles to draw; defaults to 10000
    rfrac : float, optional
        physical extent of generated particle set in units of r200c; defaults to 6
    rfrac_los : float, optional
        physical extent of generated particle set in units of r200c in the line-of-sight dimension. 
        Defaults to None, in which case it is set to match rfrac
    nsrcs : int
        Number of sources to place on the source plane. Defaults to 10000
    lenspix : int
        Number of pixels on one side of the grid on which to compute density and lensing quantities
        (total number of pixels is lenspix^2)
    out_dir : str, optinal
        location for output, does not have to exist; defaults to "./output/" where "." is the current
        working directory. Within this location, a directory will be created as 
        "halo_z{:.2f}_N{}_{:.2f}r200c".format(z, N, rfrac)
    vis : bool, optional
        flag to send to make_simple_halo to generate a figure of the NFW particles or not
    density_estimator : string, optional
        which density estimator to use; either 'dtfe' or 'sph'
    seed : float, optional
            Random seed to pass to HaloTools for generation of radial particle positions, and
            use for drawing concentrations and angular positions of particles. None for stocahstic
            results
    '''

    out_dir=os.path.abspath("{}/halo_zl{:.2f}_zs{:.2f}_N{}_{:.2f}r200c_{:.2f}r200clos_nsrcs{}_lenspix{}".format(
                             out_dir, zl, zs, N, rfrac, rfrac_los, nsrcs, lenspix))

    print('\n\n=============== working on halo at {} ==============='.format(out_dir.split('/')[-1]))
    print('Populating halo with particles')
    halo = NFW(m200c = 1e14, z=zl, seed=seed)
    halo.populate_halo(N=N, rfrac=rfrac, rfrac_los=rfrac_los)
    print('writing out')
    halo.output_particles(output_dir = out_dir, vis_debug=vis)
    
    raytrace_lens(out_dir, zs=[zs], vis=vis, nsrcs=nsrcs, lenspix=lenspix, density_estimator=density_estimator)


# ======================================================================================================


def raytrace_lens(halo_dir, nsrcs, lenspix, lensing_dir=None, zs=[1.0], seed=606, vis=False, density_estimator='dtfe'):
    '''
    Compute lensing maps for an NFW particle distribution for a single lens plane and a source population zs

    Parameters
    ----------
    halo_dir : str
        location of output of make_halo output (out_dir arg in make_halo())
    nsrcs : int
        Number of sources to place on the source plane. Defaults to 10000
    lenspix : int
        Number of pixels on one side of the grid on which to compute density and lensing quantities
        (total number of pixels is lenspix^2)
    lensing_dir : str, optional
        location for lensing output, does not have to exist; defaults to 
        "{}/lensing_maps/zs_{}".format(halo_dir, zs)
    zs : list, optional
        source redshift to populate; defaults [1.0], to a single source plane at z=1
    seed : float, optional
        Random seed to pass to make_lensing_mocks for placement of interpolation points on lensing
        maps. None gives stochastic results.
    vis : bool, optional
        flag to send to the raytracing modules to generate shear/deflection figures or not (takes long)
    density_estimator : string, optional
        which density estimator to use; either 'dtfe' or 'sph'
    '''
    if(lensing_dir is None):
        lensing_dir="{}/lensing_maps_zs_{}".format(halo_dir, '_'.join(map(str, zs)))
    
    print('raytracing from zs = {}'.format(zs))
    rt = raytracer(halo_dir, lensing_dir, zs, seed=seed)
    rt.halo_raytrace(nsrcs, lenspix, density_estimator)
    if(vis):
        print('drawing lensing maps'.format(zs))
        rt.vis_outputs()


# ===============================================================================



if __name__ == '__main__':

    # default params
    zl, zs, N, rfrac, rfrac_los, nsrcs, lenspix, out_dir, vis, de = \
        0.2, 1.0, 20000, 6, 6, 10000, 1024, './output', True, 'dtfe'

    # override default by argv
    if(len(sys.argv) > 1): zl = float(sys.argv[1])
    if(len(sys.argv) > 2): zs = float(sys.argv[2])
    if(len(sys.argv) > 3): N = int(sys.argv[3])
    if(len(sys.argv) > 4): rfrac = float(sys.argv[4])
    if(len(sys.argv) > 5): rfrac_los = float(sys.argv[5])
    if(len(sys.argv) > 6): nsrcs = int(sys.argv[6])
    if(len(sys.argv) > 7): lenspix = int(sys.argv[7])
    if(len(sys.argv) > 8): out_dir = sys.argv[8]
    if(len(sys.argv) > 9): vis = bool(int(sys.argv[9]))
    if(len(sys.argv) > 10): de = sys.argv[10]

    make_halo(zl, zs, N, rfrac, rfrac_los, nsrcs, lenspix, out_dir, vis, de)
