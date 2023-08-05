import numpy as np
import os
import iragnsep
import glob

from astropy.cosmology import WMAP9 as cosmo
from astropy import units as u
from astropy import constants as const
from scipy import integrate
from scipy.interpolate import UnivariateSpline
from scipy.constants import h,k
from numba import njit

c = const.c.value
Lsun = const.L_sun.value

def get_prop(df, echar, z = 0.01, specOn = True, templ = ''):

	"""
    This function calculates the IR properties of the AGN and their hosts.
    ------------
    :param df: data-frame containing the results from the fits (i.e. optimised parameters) as returned by SEDanalysis.
    :param echar: characteristic uncertainties to calculate the uncertainties on the parameters.
    ------------
    :keyword z: redshift
	:keyword specOn: set to True if the data contain a spectrum in addition to the photometry.
    :keyword templ: set the templates that have been used in the fits.
    ------------
    :return loglum_hostIR: the host IR (8--1000microns) log-luminosity free of AGN contamination (Lsun).
    :return eloglum_hostIR: uncertainties on loglum_hostIR.
	:return loglum_hostMIR: the host IR (5--35microns) log-luminosity free of AGN contamination (Lsun).
    :return eloglum_hostIR: uncertainties on loglum_hostMIR.
	:return loglum_hostFIR: the host IR (40--1000microns) log-luminosity free of AGN contamination (Lsun).
    :return eloglum_hosFIR: uncertainties on loglum_hostFIR.
	:return loglum_AGNIR: the AGN IR log-luminosity free of host contamination (Lsun).
	:return loglum_AGNMIR: the AGN MIR log-luminosity free of host contamination (Lsun).
	:return loglum_AGNFIR: the AGN FIR log-luminosity free of host contamination (Lsun).
	:return AGNfrac_IR: the AGN fraction in the IR.
	:return AGNfrac_MIR: the AGN fraction in the MIR.
	:return AGNfrac_FIR: the AGN fraction in the FIR.
	:return SFR: the SFR of the galaxy free of AGN contamination.
	:return eSFR: the uncertainties on SFR.
	:return wSFR: the SFR of the galaxy free of AGN contamination weighted by its Akaike weight.
	:return ewSFR: the uncertainties on wSFR.
    """

	if len(templ) == 0:
		path = os.path.dirname(iragnsep.__file__)
		templ = pd.read_csv(path+'/iragnsep_templ.csv')

	# Extract the name of the templates
	keys = templ.keys().values
	nameTempl_gal = []
	nameTempl_AGN = []
	nameTempl_PAH = []
	nameTempl_Siem = []
	for key in keys:
		if str(key).startswith('gal'):
			if str(key).endswith('PAH') == False:
				nameTempl_gal.append(key)
			else:
				nameTempl_PAH.append(key)
		if str(key).startswith('AGN'):
			if str(key).endswith('Siem'):
				nameTempl_Siem.append(key)
			else:
				nameTempl_AGN.append(key)

	# Test that we have template for everything (if no galaxy then it crashes)
	if len(nameTempl_gal) == 0:
		raise ValueError('The galaxy template does not exist. The name of the column defining nuLnu for the galaxy template needs to start with "gal".')
	if len(nameTempl_AGN) == 0:
		print('Warning: The template for AGN is empty. The name of the column defining nuLnu for the AGN templates needs to start with "AGN".')

	# define the wavelengths
	try:
		wavTempl = templ['lambda_mic'].values
	except:
		raise ValueError('Rename the wavelengths column of the template "lambda_mic".')

	nu = c/wavTempl/1e-6 #Hz
	o_IR = np.where((nu > c/1000./1e-6) & (nu < c/8./1e-6))[0][::-1]
	o_MIR = np.where((nu > c/35./1e-6) & (nu < c/5./1e-6))[0][::-1]
	o_FIR = np.where((nu > c/1000./1e-6) & (nu < c/40./1e-6))[0][::-1]
	dMpc = cosmo.luminosity_distance(z).value
	dmeter = dMpc*u.Mpc.to(u.m)
	d2z = dmeter**2./(1.+z) # K correction=>https://ned.ipac.caltech.edu/level5/Sept02/Hogg/Hogg2.html
	JyToLsun = 1e-26 * 4. * np.pi * d2z/Lsun

	loglum_hostIR = []
	eloglum_hostIR = []
	loglum_hostMIR = []
	eloglum_hostMIR = []
	loglum_hostFIR = []
	eloglum_hostFIR = []
	loglum_AGNIR = []
	loglum_AGNMIR = []
	loglum_AGNFIR = []

	if specOn == True:

		for i in range(0, len(df)):

			obj = df.iloc[i]

			#host IR luminosity
			normDust = 10**obj['logNormGal_dust']
			enormDust = echar * np.log(10)
			# enormDust = obj['elogNormGal_dust'] * np.log(10)
			nuLnuDust = normDust * templ[obj['tplName']].values
			enuLnuDust = enormDust * nuLnuDust

			normPAH = 10**obj['logNormGal_PAH']
			# enormPAH = obj['elogNormGal_PAH'] * np.log(10)
			enormPAH = echar * np.log(10)
			nuLnuPAH = normPAH * templ['gal_PAH'].values
			enuLnuPAH = enormPAH * nuLnuPAH

			nuLnuGal = nuLnuDust + nuLnuPAH
			enuLnuGal = np.sqrt(enuLnuDust ** 2. + enuLnuPAH ** 2.)
			LnuGal = nuLnuGal/nu
			eLnuGal = enuLnuGal/nu

			loglum_hostIR.append(round(np.log10(np.trapz(LnuGal[o_IR], nu[o_IR], dx = np.gradient(nu[o_IR]))),3)) #Lsun
			elum_hostIR_i = 0
			for nu_i, nu_j, nu_k, eLnuGal_j, eLnuGal_k in zip(nu[o_IR[1:-2]], nu[o_IR[2:-1]], nu[o_IR[3:]], eLnuGal[o_IR[2:-1]], eLnuGal[o_IR[3:]]):
				elum_hostIR_i += 1./4. * (nu_j - nu_i)**2. * eLnuGal_j ** 2. + 1./4. * (nu_k - nu_j)**2. * eLnuGal_k ** 2.
			elum_hostIR = np.sqrt(elum_hostIR_i)
			eloglum_hostIR.append(round(0.434 * elum_hostIR/10**np.array(loglum_hostIR[-1]),3))
			
			loglum_hostMIR.append(round(np.log10(np.trapz(LnuGal[o_MIR], nu[o_MIR], dx = np.gradient(nu[o_MIR]))),3)) #Lsun
			elum_hostMIR_i = 0
			for nu_i, nu_j, nu_k, eLnuGal_j, eLnuGal_k in zip(nu[o_MIR[1:-2]], nu[o_MIR[2:-1]], nu[o_MIR[3:]], eLnuGal[o_MIR[2:-1]], eLnuGal[o_MIR[3:]]):
				elum_hostMIR_i += 1./4. * (nu_j - nu_i)**2. * eLnuGal_j ** 2. + 1./4. * (nu_k - nu_j)**2. * eLnuGal_k ** 2.
			elum_hostMIR = np.sqrt(elum_hostMIR_i)
			eloglum_hostMIR.append(round(0.434 * elum_hostMIR/10**np.array(loglum_hostMIR[-1]),3))
			
			loglum_hostFIR.append(round(np.log10(np.trapz(LnuGal[o_FIR], nu[o_FIR], dx = np.gradient(nu[o_FIR]))),3)) #Lsun
			elum_hostFIR_i = 0
			for nu_i, nu_j, nu_k, eLnuGal_j, eLnuGal_k in zip(nu[o_FIR[1:-2]], nu[o_FIR[2:-1]], nu[o_FIR[3:]], eLnuGal[o_FIR[2:-1]], eLnuGal[o_FIR[3:]]):
				elum_hostFIR_i += 1./4. * (nu_j - nu_i)**2. * eLnuGal_j ** 2. + 1./4. * (nu_k - nu_j)**2. * eLnuGal_k ** 2.
			elum_hostFIR = np.sqrt(elum_hostFIR_i)
			eloglum_hostFIR.append(round(0.434 * elum_hostFIR/10**np.array(loglum_hostFIR[-1]),3))
			
			if obj['AGNon'] == 1:
				modelAGN1 = 10**obj['logNorm_Si11'] * Gauss_jit(wavTempl*(1.+z), np.log10(11.*(1.+z)), 0.05)
				modelAGN2 = 10**obj['logNorm_Si18'] * Gauss_jit(wavTempl*(1.+z), np.log10(18.*(1.+z)), 0.07)
				modelAGN3 = 10**obj['logNormAGN_PL'] * AGNmodel_jit(wavTempl*(1.+z), 15.*(1.+z), obj['lBreak_PL']*(1.+z), obj['alpha1_PL'], obj['alpha2_PL'], -3.5)

				LnuAGN = (modelAGN1 + modelAGN2 + modelAGN3) * JyToLsun
				
				loglum_AGNIR.append(round(np.log10(np.trapz(LnuAGN[o_IR], nu[o_IR], dx = np.gradient(nu[o_IR]))),3)) #Lsun
				loglum_AGNMIR.append(round(np.log10(np.trapz(LnuAGN[o_MIR], nu[o_MIR], dx = np.gradient(nu[o_MIR]))),3)) #Lsun
				loglum_AGNFIR.append(round(np.log10(np.trapz(LnuAGN[o_FIR], nu[o_FIR], dx = np.gradient(nu[o_FIR]))),3)) #Lsun
			else:
				loglum_AGNIR.append(0.0)
				loglum_AGNMIR.append(0.0)
				loglum_AGNFIR.append(0.0)
	else:
		for i in range(0, len(df)):

			obj = df.iloc[i]

			#host IR luminosity
			normDust = 10**obj['logNormGal_dust']
			enormDust = obj['elogNormGal_dust'] * np.log(10)
			nuLnuDust = normDust * templ[obj['tplName_gal']].values
			enuLnuDust = enormDust * nuLnuDust

			normPAH = 10**obj['logNormGal_PAH']
			enormPAH = obj['elogNormGal_PAH'] * np.log(10)
			nuLnuPAH = normPAH * templ['gal_PAH'].values
			enuLnuPAH = enormPAH * nuLnuPAH

			nuLnuGal = nuLnuDust + nuLnuPAH
			enuLnuGal = np.sqrt(enuLnuDust ** 2. + enuLnuPAH ** 2.)
			LnuGal = nuLnuGal/nu
			eLnuGal = enuLnuGal/nu

			loglum_hostIR.append(round(np.log10(np.trapz(LnuGal[o_IR], nu[o_IR], dx = np.gradient(nu[o_IR]))),3)) #Lsun
			elum_hostIR_i = 0
			for nu_i, nu_j, nu_k, eLnuGal_j, eLnuGal_k in zip(nu[o_IR[1:-2]], nu[o_IR[2:-1]], nu[o_IR[3:]], eLnuGal[o_IR[2:-1]], eLnuGal[o_IR[3:]]):
				elum_hostIR_i += 1./4. * (nu_j - nu_i)**2. * eLnuGal_j ** 2. + 1./4. * (nu_k - nu_j)**2. * eLnuGal_k ** 2.
			elum_hostIR = np.sqrt(elum_hostIR_i)
			eloglum_hostIR.append(round(0.434 * elum_hostIR/10**np.array(loglum_hostIR[-1]),3))
			
			loglum_hostMIR.append(round(np.log10(np.trapz(LnuGal[o_MIR], nu[o_MIR], dx = np.gradient(nu[o_MIR]))),3)) #Lsun
			elum_hostMIR_i = 0
			for nu_i, nu_j, nu_k, eLnuGal_j, eLnuGal_k in zip(nu[o_MIR[1:-2]], nu[o_MIR[2:-1]], nu[o_MIR[3:]], eLnuGal[o_MIR[2:-1]], eLnuGal[o_MIR[3:]]):
				elum_hostMIR_i += 1./4. * (nu_j - nu_i)**2. * eLnuGal_j ** 2. + 1./4. * (nu_k - nu_j)**2. * eLnuGal_k ** 2.
			elum_hostMIR = np.sqrt(elum_hostMIR_i)
			eloglum_hostMIR.append(round(0.434 * elum_hostMIR/10**np.array(loglum_hostMIR[-1]),3))
			
			loglum_hostFIR.append(round(np.log10(np.trapz(LnuGal[o_FIR], nu[o_FIR], dx = np.gradient(nu[o_FIR]))),3)) #Lsun
			elum_hostFIR_i = 0
			for nu_i, nu_j, nu_k, eLnuGal_j, eLnuGal_k in zip(nu[o_FIR[1:-2]], nu[o_FIR[2:-1]], nu[o_FIR[3:]], eLnuGal[o_FIR[2:-1]], eLnuGal[o_FIR[3:]]):
				elum_hostFIR_i += 1./4. * (nu_j - nu_i)**2. * eLnuGal_j ** 2. + 1./4. * (nu_k - nu_j)**2. * eLnuGal_k ** 2.
			elum_hostFIR = np.sqrt(elum_hostFIR_i)
			eloglum_hostFIR.append(round(0.434 * elum_hostFIR/10**np.array(loglum_hostFIR[-1]),3))

			if obj['AGNon'] == 1:
				#AGN IR luminosity
				normAGN = 10**obj['logNormAGN']
				nuLnuAGN = normAGN * templ[obj['tplName_AGN']].values

				normSi = 10**obj['logNormSiem']
				nuLnuSi = normSi * templ[nameTempl_Siem].values.flatten()

				LnuAGN = (nuLnuAGN + nuLnuSi)/nu
				
				loglum_AGNIR.append(round(np.log10(np.trapz(LnuAGN[o_IR], nu[o_IR], dx = np.gradient(nu[o_IR]))),3)) #Lsun
				loglum_AGNMIR.append(round(np.log10(np.trapz(LnuAGN[o_MIR], nu[o_MIR], dx = np.gradient(nu[o_MIR]))),3)) #Lsun
				loglum_AGNFIR.append(round(np.log10(np.trapz(LnuAGN[o_FIR], nu[o_FIR], dx = np.gradient(nu[o_FIR]))),3)) #Lsun
			else:
				loglum_AGNIR.append(0.0)
				loglum_AGNMIR.append(0.0)
				loglum_AGNFIR.append(0.0)

	#Ratio of luminosities
	loglum_hostIR = np.array(loglum_hostIR)
	eloglum_hostIR = np.array(eloglum_hostIR)
	loglum_hostMIR = np.array(loglum_hostMIR)
	eloglum_hostMIR = np.array(eloglum_hostMIR)
	loglum_hostFIR = np.array(loglum_hostFIR)
	eloglum_hostFIR = np.array(eloglum_hostFIR)
	
	loglum_AGNIR = np.array(loglum_AGNIR)
	loglum_AGNMIR = np.array(loglum_AGNMIR)
	loglum_AGNFIR = np.array(loglum_AGNFIR)

	AGNfrac_IR = np.round(10**loglum_AGNIR/(10**loglum_hostIR + 10**loglum_AGNIR),2)
	o = np.where(loglum_AGNIR == 0.)[0]
	AGNfrac_IR[o] = 0.

	AGNfrac_MIR = np.round(10**loglum_AGNMIR/(10**loglum_hostMIR + 10**loglum_AGNMIR),2)
	o = np.where(loglum_AGNMIR == 0.)[0]
	AGNfrac_MIR[o] = 0.

	AGNfrac_FIR = np.round(10**loglum_AGNFIR/(10**loglum_hostFIR + 10**loglum_AGNFIR),2)
	o = np.where(loglum_AGNFIR == 0.)[0]
	AGNfrac_FIR[o] = 0.

	SFR = np.round(1.09e-10 * 10**loglum_hostIR,3) #Chabrier
	eSFR = np.round(1.09e-10 * 10**loglum_hostIR * np.log(10) * eloglum_hostIR,3)
	wSFR = np.round(1.09e-10 * 10**loglum_hostIR * df['Aw'].values,3)
	ewSFR = np.round(1.09e-10 * 10**loglum_hostIR * df['Aw'].values * np.log(10) * eloglum_hostIR,3)

	return loglum_hostIR, eloglum_hostIR, \
		   loglum_hostMIR, eloglum_hostMIR, \
		   loglum_hostFIR, eloglum_hostFIR, \
		   loglum_AGNIR, loglum_AGNMIR, loglum_AGNFIR, \
		   AGNfrac_IR, AGNfrac_MIR, AGNfrac_FIR, SFR, eSFR, wSFR, ewSFR


