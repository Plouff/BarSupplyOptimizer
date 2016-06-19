"""
@file ConfigManager.py
@brief 

author: Nassim Zga
created: 14 juin 2016
"""

import configparser
import os.path

class InputFileConfig():
	"""
	Input file configuration
	"""
	def __init__(self, inputFile, dateCol, lengthCol, barCountCol):
		self.inputFile = inputFile
		self.dateCol = dateCol
		self.lengthCol = lengthCol
		self.barCountCol = barCountCol

class DetailedRunConfig():
	"""
	The detailed run configuration
	"""
	def __init__(self, supplierBarLength, toTrashLimit, outputDir, inputCsvFile):
		self.supplierBarLength = supplierBarLength
		self.toTrashLimit = toTrashLimit
		self.outputDir = outputDir.strip()
		self.outputCsvName = "{}_{}_{}.csv".format(
			os.path.splitext(os.path.basename(inputCsvFile))[0],
			supplierBarLength, toTrashLimit)
		# To avoid looking from /
		if outputDir == "":
			outputDir = '.'
		self.outputCsv = "{}/{}".format(outputDir, self.outputCsvName)

class OptimizationRunConfig():
	"""
	The optimum finder run configuration
	"""
	def __init__(self,
		supplierBarLengthMin, supplierBarLengthMax, supplierBarLengthStep,
		toTrashLimitMin, toTrashLimitMax, toTrashLimitStep,
		outputDir, inputCsvFile):
		self.supplierBarLengthMin = supplierBarLengthMin
		self.supplierBarLengthMax = supplierBarLengthMax
		self.supplierBarLengthStep = supplierBarLengthStep
		self.toTrashLimitMin = toTrashLimitMin
		self.toTrashLimitMax = toTrashLimitMax
		self.toTrashLimitStep = toTrashLimitStep
		self.outputDir = outputDir.strip()
		self.outputCsvName = "{}_fournisseur_{}_{}_{}__poubelle_{}_{}_{}.csv".format(
			os.path.splitext(os.path.basename(inputCsvFile))[0],
			supplierBarLengthMin, supplierBarLengthMax, supplierBarLengthStep,
			toTrashLimitMin, toTrashLimitMax, toTrashLimitStep)

		# To avoid looking from /
		if outputDir == "":
			outputDir = '.'
		self.outputCsv = "{}/{}".format(outputDir, self.outputCsvName)


class BarSupplyOptimizerConfig():
	'''
	Class holding processed data after parsing
	'''

	def __init__(self,
		inputFileConfig,
		detailedRunConfig,
		optimizationRunConfig,
		optimizationEnabled,
		logFile,
		loggingLevel):
		'''
		Constructor
		'''
		self.inputFileConfig = inputFileConfig
		self.detailedRunConfig = detailedRunConfig
		self.optimizationRunConfig = optimizationRunConfig
		self.optimizationEnabled = optimizationEnabled
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
		# To avoid looking from /
		if configDir == "":
			configDir = '.'
		logFile = "{}/{}".format(configDir, logFile)

		#
		# CsvDentrée
		#
		relativeInputCsvPath = config['CsvDentrée']['CheminVersCsvBarresEntrees']
		inputCsvFile = "{}/{}".format(configDir, relativeInputCsvPath)
		dateCol = config['CsvDentrée']['NomColonneDate']
		lengthCol = config['CsvDentrée']['NomColonneLongueur']
		barCountCol = config['CsvDentrée']['NomColonneQuantité']
		inputFileConfig = InputFileConfig(inputCsvFile, dateCol, lengthCol, barCountCol)

		#
		# Optimum finder mode
		#
		optimizerConfig = {}
		optimizerConfig['supplierLengthMin'] = int(config['ModeRechercheOptimum']['TailleDesBarresFournisseurMin'])
		optimizerConfig['supplierLengthMax'] = int(config['ModeRechercheOptimum']['TailleDesBarresFournisseurMax'])
		optimizerConfig['supplierLengthStep'] = int(config['ModeRechercheOptimum']['TailleDesBarresFournisseurPas'])
		optimizerConfig['toTrashLengthMin'] = int(config['ModeRechercheOptimum']['TailleMiniPoubelleMin'])
		optimizerConfig['toTrashLengthMax'] = int(config['ModeRechercheOptimum']['TailleMiniPoubelleMax'])
		optimizerConfig['toTrashLengthStep'] = int(config['ModeRechercheOptimum']['TailleMiniPoubellePas'])

		# Output dir computation
		relativeOutputDir = config['ModeRechercheOptimum']['RépertoireCsvResultatsOptimisation']
		outputDir = "{}/{}".format(configDir, relativeOutputDir)

		optimizationRunConfig = OptimizationRunConfig(
			optimizerConfig['supplierLengthMin'],
			optimizerConfig['supplierLengthMax'],
			optimizerConfig['supplierLengthStep'],
			optimizerConfig['toTrashLengthMin'],
			optimizerConfig['toTrashLengthMax'],
			optimizerConfig['toTrashLengthStep'],
			outputDir,
			inputCsvFile)

		#
		# ModeSimulationDétaillée
		#
		supplierBarLength = int(config['ModeSimulationDétaillée']['TailleDesBarresFournisseur'])
		toTrashLimit = int(config['ModeSimulationDétaillée']['TailleMiniPoubelle'])

		# Output dir computation
		relativeOutputDir = config['ModeSimulationDétaillée']['RépertoireCsvResultatsDetaillé']
		outputDir = "{}/{}".format(configDir, relativeOutputDir)

		detailedRunConfig = DetailedRunConfig(supplierBarLength, toTrashLimit,
			outputDir, inputCsvFile)

		# Debug
		loggingLevel = config['Debug']['LoggingLevel']

		barConfig = BarSupplyOptimizerConfig(
			inputFileConfig,
			detailedRunConfig,
			optimizationRunConfig,
			modeOptimizerEnabled,
			logFile,
			loggingLevel)

		return barConfig

