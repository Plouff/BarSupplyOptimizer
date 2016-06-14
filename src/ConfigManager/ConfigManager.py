"""
@file ConfigManager.py
@brief 

author: Nassim Zga
created: 14 juin 2016
"""

import configparser
import os.path

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

	def ParseConfig(self):
		config = configparser.ConfigParser()
		config.read(self.configPath)

		configDir = os.path.dirname(self.configPath)

		# ConfigDesBarres
		supplierBarLength = int(config['ConfigDesBarres']['TailleDesBarresFournisseur'])
		toTrashLimit = int(config['ConfigDesBarres']['TailleMiniPoubelle'])

		# CsvDentrée
		relativeInputCsvPath = config['CsvDentrée']['CheminVersCsvBarresEntrees']
		inputCsvFile = "{}/{}".format(configDir, relativeInputCsvPath)
		dateCol = config['CsvDentrée']['NomColonneDate']
		lengthCol = config['CsvDentrée']['NomColonneLongueur']
		barCountCol = config['CsvDentrée']['NomColonneQuantité']

		# CsvDetailléDeSortie
		relativeOutputDir = config['CsvDetailléDeSortie']['RépertoireCsvResultatsDetaillé']
		configDir = os.path.dirname(self.configPath)
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
			loggingLevel)

		return barConfig

