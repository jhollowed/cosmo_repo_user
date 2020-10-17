import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
binstat = stats.binned_statistic
import scipy
import glob
import h5py
from pyquaternion import Quaternion

import sys
import pdb
import astropy.units as u
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=71, Om0=0.220, Ob0=0.02258*(0.71**2), name='OuterRim')

sys.path.insert(0, "/Users/joe/repos/shearfit/shearfit")
sys.path.insert(0, "/Users/joe/repos/mpwl-raytrace")
import halo_inputs as inps
import cosmology as cm
from analytic_profiles import NFW
from lensing_system import obs_lens_system

class profile_checker():

    def __init__(self, halo_dir):
        
        self.halo_dir = halo_dir
        self.inp = inps.single_plane_inputs(halo_dir, halo_dir)
        self.halo_props = self.inp.halo_props
        
        self.zl = self.halo_props['halo_redshift']
        self.a = 1/(1+self.zl)
        self.c200c = self.halo_props['sod_halo_cdelta']
        self.r200c = self.halo_props['sod_halo_radius']
        self.m200c = self.halo_props['sod_halo_mass']
        self.rs = self.r200c / self.c200c
        self.dc = (200/3) * self.c200c**3 / (np.log(1+self.c200c) - self.c200c/(1+self.c200c))
        self.pc = cosmo.critical_density(self.zl).to(u.solMass/u.Mpc**3)
        self.halo_r = cosmo.comoving_distance(self.zl).value
        
        self.rfrac = float(halo_dir.split('/')[-1].split('r200c_')[0].split('_')[-1])
        
        # define object for computing true profiles
        self.nfw = NFW(self.r200c, self.c200c, self.zl)
        

    def read_particles(self):
        
        self.xxp_los = np.array([])
        self.yyp_los = np.array([])
        self.zzp_los = np.array([])
        self.zp_los = np.array([])
        self.tp_los = np.array([])
        self.pp_los = np.array([])
        self.pdir = self.inp.input_prtcls_dir
        
        columns = ['redshift', 'x', 'y', 'z', 'theta', 'phi']
        arrs = [self.zp_los, self.xxp_los, self.yyp_los, self.zzp_los, self.tp_los, self.pp_los]

        for i in range(len(arrs)):
                arrs[i] = np.fromfile('{0}/{1}.bin'.format(self.pdir, columns[i]), dtype = "f")
        self.zp_los, self.xxp_los, self.yyp_los, self.zzp_los, self.tp_los, self.pp_los = arrs
       
        self.xxp_los = (self.xxp_los - np.mean(self.xxp_los)) * self.a
        self.yyp_los = (self.yyp_los - np.mean(self.yyp_los)) * self.a
        self.zzp_los = (self.zzp_los - np.mean(self.zzp_los)) * self.a
        self.rrp_los = np.linalg.norm([self.xxp_los, self.yyp_los, self.zzp_los], axis=0)

        self.tp_los = self.tp_los - np.mean(self.tp_los)
        self.pp_los = self.pp_los - np.mean(self.pp_los)
        
        self.lens = obs_lens_system(self.zl, cosmo=cosmo)
        self.lens.set_background(self.tp_los, self.pp_los, self.zp_los, yt=np.zeros(len(self.zp_los)))
    
    
    def read_density_estimate(self):
        
        self.xxp_los = np.array([])
        self.yyp_los = np.array([])
        self.zzp_los = np.array([])
        self.zp_los = np.array([])
        self.tp_los = np.array([])
        self.pp_los = np.array([])
        self.pdir = self.inp.input_prtcls_dir
        
        columns = ['redshift', 'x', 'y', 'z', 'theta', 'phi']
        arrs = [self.zp_los, self.xxp_los, self.yyp_los, self.zzp_los, self.tp_los, self.pp_los]

        for i in range(len(arrs)):
                arrs[i] = np.fromfile('{0}/{1}.bin'.format(self.pdir, columns[i]), dtype = "f")
        self.zp_los, self.xxp_los, self.yyp_los, self.zzp_los, self.tp_los, self.pp_los = arrs
       
        self.xxp_los = (self.xxp_los - np.mean(self.xxp_los)) * self.a
        self.yyp_los = (self.yyp_los - np.mean(self.yyp_los)) * self.a
        self.zzp_los = (self.zzp_los - np.mean(self.zzp_los)) * self.a
        self.rrp_los = np.linalg.norm([self.xxp_los, self.yyp_los, self.zzp_los], axis=0)

        self.tp_los = self.tp_los - np.mean(self.tp_los)
        self.pp_los = self.pp_los - np.mean(self.pp_los)
        
        self.lens = obs_lens_system(self.zl, cosmo=cosmo)
        self.lens.set_background(self.tp_los, self.pp_los, self.zp_los, yt=np.zeros(len(self.zp_los)))


    def view_particles(self):
        '''
        Plots the particle positions in projection
        '''
        f = plt.figure()
        ax = f.add_subplot(111)
        ax.scatter(self.xxp_los, self.yyp_los, alpha=0.1)

        ax.set_xlabel(r'$\theta\>\>[\mathrm{arcsec}]$')
        ax.set_ylabel(r'$\phi\>\>[\mathrm{arcsec}]$')
        plt.show()


    def random_rotate_halo(self):
        '''
        Modifies the object by rotating the halo by an azimuth phi.
        '''
        
        u = np.random.uniform(low=0, high=1)
        phi_rot = 2*np.pi*u
        axis = np.random.uniform(low=0, high=1, size=3)

        for i in range(len(self.xxp_los)):
            v = [self.xxp_los[i], self.yyp_los[i], self.zzp_los[i]]
            rotated_r = Quaternion(axis=axis, angle=phi_rot).rotate(v)
            self.xxp_los[i] = rotated_r[0]
            self.yyp_los[i] = rotated_r[1]
            self.zzp_los[i] = rotated_r[2]
        
        xxp_dist = self.xxp_los + self.halo_r
        rrp_dist = np.linalg.norm([xxp_dist, self.yyp_los, self.zzp_los], axis=0)
        
        self.tp_los = np.arccos(self.zzp_los / rrp_dist) * 180/np.pi * 3600
        self.pp_los = np.arctan(self.yyp_los / xxp_dist) * 180/np.pi * 3600 
    

    def measure_numerical_delta_sigma_theory(self, nbins, plot=True, projection='cartesian'):
        '''
        Numerically measure ΔΣ for the analytic truncated profile correction, via Wright+Brainerd Eq. 12, 
        computing the mean surface density interior to a radius x (the integral Eq.13) numerically from 
        the measured projected profile given by self.generate_profile_projected
        
        Parameters
        ----------
        nbins : int
            The number of radial bins to use in the density estimation
        '''
        
        
        # ------------- measure projected profile at bin mean positions --------------
        if(projection == 'cartesian'):
            x1 = self.yyp_los
            x2 = self.zzp_los
            r = np.linalg.norm([self.yyp_los, self.zzp_los], axis=0)
        elif(projection == 'angular'):
            x1 = self.tp_los
            x2 = self.pp_los
            r = np.linalg.norm([self.tp_los, self.pp_los], axis=0) * self.halo_r 
        else:
            raise RuntimeError('pojection must either be \'cartesian\' or \'angular\'')
        
        # ---------- Define integrand from Eq.13 ----------
        interior_x = 1e-3
        x = np.linspace(interior_x, np.max(r)/self.rs, nbins)
        x = np.logspace(np.log10(interior_x), np.log10(np.max(r)/self.rs), nbins)
        sigma_true = (self.nfw.sigma(x*self.rs) * (u.solMass/u.pc**2)).to(u.solMass/u.Mpc**2)
        
        sigma = self.truncated_profile_correction(x)
        integrand = lambda x: np.array(x) * self.truncated_profile_correction(np.array(x))
    
        # ---------- numerically integrate profile ---------- 
        sigma_bar = np.zeros(len(x))
        sigma_bar_err = np.zeros(len(x)) 
        for i in range(len(x)):
            if(i % 10 == 0): print('integrating for x {}/{}'.format(i, len(x)))
            intres, interr = scipy.integrate.quad(integrand, 0, x[i])
            sigma_bar[i]= 2/x[i]**2 * intres
            sigma_bar_err[i] = 2/x[i]**2 * interr
        
        # ---------- find true Σ(<r) from Eq.12 ----------
        sigma_bar_true = np.zeros(len(x))
        pref = (4 * self.rs * self.dc * self.pc)
        x1, x2 = x[x < 1], x[x > 1]
        sigma_bar_true[x < 1] = 1/x1**2 * ((2/np.sqrt(1-x1**2) * np.arctanh(np.sqrt((1-x1)/(1+x1)))) +\
                                np.log(x1/2))
        sigma_bar_true[x == 1] = 1 + np.log(1/2) 
        sigma_bar_true[x > 1] = 1/x2**2 * ((2/np.sqrt(x2**2-1) * np.arctan(np.sqrt((x2-1)/(1+x2)))) +\
                                np.log(x2/2))
        sigma_bar_true = pref * sigma_bar_true
            
        # ---------- find differential surface density ----------
        print('computing delta_sigma')
        delta_sigma = (sigma_bar - sigma) 
        delta_sigma_err = sigma_bar_err 

        # ---------- find true delta sigma ----------
        delta_sigma_true = self.nfw.delta_sigma(x * self.rs) * u.solMass/u.pc**2
        delta_sigma_true = delta_sigma_true.to(u.solMass/u.Mpc**2)
 
        # ---------- plot ----------
        if(plot):
            f = plt.figure(figsize=(16, 12))
            ax = f.add_subplot(321)
            ax.loglog(x, sigma_true, '--k', label='uncorrected')
            ax.errorbar(x, sigma, fmt='-x', label='corrected', color='r')
            if(projection=='cartesian'): ax.set_title('Projected profile')
            ax.set_ylabel('Σ(x) [solMass/Mpc^2]')
            plt.legend()
            
            ax = f.add_subplot(323)
            plt.loglog(x, sigma_true * x, '--k', label='uncorrected')
            plt.errorbar(x, integrand(x), fmt='-x', label='corrected', color='orange')
            ax.set_ylabel('x*Σ(x) [solMass/Mpc^2]')
            plt.legend()
            
            ax = f.add_subplot(325)
            plt.loglog(x, sigma_bar_true, '--k', label='uncorrected')
            plt.errorbar(x, sigma_bar, yerr=sigma_bar_err, fmt='-x', label='corrected', color='m')
            ax.set_xlabel('x')
            ax.set_ylabel('Σ(<x) [solMass/Mpc^2]')
            plt.legend()
            
            ax = f.add_subplot(322)
            ax.loglog(x, delta_sigma_true.value, '--k', label='uncorrected')
            plt.loglog(x, delta_sigma, '-x', label='correctred')
            ax.set_ylabel('Σ(<x) - Σ(x) [solMass/Mpc^2]')
            plt.legend()
            
            ax = f.add_subplot(324)
            ax.plot(x, np.zeros(len(delta_sigma_true)), '--k', label='uncorrected')
            ax.plot(x, (delta_sigma - delta_sigma_true.value)/delta_sigma_true.value, '-x',
                    label='corrected', color='c')
            ax.set_ylim([-0.1, 0.1])
            ax.set_xlabel('x')
            ax.set_ylabel('(ΔΣ - ΔΣ_true) / ΔΣ_true')
            plt.legend()
            plt.savefig('/Users/joe/Desktop/verif.png', dpi=300)
            plt.show()

             
    def measure_profile_projected(self, nbins, projection='cartesian', plot=True):
        
        # measure projected profile at bin mean positions
        if(projection == 'cartesian'):
            x1 = self.yyp_los
            x2 = self.zzp_los
            r = np.linalg.norm([self.yyp_los, self.zzp_los], axis=0)
        elif(projection == 'angular'):
            x1 = self.tp_los
            x2 = self.pp_los
            r = np.linalg.norm([self.tp_los, self.pp_los], axis=0) * self.halo_r 
        else:
            raise RuntimeError('pojection must either be \'cartesian\' or \'angular\'')
        
        binned_r = binstat(r, r, 'mean', bins=nbins)
        rm = binned_r[0]
        edges = binned_r[1]

        # compute bivarite gaussian kde on a grid of resolution 100x100
        X1, X2 = np.mgrid[np.min(x1):np.max(x1):100j, np.min(x2):np.max(x2):100j]
        positions = np.vstack([X1.ravel(), X2.ravel()])
        values = np.vstack([x1, x2])
        kernel = stats.gaussian_kde(values)
        kde2d = np.rot90(np.reshape(kernel(positions).T, X1.shape)) * self.halo_props['mpp']

        # compress to radial dimension
        kde = np.ravel(kde2d)
        kde_r = np.linalg.norm(positions, axis=0)
        
        counts = binstat(r, r, 'count', bins=nbins)[0]
        mass = counts * self.halo_props['mpp'] * u.solMass
        area = np.pi * np.diff(edges**2) * u.Mpc**2
        rho = mass / area 
        err = mass / np.sqrt(counts) / area

        # compute truth
        rho_true = (self.nfw.sigma(rm) * (u.solMass/u.pc**2)).to(u.solMass/u.Mpc**2)

        # compute truncated correction
        # arguments should be the radial position as R/rs, and the extent of the halo as rmax/rs, 
        # where rmax is rfrac * r200c
        
        Z = lambda x,R: np.sqrt(R**2 - x**2)
        t1 = lambda x,R: Z(x,R) * (np.sqrt(x**2 + Z(x,R)**2) - 1) / ((x**2 - 1) * (x**2 + Z(x,R)**2 - 1))
        # x < 1 piece
        t2_xl = lambda x,R: ( np.arctanh( Z(x,R) / np.sqrt(-(x**2-1) * (x**2 + Z(x,R)**2)) + 0j ) -
                              np.arctanh( Z(x,R) / np.sqrt(1-x**2) + 0j ) 
                            ) / (1-x**2)**(3/2)
        # x > 1 piece
        t2_xg = lambda x,R: ( np.arctan( Z(x,R) / np.sqrt((x**2-1) * (x**2 + Z(x,R)**2)) ) - 
                              np.arctan( Z(x,R) / np.sqrt(x**2-1) ) 
                            ) / (x**2 - 1)**(3/2)
        ss2 = lambda x,R: t1(x,R) + np.real(np.hstack([t2_xl(x[x<1],R), t2_xg(x[x>1],R)]))
        
        #mask = rm > self.rs
        mask = rm/self.rs != 1
        x = rm[mask] / self.rs
        R = self.rfrac * self.r200c / self.rs
        pref = (2 * self.rs * self.dc * self.pc)
        correction = pref * ss2(x, R)        

        if(plot):
            plt.figure()
            plt.loglog(rm, rho_true, '--k', label='truth')
            plt.loglog(rm[mask], correction, '--r', label='correction', zorder=99)
            plt.errorbar(rm, rho.value, yerr=err.value, fmt='-x', label='measred')
            if(projection=='cartesian'): plt.title('Projected z-y')
            if(projection=='angular'): plt.title('Projected θ-φ')
            plt.xlabel('r [Mpc]')
            plt.ylabel('Σ [solMass/Mpc^2]')
            plt.legend()
        
        return [rm, rho.value, err.value, rho_true]


    def truncated_profile_correction(self, x):
        
        # compute truncated correction
        # arguments should be the radial position as R/rs, and the extent of the halo as rmax/rs,
        # where rmax is rfrac * r200c

        Z = lambda x,R: np.sqrt(R**2 - x**2)
        t1 = lambda x,R: Z(x,R) * (np.sqrt(x**2 + Z(x,R)**2) - 1) / ((x**2 - 1) * (x**2 + Z(x,R)**2 - 1))
        # x < 1 piece
        t2_xl = lambda x,R: ( np.arctanh( Z(x,R) / np.sqrt(-(x**2-1) * (x**2 + Z(x,R)**2)) + 0j ) -
                              np.arctanh( Z(x,R) / np.sqrt(1-x**2) + 0j )
                            ) / (1-x**2)**(3/2)
        # x > 1 piece
        t2_xg = lambda x,R: ( np.arctan( Z(x,R) / np.sqrt((x**2-1) * (x**2 + Z(x,R)**2)) ) -
                              np.arctan( Z(x,R) / np.sqrt(x**2-1) )
                            ) / (x**2 - 1)**(3/2)
        ss2 = lambda x,R: t1(x,R) + np.real(np.hstack([t2_xl(x[x<1],R), t2_xg(x[x>1],R)]))

        mask = x != 1
        R = self.rfrac * self.r200c / self.rs
        pref = (2 * self.rs * self.dc * self.pc)
        correction = pref * ss2(x, R)
        return correction.value
        

    def measure_profile_3d(self, nbins):
        
        # measure 3d profile at bin mean positions
        r = np.linalg.norm([self.xxp_los, self.yyp_los, self.zzp_los], axis=0)
        binned_r = binstat(r, r, 'mean', bins=nbins)
        rm = binned_r[0]
        edges = binned_r[1]
        
        counts = binstat(r, r, 'count', bins=nbins)[0]
        mass = counts * self.halo_props['mpp'] * u.solMass
        volume = 4/3 * np.pi * np.diff(edges**3) * u.Mpc**2
        rho = mass / volume
        
        err = mass / np.sqrt(counts) / volume

        # compute truth
        rho_true = (self.nfw.rho(rm) * (u.solMass/u.Mpc**3))

        plt.figure()
        plt.errorbar(rm, rho.value, yerr=err.value, fmt='-x', label='measred')
        plt.loglog(rm, rho_true, '--k', label='truth')
        plt.title('3d')
        plt.xlabel('r [Mpc]')
        plt.ylabel('ρ [solMass/Mpc^3]')
        plt.legend()


        

        

if(__name__ == '__main__'):

    halo_dir = '/Users/joe/repos/repo_user/nfw_validation/validation_halos/'\
               'halo_zl0.20_zs1.00_N20000_6.00r200c_6.00r200clos_nsrcs200_lenspix1024_seed606'
    p = profile_checker(halo_dir)
    p.read_particles()
    #p.measure_profile_projected(nbins=100, plot=True)
    p.measure_numerical_delta_sigma_theory(nbins=100, plot=True)

    #p.polyfit_delta_sigma(100, 20, 15, halo_dir='/Users/joe/repos/repo_user/nfw_validation/validation_halos')
    #p.measure_numerical_delta_sigma(100, 20, halo_dir='/Users/joe/repos/repo_user/nfw_validation/validation_halos')
    plt.show()
