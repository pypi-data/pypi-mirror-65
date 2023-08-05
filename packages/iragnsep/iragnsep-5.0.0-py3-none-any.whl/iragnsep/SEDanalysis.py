import numpy as np
import pandas as pd
import os
import emcee

from emcee import EnsembleSampler
from .func import *
from .classes import *
from numba import njit

#########################################################
#														#
#		PHOTOMETRIC + SPEC VERSION OF THE FITTING		#
#														#
#########################################################
@njit
def lnpostfn_spec_noAGN(theta, P, modelBG, modelSG, fluxFit, efluxFit, UL, wei, z):
	
	"""
    This function calculates the log-likelihood between spectral + photometric data and model without AGN contribution.
    ------------
    :param theta: vector containing the parameters.
    :param P: vector containing the priors for each of the parameters.
    :param modelBG: model dust continuum template.
    :param modelSG: model PAH template.
    :param fluxFit: observed fluxes.
    :param efluxFit: uncertainties on the observed fluxes.
    :param UL: vector contaning the upper-limits, if any.
    :param wei: weighting of the data points.
    :param z: redshift.
    ------------
    :return logl: log-likelihood of the model knowing the parameters theta.
    """

    # Set a variable for the loglikelihood
	logl = 0

	# Test if the sum of the wei is equal to 1, which is used as a flag for the final calculation of the loglikelihood of the model.
	# If it is the final calculation (i.e. paraneters have been optimised) we do not account for the priors.	
	if np.sum(wei != 1):
		# Prior constraint on the dust normalisation
		logl += -0.5*(theta[0])**2./P[0][1]**2.

		# Prior constraint on the PAH emission
		logl += -0.5*(theta[1])**2./P[1][1]**2.
		# Constraint on the 0.3 dex between the PAH and the dust continuum
		logl += - 0.5*(theta[1] + P[1][0] - (0.24 + 0.86 * (theta[0] + P[0][0])))**2./0.1**2.
	
	# Define the model knowing the parameters theta
	ymodel = 10**(theta[0] + P[0][0]) * modelBG + 10**(theta[1] + P[1][0]) * modelSG

	# Calculate the log-likelihood for the upper limits
	o = np.where(UL == 1)[0]
	if len(o) > 0:
		logl += loglUL(ymodel[o], fluxFit[o])

	# Calculate the log-likelihood for the detected values
	o = np.where(UL == 0)[0]
	logl += logldet(ymodel[o], fluxFit[o], efluxFit[o], wei[o])

	return logl


@njit
def lnpostfn_spec_wAGN(theta, P, modelBG, modelSG, fluxFit, efluxFit, UL, wei, z, wavFit):

	"""
    This function calculates the log-likelihood between spectral + photometric data and model that includes AGN contribution.
    ------------
    :param theta: vector containing the parameters.
    :param P: vector containing the priors for each of the parameters.
    :param modelBG: model dust continuum template.
    :param modelSG: model PAH template.
    :param fluxFit: observed fluxes.
    :param efluxFit: uncertainties on the observed fluxes.
    :param UL: vector contaning the upper-limits, if any.
    :param wei: weighting of the data points.
    :param z: redshift.
    :param wavFit: observed wavelengths.
    ------------
    :return logl: log-likelihood of the model knowing the parameters theta.
    """
	
	# set a variable for the log-likelihood
	logl = 0

	# Test if the sum of the wei is equal to 1, which is used as a flag for the final calculation of the loglikelihood of the model.
	# If it is the final calculation (i.e. paraneters have been optimised) we do not account for the priors.	
	if np.sum(wei != 1):
		# Normal prior on the norm of the dust
		logl += -0.5*(theta[0])**2./P[0][1]**2.

		# Normal prior on the norm of the PAH
		logl += -0.5*(theta[1])**2./P[1][1]**2.
		# Constraint on the 0.3 dex between the dust contrinuum and the PAH emission
		logl += - 0.5*(theta[1] + P[1][0] - (0.24 + 0.86 * (theta[0] + P[0][0])))**2./0.1**2.

		# Normal prior on the AGN power law
		logl += -0.5*(theta[2])**2./P[2][1]**2.

		# Normal prior on alpha1 + boundaries (i.e. -4.<alpha1<4.)
		if (theta[3]+P[3][0] < -4.) | (theta[3]+P[3][0] > 4.) == True:
				return -np.inf
		logl += -0.5*(theta[3])**2./P[3][1]**2.

		# Normal prior on alpha2 + boundaries (i.e. -4.<alpha2<2.)
		if (theta[4]+P[4][0] < -4.) | (theta[4]+P[4][0] > 2.) == True:
				return -np.inf
		logl += -0.5*(theta[4])**2./P[4][1]**2.

		# Normal Prior on the normalisation of the Si emission at 11 microns
		logl += -0.5*(theta[5])**2./P[5][1]**2.

		# Normal Prior on the normalisation of the Si emission at 18 microns
		logl += -0.5*(theta[6])**2./P[6][1]**2.

		# Prior on the position of the break + boundaries (i.e. 15<lbreak<100.)
		# Prior is flat below the best guess for lbreak and fall at wavelengths beyond that value.
		if (theta[7]+P[7][0] <= 15.) | (theta[7]+P[7][0] >= 100.) == True:
				return -np.inf
		x = (np.log10(np.array(theta[7]+P[7][0])) - np.log10(P[7][0]))/np.sqrt(2.)/P[7][1]
		logl += np.log(1. - 0.5 * (1. + erf_approx(np.array([x]))))

		# Calculate the model for the AGN given parameters theta.
		modelPL = 10**(theta[2] + P[2][0]) * AGNmodel_jit(wavFit, 15.*(1.+z), (theta[7]+P[7][0])*(1.+z), theta[3]+P[3][0], theta[4]+P[4][0], -3.5)
		modelSi11 = 10**(theta[5] + P[5][0]) * Gauss_jit(wavFit, np.log10(11.*(1.+z)), 0.05)
		modelSi18 = 10**(theta[6] + P[6][0]) * Gauss_jit(wavFit, np.log10(18.*(1.+z)), 0.07)

		# Calculate the full model (galaxy + AGN) given parameters theta.
		ymodel = modelPL + modelSi11 + modelSi18 + 10**(theta[0] + P[0][0]) * modelBG + 10**(theta[1]+ P[1][0]) * modelSG
	else:
		# if final calculation of the log-likelihood (i.e. parameters have been optimised), the models (galaxy and AGN) have been
		# calculated prior to this (i.e. kind of like templates, since the IRS has been reduced to at least 3 data points) and we just combine them in a full model.
		ymodel = 10**(theta[0] + P[0][0]) * modelBG + 10**(theta[1]+ P[1][0]) * modelSG + wavFit #wavFit actually contains the reduced AGN model

	# Calculate the log-likelihood for the undetected values
	o = np.where(UL == 1)[0]
	if len(o) > 0:
		logl += loglUL(ymodel[o], fluxFit[o])

	# Calculate the log-likelihood for detected values
	o = np.where(UL == 0)[0]
	logl += logldet(ymodel[o], fluxFit[o], efluxFit[o], wei[o])

	return logl

