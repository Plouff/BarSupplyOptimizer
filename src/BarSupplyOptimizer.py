#! python3
# -*-coding: utf-8 -*-

"""
@file BarSupplyOptimizer.py
Bar Supply Optimizer

@author Nassim Zga
created 02/06/16
"""

# DO NOT EDIT BELOW

import sys
import logging
import os

loggingLevel = logging.DEBUG
logging.basicConfig(
	format='%(levelname)s: %(message)s',
	#format='%(asctime)s %(levelname)s: %(message)s',
	level=loggingLevel,
	datefmt='%m/%d/%Y %H:%M:%S')

rootLogger = logging.getLogger()

#consoleHandler = logging.StreamHandler()
#rootLogger.addHandler(consoleHandler)

# Custom modules
from BarManager.BarManager import BarManager
from CsvManager.BarCsvReader import BarCsvReader
from CsvManager.CsvWriter import CsvWriter
from ConfigManager.ConfigManager import ConfigManager

def ExitWithError():
	input("Press any key to quit the program")
	sys.exit(1)

def LoadConfiguration(configPath):
	"""
	Load config.ini file
	"""
	try:
		configManager = ConfigManager(configPath)
		barConfig = configManager.ParseConfig()
		return barConfig
	except (KeyboardInterrupt, SystemExit):
		raise
	except IOError:
		logging.exception("Config file BarSupplyOptimizerConfig.ini not found")
		ExitWithError()
	except: # catch all other exceptions
		logging.exception("Couldn't load BarSupplyOptimizerConfig.ini")
		ExitWithError()


def ReadInputCsv(barConfig):
	"""
	Read input CSV
	"""
	try:
		csvReader = BarCsvReader(barConfig.inputCsvFile)
		logging.info("Opening input CSV {}".format(barConfig.inputCsvFile))
		inputDataDic = csvReader.ParseCsv(barConfig.dateCol, barConfig.lengthCol,
			barConfig.barCountCol)
		return inputDataDic
	except (KeyboardInterrupt, SystemExit):
		raise
	except IOError:
		logging.exception("Input CSV file '{}' not found".format(barConfig.inputCsvFile))
		ExitWithError()
	except: # catch all other exceptions
		logging.exception("Couldn't load input CSV check BarSupplyOptimizerConfig.ini")
		ExitWithError()

def RunAnalysis(inputDataDic, toTrashLimit, supplierBarLength):
	"""
	Launch one analysis
	"""
	# Create a bar manager
	barManager = BarManager(toTrashLimit, supplierBarLength)

	# Process input data
	for currentDate in inputDataDic.keys():
		logging.debug("Day {}: {}".format(currentDate, inputDataDic[currentDate]))

		# Loop over bars by date
		for cutLength in inputDataDic[currentDate]:
			logging.debug("Processing [{}, {}]".format(cutLength, currentDate,))
			barManager.ProcessBar(currentDate, cutLength)

		logging.debug("")

	# Compute final results
	barManager.ComputeFinalResults()

	# Print final results
	return barManager


def LaunchSimulation(barConfig, inputDataDic):
	"""
	Launch simulation
	"""
	if not barConfig.optimizerConfig['optimizerEnabled']:
		#
		# Launch one simulation
		#
		try:
			barManager = RunAnalysis(inputDataDic, barConfig.toTrashLimit,
				barConfig.supplierBarLength)
		except: # catch all other exceptions
			logging.exception("Simulation failed (see detail below)")
			ExitWithError()

		# Bar CSV writer
		csvWriter = CsvWriter(barConfig.outputCsv)
		try:
			csvWriter.writeDetailedLogCsv(barManager.GetLoggerList())
		except: # catch all other exceptions
			logging.exception("Failed to write output CSV '{}' (see detail below)".format(
				barConfig.outputCsv))
			ExitWithError()

	else:
		#
		# Launch optimizer mode
		#
		results = []
		for supplierBarLength in range(
				barConfig.optimizerConfig['supplierLengthMin'],
				barConfig.optimizerConfig['supplierLengthMax'],
				barConfig.optimizerConfig['supplierLengthStep']):
			for toTrashLimit in range(
					barConfig.optimizerConfig['toTrashLengthMin'],
					barConfig.optimizerConfig['toTrashLengthMax'],
					barConfig.optimizerConfig['toTrashLengthStep']):
				try:
					barManager = RunAnalysis(inputDataDic, toTrashLimit, supplierBarLength)
				except: # catch all other exceptions
					logging.exception("Simulation failed (see detail below)")
					ExitWithError()
				results.append(barManager.results)

		csvWriter = CsvWriter(barConfig.outputCsv)
		try:
			csvWriter.writeOptimizationCsv(results)
		except PermissionError:
			logging.exception("No permission to write output CSV '{}' (check if the file is readonly or owned by someone else)".format(
				barConfig.outputCsv))
			ExitWithError()
		except: # catch all other exceptions
			logging.exception("Failed to write output CSV '{}' (see detail below)".format(
				barConfig.outputCsv))
			ExitWithError()

"""
Script wrapper
"""
if __name__ == '__main__':
	cutBarCount = 0

	# Config parsing
	barConfig = LoadConfiguration("../BarSupplyOptimizerConfig.ini")
	# LogFile setup
	fileHandler = logging.FileHandler(filename=barConfig.logFile, mode='w')
	rootLogger.addHandler(fileHandler)

	# Logging level
	if barConfig.loggingLevel.lower() == "debug":
		rootLogger.setLevel(logging.DEBUG)
	else:
		rootLogger.setLevel(logging.INFO)

	# Input bar CSV reader
	inputDataDic = ReadInputCsv(barConfig)

	# Simulations
	LaunchSimulation(barConfig, inputDataDic)

	logging.info("---------------------")
	logging.info("Processing successful")
	logging.info("---------------------")
	input("Press any key to quit the program")
	sys.exit(0)