import os
import sys
import pdb
import numpy as np
import astropy.units as u

sys.path.append('/home/hollowed/repos/mpwl-raytrace/test_cases') # cooley
sys.path.append('/home/hollowed/repos/mpwl-raytrace/') # cooley
sys.path.append('/Users/joe/repos/mpwl-raytrace/test_cases') # miniroomba
sys.path.append('/Users/joe/repos/mpwl-raytrace/') # miniroomba
from make_simple_lens import NFW
from raytrace_simple_lens import raytracer
import cosmology as cm


# ======================================================================================================


def make_halo(zl=0.3, zs=1.0, N=10000, rmax=6, depth=6, nsrcs=10000, 
              lenspix=1024, out_dir='./output', vis=False, density_estimator='dtfe', 
              seed=606, skip_raytrace=False, cosmo = cm.OuterRim_params):
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
    rmax : float, optional
        physical extent of generated particle set in units of r200c; defaults to 6
    depth : float, optional
        physical extent of generated particle set in units of r200c in the line-of-sight dimension. 
        Defaults to None, in which case it is set to match rmax
    nsrcs : int
        Number of sources to place on the source plane. Defaults to 10000
    lenspix : int
        Number of pixels on one side of the grid on which to compute density and lensing quantities
        (total number of pixels is lenspix^2)
    out_dir : str, optinal
        location for output, does not have to exist; defaults to "./output/" where "." is the current
        working directory. Within this location, a directory will be created as 
        "halo_z{:.2f}_N{}_{:.2f}r200c".format(z, N, rmax)
    vis : bool, optional
        flag to send to make_simple_halo to generate a figure of the NFW particles or not
    density_estimator : string, optional
        which density estimator to use; either 'dtfe' or 'sph'
    seed : float, optional
            Random seed to pass to HaloTools for generation of radial particle positions, and
            use for drawing concentrations and angular positions of particles. None for stocahstic
            results
    skip_raytrace : bool, optional
        Whether or not to skip the raytracing, outputting only the generated particle set. 
        Defaults to False.
    cosmo : astropy cosmology object, optional
        The cosmology object to use in the particle generation and lensing. Defaults to Outer Rim
    '''

    out_dir=os.path.abspath("{}/halo_zl{:.2f}_zs{:.2f}_N{}_{:.2f}r200c_{:.2f}r200clos_nsrcs{}_lenspix{}_seed{}".format(
                             out_dir, zl, zs, N, rmax, depth, nsrcs, lenspix, seed))

    print('\n\n=============== working on halo at {} ==============='.format(out_dir.split('/')[-1]))
    print('Populating halo with particles')
    
    # set radius such that m200c = 1e14 at z=0, and concentration from child c-M relation at z=0
    # verified with halotools
    m200c = 1e14
    c = 4.37
    rho = cm.rho_crit_z0().value
    r200c = (3*m200c/(4*np.pi*rho*200))**(1/3)

    halo = NFW(r200c=r200c, c=c, z=zl, seed=seed)
    halo.populate_halo(N=N, rfrac=rmax)
    #halo.populate_halo_fov(N=N, rfrac=rmax, depth=depth)
    
    print('writing out')
    halo.output_particles(output_dir=out_dir, vis_debug=vis)
    
    print('starting raytrace')
    if(not skip_raytrace):
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
    zl, zs, N, rmax, depth, nsrcs, lenspix, out_dir, vis, de, seed, skip_raytrace = \
        0.2, 1.0, 20000, 6, 6, 10000, 1024, './output', True, 'dtfe', 606, False

    # override default by argv
    if(len(sys.argv) > 1): zl = float(sys.argv[1])
    if(len(sys.argv) > 2): zs = float(sys.argv[2])
    if(len(sys.argv) > 3): N = int(sys.argv[3])
    if(len(sys.argv) > 4): rmax = float(sys.argv[4])
    if(len(sys.argv) > 5): depth = float(sys.argv[5])
    if(len(sys.argv) > 6): nsrcs = int(sys.argv[6])
    if(len(sys.argv) > 7): lenspix = int(sys.argv[7])
    if(len(sys.argv) > 8): out_dir = sys.argv[8]
    if(len(sys.argv) > 9): vis = bool(int(sys.argv[9]))
    if(len(sys.argv) > 10): de = sys.argv[10]
    if(len(sys.argv) > 11): seed = int(sys.argv[11])
    if(len(sys.argv) > 12): skip_raytrace = bool(sys.argv[12])

    make_halo(zl, zs, N, rmax, depth, nsrcs, lenspix, out_dir, vis, de, seed, skip_raytrace)