def basictests(wavSpec, fluxSpec, efluxSpec, wavPhot, fluxPhot, efluxPhot, filters, z, specOn = True):

	"""
    This function runs some basic tests prior to run the main fitting code.
    ------------
    :param wavSpec: observed wavelengths for the spectrum (in microns).
    :param fluxSpec: observed fluxes for the spectrum (in Jansky).
    :param efluxSpec: observed uncertainties on the fluxes for the spectrum (in Jansky).
    :param wavPhot: observed wavelengths for the photometry (in microns).
    :param fluxPhot: observed fluxes for the photometry (in Jansky).
    :param efluxPhot: observed uncertainties on the fluxes for the photometry (in Jansky).
    :param filters: name of the photometric filters to include in the fit.
    :param z: redshift.
    ------------
	:keyword specOn: set to True if the data contain a spectrum in addition to the photometry.
    ------------
    :return 0
    """

	if (len(wavPhot) != len(fluxPhot)) or (len(wavPhot) != len(efluxPhot)):
		raise ValueError("PHOTOMETRY ISSUE: Crashed because wavelengths, fluxes and uncertainties on the fluxes have different lengths.")
	if len(filters) != len(wavPhot):
		raise ValueError("FILTERS ISSUE: Crashed because the number of filters provided does not correspond to the number of photometry points.")
	if (any(fluxPhot<0) == True) or (any(efluxPhot<0) == True) or (any(wavPhot<0) == True):
		raise ValueError("PHOTOMETRY ISSUE: Crash caused by some negative values in the wavelengths, fluxes or uncertainties on the fluxes.")
	if (any(fluxPhot != fluxPhot) == True) or (any(efluxPhot != efluxPhot) == True) or (any(wavPhot != wavPhot) == True):
		raise ValueError("PHOTOMETRY ISSUE: Crash caused by some non-numerical values in the wavelengths, fluxes or uncertainties on the fluxes.")
	if specOn == True:
		#test that the length of wavelength is the same as the data
		if (len(wavSpec) != len(fluxSpec)) or (len(wavSpec) != len(efluxSpec)):
			raise ValueError("SPECTRUM ISSUE: Crashed because wavelengths, fluxes and uncertainties on the fluxes have different lengths.")
		#test that there are no negative values
		if (any(fluxSpec<0) == True) or (any(efluxSpec<0) == True) or (any(wavSpec<0) == True):
			raise ValueError("SPECTRUM ISSUE: Crash caused by some negative values in the wavelengths, fluxes or uncertainties on the fluxes.")
		#test that there are NAN
		if (any(fluxSpec != fluxSpec) == True) or (any(efluxSpec != efluxSpec) == True) or (any(wavSpec != wavSpec) == True):
			raise ValueError("SPECTRUM ISSUE: Crash caused by some non-numerical values in the wavelengths, fluxes or uncertainties on the fluxes.")

	#test if the filter exists
	path = os.path.dirname(iragnsep.__file__) + '/Filters/'
	files = [f for f in glob.glob(path + "*.csv")]
	count = -1
	for f in [path+f+"Filter.csv" for f in filters]:
		count += 1
		if (f in files) == False:
			raise ValueError(" \n The filter "+ str(filters[count]) + " does not exist. This version does not allow you to add some filters." + \
							 " Please get in touch with us to add the required filters (e.p.bernhard@sheffield.ac.uk). Available filters are:" +\
							 " IRAC1 , IRAC2 , IRAC3 , IRAC4 , WISE_W1 , WISE_W2 , WISE_W3 , WISE_W4 , IRAS12, IRAS60, IRAS100 , MIPS24, MIPS70," +\
							 " MIPS160 , PACS70, PACS100 , PACS160, SPIRE250ps , SPIRE350ps , SPIRE500ps")

	#Test if the redshift has been given by the user
	if z<0:
		zdefault = input('Warning: The redshift is set to the default value of 0.01. The keyword "z" allows you to indicate the redshift of the source.\n '+\
						 ' Press enter to continue, or type "exit" to abort.\n')
		if zdefault == "exit":
			exit()
		else:
			pass

	# Test that the wavelengths are in ascening order
	dlambda = np.gradient(wavPhot)
	o = np.where(dlambda < 0.)[0]
	if len(o) > 0.:
		raise ValueError('PHOTOMETRY ISSUE: Wavelenghts need to be in ascending order.')
	if (specOn == True):
		dlambda = np.gradient(wavSpec)
		o = np.where(dlambda < 0.)[0]
		if len(o) > 0.:
			raise ValueError('SPECTRUM ISSUE: Wavelenghts need to be in ascending order.')

	if specOn == True:
		# Test if it can concatenate the Spectra aand the photometry
		try:
			wav = np.concatenate([wavSpec, wavPhot])
		except:
			raise ValueError("WAVELENGTHS: Spectral data cannot be concatenated to photometric data. Please check data.")
		try:
			flux = np.concatenate([fluxSpec, fluxPhot])
		except:
			raise ValueError("FLUXES: Spectral data cannot be concatenated to photometric data. Please check data.")
		try:
			eflux = np.concatenate([efluxSpec, efluxPhot])
		except:
			raise ValueError("UNCERTAINTIES ON THE FLUXES: Spectral data cannot be concatenated to photometric data. Please check data.")
	else:
		# Break as not enough data points anyway,
		if len(wavPhot) < 4:
			if len(wavPhot) == 3:
				restWav = wavPhot/(1.+z)
				NFIR = len(np.where(restWav>60.)[0])
				if (NFIR > 0.) & (NFIR != len(wavPhot)):
					pass
				else:
					raise ValueError('There is not enough data points to fit the model when compared to the number of degrees of freedom. It needs a minimum of' + \
								 ' 3 photometric point, with at least 1 FIR (i.e. rest-wavelength>60micron) flux, including upper-limits.')
	
			else:
				raise ValueError('There is not enough data points to fit the model when compared to the number of degrees of freedom. It needs a minimum of' + \
								 ' 3 photometric point, with at least 1 FIR (i.e. rest-wavelength>60micron) flux, including upper-limits.')