def runSEDspecFit(wavSpec, fluxSpec, efluxSpec,\
				  wavPhot, fluxPhot, efluxPhot, filters, \
				  z = -0.01,\
				  ULPhot = [], \
				  obsCorr = True,\
				  tau9p7_fixed = -99., \
				  Nmc = 10000, pgrbar = 1, \
				  Pdust = [10., 3.], PPAH = [9., 3.], Ppl = [-1., 3.], Pbreak = [1.603, 0.01], Pslope1 = [1., 2.], Pslope2 = [1., 2.], \
				  Plsg = [-1., 3.], Pllg = [-1., 3.],\
				  templ = ''):

	"""
    This function fits the observed SED when a spectrum is combined to photometric data. The observed wavelengths, fluxes and uncertainties on the fluxes are passed separately for the spectrum and the photometric data.
    ------------
    :param wavSpec: observed wavelengths for the spectrum (in microns).
    :param fluxSpec: observed fluxes for the spectrum (in Jansky).
    :param efluxSpec: observed uncertainties on the fluxes for the spectrum (in Jansky).
    :param wavPhot: observed wavelengths for the photometry (in microns).
    :param fluxPhot: observed fluxes for the photometry (in Jansky).
    :param efluxPhot: observed uncertainties on the fluxes for the photometry (in Jansky).
    :param filters: name of the photometric filters to include in the fit.
    ------------
    :keyword z: redshift of the source. Default = 0.01.
    :keyword ULPhot: vector of length Nphot, where Nphot is the number of photometric data. If any of the value is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
    :keyword obsCorr: if set to True, iragnsep attempt to calculate the total silicate absorption at 9.7micron, and to correct the observed fluxes for obscuration. Default = True
    :keyword tau9p7_fixed: can be used to pass a fixed value for the total silicate absorption at 9.7 micron. Default = -99.
    :keyword Nmc: numer of MCMC run. Default = 10000.
    :keyword pgrbar: if set to 1, display a progress bar while fitting the SED. Default = 1.
    :keyword Pdust: normal prior on the log-normalisation of the galaxy dust continuum template. Default = [10., 3.] ([mean, std dev]).
    :keyword PPAH: normal prior on the log-normalisation of the PAH template. Default = [9., 3.] ([mean, std dev]).
	:keyword Ppl: normal prior on the log-normalisation AGN continuum (defined at 10 micron). Default = [-1., 3.] ([mean, std dev]).
	:keyword Pbreak: normal prior on lbreak, the position of the log-break. Default = [1.6, 0.01] ([mean, std dev]).
	:keyword Pslope1: normal prior on alpha1, the slope of the first power-law defined between 1<lambda<15 microns. Default = [1., 2.] ([mean, std dev]).
	:keyword Pslope2: normal prior on alpha2, the slope of the second power-law defined between 15<lambda<lbreak. Default = [1., 2.] ([mean, std dev]).
	:keyword Plsg: normal prior on the log-normalisation of the silicate emission at 11micron. Default = [-1., 3.] ([mean, std dev]).
	:keyword Pllg: normal prior on the log-normalisation of the silicate emission at 18micron. Default = [-1., 3.] ([mean, std dev]).
	:keyword templ: pass the template to be used. If none, use the library of templates from Bernhard et al. (in prep.). Default: ''.
	------------
    :return res_fit: dataframe containing the results of all the possible fits.
    :return res_fitBM: dataframe containing the results of the best fit only.
    """

    # Redefine the average break position in linear space
	Pbreak[0] = 10**Pbreak[0]

	# If no template are used, open the Bernhard20 templates.
	if len(templ) == 0:
		path = os.path.dirname(iragnsep.__file__)
		templ = pd.read_csv(path+'/iragnsep_templ.csv')

	# Extract the names of the templates
	keys = templ.keys().values
	nameTempl_gal = []
	nameTempl_PAH = []
	for key in keys:
		if str(key).startswith('gal'):
			if str(key).endswith('PAH') == False:
				nameTempl_gal.append(key)
			else:
				nameTempl_PAH.append(key)

	# Test that we have template for everything (if no galaxy then it crashes)
	if len(nameTempl_gal) == 0:
		raise ValueError('The galaxy template does not exist. The name of the column defining nuLnu for the galaxy template needs to start with "gal".')

	# define the wavelengths
	try:
		wavTempl = templ['lambda_mic']
	except:
		raise ValueError('Rename the wavelengths column of the template "lambda_mic".')

	# Define the rest wavelengths for the photometric and the spectral data
	wavSpec_rest = wavSpec/(1. + z)
	wavPhot_rest = wavPhot/(1. + z)

	# Correct for absorption, using the total 9.7micron absorption feature.
	if tau9p7_fixed == -99.:
		# Test if there are actually data in the wavelength range, if not, continue the fit without correcting for obscuration
		o = np.where((wavSpec_rest > 9.) & (wavSpec_rest < 10.))[0]
		if (len(o) == 0.) & (obsCorr == True):
			print('*******************')
			print('It has failed to correct for obscuration. The most likely explanation is redshift since it needs the restframe anchor ' + \
					   'wavelengths to measure the strength of the silicate absorption. The fit is continued without correcting for obscuration.')
			print('*******************')
			obsCorr = False

		# Correct for obscuration. If it somehow fails, continue the fit without correcting for obscuration.
		if obsCorr == True:
			try:
				_tau9p7 = obsC(wavSpec_rest, fluxSpec, efluxSpec)
				_tau9p7 = round(_tau9p7,3)
			except:
				_tau9p7 = -99.
				print('*******************')
				print('It has failed to correct the IRS spectrum for obscuration. The most likely explanation is redshift since it needs the restframe anchor ' + \
					   'wavelengths to measure the strength of the silicate absorption. The fit is continued without correcting for obscuration.')
				print('*******************')
				pass
		else:
			_tau9p7 = -99.
	else:
		# If fixed, use tau9p7 fixed by the user
		_tau9p7 = tau9p7_fixed

	if _tau9p7 > 0:
		tauSpec = KVTextinctCurve(wavSpec_rest) * _tau9p7
		tauPhot = KVTextinctCurve(wavPhot_rest) * _tau9p7

		fluxSpec_corr = fluxSpec/((1. - np.exp(-tauSpec))/tauSpec)
		efluxSpec_corr = efluxSpec/((1. - np.exp(-tauSpec))/tauSpec)
		fluxPhot_corr = fluxPhot/((1. - np.exp(-tauPhot))/tauPhot)
		efluxPhot_corr = efluxPhot/((1. - np.exp(-tauPhot))/tauPhot)
	else:
		fluxSpec_corr = fluxSpec
		efluxSpec_corr = efluxSpec
		fluxPhot_corr = fluxPhot
		efluxPhot_corr = efluxPhot
		_tau9p7 = -99.

	# Concatenate the spectral and the photometric data.
	wavFit = np.concatenate([wavSpec, wavPhot])
	fluxFit = np.concatenate([fluxSpec_corr, fluxPhot_corr])
	efluxFit = np.concatenate([efluxSpec_corr, efluxPhot_corr])

	#Calculate the weights that should be allocated to the spectra, with respect to the photometry
	Npoints = float(len(fluxFit))
	Photwei = 1./((Npoints-len(wavSpec))/Npoints)
	Specwei = 1./((len(wavSpec))/Npoints)
	Specwei_dist = np.zeros(len(wavSpec)) + Specwei
	Photwei_dist = np.zeros(len(wavPhot)) + Photwei
	wei = np.concatenate([Specwei_dist, Photwei_dist])

	# Prepare the upper limits. Set a vector of zeros for the spectra. Set a vector fo zeros for the photometry if UL is underfined.
	if len(ULPhot) != len(wavPhot):
		ULPhot = np.zeros(len(wavPhot))
	ULSpec = np.zeros(len(wavSpec))
	UL = np.concatenate([ULSpec, ULPhot])

	# Calculate the number of points that the spectra should be reduced to for the final calculation of the log-likelihood of the model,
	# knowing the optimised parameters.
	photoCov = max(wavPhot) - max(wavSpec)
	photo_covPerDat = float(len(fluxPhot))/photoCov
	specCov = max(wavSpec) - min(wavSpec)
	Npoints_red = (photo_covPerDat * specCov) + 1
	if Npoints_red < 4:
		Npoints_red = 4

	wavSpecAnchor = 10**np.linspace(np.log10(min(wavSpec)), np.log10(max(wavSpec)), Npoints_red)
	wavSpec_red = []
	fluxSpec_red = []
	for i in range(0, Npoints_red-1):
		o = np.where((wavSpec >= wavSpecAnchor[i]) & (wavSpec < wavSpecAnchor[i+1]))[0]
		wavSpec_red.append(np.mean(wavSpec[o]))
		fluxSpec_red.append(np.mean(fluxSpec_corr[o]))
	efluxSpec_red = np.array(fluxSpec_red) * np.mean(efluxPhot/fluxPhot)

	# These variables contain the reduced observed wavelengths, fluxex, and uncertainties.
	wavFit_red = np.concatenate([wavSpec_red, wavPhot])
	fluxFit_red = np.concatenate([fluxSpec_red, fluxPhot_corr])
	efluxFit_red = np.concatenate([efluxSpec_red, efluxPhot_corr])
	ULSpec_red = np.zeros(len(wavSpec_red))
	UL_red = np.concatenate([ULSpec_red, ULPhot])
	wei_red = np.ones(len(wavFit_red))

	# Define the free parameters
	lsg_perTempl = [] #silicate at 11 micron
	elsg_perTempl = []
	llg_perTempl = [] #silicate at 18 micron
	ellg_perTempl = []
	lnAGN_perTempl = [] #norm AGN continuum
	elnAGN_perTempl = []
	coff_perTempl = [] #cut off or position of the break
	ecoff_perTempl = []
	alpha1_perTempl = [] #slope of the first power law
	ealpha1_perTempl = []
	alpha2_perTempl = [] #slope of the second power law
	ealpha2_perTempl = []
	
	lnDust_perTempl = [] #dust continuum
	elnDust_perTempl = []
	lnPAH_perTempl = [] #PAH emission
	elnPAH_perTempl = []
	
	logl_perTempl = [] #log-likelihood of the mode
	tplName_perTempl = []#Name of the template 
	tau9p7_save = []#total absorption at 9.7 micron
	AGNon = []#flag for the use of the AGN in the fit
	nParms = []# number of parameters

	# Fit looping over every of our galaxy templates
	for name_i in nameTempl_gal:
		assert isinstance(name_i, str), "The list nameTempl requests strings as it corresponds to the names" + \
										" given to the various templates of galaxies to use for the fit."

		if pgrbar == 1:
			print("****************************************")
			print("  Fit of "+name_i+" as galaxy template  ")
			print("****************************************")

		# Define synthetic fluxes for the dust continuum model at the observed wavelength to match the observed fluxes
		nuLnuBGTempl = templ[name_i].values

		Fnu = nuLnuToFnu(wavTempl, nuLnuBGTempl, z)
		fluxSpec_model = np.interp(wavSpec_rest, wavTempl, Fnu)

		SEDgen = modelToSED(wavTempl, nuLnuBGTempl, z)
		fluxPhot_model = []
		for filt in filters:
		 	fluxPhot_model.append(getattr(SEDgen, filt)())
		modelBG_phot = fluxPhot_model

		modelBG = np.concatenate([fluxSpec_model, fluxPhot_model])

		# Define synthetic fluxes for the PAH model at the observed wavelength to match the observed fluxes.
		# When an empirical template is used, define a vector of zeros so that no PAH emission is accounted for.
		if name_i.endswith('dust') == False:
			modelSG = np.zeros(len(modelBG))
			modelSG_phot = np.zeros(len(modelBG_phot))
		else:
			nuLnuSGTempl = templ[nameTempl_PAH[0]].values

			Fnu = nuLnuToFnu(wavTempl, nuLnuSGTempl, z)
			fluxSpec_model = np.interp(wavSpec_rest, wavTempl, Fnu)

			SEDgen = modelToSED(wavTempl, nuLnuSGTempl, z)
			fluxPhot_model = []
			for filt in filters:
				fluxPhot_model.append(getattr(SEDgen, filt)())
			modelSG_phot = fluxPhot_model

			modelSG = np.concatenate([fluxSpec_model, fluxPhot_model])

		# fit without the AGN
		ndim = 2 #Number of paraneter
		nwalkers = int(2. * ndim) #number of walkers

		# Define the starting point of each of the parameters. Flat distrib. between -1 and 1. Parameters are normalised with a zero mean to ease convergence.
		parms = np.zeros(shape=(nwalkers, ndim))
		parms[:,0] = np.random.uniform(low = -1., high = 1., size=nwalkers) # norm Dust
		parms[:,1] = np.random.uniform(low = -1., high = 1., size=nwalkers) # norm PAH

		# Set the ensemble sampler of Goodman&Weare and run the MCMC for Nmc steps.
		sampler = EnsembleSampler(nwalkers, ndim, lnpostfn_spec_noAGN, args = (np.array([Pdust, PPAH]), modelBG, modelSG, fluxFit, efluxFit, \
								  UL, wei, z))
		sampler.run_mcmc(parms, Nmc, progress=bool(pgrbar))
		
		# Build the flat chain after burning 20% of it and thinning to every 10 values.
		NburnIn = int(0.2 * Nmc)
		chain = sampler.get_chain(discard=NburnIn, thin=10, flat=True)

		# Save the optimised parameters. Median of the posterior as best fitting value and std dev as 1sigma uncertainties.
		# Dust continuum
		lnDust_perTempl.append(round(np.median(chain[:,0]),3))
		elnDust_perTempl.append(round(np.std(chain[:,0]),3))

		# PAH continuum (-20. for empirical template since no PAH should be added).
		if np.sum(modelSG) > 0.:
			lnPAH_perTempl.append(round(np.median(chain[:,1]),3))
			elnPAH_perTempl.append(round(np.std(chain[:,1]),3))
		else:
			lnPAH_perTempl.append(-20.)
			elnPAH_perTempl.append(0.0)

		# Norm AGN, here -99. since no AGN accounted for
		lnAGN_perTempl.append(-99.)
		elnAGN_perTempl.append(-99.)

		# slope of the first power law, here -99. since no AGN accounted for
		alpha1_perTempl.append(-99.)
		ealpha1_perTempl.append(-99.)

		# slope of the second power law, here -99. since no AGN accounted for
		alpha2_perTempl.append(-99.)
		ealpha2_perTempl.append(-99.)

		# cut off or position of the break, here -99. since no AGN accounted for
		coff_perTempl.append(-99.)
		ecoff_perTempl.append(-99.)

		# silicate emisison at 11 microns, here -99. since no AGN accounted for
		lsg_perTempl.append(-99.)
		elsg_perTempl.append(-99.)

		# silicate emisison at 18 microns, here -99. since no AGN accounted for
		llg_perTempl.append(-99.)
		ellg_perTempl.append(-99.)

		# Calculate the reduced model flux and calculate the final log-likleihood, knowing the optimised parameters.
		fluxSpecModelBG_red = []
		fluxSpecModelSG_red = []
		for i in range(0, Npoints_red-1):
			o = np.where((wavSpec >= wavSpecAnchor[i]) & (wavSpec < wavSpecAnchor[i+1]))[0]
			fluxSpecModelBG_red.append(np.mean(modelBG[o]))
			fluxSpecModelSG_red.append(np.mean(modelSG[o]))

		modelBG_red = np.concatenate([fluxSpecModelBG_red, modelBG_phot])
		modelSG_red = np.concatenate([fluxSpecModelSG_red, modelSG_phot])

		logl = lnpostfn_spec_noAGN(np.array([lnDust_perTempl[-1], lnPAH_perTempl[-1]]), \
								   np.array([Pdust, PPAH]), \
								   modelBG_red, modelSG_red, \
								   fluxFit_red, efluxFit_red, \
								   UL_red, wei_red, z)
		logl_red = logl/float(len(modelBG_red))
		logl_perTempl.append(logl)

		# Flag for the used of an AGN. Here 0., since no AGN is accounted for.
		AGNon.append(0.)
		# save the number of parameters
		nParms.append(2)
		# save the name of the template
		tplName_perTempl.append(name_i)
		# Save teh total absorption at 9.7 microns.
		tau9p7_save.append(round(_tau9p7,3))

		# Fit including the full AGN model.
		ndim = 8 #NUmber of parms
		nwalkers = int(2. * ndim) # Number of walkers

		# Define the starting parms. Each of them has been normalised to a mean of zero to ease convergence.
		parms = np.zeros(shape=(nwalkers, ndim))
		parms[:,0] = np.random.uniform(low = -1., high = 1., size=nwalkers) # norm Dust
		parms[:,1] = np.random.uniform(low = -1., high = 1., size=nwalkers) # norm PAH
		parms[:,2] = np.random.uniform(low = -1., high = 1., size=nwalkers) # norm PL AGN
		parms[:,3] = np.random.uniform(low = -1., high = 0., size=nwalkers) # alpha1
		parms[:,4] = np.random.uniform(low = 0., high = 1., size=nwalkers) # alpha2
		parms[:,5] = np.random.uniform(low = -1., high = 1., size=nwalkers) # 10micron
		parms[:,6] = np.random.uniform(low = -1., high = 1., size=nwalkers) # 18micron
		parms[:,7] = np.random.uniform(low = -10., high = 10., size=nwalkers) # Break

		# Set the ensemble sample of Goodman&Weare and run the MCMC for Nmc steps
		sampler = EnsembleSampler(nwalkers, ndim, lnpostfn_spec_wAGN, args = (np.array([Pdust, PPAH, Ppl, Pslope1, Pslope2, Plsg, Pllg, Pbreak]), \
								  modelBG, modelSG, fluxFit, efluxFit, UL, wei, z, wavFit))
		sampler.run_mcmc(parms, Nmc, progress=bool(pgrbar))

		# Build the flat chain after burning 20% of the chain and thinning to every 10 values.
		chain = sampler.get_chain(discard=NburnIn, thin=10, flat=True)

		# Save the results
		#Dust continuum
		lnDust_perTempl.append(round(np.median(chain[:,0]),3))
		elnDust_perTempl.append(round(np.std(chain[:,0]),3))

		# PAH emission (set to -20. for empirircal templates)
		if np.sum(modelSG) > 0.:
			lnPAH_perTempl.append(round(np.median(chain[:,1]),3))
			elnPAH_perTempl.append(round(np.std(chain[:,1]),3))
		else:
			lnPAH_perTempl.append(-20.)
			elnPAH_perTempl.append(0.0)

		# Norm of the AGN continuum
		lnAGN_perTempl.append(round(np.median(chain[:,2]),3))
		elnAGN_perTempl.append(round(np.std(chain[:,2]),3))

		# slope of the first power law
		alpha1_perTempl.append(round(np.median(chain[:,3]),3))
		ealpha1_perTempl.append(round(np.std(chain[:,3]),3))

		# slope of the second power law
		alpha2_perTempl.append(round(np.median(chain[:,4]),3))
		ealpha2_perTempl.append(round(np.std(chain[:,4]),3))

		# silicate emission at 11 micron
		lsg_perTempl.append(round(np.median(chain[:,5]),3))
		elsg_perTempl.append(round(np.std(chain[:,5]),3))

		# silicate emisison at 18 micron
		llg_perTempl.append(round(np.median(chain[:,6]),3))
		ellg_perTempl.append(round(np.std(chain[:,6]),3))

		# cut off or position of the break
		coff_perTempl.append(round(np.median(chain[:,7]),3))
		ecoff_perTempl.append(round(np.std(chain[:,7]),3))

		# Define the reduced model (AGN + galaxy) for the final comparison
		modelPL = 10**(lnAGN_perTempl[-1] + Ppl[0]) * AGNmodel_jit(wavFit, 15.*(1.+z), (coff_perTempl[-1] + Pbreak[0])*(1.+z), \
					   alpha1_perTempl[-1] + Pslope1[0], alpha2_perTempl[-1]+Pslope2[0], -3.5)
		modelSi11 = 10**(lsg_perTempl[-1] + Plsg[0]) * Gauss_jit(wavFit, np.log10(11.*(1.+z)), 0.05)
		modelSi18 = 10**(llg_perTempl[-1] + Pllg[0]) * Gauss_jit(wavFit, np.log10(18.*(1.+z)), 0.07)
		modelAGN = modelPL + modelSi11 + modelSi18

		modelAGNSpec_red = []
		for i in range(0, Npoints_red-1):
			o = np.where((wavSpec >= wavSpecAnchor[i]) & (wavSpec < wavSpecAnchor[i+1]))[0]
			modelAGNSpec_red.append(np.mean(modelAGN[o]))
		modelAGN_red = np.concatenate([modelAGNSpec_red, np.interp(wavPhot, wavFit, modelAGN)])

		# save the loglikelihood of the model knowing the optimised parameters
		theta = np.array([lnDust_perTempl[-1], lnPAH_perTempl[-1], lnAGN_perTempl[-1], alpha1_perTempl[-1], \
				 		  alpha2_perTempl[-1], lsg_perTempl[-1], llg_perTempl[-1], coff_perTempl[-1]])
		Pr = np.array([Pdust, PPAH, Ppl, Pslope1, Pslope2, Plsg, Pllg, Pbreak])
		logl = lnpostfn_spec_wAGN(theta, \
								  Pr, \
								  modelBG_red, modelSG_red, \
								  fluxFit_red, efluxFit_red, \
								  UL_red, wei_red, z, modelAGN_red)

		logl_red = logl/float(len(modelBG_red))
		logl_perTempl.append(logl)

		# AGNon = 1 since AGN is accounted for
		AGNon.append(1.)
		# Save the number of parameters
		nParms.append(8)
		# Save the name of the galaxy template
		tplName_perTempl.append(name_i)
		# Save the total obscuration at 9.7 microns
		tau9p7_save.append(round(_tau9p7,3))

	# Find the best model and the Akaike weight
	bestModelInd, Awi = exctractBestModel(logl_perTempl, nParms, len(wavFit), corrected = False)
	bestModelFlag = np.zeros(len(AGNon))
	bestModelFlag[bestModelInd] = 1

	# Save the results in a table
	resDict = {'logNormGal_dust': np.array(lnDust_perTempl) + Pdust[0], 'elogNormGal_dust': np.array(elnDust_perTempl), \
			   'logNormGal_PAH': np.array(lnPAH_perTempl) + PPAH[0], 'elogNormGal_PAH': np.array(elnPAH_perTempl), \
			   'logNormAGN_PL': np.array(lnAGN_perTempl) + Ppl[0], 'elogNormAGN_PL': np.array(elnAGN_perTempl), \
			   'lBreak_PL': np.array(coff_perTempl) + Pbreak[0], 'elBreak_PL': np.array(ecoff_perTempl), \
			   'alpha1_PL': np.array(alpha1_perTempl) + Pslope1[0], 'ealpha1_PL': np.array(ealpha1_perTempl), \
			   'alpha2_PL': np.array(alpha2_perTempl) + Pslope2[0], 'ealpha2_PL': np.array(ealpha2_perTempl), \
			   'logNorm_Si11': np.array(lsg_perTempl) + Plsg[0], 'elogNorm_Si11': np.array(elsg_perTempl), \
			   'logNorm_Si18': np.array(llg_perTempl) + Pllg[0], 'elogNorm_Si18': np.array(ellg_perTempl), \
			   'logl': logl_perTempl, 'AGNon': AGNon, 'tplName': tplName_perTempl,\
			   'bestModelFlag': bestModelFlag, 'Aw': Awi, 'tau9p7': tau9p7_save}

	dfRes = pd.DataFrame(resDict)

	return dfRes


