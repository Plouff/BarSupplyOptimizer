"""
@file CsvManager.py
@brief The bar CSV file reader module

@author Nassim Zga
created 04/06/16
"""

import csv
import logging
from collections import OrderedDict

class BarCsvReader():
		'''
		The reader for bar CSV files
		'''


		def __init__(self, csvPath):
			'''
			Constructor
			'''
			self.csvPath = csvPath
			self.cutBarCount = 0

		def ParseCsv(self, dateCol, lengthCol, barCountCol):
			'''
			The bar CSV parser

			@return inputDic An OrderedDict of {length1, ..., lengthN} indexed by date
			'''
			inputDic = OrderedDict()

			with open(self.csvPath, newline='') as csvfile:
				reader = csv.DictReader(csvfile, dialect='excel', delimiter=';')
				for row in reader:
					# If currentDate is empty create empty list
					if row[dateCol] not in inputDic.keys():
						inputDic[row[dateCol]] = []

					# Use the quantity column to add N time the current length
					for barCount in range(int(row[barCountCol])):
						inputDic[row[dateCol]].append(int(row[lengthCol]))
						# Increment bar count
						self.cutBarCount = self.cutBarCount + 1

					logging.debug("Found {} bar(s) of length {} for currentDate {}".format(
						row[barCountCol], row[lengthCol], row[dateCol]))


			logging.debug("Found {} bars".format(self.cutBarCount))

			return inputDic