def exctractBestModel(logl, k, n, corrected = True):

	"""
    This function extracts the best model and calculates the Akaike weights based on the log-likelihood returned by the fits.
    ------------
    :param logl: log-likelihood returned by the fits.
    :param k: number of free parameters.
    :param n: number of data points.
    ------------
	:keyword corrected: if set to True, calculates the corrected AIC for small number of data points.
    ------------
    :return bestModelInd: the index of the best model fit.
    :return Awi: Akaike weights of each of the models, with respect to the best model.
    """

	nkdif = np.array(n)-np.array(k)
	o = np.where(nkdif == 1)[0]
	if len(o) > 0:
		corrected = False

	if corrected == True:
		AIC = 2*np.array(k) - 2.*np.array(logl) + (2.*np.array(k)**2. + 2.*np.array(k))/(np.array(n)-np.array(k)-1.)
	else:
		AIC = 2*np.array(k) - 2.*np.array(logl)

	bestModelInd = np.where(AIC == np.min(AIC))[0]
	AICmin = AIC[bestModelInd]
	AwiNorm = np.sum(np.exp(-0.5 * (AIC-AICmin)))

	Awi = np.exp(-0.5 * (AIC-AICmin))/AwiNorm

	return bestModelInd, Awi

def nuLnuToFnu(spec_wav, nuLnu, z):

	"""
    This function calculates the observed flux from nuLnu.
    ------------
    :param spec_wav: rest-wavelengths (in microns).
    :param nuLnu: nuLnu.
    :param z: redshift.
    ------------
    :return Fnu: observed flux on Earth of the source located at redshift z (in Jansky).
    """

	dMpc = cosmo.luminosity_distance(z).value #Mpc
	dmeter = dMpc*u.Mpc.to(u.m)
	d2z = dmeter**2./(1.+z) # K correction=>https://ned.ipac.caltech.edu/level5/Sept02/Hogg/Hogg2.html

	# Derive the observed flux
	nu = c/spec_wav/1e-6 #Hz
	Lnu = nuLnu/nu*Lsun #W/Hz
	Fnu = Lnu/4./np.pi/d2z #W/Hz/m2

	return Fnu * 1e26 # Jy