#################################################
#												#
#		PHOTOMETRIC VERSION OF THE FITTING		#
#												#
#################################################
@njit
def lnpostfn_photo_noAGN(theta, P, modelBG, modelSG, UL, fluxFit, efluxFit,wei):

	"""
    This function calculates the log-likelihood between photometric data and model without AGN contribution.
    ------------
    :param theta: vector containing the parameters.
    :param P: vector containing the priors for each of the parameters.
    :param modelBG: model dust continuum template.
    :param modelSG: model PAH template.
    :param UL: vector contaning the upper-limits, if any.
    :param fluxFit: observed fluxes.
    :param efluxFit: uncertainties on the observed fluxes.
    :param wei: weighting of the data points.
    ------------
    :return logl: log-likelihood of the model knowing the parameters theta.
    """
	
	# set the log-likelihood to zero
	logl = 0
	
	# prior constrain on the normalisation of the dust continuum for galaxy
	logl += -0.5*(theta[0])**2./P[0][1]**2.

	# prior constrain on the normalisation of the PAH
	logl += -0.5*(theta[1])**2./P[1][1]**2.
	# constrain on 0.3 dex between the normalisation of the dust to that of PAHs
	logl += - 0.5*(theta[1] + P[1][0] - (0.24 + 0.86 * (theta[0] + P[0][0])))**2./0.1**2.

	# define the full model as PAH + dust continuum
	ymodel = 10**(theta[0] + P[0][0]) * modelBG + 10**(theta[1] + P[1][0]) * modelSG

	# calculate the log-likelihood for upper-limits
	o = np.where(UL == 1)[0]
	if len(o)>0:
		logl += loglUL(ymodel[o], fluxFit[o])

	# calculate the log-likelihood for detected values
	o = np.where(UL == 0)[0]
	logl += logldet(ymodel[o], fluxFit[o], efluxFit[o], wei[o])

	return logl

