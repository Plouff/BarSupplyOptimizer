"""
@file BarStock.py
@brief Cut Stock module

@author Nassim Zga
created 04/06/16
"""

import logging

from BarManager.Bar import Bar

class BarStock():
	'''
	The stock of bars
	'''

	def __init__(self, barManager):
		'''
		Constructor
		'''
		self.bars = []
		self.manager = barManager

	def GetBarsList(self):
		"""
		Getter for bars
		"""
		return self.bars

	def StockIsEmpty(self):
		if len(self.bars):
			logging.debug("Stock is not empty")
			return False
		else:
			logging.debug("Stock is empty")
			return True

	def AddCutInBarStock(self, bar):
		self.bars.append(bar)
		logging.debug("The cut [{}, {}] was added to the stock".format(bar.length,
			 bar.dateIn))

	def RemoveBarFromStock(self, barIndex):
		bar = self.bars.pop(barIndex)
		logging.debug("Bar [{}, {}] was removed from the stock".format(bar.length,
			 bar.dateIn))

	def FindBestCutFitOrGetNewBar(self, barLengthRequired, currentDate):
		"""
		Find best bar cut that fits or a get new bar

		If a best fit is found the bar is removed from the stock

		@param barLengthRequired The bar length required
		@param currentDate The current date

		@return A bar from the stock or a supplier bar (check the length)
		"""
		bestFitCut = Bar.virtualBar(self.manager.GetSupplierBarIndex(),
			self.manager.GetSupplierLength(), currentDate)
		bestFitIndex = -1

		for barIndex, stockBar in enumerate(self.bars):
			if stockBar.length > barLengthRequired and stockBar.length < bestFitCut.length:
				# The first bar added to the stock is used since the list is created day per day
				bestFitCut = stockBar
				bestFitIndex = barIndex
				logging.debug("For [{}, {}] candidate [{}, {}] was found".format(
					barLengthRequired, currentDate, bestFitCut.length, bestFitCut.dateIn))

		if bestFitCut.length == self.manager.GetSupplierLength():
			# If the best fit bar has the length of a supplier bar => use new bar
			logging.debug("For [{}, {}] no bar was found in stock".format(
				barLengthRequired, currentDate))
		else:
			logging.debug("For [{}, {}] the best fit is [{}, {}]".format(barLengthRequired,
				currentDate, bestFitCut.length, bestFitCut.dateIn))
			# Else remove the bar from the stock and create a new cut
			self.RemoveBarFromStock(bestFitIndex)

		return bestFitCut
