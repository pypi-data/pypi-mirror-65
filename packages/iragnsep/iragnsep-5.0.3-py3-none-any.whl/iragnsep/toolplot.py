import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

from .func import *
from .classes import *

from matplotlib.font_manager import FontProperties
font0 = FontProperties(family = 'serif', variant = 'small-caps', size = 22)

############################
## Plot all the results for all the possible fit. Tag the best model in blue.
############################
def plotFitSpec(df, wavSpec, fluxSpec, efluxSpec,\
				wavPhot, fluxPhot, efluxPhot, UL = np.array([]), pathFig = './', sourceName = 'NoName', templ = '', z = 0.01, saveRes = True):
	

	"""
    This function plots the results of the fits for data which contain spectral + photometry fluxes.
    ------------
    :param df: data-frame contaning the results of the fits (i.e. optimised parameters) as returned by the function SEDanalysis.runSEDspecFit.
    :param wavSpec: observed wavelengthts for the spectrum (in microns).
    :param fluxSpec: observed fluxes for the spectrum (in Jansky).
    :param efluxSpec: observed uncertainties on the fluxes for the spectrum (in Jansky).
    :param wavPhot: observed wavelengths for the photometry (in microns).
    :param fluxPhot: observed fluxes for the photometry (in Jansky).
    :param efluxPhot: observed uncertainties on the fluxes for the photometry (in Jansky).
    ------------
    :keyword z: redshift of the source. Default = 0.01.
    :keyword UL: vector of length Nphot, where Nphot is the number of photometric data. If any of the values is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
  	:keyword sourceName: name of the source. Default = 'NoName'.
	:keyword pathFig: if saveRes is set to True, the figues showing the results of the fits will be saved at the location pathFig. Default = './'.
	:keyword saveRes: if set to True, the tables containing the results of the fits as well as the figures are saved. Default = True.
	:keyword templ: set the templates that have been used in the fits.
	------------
    :return 0
    """

    # concatenate the spectral and photo fluxes
	flux = np.concatenate([fluxSpec, fluxPhot])

	# define the upper limits if not.
	if len(UL) == 0.:
		UL = np.zeros(len(wavPhot))

	# define the templates to Bernhard+20 if not.
	if len(templ) == 0:
		path = os.path.dirname(iragnsep.__file__)
		templ = pd.read_csv(path+'/iragnsep_templ.csv')

	# Extract the name of the templates
	keys = templ.keys().values
	nameTempl_gal = []
	nameTempl_PAH = []
	for key in keys:
		if str(key).startswith('gal'):
			if str(key).endswith('PAH') == False:
				nameTempl_gal.append(key)
			else:
				nameTempl_PAH.append(key)

	# Test that we have templates for everything (if no galaxy then it crashes)
	if len(nameTempl_gal) == 0:
		raise ValueError('The galaxy template does not exist. The name of the column defining nuLnu for the galaxy template needs to start with "gal".')
	
	# define the wavelengths
	try:
		wavTempl = templ['lambda_mic'].values
	except:
		raise ValueError('Rename the wavelengths column of the template "lambda_mic".')

	# Open 2 figures, 1 for all the possible fits and 1 for the best weighted average model.
	fig1, axs1 = plt.subplots(2,6, sharex = True, sharey = True, figsize = (27, 12))
	fig1.subplots_adjust(hspace = 0.0, wspace=0., left  = 0.06, right = 0.99, bottom = 0.10, top = 0.95)
	axs1 = axs1.ravel()

	fig2, axs2 = plt.subplots(figsize = (11, 8))
	fig2.subplots_adjust(hspace = 0.0, wspace=0., left  = 0.15, right = 0.95, bottom = 0.15, top = 0.95)
	axs2.tick_params(axis='both', labelcolor='k', labelsize = 25, width = 1, size = 15, which = 'major', direction = 'inout')
	axs2.tick_params(axis='both', width = 1, size = 10, which = 'minor', direction = 'inout')

	# Loop on all the possible combinations of models
	count = 0
	for i in range(0, len(df)):
		obj = df.iloc[i]

		# Extract the optimised best parameters and their uncertainties
		normDust = 10**obj['logNormGal_dust']
		nuLnuDust = normDust * templ[obj['tplName']].values
		enuLnuDust = normDust * templ['e'+obj['tplName']].values

		normPAH = 10**obj['logNormGal_PAH']
		nuLnuPAH = normPAH * templ['gal_PAH'].values
		enuLnuPAH = normPAH * templ['egal_PAH'].values

		nuLnuGal = nuLnuDust + nuLnuPAH
		enuLnuGal = np.sqrt(enuLnuDust**2. + enuLnuPAH**2.)

		# Add the exctinction if measured
		_tau9p7 = obj['tau9p7']
		if _tau9p7 != -99.:
			tau = KVTextinctCurve(wavTempl) * _tau9p7
			exctCorr = (1. - np.exp(-tau))/tau
		else:
			exctCorr = 1.

		# Calculate the observed flux, affected by attenuation
		FnuGal = nuLnuToFnu(wavTempl, nuLnuGal, z)*exctCorr
		eFnuGal = nuLnuToFnu(wavTempl, enuLnuGal, z)*exctCorr

		# Define the AGN contribution
		if obj['AGNon'] == 1:
			modelAGN1 = 10**obj['logNorm_Si11'] * Gauss_jit(wavTempl*(1.+z), np.log10(11.*(1.+z)), 0.05)
			modelAGN2 = 10**obj['logNorm_Si18'] * Gauss_jit(wavTempl*(1.+z), np.log10(18.*(1.+z)), 0.07)
			modelAGN3 =  10**obj['logNormAGN_PL'] * AGNmodel_jit(wavTempl*(1.+z), 15.*(1.+z), obj['lBreak_PL']*(1.+z), obj['alpha1_PL'], obj['alpha2_PL'], -3.5)

			FnuAGN = (modelAGN1 + modelAGN2 + modelAGN3)*exctCorr

			FnuTot = FnuGal + FnuAGN
		else:
			FnuTot = FnuGal

		# Figure with all the fits.
		o = np.where(UL < 1.)[0]
		axs1[count].errorbar(wavPhot[o]/(1.+z), fluxPhot[o], yerr = efluxPhot[o], fmt = '.', color = '#292F33', alpha = 1.0, label = 'Observed SED')
		o = np.where(UL > 0.)[0]
		axs1[count].errorbar(wavPhot[o]/(1.+z), fluxPhot[o], yerr = fluxPhot[o]/3., fmt = '.', color = '#292F33', alpha = 1.0, label = '_no_label_', uplims = True)
		axs1[count].errorbar(wavSpec/(1.+z), fluxSpec, yerr = efluxSpec, fmt = '.', color = '#292F33', alpha = 1.0, label = '_no_label_')

		if obj['AGNon'] == 1:
			axs1[count].plot(wavTempl, FnuGal, '--', color = '#66757F', label = 'Galaxy comp. ('+obj['tplName']+')')
			axs1[count].plot(wavTempl, FnuAGN, '-.', color = '#66757F', label = 'AGN comp. (full model)')
			if obj['bestModelFlag'] == 1.:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = '#55ACEE', ecolor = 'k', \
								linewidth = 3, elinewidth=0.5, label = 'Total (AGN + Galaxy)', errorevery = 3)
			else:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = 'k', ecolor = 'k', \
									linewidth = 1, elinewidth=0.5, label = 'Total (AGN + Galaxy)', errorevery = 3)
		else:
			if obj['bestModelFlag'] == 1.:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = '#55ACEE', ecolor = 'k', \
								linewidth = 3, elinewidth=0.5, label = 'Total ('+obj['tplName']+')', errorevery = 3)
			else:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = 'k', ecolor = 'k', \
									linewidth = 1, elinewidth=0.5, label = 'Total ('+obj['tplName']+')', errorevery = 3)


		axs1[count].set_xscale('log')
		axs1[count].set_yscale('log')
		axs1[count].set_xlim([3./(1.+z), 800./(1.+z)])
		axs1[count].set_ylim([min(flux)/10., max(flux)*20.])
		axs1[count].set_xlabel(r'$\lambda_{\rm rest}\ (\mu {\rm m})$', fontsize = 28)
		if (count == 0) or (count == 6):
			axs1[count].set_ylabel(r'Flux (Jy)', fontsize = 28)
		axs1[count].legend(frameon = False, loc = 'upper left', fontsize = 15)
		if round(obj['Aw']*100.) > 50.:
			axs1[count].text(10., min(flux)/6., 'Aw = '+str(round(obj['Aw']*100.))+'%', fontsize = 25, c = '#ff4d4d')
		else:
			axs1[count].text(10., min(flux)/6., 'Aw = '+str(round(obj['Aw']*100.))+'%', fontsize = 25, c = 'k')
		axs1[count].tick_params(axis='both', labelcolor='k', labelsize = 25, width = 1, size = 15, which = 'major', direction = 'inout')
		axs1[count].tick_params(axis='both', width = 1, size = 10, which = 'minor', direction = 'inout')

		count += 1

		# Best model Figure
		if obj['Aw'] > 0.1:
			if obj['AGNon'] == 1:
				axs2.plot(wavTempl, FnuTot, '-', color = 'k', \
						 linewidth = 1, label = obj['tplName']+' + AGN ('+str(round(obj['Aw']*100.))+'%)', alpha = obj['Aw']/2.)				
			else:
				axs2.plot(wavTempl, FnuTot, '-', color = 'k', \
						 linewidth = 1, label = obj['tplName']+' ('+str(round(obj['Aw']*100.))+'%)', alpha = obj['Aw']/2.)

		try:
			FnuTot_Aw += FnuTot * obj['Aw']
			eFnuTot_Aw += (eFnuGal*obj['Aw'])**2.
			FnuGal_Aw += FnuGal * obj['Aw']
			if obj['AGNon'] == 1:
				FnuAGN_Aw += FnuAGN * obj['Aw']
		except:
			FnuTot_Aw = FnuTot * obj['Aw']
			eFnuTot_Aw = (eFnuGal * obj['Aw'])**2.
			FnuGal_Aw = FnuGal * obj['Aw']
			if obj['AGNon'] == 1:
				FnuAGN_Aw = FnuAGN * obj['Aw']
			else:
				FnuAGN_Aw = FnuGal_Aw * 0.

	axs2.errorbar(wavTempl, FnuTot_Aw, yerr = np.sqrt(eFnuTot_Aw), fmt = '-', color = 'k', elinewidth = 0.5, linewidth = 3, label = 'Best weighted fit [Total]',\
			 ecolor = 'k', alpha = 0.4, errorevery = 3)
	axs2.plot(wavTempl, FnuGal_Aw, '--', color = '#E94B3C', \
						 linewidth = 2, label = 'Best weighted fit [Galaxy]', alpha = 0.7)
	axs2.plot(wavTempl, FnuAGN_Aw, '-.', color = '#6395F2', \
						 linewidth = 2, label = 'Best weighted fit [AGN]', alpha = 0.7)

	o = np.where(UL < 1.)[0]
	axs2.errorbar(wavPhot[o]/(1.+z), fluxPhot[o], yerr = efluxPhot[o], fmt = 'o', color = '#292F33', alpha = 0.9, label = 'Observed Photometry', mfc = 'none', mew = 1, ms = 10)

	o = np.where(UL > 0.)[0]
	axs2.errorbar(wavPhot[o]/(1.+z), fluxPhot[o], yerr = fluxPhot[o]/5., fmt = 'o', color = '#292F33', alpha = 0.9, label = '_no_label_', uplims = True, mfc = 'none', mew = 1, ms = 10)

	axs2.errorbar(wavSpec/(1.+z), fluxSpec, yerr = efluxSpec, fmt = '.', color = '#292F33', alpha = 0.9, label = 'Observed Spectrum')

	axs2.set_xscale('log')
	axs2.set_yscale('log')
	axs2.set_xlim([3./(1.+z), 800./(1.+z)])
	axs2.set_ylim([min(flux)/5., max(flux)*10.])
	axs2.set_xlabel(r'$\lambda_{\rm rest}\ (\mu {\rm m})$', FontProperties = font0)
	axs2.set_ylabel(r'Flux (Jy)', FontProperties = font0)
	axs2.legend(frameon = False, fontsize = 16, ncol = 2)

	# If saveRes is True, then save the figures to the location specified in pathFig.
	if saveRes == True:
		fig1.savefig(pathFig+sourceName+'_fitResAll_spec.pdf')
		fig2.savefig(pathFig+sourceName+'_fitResBM_spec.pdf')
	else:
		plt.show()
	plt.close('all')