def getFluxInFilt(filt_wav, filt_QE, spec_wav, nuLnu, z):

	"""
    This function calculates the synthetic flux in a given filter and at a given redshift from a source with luminosity nuLnu.
    ------------
    :param filt_wav: passband of the filter.
	:param filt_QE: quantum efficient of the filter.
 	:param spec_wav: rest-wavelengths (in microns).
    :param nuLnu: nuLnu.
    :param z: redshift.
    ------------
    :return flux_Obs: observed flux on Earth of the source located at redshift z with luminosity nuLnu (in Jansky).
    """

	norm = integrate.trapz(filt_QE, x=c/filt_wav/1e-6)

	Fnu_0 = nuLnuToFnu(spec_wav, nuLnu, z) #Flux received on Earth
	lambda_0 = spec_wav * (1. + z) # Wavelenght of emission
	Fnu_0filt = np.interp(filt_wav, lambda_0, Fnu_0) # Move the template to grab the redshifted flux
	flux_Obs = integrate.trapz(Fnu_0filt*filt_QE, x = c/filt_wav/1e-6)/norm # This is the flux received on Earth

	return flux_Obs

@njit
def logldet(ym, ydat, eydat, wei):

	"""
    This function calculates the log-likelihood of detected data.
    ------------
    :param ym: model values.
	:param ydat: observed values.
 	:param eydat: observed uncertaities.
    :param wei: weights of the data points.
    ------------
    :return logl: log-likelihood of the model.
    """

	sigma = 0.434 * eydat/ydat
	logl = np.sum((-0.5*(np.log10(ydat) - np.log10(ym))**2./sigma**2.)*wei)

	return logl

