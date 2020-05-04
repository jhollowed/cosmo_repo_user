import os
import pdb
import sys
import h5py
import glob
import cycler
import numpy as np
from scipy import stats
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt

sys.path.insert(0, "/Users/joe/repos/shearfit/shearfit")
from analytic_profiles import NFW
from astropy.cosmology import WMAP7
from lensing_system import obs_lens_system
from mass_concentration import child2018 as cm
from fit_profile import fit_nfw_profile_lstq as fit
from fit_profile import fit_nfw_profile_gridscan as fit_gs
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=71, Om0=0.220, Ob0=0.02258*(0.71**2), name='OuterRim')

def nfw_test(halo_cutout_dir='/Users/joe/repos/mpwl-raytrace/NFW_test_cases/lensing_output/nfw_0.1', 
             makeplot = True, showfig=True, stdout=True, bin_data=True, rbins=25, rmin=0, nfw=False):
    """
    This function performs an example run of the package, fitting an NFW profile to background 
    source data as obtained from ray-tracing through Outer Rim lightcone halo cutouts. The process 
    is as follows:
    1) sources positions, redshifts, and shears are read in from ray-tacing outputs
    4) an NFW profile is fit to the scaled tangential shear ΔΣ = γ_t * Σ_c, using three methods:
        - allow both the concentration and halo radius to float
        - only fit the halo radius, inferring the concentration from a c-M relation
        - do a grid scan over the parameter pair including radius and concentration
    
    Parameters
    ----------
    halo_dir : string
        Path to a halo cutout ray-tacing output directory. If `None`, then randomly select a simulated
        halo from those available on the filesystem (assumes the code to be running on Cori at NERSC). 
        This directory is assumed to contain an HDF5 file giving ray-traced maps, as well as a properties.csv
        file, containing the intrinsic halo properties from the simulation.
    max_z : float
        The maximum number of lens planes used about the halo redshift in the ray tracing
    makeplot : boolean
        Whether or not to make render a plot. If `True`, perform a  grid scan in addition to the 
        two profile fits to plot residuals over parameter space. If `False`, return after fit and
        skip parameter sweep, plot nothing. Defaults to `True`.
    showfig : boolean
        Whether or not to `show` the profile fit plot. If `False`, save to `png` file instead. 
        Defaults to `True`.
    stdout : bool
        Whether or not to supress print statements (useful for parallel runs). `False` means all
        print statements will be suppressed. Defaults to `True`.
    bin_data : bool
        whether or not to fit to shears averaged in radial bins, rather than to each individual source.
        Defaults to `True`.
    rbins : int
        Number of bins distribute over the radial range of the data, if `bin_data == True`.
    rmin : float
        The minimum radial distance of sources to include in the fit in Mpc/h (e.g. `rmin = 0.3` will
        remove the inner 300kpc/h of source information). Defaults to `0`.
    """
    
    global pprint
    if(stdout == True): pprint = lambda s: print(s, flush=True)
    else: pprint = lambda s: None

    pprint('reading lensing mock data')
    [sim_lens, true_profile] = read_nfw(halo_cutout_dir)
    #out_dir = '{}/profile_fits'.format(halo_cutout_dir)
    out_dir = './profile_fits'
    if not os.path.exists(out_dir): os.makedirs(out_dir)
    fit_nfw(sim_lens, true_profile, showfig=showfig, 
            out_dir=out_dir, makeplot = makeplot, bin_data=bin_data, 
            rbins=rbins, rmin=rmin, nfw=nfw)


