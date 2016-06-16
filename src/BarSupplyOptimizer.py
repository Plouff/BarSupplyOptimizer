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


def LaunchSimulation(inputDic, toTrashLimit, supplierBarLength):
	# Create a bar manager
	barManager = BarManager(toTrashLimit, supplierBarLength)

	# Process input data
	for currentDate in inputDic.keys():
		logging.debug("Day {}: {}".format(currentDate, inputDic[currentDate]))

		# Loop over bars by date
		for cutLength in inputDic[currentDate]:
			logging.debug("Processing [{}, {}]".format(cutLength, currentDate,))
			barManager.ProcessBar(currentDate, cutLength)

		logging.debug("")

	# Compute final results
	barManager.ComputeFinalResults()

	# Print final results
	return barManager

"""
Script wrapper
"""
if __name__ == '__main__':
	cutBarCount = 0

	# Config parsing
	configManager = ConfigManager("../BarSupplyOptimizerConfig.ini")
	barConfig = configManager.ParseConfig()

	supplierBarLength = barConfig.supplierBarLength
	toTrashLimit = barConfig.toTrashLimit
	inputCsvPath = barConfig.inputCsvFile
	outputCsvPath = barConfig.outputCsv
	dateCol = barConfig.dateCol
	lengthCol = barConfig.lengthCol
	barCountCol = barConfig.barCountCol
	optimizerConfig = barConfig.optimizerConfig

	# LogFile setup
	fileHandler = logging.FileHandler(filename=barConfig.logFile, mode='w')
	rootLogger.addHandler(fileHandler)

	if barConfig.loggingLevel.lower() == "debug":
		rootLogger.setLevel(logging.DEBUG)
	else:
		rootLogger.setLevel(logging.INFO)

	# Input bar CSV reader
	logging.info("Opening input CSV {}".format(inputCsvPath))
	csvReader = BarCsvReader(inputCsvPath)
	inputDic = csvReader.ParseCsv(dateCol, lengthCol, barCountCol)

	if not optimizerConfig['optimizerEnabled']:
		#
		# Launch one simulation
		#
		barManager = LaunchSimulation(inputDic, toTrashLimit, supplierBarLength)
		# Bar CSV writer
		csvWriter = CsvWriter(outputCsvPath)
		csvWriter.writeDetailedLogCsv(barManager.GetLoggerList())
	else:
		#
		# Launch optimizer mode
		#
		results = []
		for supplierBarLength in range(
				optimizerConfig['supplierLengthMin'],
				optimizerConfig['supplierLengthMax'],
				optimizerConfig['supplierLengthStep']):
			for toTrashLimit in range(
					optimizerConfig['toTrashLengthMin'],
					optimizerConfig['toTrashLengthMax'],
					optimizerConfig['toTrashLengthStep']):
				barManager = LaunchSimulation(inputDic, toTrashLimit, supplierBarLength)
				results.append(barManager.results)

		csvWriter = CsvWriter(outputCsvPath)
		csvWriter.writeOptimizationCsv(results)


	sys.exit(0)