@njit
def erf_approx(x):
	"""
    This function calculates an approximation of the error function.
    ------------
    :param x: x values to which the error function is calculated at.
    ------------
    :return erf_approx_eval: approximate value of the error function.
    """

	t_erf = 1./(1. + 0.5*np.abs(x))
	tau_erf = t_erf*np.exp(-x**2. - 1.26551223 + 1.00002368*t_erf + 0.37409196*t_erf**2. + 0.09678418*t_erf**3.\
								  - 0.18628806*t_erf**4., + 0.27886807*t_erf**5. - 1.13520398*t_erf**6. + 1.48851587*t_erf**7. \
								  - 0.82215223*t_erf**8. + 0.17087277*t_erf**9.)
	for i, xnden in np.ndenumerate(x):
		if xnden >= 0:
			erf_approx_eval = 1. - tau_erf
		else:
			erf_approx_eval = tau_erf - 1.

	return erf_approx_eval[0]

@njit
def loglUL(ym, ydat):

	"""
    This function calculates the log-likelihood of undetected data.
    ------------
    :param ym: model values.
	:param ydat: observed values.
    ------------
    :return logl: log-likelihood of the model.
    """

	
	logl = 0
	x = (np.log10(ym) - np.log10(ydat))/np.sqrt(2.)/0.15
	t_erf = 1./(1. + 0.5*np.abs(x))
	tau_erf = t_erf*np.exp(-x**2. - 1.26551223 + 1.00002368*t_erf + 0.37409196*t_erf**2. + 0.09678418*t_erf**3.\
								  - 0.18628806*t_erf**4., + 0.27886807*t_erf**5. - 1.13520398*t_erf**6. + 1.48851587*t_erf**7. \
								  - 0.82215223*t_erf**8. + 0.17087277*t_erf**9.)
	for i, xnden in np.ndenumerate(x):
		if xnden >= 0:
			erf_approx = 1. - tau_erf
			logl += np.sum(np.log(1. - (0.5 * (1. + erf_approx))))
		else:
			erf_approx = tau_erf - 1.
			logl += np.sum(np.log(1. - (0.5 * (1. + erf_approx))))

	return logl


