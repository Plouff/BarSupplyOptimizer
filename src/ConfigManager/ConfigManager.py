"""
@file ConfigManager.py
@brief 

author: Nassim Zga
created: 14 juin 2016
"""

import configparser
import os.path
from builtins import IOError

class BarSupplyOptimizerConfig():
	'''
	Class holding processed data after parsing
	'''

	def __init__(self,
		supplierBarLength,
		toTrashLimit,
		inputCsvFile,
		dateCol,
		lengthCol,
		barCountCol,
		outputCsv,
		optimizerConfig,
		logFile,
		loggingLevel):
		'''
		Constructor
		'''
		self.supplierBarLength = supplierBarLength
		self.toTrashLimit = toTrashLimit
		self.inputCsvFile = inputCsvFile
		self.dateCol = dateCol
		self.lengthCol = lengthCol
		self.barCountCol = barCountCol
		self.outputCsv = outputCsv
		self.optimizerConfig = optimizerConfig
		self.logFile = logFile
		self.loggingLevel = loggingLevel


class ConfigManager():
	'''
	Config.ini file manager
	'''

	def __init__(self, configPath):
		'''
		Constructor
		'''
		self.configPath = configPath
		if not os.path.exists(self.configPath):
			raise FileNotFoundError(self.configPath)

	def ParseConfig(self):
		config = configparser.ConfigParser()
		config.read(self.configPath)

		configDir = os.path.dirname(self.configPath)

		# Configuration
		enableOptimizerMode = config['Configuration']['ActiverModeOptimisation']
		if enableOptimizerMode.lower().strip() == 'vrai':
			modeOptimizerEnabled = True
		else:
			modeOptimizerEnabled = False

		logFile = config['Configuration']['logFile']
		logFile = "{}/{}".format(configDir, logFile)

		# CsvDentrée
		relativeInputCsvPath = config['CsvDentrée']['CheminVersCsvBarresEntrees']
		inputCsvFile = "{}/{}".format(configDir, relativeInputCsvPath)
		dateCol = config['CsvDentrée']['NomColonneDate']
		lengthCol = config['CsvDentrée']['NomColonneLongueur']
		barCountCol = config['CsvDentrée']['NomColonneQuantité']

		# Optimum finder mode
		optimizerConfig = {}
		if modeOptimizerEnabled:
			# ModeRechercheOptimum
			optimizerConfig['optimizerEnabled'] = True
			optimizerConfig['supplierLengthMin'] = int(config['ModeRechercheOptimum']['TailleDesBarresFournisseurMin'])
			optimizerConfig['supplierLengthMax'] = int(config['ModeRechercheOptimum']['TailleDesBarresFournisseurMax']) + 1
			optimizerConfig['supplierLengthStep'] = int(config['ModeRechercheOptimum']['TailleDesBarresFournisseurPas'])
			optimizerConfig['toTrashLengthMin'] = int(config['ModeRechercheOptimum']['TailleMiniPoubelleMin'])
			optimizerConfig['toTrashLengthMax'] = int(config['ModeRechercheOptimum']['TailleMiniPoubelleMax']) + 1
			optimizerConfig['toTrashLengthStep'] = int(config['ModeRechercheOptimum']['TailleMiniPoubellePas'])

			# Following variables are not used
			supplierBarLength = None
			toTrashLimit = None

			# Output file computation
			relativeOutputDir = config['ModeRechercheOptimum']['RépertoireCsvResultatsOptimisation']
			outputDir = "{}/{}".format(configDir, relativeOutputDir)
			outputCsvName = "{}_fournisseur_{}_{}_{}__poubelle_{}_{}_{}.csv".format(
				os.path.splitext(os.path.basename(inputCsvFile))[0],
				optimizerConfig['supplierLengthMin'],
				optimizerConfig['supplierLengthMax'] - 1,
				optimizerConfig['supplierLengthStep'],
				optimizerConfig['toTrashLengthMin'],
				optimizerConfig['toTrashLengthMax'] - 1,
				optimizerConfig['toTrashLengthStep'])
			outputCsv = "{}/{}".format(outputDir, outputCsvName)
		else:
			optimizerConfig['optimizerEnabled'] = False
			# ModeSimulationDétaillée
			supplierBarLength = int(config['ModeSimulationDétaillée']['TailleDesBarresFournisseur'])
			toTrashLimit = int(config['ModeSimulationDétaillée']['TailleMiniPoubelle'])

			# Output file computation
			relativeOutputDir = config['ModeSimulationDétaillée']['RépertoireCsvResultatsDetaillé']
			outputDir = "{}/{}".format(configDir, relativeOutputDir)
			outputCsvName = "{}_{}_{}.csv".format(
				os.path.splitext(os.path.basename(inputCsvFile))[0],
				supplierBarLength,
				toTrashLimit)
			outputCsv = "{}/{}".format(outputDir, outputCsvName)

		# Debug
		loggingLevel = config['Debug']['LoggingLevel']

		barConfig = BarSupplyOptimizerConfig(
			supplierBarLength,
			toTrashLimit,
			inputCsvFile,
			dateCol,
			lengthCol,
			barCountCol,
			outputCsv,
			optimizerConfig,
			logFile,
			loggingLevel)

		return barConfig

