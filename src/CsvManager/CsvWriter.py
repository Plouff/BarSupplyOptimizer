"""
@file CsvWriter.py
@brief The output CSV writter

author: Nassim Zga
created: 12 juin 2016
"""

import csv
import logging
import os

class CsvWriter():
	'''
	The CSV writer
	'''


	def __init__(self, outCsvPath, barsLogList):
		'''
		Constructor
		'''
		self.barsLogList = barsLogList
		self.outCsvPath = outCsvPath

	def writeOutputLogCsv(self):
		with open(self.outCsvPath, 'wt') as csvfile:
			writer = csv.writer(csvfile, delimiter=';',
				 quoting=csv.QUOTE_ALL, lineterminator=os.linesep)

			# Write header row
			writer.writerow(["Barre n°", "Barre neuve n°", "Longueur resultante", "Date entree stock", "Date sortie stock", "Stock/Poubelle"])

			# Write data rows
			for bar in self.barsLogList:
				stockPoubelle = None
				if bar.InStockOrInTrash is "Trash":
					stockPoubelle = "Poubelle".strip()
				else:
					stockPoubelle = "Stock".strip()

				writer.writerow([
					bar.index + 1,
					bar.supplierBarIndex,
					bar.length,
					bar.dateIn,
					bar.dateOut,
					stockPoubelle
					])

		logging.debug("Output CSV {} written".format(self.outCsvPath))

		