@njit
def Gauss_jit(x, mu, sigma):
	"""
    This function calculates a Gaussian normalised to its maximum.
    ------------
    :param x: x-values.
	:param mu: mean.
 	:param sigma: standard deviation.
    ------------
    :return Bnu: Gaussian evaluated at x, normalised to its maximum.
    """

	Bnu = np.exp(-(np.log10(x)-mu)**2./2./sigma/sigma)

	return Bnu/np.max(Bnu)

@njit
def AGNmodel_firstPL_jit(x, lambdab, alpha1, alpha2, s):
	
	"""
    This function calculates the first broken power-law of the AGN model.
    ------------
    :param x: x-values.
	:param lambdab: position of the break.
 	:param alpha1: slope of the first power-law.
 	:param alpha2: slope of the second power-law.
    :param s: sharpness parameter for the break between alpha1 and alpha2. 
    ------------
    :return Bnu: corresponding broken power law evaluated at x, and normalised at 10 microns.
    """

	Bnu = x**alpha1*(1. + (x/lambdab)**(abs(alpha2-alpha1)*s))**(np.sign(alpha2-alpha1)/s)
	BnuNorm = np.interp(10., x, Bnu)

	return Bnu/BnuNorm

@njit
def AGNmodel_jit(x, lambdab1, lambdab2, alpha1, alpha2, alpha3):

	"""
    This function calculates the second broken power-law of the AGN model.
    ------------
    :param x: x-values.
	:param lambdab1: position of the break for the first broken power law.
	:param lambdab2: position of the break for the second broken power law.
 	:param alpha1: slope of the first power-law.
 	:param alpha2: slope of the second power-law.
 	:param alpha2: slope of the third power-law.
    ------------
    :return Bnu: corresponding double-broken power law evaluated at x, and normalised at 10 microns.
    """

	Bnu0 = AGNmodel_firstPL_jit(x, lambdab1, alpha1, alpha2,2.)
	Bnu1 = x**alpha2*(1. + (x/lambdab2)**(abs(alpha3-alpha2)*2.))**(np.sign(alpha3-alpha2)/2.)

	xJoint = (lambdab1 + lambdab2)/2.
	Bnu1Norm = Bnu1/np.interp(xJoint, x, Bnu1)*np.interp(xJoint, x, Bnu0)

	Bnu = Bnu0
	o = np.where(x >= xJoint)[0]
	Bnu[o] = Bnu1Norm[o]

	return Bnu