def read_nfw(halo_cutout_dir):

    # get ray-trace hdf5 and properties csv
    rtfs = glob.glob('{}/*mock*.hdf5'.format(halo_cutout_dir))
    #rtfs = glob.glob('{}/*grid*.hdf5'.format(halo_cutout_dir))
    
    pfs = glob.glob('{}/properties.csv'.format(halo_cutout_dir))
    assert len(pfs) == 1, "Exactly one properties file is expected in {}".format(halo_cutout_dir)

    # read lens properties from csv, source data from hdf5
    props_file = pfs[0]
    props = np.genfromtxt(props_file, delimiter=',', names=True)
    zl = props['halo_redshift']
    r200c = props['sod_halo_radius']
    c = props['sod_halo_cdelta']
    c_err = props['sod_halo_cdelta_error']
    m200c = props['sod_halo_mass']
    true_profile = NFW(r200c, c, zl, c_err = c_err, cosmo=cosmo)
    
    raytrace_file = h5py.File(rtfs[0], 'r')
    nplanes = len(list(raytrace_file.keys()))
    t1, t2, y1, y2, k, zs = [], [], [], [], [], []

    # stack data from each source plane
    for i in range(nplanes):
        plane_key = list(raytrace_file.keys())[i]
        plane = raytrace_file[plane_key]
        
        # for running with mocks (fitting to shears)
        plane_z = plane['zs'][0]   
        # for running with grids (fitting to density)
        #plane_z = 10

        #ignore this plane if infront of the halo
        if(plane_z < zl): continue
         
        y1 = np.hstack([y1, np.ravel(plane['shear1'][:])])
        y2 = np.hstack([y2, np.ravel(plane['shear2'][:])])
        t1 = np.hstack([t1, np.ravel(plane['x1'][:])])
        t2 = np.hstack([t2, np.ravel(plane['x2'][:])])
        k = np.hstack([k, np.ravel(plane['kappa0'][:])])
        zs = np.hstack([zs, np.ones(len(t1)-len(zs)) * plane_z])
        
        # if using grid maps with density output
        #rho = np.hstack([k, np.ravel(plane['density'][:])])
        # otherwise
        rho = None
    
    # trim the fov borders by 10% to be safe
    mask = np.logical_and(np.abs(t1)<props['boxRadius_arcsec']*0.9, 
                          np.abs(t2)<props['boxRadius_arcsec']*0.9)
    t1 = t1[mask]
    t2 = t2[mask]
    zs = zs[mask]
    y1 = y1[mask]
    y2 = y2[mask]
    k = k[mask]
    
    sim_lens = obs_lens_system(zl)
    sim_lens.set_background(t1, t2, zs, y1=y1, y2=y2, k=k, rho=rho)

    raytrace_file.close()
    
    return [sim_lens, true_profile]

    
