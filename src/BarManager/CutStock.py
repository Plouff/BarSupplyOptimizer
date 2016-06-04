"""
@file CutStock.py
@brief Cut Stock module

@author Nassim Zga
created 04/06/16
"""

import logging

class Cut:
	"""
	Helper class for bars in stock
	"""
	def __init__(self, length, dateIn):
		self.length = length
		self.dateIn = dateIn
		self.dateOut = 0

class CutStock():
		'''
		The stock of cuts
		'''


		def __init__(self):
			'''
			Constructor
			'''
			self.cuts = []

		def StockIsEmpty(self):
			if len(self.cuts):
				logging.debug("Stock is not empty")
				return False
			else:
				logging.debug("Stock is empty")
				return True