def KVTextinctCurve(lambda_obs):

	"""
    This function calculates the extinction curve from Kemper et al. (2004).
    ------------
    :param lambda_obs: observed wavelengths.
    ------------
    :return tau_return: absorption coefficient tau per wavelength.
    """

	lambda_mic = np.arange(1., 1000., 0.01)
	kvt_wav = 8.0, 8.2, 8.4,  8.6,  8.8,  9.0,  9.2,  9.4, 9.6, 9.7, 9.75, 9.8, 10.0, 10.2,\
			  10.4, 10.6, 10.8, 11.0, 11.2, 11.4,11.6, 11.8, 12.0, 12.2, 12.4, 12.6, 12.7
	kvt_prof= .06, .09, .16, .275, .415, .575, .755, .895, .98, .99, 1.00, .99, .94 ,  .83,\
			  .745, .655,  .58, .525,  .43,  .35, .27,  .20,  .13,  .09,  .06, .045, .04314 

	PSIlambda = np.zeros(len(lambda_mic))

	o = np.where((lambda_mic > 8) & (lambda_mic < 12.7))[0]
	if len(o) > 0:
		PSIlambda[o] = np.interp(lambda_mic[o], kvt_wav, kvt_prof)

	PSI8 = 0.06
	o = np.where(lambda_mic <= 8)[0]
	if len(o) > 0:
		PSIlambda[o] = PSI8*np.exp(2.03*(lambda_mic[o]-8.))

	o = np.where(lambda_mic >= 12.7)[0]
	if len(o) > 0:
		PSIlambda[o] = 0.247 * drude(lambda_mic[o], 0.4, 18.)

	PSI9p7 = np.interp(9.7, lambda_mic, PSIlambda)
	tau = (0.9*PSIlambda + 0.1*(9.7/lambda_mic)**1.7)/PSI9p7

	tau_return = np.zeros(len(lambda_obs))+1e-10
	o = np.where(lambda_obs < max(lambda_mic))[0]
	if len(o) > 0:
		tau_return[o] = np.interp(lambda_obs[o], lambda_mic, tau)
	return tau_return