@njit
def lnpostfn_photo_wAGN(theta, P, modelBG, modelSG, modelAGN, modelSi, UL, fluxFit, efluxFit,wei):
	
	"""
    This function calculates the log-likelihood between photometric data and model that includes AGN contribution.
    ------------
    :param theta: vector containing the parameters.
    :param P: vector containing the priors for each of the parameters.
    :param modelBG: model dust continuum template.
    :param modelSG: model PAH template.
    :param modelAGN: model AGN continuum template.
    :param modelSi: model silicate emission template.
    :param UL: vector contaning the upper-limits, if any.
    :param fluxFit: observed fluxes.
    :param efluxFit: uncertainties on the observed fluxes.
    :param wei: weighting of the data points.
    ------------
    :return logl: log-likelihood of the model knowing the parameters theta.
    """
	# set the log-likelihood to zero
	logl = 0

	# prior constrain on the normalisation of the dust continuum for galaxy
	logl += -0.5*(theta[0])**2./P[0][1]**2.
	
	# prior constrain on the normalisation of the PAH
	logl += -0.5*(theta[1])**2./P[1][1]**2.
	# constrain on 0.3 dex between the normalisation of the dust to that of PAHs
	logl += -0.5*(theta[1] + P[1][0] - (0.24 + 0.86 * (theta[0] + P[0][0])))**2./0.1**2.

	# prior constrain on the normalisation of the AGN continuum
	logl += -0.5*(theta[2])**2./P[2][1]**2.

	# prior constrain on the normalisation of the silicate emission
	logl += -0.5*(theta[3])**2./P[3][1]**2.

	# define the full model as PAH + dust continuum + AGN continuum + silicate emission
	ymodel = 10**(theta[0] + P[0][0]) * modelBG + 10**(theta[1] + P[1][0]) * modelSG + 10**(theta[2] + P[2][0]) * modelAGN + 10**(theta[3] + P[3][0]) * modelSi

	# calculate the log-likelihood for upper-limits
	o = np.where(UL == 1)[0]
	if len(o)>0:
		logl += loglUL(ymodel[o], fluxFit[o])
	
	# calculate the log-likelihood for detected values
	o = np.where(UL == 0)[0]
	logl += logldet(ymodel[o], fluxFit[o], efluxFit[o], wei[o])

	return logl


