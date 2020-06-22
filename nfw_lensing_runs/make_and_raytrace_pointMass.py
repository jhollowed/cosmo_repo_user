import os
import sys
import pdb
sys.path.append('/home/hollowed/repos/mpwl-raytrace/NFW_test_cases') # cooley
sys.path.append('/Users/joe/repos/mpwl-raytrace/NFW_test_cases') # miniroomba
from make_simple_halo import NFW
from make_simple_halo import PointMass
from raytrace_simple_halo import raytracer


# ======================================================================================================


def make_pointmass(zl=0.3, zs=1.0, fov_size=1, nsrcs=10000, lenspix=1024, vis=False, out_dir='./output', 
                   density_estimator='dtfe', seed=606):
    '''
    Generate a point mass and place it at a redshift z via the methods in mpwl_raytrace

    Parameters
    ----------
    zl : float, optional
        redshift of lens; defaults to 0.2
    zs : float, optional
        redshift of sources; defaults to 1.0
    fov_size : float, optional
        half-side-length of the fov to construct, in proper Mpc at the lens redshift; defaults to 1
    nsrcs : int
        Number of sources to place on the source plane. Defaults to 10000
    lenspix : int
        Number of pixels on one side of the grid on which to compute density and lensing quantities
        (total number of pixels is lenspix^2)
    vis : bool, optional
        flag to send to make_simple_halo to generate a figure of the NFW particles or not
    out_dir : str, optinal
        location for output, does not have to exist; defaults to "./output/" where "." is the current
        working directory. Within this location, a directory will be created as 
        "halo_z{:.2f}_N{}_{:.2f}r200c".format(z, N, rfrac)
    density_estimator : string, optional
        which density estimator to use; either 'dtfe' or 'sph'
    '''

    out_dir=os.path.abspath("{}/halo_zl{:.2f}_zs{:.2f}_N{}_{:.2f}r200c_{:.2f}r200clos_nsrcs{}_lenspix{}".format(
                             out_dir, zl, zs, N, rfrac, rfrac_los, nsrcs, lenspix))

    print('\n\n=============== working on halo at {} ==============='.format(out_dir.split('/')[-1]))
    print('Placing point mass and writing out')
    pointmass = PointMass(m=1e14, z=zl)
    pointmass.output_particles(fov_size, output_dir=out_dir)
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
    zl, zs, fov_size, nsrcs, lenspix, out_dir, vis, de = \
        0.2, 1.0, 1, 10000, 1024, './output', True, 'dtfe'

    # override default by argv
    if(len(sys.argv) > 1): zl = float(sys.argv[1])
    if(len(sys.argv) > 2): zs = float(sys.argv[2])
    if(len(sys.argv) > 3): fov_size = float(sys.argv[4])
    if(len(sys.argv) > 4): nsrcs = int(sys.argv[6])
    if(len(sys.argv) > 5): lenspix = int(sys.argv[7])
    if(len(sys.argv) > 6): out_dir = sys.argv[8]
    if(len(sys.argv) > 7): vis = bool(int(sys.argv[9]))
    if(len(sys.argv) > 8): de = sys.argv[10]

    make_pointmass(zl, zs, fov_size, nsrcs, lenspix, vis, out_dir, de)
