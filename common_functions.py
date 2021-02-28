import numpy, astropy, astropy.io.fits

#Speed of light
c = 299792.458 #km/s
#HI line rest frequency
f0 = 1.420405751 #GHz
#Hubble constant
H0 = 70. #km/s/Mpc
h = H0/100.
#Solar mass
Msol = 1.99E30 #kg
#Proton mass
mp = 1.67E-27 #kg
#Parsec
pc = 3.086E16 #m

def v_rad(v_opt):
    '''
    Conversion from optical to radio velocity.
    
    Inputs:
        v_opt: Optical velocity [km/s].
        
    Outputs:
        v_rad: Radio velocity [km/s].
    '''
    
    return c*(1. - (1./(1.+(v_opt/c))))

def v_opt(v_rad):
    '''
    Conversion from radio to optical velocity.
    
    Inputs:
        v_rad: Radio velocity [km/s].
        
    Outputs:
        v_opt: Optical velocity [km/s].
    '''
    
    return c*((1./(1.-(v_rad/c))) - 1.)

def read_fitscube(filename,need_beam=False,widths=False,mask=False,verbose=False):
    '''
    Reads a fits cube that is RA, Dec, Vel and builds the axes.
    
    Inputs:
        filename = String indicating the full location of the fits file.
        need_beam = Boolean indicating whether to return beam dimensions.
        widths = Boolean indicating whether to return axes step sizes.
        verbose = Boolean indicating whether to print all output.
        
    Outputs:
        cube = The data values from the fits file.
        cube_ra = Right ascension axis values [deg].
        cube_dec = Declination axis values [deg].
        cube_vel = Velocity axis values [km/s].
        bmaj = (if need_beam) Beam major axis diameter [arcsec].
        bmin = (if need_beam) Beam major axis diameter [arcsec].
        pa = (if need_beam) Beam position angle [deg].
        beam_factor = (if need_beam) Ratio of beam area to pixel area.
        cube_dx = (if widths) RA axis step size [deg].
        cube_dy = (if widths) Dec axis step size [deg].
        cube_dv = (if widths) Velocity axis step size [km/s].
    '''
    
    cube_fits = astropy.io.fits.open(filename)

    cube = cube_fits[0].data
    cube_head = cube_fits[0].header

    cube_dx = cube_head['CDELT1']
    cube_dy = cube_head['CDELT2']
    cube_dv = cube_head['CDELT3']

    cube_ra = cube_head['CRVAL1'] + cube_dx * numpy.arange(1,1+cube_head['NAXIS1']) - cube_dx * cube_head['CRPIX1'] # RA
    cube_dec = cube_head['CRVAL2'] + cube_dy * numpy.arange(1,1+cube_head['NAXIS2']) - cube_dy * cube_head['CRPIX2'] # Dec
    cube_vel = cube_head['CRVAL3'] + cube_dv * numpy.arange(1,1+cube_head['NAXIS3']) - cube_dv * cube_head['CRPIX3']

    if 'm/s' == str.strip(cube_head['CUNIT3']) or 'M/S' == str.strip(cube_head['CUNIT3']):
        if verbose:
            print("Velocity units are m/s. Converting to km/s.")
        cube_vel = cube_vel/1000. #km/s
        cube_dv = cube_dv/1000. #km/s
    elif 'km/s' == str.strip(cube_head['CUNIT3']) or 'KM/S' == str.strip(cube_head['CUNIT3']):
        if verbose:
            print("Velocity units are km/s.")
        pass
    else:
        print("Warning: Velocity units not recognised.")
        print("Warning: Units listed as: "+cube_head['CUNIT3'])
    
    if 'OPT' in str(cube_head['CTYPE3']) or 'opt' in str(cube_head['CTYPE3']):
        if verbose:
            print("Velocity convention is optical.")
        pass
    elif 'RAD' in str(cube_head['CTYPE3']) or 'rad' in str(cube_head['CTYPE3']) or int(cube_head['VELREF']) > 256:
        if verbose:
            print("Velocity convention is radio. Converting to optical.")
        cube_vel = v_opt(cube_vel)
    else:
        print("Warning: Could not identify radio or optical velocity convention.")
        print("Warning: Convention listed as: "+cube_head['CTYPE3'])

    bmaj,bmin,pa = cube_head['BMAJ']*3600.,cube_head['BMIN']*3600., cube_head['BPA']
    pixel = cube_head['CDELT2']*3600.

    beam_factor = (numpy.pi*bmaj*bmin/(pixel**2.))/(4.*numpy.log(2.))
    
    cube_fits.close()
    
    if mask:
        cube = numpy.where(cube > 0, 1, 0)
    
    if need_beam and widths:
        return cube,cube_ra,cube_dec,cube_vel,bmaj,bmin,pa,beam_factor,cube_dx,cube_dy,cube_dv
    elif need_beam:
        return cube,cube_ra,cube_dec,cube_vel,bmaj,bmin,pa,beam_factor
    elif widths:
        return cube,cube_ra,cube_dec,cube_vel,cube_dx,cube_dy,cube_dv
    else:
        return cube,cube_ra,cube_dec,cube_vel
    
def gaussian(x, mu, sig):
    '''
    Gaussian with mean mu and standard deviation sig.
    
    Inputs:
        x: Independent variable.
        mu: Mean of Gaussian distribution.
        sig: Standard deviation of Gaussian.
        
    Outputs:
        y: Value of Gaussian distribution at x.
    '''
    
    return numpy.exp(-numpy.power((x - mu)/sig, 2.)/2.)
    
def gaussian2d(x, y, mux, muy, sigx, sigy):
    '''
    Two dimensional Gaussian with mean (mux,muy) and standard deviations sigx and sigy in the x and y directions respectively.
    
    Inputs:
        x: x coordinate.
        y: y coordinate.
        mux: Mean of Gaussian distribution in the x-direction.
        muy: Mean of Gaussian distribution in the y-direction.
        sigx: Standard deviation of Gaussian in the x-direction.
        sigy: Standard deviation of Gaussian in the y-direction.
        
    Outputs:
        val: Value of Gaussian distribution at x,y.
    '''
    
    return numpy.exp(-numpy.power((x - mux)/sigx, 2.)/2.)*numpy.exp(-numpy.power((y - muy)/sigy, 2.)/2.)