def runSEDphotFit(lambdaObs, fluxObs, efluxObs, \
				  filters, \
				  z = 0.01, \
				  UL = [], \
				  Nmc = 10000, pgrbar = 1, \
				  NoSiem = False, \
				  Pdust = [10., 13], PPAH = [9., 3.], PnormAGN = [10., 3.], PSiEm = [10., 3.], \
				  templ = ''):

	"""
    This function fits the observed photometric SED.
    ------------
    :param lambdaObs: observed wavelengths (in microns).
    :param fluxObs: observed fluxes (in Jansky).
    :param efluxObs: observed uncertainties on the fluxes (in Jansky).
    :param filters: name of the photometric filters to include in the fit.
    ------------
    :keyword z: redshift of the source. Default = 0.01.
    :keyword UL: vector of length Nphot, where Nphot is the number of photometric data. If any of the value is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
    :keyword Nmc: numer of MCMC run. Default = 10000.
    :keyword pgrbar: if set to 1, display a progress bar while fitting the SED. Default = 1.
	:keyword NoSiem: if set to True, no silicate emission template is included in the fit. Default = False.
    :keyword Pdust: normal prior on the log-normalisation of the galaxy dust continuum template. Default = [10., 3.] ([mean, std dev]).
    :keyword PPAH: normal prior on the log-normalisation of the PAH template. Default = [9., 3.] ([mean, std dev]).
    :keyword PnormAGN: normal prior on the log-normalisation of the AGN template. Default = [10., 3.] ([mean, std dev]).
    :keyword PSiem: normal prior on the log-normalisation of the silicate emission template. Default = [10., 3.] ([mean, std dev]).
    :keyword templ: pass the template to be used. If none, use the library of templates from Bernhard et al. (in prep.). Default: ''.
	------------
    :return dfRes: dataframe containing the results of all the possible fits.
    """

	# If no templates are passed, open the Bernhard+20 templates.
	if len(templ) == 0:
		path = os.path.dirname(iragnsep.__file__)
		templ = pd.read_csv(path+'/iragnsep_templ.csv')

	# Extract the name of the templates
	keys = templ.keys().values
	nameTempl_gal = []
	nameTempl_PAH = []
	nameTempl_AGN = []
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

	# define the wavelengths
	try:
		wavTempl = templ['lambda_mic'].values
	except:
		raise ValueError('Rename the wavelengths column of the template "lambda_mic".')

	# calculate the uncertainties on the fluxes
	unc = efluxObs/fluxObs
	
	# define the weighting accordingly
	wei_i = 1./unc**2./np.sum(1./unc**2.)
	wei = (1./wei_i)/np.sum(1./wei_i)
	wei_final = wei*np.gradient(lambdaObs)

	# Define a vectors of zeros if no upper limts are passed.
	if len(UL) != len(lambdaObs):
		UL = np.zeros(len(lambdaObs))

	# Define the free parameters
	# Norm AGN continuum
	lnAGN_perTempl = []
	elnAGN_perTempl= []

	# Norm silicate emission
	lnSi_perTempl = []
	elnSi_perTempl = []

	# Norm dust continuum
	lnDust_perTempl = []
	elnDust_perTempl = []

	# Norm PAHs
	lnPAH_perTempl = []
	elnPAH_perTempl = []

	# final loglikelihood of the model
	logl_perTempl = []
	# name of the AGN and galaxy template
	tplNameGal_perTempl = []
	tplNameAGN_perTempl = []
	# if AGN is accounted for (1) or not (0)
	AGNon = []
	# Number of parameters in the model
	nParms = []

	# We loop over the 6 galaxy templates, first fitting only galaxy templates and then including the AGN templates.
	for name_i in nameTempl_gal:
		assert isinstance(name_i, str), "The list nameTempl requests strings as it corresponds to the names" + \
										" given to the various templates of galaxies to use for the fit."

		if pgrbar == 1:
			print("****************************************")
			print("  Fit of "+name_i+" as galaxy template  ")
			print("****************************************")

		# calculate the synthetic photometry of the Dust continuum template at wavelengths lambdaObs.
		nuLnuBGTempl = templ[name_i].values
		# Convert to photometric flux
		SEDgen = modelToSED(wavTempl, nuLnuBGTempl, z)
		modelBG = []
		for filt in filters:
			modelBG.append(getattr(SEDgen, filt)())

		modelBG = np.array(modelBG)

		# calculate the synthetic photometry of the PAH template at wavelengths lambdaObs.
		# When the empirical template is used, simply set a vector of zeros, so no separate contributions are accounted for as PAH emission.
		if name_i.endswith('dust') == False:
			modelSG = modelBG * 0.
			emodelSG = modelBG * 0.
		else:
			nuLnuSGTempl = templ['gal_PAH'].values
			SEDgen = modelToSED(wavTempl, nuLnuSGTempl, z)
			modelSG = []
			for filt in filters:
				modelSG.append(getattr(SEDgen, filt)())

			modelSG = np.array(modelSG)

		# Perform the fit without the AGN contribution
		ndim = 2 # Number of free params
		nwalkers = int(2. * ndim) # Number of walkers

		# Define the parameters as flat distributions between -1 and 1. (We normalised to zero each parameters to ease convergence).
		parms = np.zeros(shape=(nwalkers, ndim))
		parms[:,0] = np.random.uniform(low = -1., high = 1., size=nwalkers) # norm Dust
		parms[:,1] = np.random.uniform(low = -1., high = 1., size=nwalkers) # norm PAH

		# Set the ensemble sampler of Goodman&Weare and run the MCMC for Nmc steps
		sampler = EnsembleSampler(nwalkers, ndim, lnpostfn_photo_noAGN, args = (np.array([Pdust, PPAH]), modelBG, modelSG, UL, fluxObs, efluxObs,wei))
		sampler.run_mcmc(parms, Nmc, progress=bool(pgrbar))

		# Build the flat chain, after burning 20% of the chain and thinning to every 10 values.
		NburnIn = int(0.2 * Nmc)
		chain = sampler.get_chain(discard=NburnIn, thin=10, flat=True)

		# Save the best fit parameters. Median of the posterior is taken as the best fit parameter and the standard deviation as 1sigma uncertainties.
		# Norm dust continuum
		lnDust_perTempl.append(round(np.median(chain[:,0]),3))
		elnDust_perTempl.append(round(np.std(chain[:,0]),3))

		# Norm PAH emission (or -20. when the empirical template is used).
		if np.sum(modelSG) > 0.:
			lnPAH_perTempl.append(round(np.median(chain[:,1]),3))
			elnPAH_perTempl.append(round(np.std(chain[:,1]),3))
		else:
			lnPAH_perTempl.append(-20.)
			elnPAH_perTempl.append(0.0)

		# Calulate the final loglikelihood of the model, using the best fit parameters.
		logl_perTempl.append(round(lnpostfn_photo_noAGN(np.array([lnDust_perTempl[-1], lnPAH_perTempl[-1]]), np.array([Pdust, PPAH]), \
								   modelBG, modelSG, UL, fluxObs, efluxObs,wei_final),3))
		
		# Norm on the silicate emission. -99. here since no AGN is accounted for.
		lnSi_perTempl.append(-99.)
		elnSi_perTempl.append(-99.)

		# Norm on the AGN template. -99. here since no AGN is accounted for.
		lnAGN_perTempl.append(-99.)
		elnAGN_perTempl.append(-99.)

		# No AGN in this fits, so AGNon set to zero
		AGNon.append(0.)
		# Save the numbers of parameters used in the fit, i.e. 2.
		nParms.append(2.)
		# Save the name of the template for the galaxy.
		tplNameGal_perTempl.append(name_i)
		# No AGN templates used in this fit, so name of the AGN template is set to 'N/A'.
		tplNameAGN_perTempl.append(str('N/A'))


		# Fit including the AGN. Loop over the two templates AGN A and AGN B.
		for AGN_i in nameTempl_AGN:

			# calculate the synthetic photometry of the AGN template at wavelengths lambdaObs.
			nuLnu_AGN = templ[AGN_i].values
			# generate the photometry
			SEDgen = modelToSED(wavTempl, nuLnu_AGN, z)
			modelAGN = []
			for filt in filters:
				modelAGN.append(getattr(SEDgen, filt)())

			modelAGN = np.array(modelAGN)

			# calculate the synthetic photometry of the silicate template at wavelengths lambdaObs.
			# If no silicate emission is considered, set a vector of zeros so that no silicate emisison is account for.
			modelSiem = []
			if NoSiem == False:
				nuLnu_Siem = templ[nameTempl_Siem].values.flatten()
				SEDgen = modelToSED(wavTempl, nuLnu_Siem, z)
				for filt in filters:
					modelSiem.append(getattr(SEDgen, filt)())

				modelSiem = np.array(modelSiem)
			else:
				modelSiem = modelAGN * 0.

			# Perform the fit with the AGN contribution
			ndim = 4 # Number of parmameters
			nwalkers = int(2. * ndim) # Number of walkers

			# Define the starting parameters as flat distributions between -1 and 1. We normalised each parameter to zero to each convergence.
			parms = np.zeros(shape=(nwalkers, ndim))
			parms[:,0] = np.random.uniform(low = -1., high = 1., size=nwalkers) # norm Dust
			parms[:,1] = np.random.uniform(low = -1., high = 1., size=nwalkers) # norm PAH
			parms[:,2] = np.random.uniform(low = -1., high = 1., size=nwalkers) # normAGN
			parms[:,3] = np.random.uniform(low = -1., high = 1., size=nwalkers) # normSi

			# Set the ensemble sampler of Goodman&Weare and run the MCMC for Nmc steps.
			sampler = EnsembleSampler(nwalkers, ndim, lnpostfn_photo_wAGN, args = (np.array([Pdust, PPAH, PnormAGN, PSiEm]), \
									  modelBG, modelSG, modelAGN, modelSiem, UL, fluxObs, efluxObs,wei))
			sampler.run_mcmc(parms, Nmc, progress=bool(pgrbar))

			# Build the flat chain, after burning 20% of the chain and thinning to every 10 values in the chain.
			chain = sampler.get_chain(discard=NburnIn, thin=10, flat=True)

			# Save the best fit parameters. Median of the posterior is taken as the best fit parameter and the standard deviation as 1sigma uncertainties.
			# Dust Normalisation
			lnDust_perTempl.append(round(np.median(chain[:,0]),3))
			elnDust_perTempl.append(round(np.std(chain[:,0]),3))

			# PAH normalisation
			if np.sum(modelSG) > 0.:
				lnPAH_perTempl.append(round(np.median(chain[:,1]),3))
				elnPAH_perTempl.append(round(np.std(chain[:,1]),3))
			else:
				lnPAH_perTempl.append(-20.)
				elnPAH_perTempl.append(0.0)

			# AGN continuum Norm
			lnAGN_perTempl.append(round(np.median(chain[:,2]),3))
			elnAGN_perTempl.append(round(np.std(chain[:,2]),3))

			# Si emission Norm
			if NoSiem == True:
				lnSi_perTempl.append(-20.)
				elnSi_perTempl.append(0.0)
			else:
				lnSi_perTempl.append(round(np.median(chain[:,3]),3))
				elnSi_perTempl.append(round(np.std(chain[:,3]),3))

			# Numbers of params in the model
			nParms.append(4.)
 
			# AGN accounted for in this case, so AGNon = 1
			AGNon.append(1.)

			# Name of the galaxy template
			tplNameGal_perTempl.append(name_i)

			# Name of the AGN template
			tplNameAGN_perTempl.append(AGN_i)

			# loglikelihood of the model
			logl_perTempl.append(round(lnpostfn_photo_wAGN(np.array([lnDust_perTempl[-1], lnPAH_perTempl[-1], lnAGN_perTempl[-1], \
									   lnSi_perTempl[-1]]), np.array([Pdust, PPAH, PnormAGN, PSiEm]), modelBG, modelSG, modelAGN, \
									   modelSiem, UL, fluxObs, efluxObs,wei_final),3))

	# Find the best model and the Akaike weight amongst all the 18 possible fits by comparing their final loglikelihood
	bestModelInd, Awi = exctractBestModel(logl_perTempl, nParms, len(lambdaObs), corrected = True)
	bestModelFlag = np.zeros(len(AGNon))
	bestModelFlag[bestModelInd] = 1

	# Save the results in a table
	resDict = {'logNormGal_dust': np.array(lnDust_perTempl) + Pdust[0], 'elogNormGal_dust': np.array(elnDust_perTempl), \
			   'logNormGal_PAH': np.array(lnPAH_perTempl) + PPAH[0], 'elogNormGal_PAH': np.array(elnPAH_perTempl), \
			   'logNormAGN': np.array(lnAGN_perTempl) + PnormAGN[0], 'elogNormAGN': np.array(elnAGN_perTempl), \
			   'logNormSiem': np.array(lnSi_perTempl) + PSiEm[0], 'elogNormSiem': np.array(elnSi_perTempl), \
			   'logl': logl_perTempl, 'AGNon': AGNon, 'tplName_gal': tplNameGal_perTempl, 'tplName_AGN': tplNameAGN_perTempl,\
			   'bestModelFlag': bestModelFlag, 'Aw': Awi}

	dfRes = pd.DataFrame(resDict)

	return dfRes