def fit_nfw(lens, true_profile, makeplot=True, showfig=False, out_dir='.', 
                   bin_data=True, rbins=25, rmin = 0, nfw=False):

    zl = lens.zl
    r200c = true_profile.r200c
    m200c = true_profile.radius_to_mass()
    c = true_profile.c
    bg = lens.get_background()
    sigmaCrit = lens.calc_sigma_crit()
    yt = bg['yt']
    r = bg['r']
    k = bg['k']
    zs = bg['zs']

    # do inner radius cut and bin data
    pprint('doing radial masking and binning')
    radial_mask = (r >= rmin)
    sigmaCrit = sigmaCrit[radial_mask]
    yt = yt[radial_mask]
    r = r[radial_mask]
    k = k[radial_mask]
    zs = zs[radial_mask]
        
    # if using grid maps with density output
    #rho = rho[radial_mask]
    #fit_var = rho
    # otherwise
    fit_var = yt*sigmaCrit

    
    binned_dsig = stats.binned_statistic(r, fit_var, statistic='mean', bins=rbins)
    binned_r = stats.binned_statistic(r, r, statistic='mean', bins=rbins)

    rsamp = np.linspace(min(r), max(r), 1000)
    dSigma_true = true_profile.delta_sigma(rsamp)

    e = true_profile.sigma(r)
    se = true_profile.delta_sigma(r)
    kk = k * sigmaCrit
    binned_kk = stats.binned_statistic(r, kk, statistic='mean', bins=rbins)
    binned_yt = stats.binned_statistic(r, yt, statistic='mean', bins=rbins)
    

    # fit the concentration and radius
    pprint('fitting with floating concentration')
    fitted_profile = NFW(0.75, 3.0, zl)
    fit(lens, fitted_profile, rad_bounds = [0.1, 15], conc_bounds = [1, 10], 
        bootstrap=True, bin_data=bin_data, bins=rbins)
    [dSigma_fitted, dSigma_fitted_err] = fitted_profile.delta_sigma(rsamp, bootstrap=True)
    #dSigma_fitted = fitted_profile.delta_sigma(rsamp, bootstrap=False)
    #dSigma_fitted_err = np.zeros(len(dSigma_fitted))

    # and now do it again, iteratively using a c-M relation instead of fitting for c
    pprint('fitting with inferred c-M concentration')
    fitted_cm_profile = NFW(0.75, 3.0, zl)
    fit(lens, fitted_cm_profile, rad_bounds = [0.1, 15], cM_relation='child2018', 
        bootstrap=True, bin_data=bin_data, bins=rbins)
    [dSigma_fitted_cm, dSigma_fitted_cm_err] = fitted_cm_profile.delta_sigma(rsamp, bootstrap=True)
    #dSigma_fitted_cm = fitted_profile.delta_sigma(rsamp, bootstrap=False)
    #dSigma_fitted_cm_err = np.zeros(len(dSigma_fitted_cm))
    
    # write out fitting result
    pprint('r200c_fit = {:.4f}; m200c_fit = {:.4e}; c_fit = {:.2f}'.format(fitted_profile.r200c,
                                                                           fitted_profile.radius_to_mass(), 
                                                                           fitted_profile.c))
    pprint('r200c_cm = {:.4f}; m200c_cm = {:.4e}; c_cm = {:.2f}'.format(fitted_cm_profile.r200c, 
                                                                        fitted_cm_profile.radius_to_mass(), 
                                                                        fitted_cm_profile.c))
    pprint('r200c_true = {:.4f}; m200c_true = {:.4e}; c_true = {:.2f}'.format(r200c, 
                                                                              m200c, 
                                                                              c))
    np.save('{}/r200c_fit_{}bins_{}rmin.npy'.format(out_dir, rbins, rmin), fitted_profile.r200c)
    np.save('{}/r200c_cM_fit_{}bins_{}rmin.npy'.format(out_dir, rbins, rmin), fitted_cm_profile.r200c)
    np.save('{}/c_fit_{}bins_{}rmin.npy'.format(out_dir, rbins, rmin), fitted_profile.c)
    np.save('{}/c_cM_fit_{}bins_{}rmin.npy'.format(out_dir, rbins, rmin), fitted_cm_profile.c)

    # now do a grid scan
    pprint('doing grid scan')
    gridscan_profile = NFW(0.75, 3.0, zl)
    grid_r_bounds = [0.01, 1.2]
    grid_c_bounds = [0.5, 10]
    [grid_pos, grid_res] = fit_gs(lens, gridscan_profile, rad_bounds = grid_r_bounds, conc_bounds = grid_c_bounds, 
                                  n=100, bin_data=bin_data, bins=rbins)
    
    # visualize results... 
    rc('text', usetex=True)
    color = plt.cm.plasma(np.linspace(0.2, 0.8, 3))
    mpl.rcParams['axes.prop_cycle'] = cycler.cycler('color', color)

    # plot sources vs truth and both fits
    f = plt.figure(figsize=(12,6))
    ax = f.add_subplot(121)
    rR = rsamp/r200c

    if(not bin_data):
        ax.loglog(r/r200c, fit_var, 'xk', 
                label=r'$\gamma_{\mathrm{NFW}}\Sigma_c$', alpha=0.33)
    else:
        if(nfw):
            img = '/Users/joe/Desktop/images.jpeg'
            imscatter((binned_r[0]/r200c)[::-1], (binned_dsig[0])[::-1], img, zoom=0.3, ax=ax)
        else:
            ax.plot(binned_r[0]/r200c, binned_dsig[0], '-xk', 
                    label=r'$\gamma_{\mathrm{NFW}} \Sigma_c$')
    
    ax.plot(rR, dSigma_true, '--', label=r'$\Delta\Sigma_\mathrm{{NFW}},\>\>r_{{200c}}={:.3f}; c={:.3f}$'\
                                            .format(r200c, c), color=color[0], lw=2)
    ax.plot(rR, dSigma_fitted, label=r'$\Delta\Sigma_\mathrm{{fit}},\>\>r_{{200c}}={:.3f}; c={:.3f}$'\
                                        .format(fitted_profile.r200c, fitted_profile.c), color=color[1], lw=2)
    ax.plot(rR, dSigma_fitted_cm, label=r'$\Delta\Sigma_{{\mathrm{{fit}},c-M}},\>\>r_{{200c}}={:.3f}; c={:.3f}$'\
                                           .format(fitted_cm_profile.r200c, fitted_cm_profile.c), 
                                           color=color[2], lw=2)
    ax.fill_between(rR, dSigma_fitted - dSigma_fitted_err.T[0], 
                           dSigma_fitted + dSigma_fitted_err.T[1], 
                           color=color[1], alpha=0.2, lw=0)
    ax.fill_between(rR, dSigma_fitted_cm - dSigma_fitted_cm_err.T[0], 
                           dSigma_fitted_cm + dSigma_fitted_cm_err.T[1], 
                           color=color[2], alpha=0.33, lw=0)
    #ax.set_xscale('log')
    #ax.set_yscale('log')

    # format
    ax.legend(fontsize=12, loc='best')
    ax.set_xlabel(r'$r/R_{200c}$', fontsize=14)
    ax.set_ylabel(r'$\Delta\Sigma\>\>\lbrack\mathrm{M}_\odot\mathrm{pc}^{-2}\rbrack$', fontsize=14)


    # plot fit cost in the radius-concentration plane
    ax2 = f.add_subplot(122)
    chi2 = ax2.pcolormesh(grid_pos[0], grid_pos[1], (1/grid_res)/(np.max(1/grid_res)), cmap='plasma')
    ax2.plot([r200c], [c], 'xk', ms=10, label=r'$\mathrm{{truth}}$')
    ax2.errorbar(fitted_profile.r200c, fitted_profile.c, 
                 xerr=fitted_profile.r200c_err, yerr=fitted_profile.c_err, 
                 ms=10, marker='.', c=color[1], label=r'$\mathrm{{fit}}$')
    ax2.errorbar(fitted_cm_profile.r200c, fitted_cm_profile.c, 
                 xerr=fitted_cm_profile.r200c_err, yerr=fitted_cm_profile.c_err, 
                 ms=10, marker='.', c=color[2], label=r'${\mathrm{{fit\>w/}c\mathrm{-}M}}$')

    # include c-M relation curve
    tmp_profile = NFW(1,1,zl)
    tmp_m200c = np.zeros(len(grid_pos[0][0]))
    for i in range(len(tmp_m200c)):
        tmp_profile.r200c = grid_pos[0][0][i]
        tmp_m200c[i] = tmp_profile.radius_to_mass()
    tmp_c, tmp_dc = cm(tmp_m200c, zl, cosmo)
    ax2.plot(grid_pos[0][0], tmp_c, '--k', lw=2, label=r'$c\mathrm{-}M\mathrm{\>relation\>(Child+2018)}$')
    ax2.fill_between(grid_pos[0][0], tmp_c - tmp_dc, tmp_c + tmp_dc, color='k', alpha=0.1, lw=0)

    # format
    ax2.set_xlim(grid_r_bounds)
    ax2.set_ylim(grid_c_bounds)
    ax2.legend(fontsize=12, loc='upper right')
    cbar = f.colorbar(chi2, ax=ax2)
    cbar.set_label(r'$\mathrm{min}(\chi^2)/\chi^2$', fontsize=14)
    ax2.set_xlabel(r'$R_{200c}\>\>\left[\mathrm{Mpc/h}\right]$', fontsize=14)
    ax2.set_ylabel(r'$c_{200c}$', fontsize=14)

    plt.tight_layout()
    plt.show()
    #RRR if(showfig): plt.show()
    if(bin_data and nfw):
        f.savefig('{}/{}_shearprof_fit_{}bins_{}rmin_nfw.png'.format(out_dir, zl, rbins, rmin), dpi=300)
    if(bin_data and not nfw):
        f.savefig('{}/{}_shearprof_fit_{}bins_{}rmin.png'.format(out_dir, zl, rbins, rmin), dpi=300)
    else:
        f.savefig('{}/{}_shearprof_fit_{}rmin.png'.format(out_dir, zl, rmin), dpi=300)


def imscatter(x, y, image, ax=None, zoom=1):
    if ax is None:
        ax = plt.gca()
    try:
        image = plt.imread(image)
    except TypeError:
        # Likely already an array...
        pass
    im = OffsetImage(image, zoom=zoom)
    x, y = np.atleast_1d(x, y)
    artists = []
    for x0, y0 in zip(x, y):
        ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
        artists.append(ax.add_artist(ab))
    ax.update_datalim(np.column_stack([x, y]))
    ax.autoscale()
    return artists

if(__name__ == "__main__"): 
    nfw_test(halo_cutout_dir = '/Users/joe/repos/repo_user/nfw_lensing_runs/realizations/halo_z0.20_N10000_6.00r200c/lensing_maps_zs_1.0', bin_data=False, rmin=0.2)
