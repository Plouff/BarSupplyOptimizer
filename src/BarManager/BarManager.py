"""
@file BarManager.py
@brief The bar manager class

author: Nassim Zga
created: 04/06/16
"""

import logging

from BarManager.CutStock import CutStock

class BarInStock:
	"""
	Helper class for bars in stock
	"""
	def __init__(self, length, dateIn):
		self.length = length
		self.dateIn = dateIn

class BarInTrash:
	"""
	Helper class for bars in trash
	"""
	def __init__(self, length, toTrashDate):
		self.length = length
		self.toTrashDate = toTrashDate


class BarManager:
	"""
	The Bar Manager

	It handles the cut of bars using supplier bars or cuts from stock
	"""
	def __init__(self, toThrashLimit, supplierBarLength):
		self.toThrashLimit = toThrashLimit
		self.supplierBarLength = supplierBarLength
		self.supplierBarCount = 0
		self.cutsToThrash = []
	# The stock of bar cut
		self.stockOfCuts = []
		
		self.cutStock = CutStock()

	def IncrementSupplierBarCount(self):
		self.supplierBarCount = self.supplierBarCount + 1

	def StockIsEmpty(self):
		if len(self.stockOfCuts):
			logging.debug("Stock is not empty")
			return False
		else:
			logging.debug("Stock is empty")
			return True

	def StoreOrTrashCut(self, newCut, newCutDate):
		# If the cut is too small => to thrash
		if newCut < self.toThrashLimit:
			self.cutsToThrash.append(BarInTrash(newCut, newCutDate))
			logging.debug("The cut [{}, {}] was thrashed".format(newCut,
				 newCutDate))
		else:
			# Else the bar goes in stock
			self.stockOfCuts.append(BarInStock(newCut, newCutDate))
			logging.debug("The cut [{}, {}] was added to the stock".format(newCut,
				 newCutDate))

	def CutBarFromNewBar(self, newCutDate, cutLength):
		logging.debug("Cutting the bar from new supplier bar")
		self.IncrementSupplierBarCount()
		newCut = self.supplierBarLength - cutLength
		self.StoreOrTrashCut(newCut, newCutDate)

	def RemoveCutFromStock(self, barIndex):
		bar = self.stockOfCuts.pop(barIndex)
		logging.debug("Bar [{}, {}] was removed from the stock".format(bar.length,
			 bar.dateIn))

	def FindBestFitInStockOrUseNewBar(self, currentDate, cutLength):
		# Initialize the best fit bar to a supplier size one
		bestFitCut = BarInStock(self.supplierBarLength, currentDate)
		bestFitIndex = -1

		# Find the smallest bar in stock that can be used
		for barIndex, stockBar in enumerate(self.stockOfCuts):
			if stockBar.length > cutLength and stockBar.length < bestFitCut.length:
				# The first bar added to the stock is used since the list is created day per day
				bestFitCut = stockBar
				bestFitIndex = barIndex
				logging.debug("For [{}, {}] candidate [{}, {}] was found".format(
					cutLength, currentDate, bestFitCut.length, bestFitCut.dateIn))

		if bestFitCut.length == self.supplierBarLength:
			# If the best fit bar has the length of a supplier bar => use new bar
			self.CutBarFromNewBar(currentDate, cutLength)
			logging.debug("For [{}, {}] no bar was found in stock".format(
				cutLength, currentDate))
		else:
			logging.debug("For [{}, {}] the best fit is [{}, {}]".format(cutLength,
				currentDate, bestFitCut.length, bestFitCut.dateIn))
			# Else remove the bar from the stock and create a new cut
			self.RemoveCutFromStock(bestFitIndex)
			newCut = bestFitCut.length - cutLength
			self.StoreOrTrashCut(newCut, currentDate)

	def PrintFinalResults(self):
		cutLength = 0
		cutCount = 0
		stockCount = 0
		stockLength = 0

		logging.info("---------------------")
		logging.info("--- FINAL RESULTS ---")
		logging.info("---------------------")
		supplierLength = self.supplierBarCount * self.supplierBarLength
		logging.info("{} total supplier length ({} bars bought)".format(supplierLength,
			self.supplierBarCount))

		for count, bar in enumerate(self.cutsToThrash):
			cutCount = count
			cutLength = cutLength + int(bar.length)
		logging.info("{} total cut length ({} cuts trashed)".format(cutLength, cutCount))

		logging.info("The stock is:")
		for count, bar in enumerate(self.stockOfCuts):
			logging.info("    [{}, {}]".format(bar.length, bar.dateIn))
			stockCount = count
			stockLength = cutLength + int(bar.length)
		logging.info("{} total stock length ({} cuts in stock) ".format(stockLength, stockCount))

		waste = 100 * cutLength / supplierLength
		logging.info("Waste = {} / {} = {:.2f}%".format(cutLength, 
			supplierLength, waste))
