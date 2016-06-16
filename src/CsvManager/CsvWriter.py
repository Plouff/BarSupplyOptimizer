# -*-coding: utf-8 -*-
"""
@file CsvWriter.py
@brief The output CSV writter

author: Nassim Zga
created: 12 juin 2016
"""

import csv
import logging
import os
import errno

class CsvWriter():
	'''
	The CSV writer
	'''


	def __init__(self, outCsvPath):
		'''
		Constructor
		'''
		self.outCsvPath = outCsvPath

	def createOutputDir(self):
		if not os.path.exists(os.path.dirname(self.outCsvPath)):
			try:
				os.makedirs(os.path.dirname(self.outCsvPath))
			except OSError as exc: # Guard against race condition
				if exc.errno != errno.EEXIST:
					raise

	def writeDetailedLogCsv(self, barsLogList):
		self.createOutputDir()

		with open(self.outCsvPath, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)

			# Write header row
			writer.writerow(["Barre n°", "Barre neuve n°", "Longueur resultante",
				"Date entree stock", "Date sortie stock", "Stock/Poubelle"])

			# Write data rows
			for bar in barsLogList:
				stockPoubelle = None
				if bar.InStockOrInTrash is "Trash":
					stockPoubelle = u"Poubelle"
				else:
					stockPoubelle = u"Stock"

				if bar.dateIn:
					bar.dateIn = bar.dateIn.replace(".", "/")

				if bar.dateOut:
					bar.dateOut = bar.dateOut.replace(".", "/")

				writer.writerow([
					bar.index + 1,
					bar.supplierBarIndex,
					bar.length,
					bar.dateIn,
					bar.dateOut,
					stockPoubelle
					])

		logging.info("Output CSV {} written".format(self.outCsvPath))


	def writeOptimizationCsv(self, results):
		self.createOutputDir()

		with open(self.outCsvPath, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_ALL)

			# Write header row
			writer.writerow(["Longueur barre neuve", "Limite poubelle",
				"Nb barres achetées", "Longueur de barres achetées",
				"Nb barres jetées", "Longueur jetée", "% jeté",
				"Nb barres en stock", "Longueur du stock", "Stock max (nb barres)"])
			# Write data rows
			for res in results:
				writer.writerow([
				res.supplierBarLength,
				res.toTrashLimit,
				res.supplierBarsBought,
				res.supplierLengthBought,
				res.trashCount,
				res.trashLength,
				res.wastePercentage,
				res.stockCount,
				res.stockLength,
				res.maxBarInStock
				])
		logging.info("Output CSV {} written".format(self.outCsvPath))