############################
## Plot all the results for all the possible fit. Tag the best model in blue.
############################
def plotFitPhoto(df, wav, flux, eflux, UL = np.array([]), pathFig = './', sourceName = 'NoName', templ = '', z = 0.01, saveRes = True):
	
	"""
    This function plots the results of the fits for photometric data.
    ------------
    :param df: data-frame contaning the results of the fits (i.e. optimised parameters) as returned by the function SEDanalysis.runSEDphotFit.
    :param wav: observed wavelengthts (in microns).
    :param flux: observed fluxes (in Jansky).
    :param eflux: observed uncertainties on the fluxes (in Jansky).
    ------------
    :keyword z: redshift of the source. Default = 0.01.
    :keyword UL: vector of length Nphot, where Nphot is the number of photometric data. If any of the values is set to 1, the corresponding flux is set has an upper limit in the fit. Default = [].
  	:keyword sourceName: name of the source. Default = 'NoName'.
	:keyword pathFig: if saveRes is set to True, the figues showing the results of the fits will be saved at the location pathFig. Default = './'.
	:keyword saveRes: if set to True, the tables containing the results of the fits as well as the figures are saved. Default = True.
	:keyword templ: set the templates that have been used in the fits.
	------------
    :return 0
    """

    # Open the Bernhard+20 templates if not defined
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
		if str(key).startswith('AGN') == True:
			if str(key).endswith('Siem') == True:
				nameTempl_Siem.append(key)
			else:
				nameTempl_AGN.append(key)

	# Test that we have template for everything (if no galaxy then it crashes)
	if len(nameTempl_gal) == 0:
		raise ValueError('The galaxy template does not exist. The name of the column defining nuLnu for the galaxy template needs to start with "gal".')
	if len(nameTempl_AGN) == 0:
		raise ValueError('The AGN template does not exist. The name of the column defining nuLnu for the AGN template needs to start with "AGN".')

	# define the wavelengths
	try:
		wavTempl = templ['lambda_mic']
	except:
		raise ValueError('Rename the wavelengths column of the template "lambda_mic".')

	# Open 2 figures, 1 for all the possible fits and 1 for the best weighted average model.
	fig1, axs1 = plt.subplots(3,6, sharex = True, sharey = True, figsize = (27, 18))
	fig1.subplots_adjust(hspace = 0.0, wspace=0., left  = 0.06, right = 0.99, bottom = 0.10, top = 0.95)
	axs1 = axs1.ravel()

	fig2, axs2 = plt.subplots(figsize = (11, 8))
	fig2.subplots_adjust(hspace = 0.0, wspace=0., left  = 0.15, right = 0.95, bottom = 0.15, top = 0.95)
	axs2.tick_params(axis='both', labelcolor='k', labelsize = 25, width = 1, size = 15, which = 'major', direction = 'inout')
	axs2.tick_params(axis='both', width = 1, size = 10, which = 'minor', direction = 'inout')

	# Loop over all the model combinations of templates.
	count = 0
	for i in range(0, len(df)):
		obj = df.iloc[i]

		# Exrract the optimised parameters and their uncertainties
		normDust = 10**obj['logNormGal_dust']
		nuLnuDust = normDust * templ[obj['tplName_gal']].values
		enuLnuDust = normDust * templ['e'+obj['tplName_gal']].values

		normPAH = 10**obj['logNormGal_PAH']
		nuLnuPAH = normPAH * templ['gal_PAH'].values
		enuLnuPAH = normPAH * templ['egal_PAH'].values

		nuLnuGal = nuLnuDust + nuLnuPAH
		enuLnuGal = np.sqrt(enuLnuDust**2. + enuLnuPAH**2.)

		# Calculate the observed model fluxes
		FnuGal = nuLnuToFnu(wavTempl, nuLnuGal, z).values
		eFnuGal = nuLnuToFnu(wavTempl, enuLnuGal, z)

		# Define the optimised model AGN template
		if obj['AGNon'] == 1:
			normAGN = 10**obj['logNormAGN']
			nuLnuAGN = normAGN * templ[obj['tplName_AGN']].values
			
			normSi = 10**obj['logNormSiem']
			nuLnuSi = normSi * templ[nameTempl_Siem].values.flatten()
			
			FnuAGN =  nuLnuToFnu(wavTempl, nuLnuAGN + nuLnuSi, z)

			FnuTot = FnuGal + FnuAGN
		else:
			FnuTot = FnuGal

		# Plot with all the possible models.
		o = np.where(UL < 1.)[0]
		axs1[count].errorbar(wav[o]/(1.+z), flux[o], yerr = eflux[o], fmt = '.', color = '#292F33', alpha = 1.0, label = 'Observed SED')
		o = np.where(UL > 0.)[0]
		axs1[count].errorbar(wav[o]/(1.+z), flux[o], yerr = flux[o]/3., fmt = '.', color = '#292F33', alpha = 1.0, label = '_no_label_', uplims = True)

		if obj['AGNon'] == 1:
			axs1[count].plot(wavTempl, FnuGal, '--', color = '#66757F', label = 'Galaxy comp. ('+obj['tplName_gal']+')')
			axs1[count].plot(wavTempl, FnuAGN, '-.', color = '#66757F', label = 'AGN comp. ('+obj['tplName_AGN']+')')
			if obj['bestModelFlag'] == 1.:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = '#55ACEE', ecolor = 'k', \
								linewidth = 3, elinewidth=0.5, label = 'Total (AGN + Galaxy)', errorevery = 3)
			else:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = 'k', ecolor = 'k', \
									linewidth = 1, elinewidth=0.5, label = 'Total (AGN + Galaxy)', errorevery = 3)
		else:
			if obj['bestModelFlag'] == 1.:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = '#55ACEE', ecolor = 'k', \
								linewidth = 3, elinewidth=0.5, label = 'Total ('+obj['tplName_gal']+')', errorevery = 3)
			else:
				axs1[count].errorbar(wavTempl, FnuTot, yerr = eFnuGal, fmt = '-', color = 'k', ecolor = 'k', \
									linewidth = 1, elinewidth=0.5, label = 'Total ('+obj['tplName_gal']+')', errorevery = 3)

		axs1[count].set_xscale('log')
		axs1[count].set_yscale('log')
		axs1[count].set_xlim([3./(1.+z), 800./(1.+z)])
		axs1[count].set_ylim([min(flux)/10., max(flux)*20.])
		axs1[count].set_xlabel(r'$\lambda_{\rm rest}\ (\mu {\rm m})$', fontsize = 28)
		if (count == 0) or (count == 6) or (count == 12):
			axs1[count].set_ylabel(r'Flux (Jy)', fontsize = 28)
		axs1[count].legend(frameon = False, loc = 'upper left', fontsize = 15)
		if round(obj['Aw']*100.) > 50.:
			axs1[count].text(10., min(flux)/6., 'Aw = '+str(round(obj['Aw']*100.))+'%', fontsize = 25, c = '#ff4d4d')
		else:
			axs1[count].text(10., min(flux)/6., 'Aw = '+str(round(obj['Aw']*100.))+'%', fontsize = 25, c = 'k')
		axs1[count].tick_params(axis='both', labelcolor='k', labelsize = 25, width = 1, size = 15, which = 'major', direction = 'inout')
		axs1[count].tick_params(axis='both', width = 1, size = 10, which = 'minor', direction = 'inout')

		count += 1

		# Plots with the best model only.
		if obj['Aw'] > 0.05:
			if obj['AGNon'] == 1:
				axs2.plot(wavTempl, FnuTot, '-', color = 'k', \
						 linewidth = 1, label = obj['tplName_gal']+' + '+ obj['tplName_AGN'] + ' ('+str(round(obj['Aw']*100.))+'%)', alpha = obj['Aw'])
			else:
				axs2.plot(wavTempl, FnuTot, '-', color = 'k', \
						 linewidth = 1, label = obj['tplName_gal']+' ('+str(round(obj['Aw']*100.))+'%)', alpha = obj['Aw'])

		try:
			FnuTot_Aw += FnuTot * obj['Aw']
			eFnuTot_Aw += (eFnuGal.values*obj['Aw'])**2.
			FnuGal_Aw += FnuGal * obj['Aw']
			if obj['AGNon'] == 1:
				FnuAGN_Aw += FnuAGN * obj['Aw']
		except:
			FnuTot_Aw = FnuTot * obj['Aw']
			eFnuTot_Aw = (eFnuGal.values * obj['Aw'])**2.
			FnuGal_Aw = FnuGal * obj['Aw']
			if obj['AGNon'] == 1:
				FnuAGN_Aw = FnuAGN * obj['Aw']
			else:
				FnuAGN_Aw = FnuGal_Aw * 0.

	axs2.errorbar(wavTempl, FnuTot_Aw, yerr = np.sqrt(eFnuTot_Aw), fmt = '-', color = 'k', elinewidth = 0.5, linewidth = 2, label = 'Best weighted fit [Total]',\
				 ecolor = 'k', alpha = 0.4, errorevery = 3)
	axs2.plot(wavTempl, FnuGal_Aw, '--', color = '#E94B3C', \
						 linewidth = 2, label = 'Best weighted fit [Galaxy]', alpha = 0.8)
	axs2.plot(wavTempl, FnuAGN_Aw, '-.', color = '#6395F2', \
						 linewidth = 2, label = 'Best weighted fit [AGN]', alpha = 0.8)

	o = np.where(UL < 1.)[0]
	axs2.errorbar(wav[o]/(1.+z), flux[o], yerr = eflux[o], fmt = 'o', color = '#292F33', alpha = 0.9, label = 'Observed SED', mfc = 'none', mew = 1, ms = 10)

	o = np.where(UL > 0.)[0]
	axs2.errorbar(wav[o]/(1.+z), flux[o], yerr = flux[o]/5., fmt = 'o', color = '#292F33', alpha = 0.9, label = '_no_label_', uplims = True, mfc = 'none', mew = 1, ms = 10)

	axs2.set_xscale('log')
	axs2.set_yscale('log')
	axs2.set_xlim([3./(1.+z), 800./(1.+z)])
	axs2.set_ylim([min(flux)/5., max(flux)*10.])
	axs2.set_xlabel(r'$\lambda_{\rm rest}\ (\mu {\rm m})$', FontProperties = font0)
	axs2.set_ylabel(r'Flux (Jy)', FontProperties = font0)
	axs2.legend(frameon = False, fontsize = 16, ncol = 2)

	# if saveRes is True, save the figures at the locations pathFig.
	if saveRes == True:
		fig1.savefig(pathFig+sourceName+'_fitResAll_photo.pdf')
		fig2.savefig(pathFig+sourceName+'_fitResBM_photo.pdf')
	else:
		plt.show()
	plt.close('all')