# Drude profile
def drude(x, gamma_r, lambda_r, normed = True):
	"""
    This function calculates a Drude profile.
    ------------
    :param x: x-values.
    :param gamma_r: central wavelengths.
    :param lambda_r: fractional FWHM.
    ------------
    :keyword normed: if set to True, normalise to the maximum value.
    ------------
    :return drudeVal: the Drude profile evaluated at x.
    """
	numerateur = gamma_r**2.
	denominateur = (x/lambda_r - lambda_r/x)**2. + gamma_r**2.
	drudeVal = numerateur/denominateur

	if normed == True:
		return drudeVal/np.max(drudeVal)
	else:
		return np.max(drudeVal), drudeVal


def obsC(wavRest, flux, eflux):
	"""
    This function calculates the total obscuration at 9.7micron.
    ------------
    :param wavRest: rest-wavelength.
    :param flux: observed fluxes.
    :param eflux: uncertainties on the observed fluxes.
    ------------
    :return _tau9p7: the total obscuration at 9.7micron.
    """
	loc1 = np.where((wavRest >= 5.) & (wavRest<=7.))[0]
	loc2 = np.where((wavRest >= 14.) & (wavRest<=14.5))[0]
	loc3 = np.where((wavRest >= 25.) & (wavRest<=31.5))[0]

	if (len(loc1) <1) & (len(loc2) < 1):
	 	raise Exception()

	if len(loc3) > 0:
		k = 4
		# Get the flux in the anchored wavelengths
		wavAbs = np.concatenate((wavRest[loc1], wavRest[loc2], wavRest[loc3]))
		fluxAbs = np.concatenate((flux[loc1], flux[loc2], flux[loc3]))
		
		Npoints = float(len(loc1) + len(loc2) + len(loc3))

		wei = np.zeros(len(wavAbs))
		wei[0:len(loc1)] = 1./(len(loc1)/Npoints)
		wei[len(loc1):len(loc1)+len(loc2)] = 1./(len(loc2)/Npoints)
		wei[len(loc1)+len(loc2):] = 1./(len(loc3)/Npoints)

	else:
		k = 1

		# Get the flux in the anchored wavelengths
		wavAbs = np.concatenate((wavRest[loc1], wavRest[loc2]))
		fluxAbs = np.concatenate((flux[loc1], flux[loc2]))
		
		Npoints = float(len(loc1) + len(loc2))

		wei = np.zeros(len(wavAbs))
		wei[0:len(loc1)] = 1./(len(loc1)/Npoints)
		wei[len(loc1):len(loc1)+len(loc2)] = 1./(len(loc2)/Npoints)

	# Fit a k-order spline
	o = np.where(np.diff(wavAbs) > 0.)[0]
	spl = UnivariateSpline(np.log10(wavAbs[o]), np.log10(fluxAbs[o]), k=k, w = wei[o])
	contFlux = 10**spl(np.log10(wavRest))

	# Measure the ratio between the true and the observed flux
	fluxTrue9p7 = np.interp(9.7, wavRest, contFlux)
	locDeep = np.where((wavRest >= 9.4) & (wavRest <= 10.0))[0]
	fluxObs9p7 = np.mean(flux[locDeep])
	f9p7ratio = fluxObs9p7/fluxTrue9p7

	# Use the definition of tau9p7 and measure absorption(lambda)
	_tau9p7 = -np.log(f9p7ratio)

	return _tau9p7
	