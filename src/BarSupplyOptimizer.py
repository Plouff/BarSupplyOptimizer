#! python3
# -*-coding: utf-8 -*-

"""
@file BarSupplyOptimizer.py
Bar Supply Optimizer

@author Nassim Zga
created 02/06/16
"""

TAILLE_DES_BARRES_FOURNISSEUR = 7000
TAILLE_ENVOI_POUBELLE = 1000
# User input (in config.ini later)
csvFilePath = "../Longueurs caissons PE.csv"
dateCol = "jour de fab"
lengthCol = "Longueur profils en mm"
barCountCol = "Qté Produite"

# /!\ Les dates doivent être dans l'ordre dans le fichier d'entrée


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

fileHandler = logging.FileHandler(filename="run.log", mode='w')
rootLogger.addHandler(fileHandler)

#consoleHandler = logging.StreamHandler()
#rootLogger.addHandler(consoleHandler)

# Custom modules
from BarManager.BarManager import BarManager
from BarCsvReader.BarCsvReader import BarCsvReader


"""
Script wrapper
"""
if __name__ == '__main__':
	cutBarCount = 0

	# Bar CSV reader
	csvReader = BarCsvReader(csvFilePath)
	inputDic = csvReader.ParseCsv(dateCol, lengthCol, barCountCol)

	# Create a bar manager
	barManager = BarManager(TAILLE_ENVOI_POUBELLE, TAILLE_DES_BARRES_FOURNISSEUR)

	# Process input data
	for currentDate in inputDic.keys():
		logging.debug("Date {}: {}".format(currentDate, inputDic[currentDate]))

		# Loop over bars by date
		for cutLength in inputDic[currentDate]:
			logging.debug("Processing [{}, {}]".format(cutLength, currentDate,))
			if barManager.StockIsEmpty():
				# If stock is empty use supplier new bar
				barManager.CutBarFromNewBar(currentDate, cutLength)
			else:
				# If the stock is not empty try to find the best fit bar in the stock
				barManager.FindBestFitInStockOrUseNewBar(currentDate, cutLength)

		logging.debug("")

	# Print final results
	barManager.PrintFinalResults()


	sys.exit(0)