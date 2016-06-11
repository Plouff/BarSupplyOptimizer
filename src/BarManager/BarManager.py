"""
@file BarManager.py
@brief The bar manager class

author: Nassim Zga
created: 04/06/16
"""

import logging

from BarManager.Bar import Bar
from BarManager.CutStock import CutStock
from BarManager.CutTrash import CutTrash

class BarManager:
	"""
	The Bar Manager

	It handles the cut of bars using supplier bars or cuts from stock
	"""
	def __init__(self, toThrashLimit, supplierBarLength):
		self.toThrashLimit = toThrashLimit
		self.supplierBarLength = supplierBarLength
		self.supplierBarIndex = 0
		# The stock of bar cuts
		self.cutStock = CutStock(self)
		# The trash of bar cuts
		self.cutTrash = CutTrash(self, toThrashLimit)

	def GetSupplierLength(self):
		return self.supplierBarLength

	def GetSupplierBarIndex(self):
		return self.supplierBarIndex

	def IncrementSupplierBarIndex(self):
		self.supplierBarIndex = self.supplierBarIndex + 1

	def StockIsEmpty(self):
		return self.cutStock.StockIsEmpty()

	def StoreOrTrashCut(self, bar, currentDate):
		# If the cut is too small => to thrash
		if self.cutTrash.CheckIfGoToTrash(bar):
			self.cutTrash.SendCutToTrash(bar, currentDate)
		else:
			# Else the bar goes in stock
			bar.dateIn = currentDate
			self.cutStock.AddCutInStock(bar)

	def CutBarFromNewBar(self, currentDate, cutLength):
		logging.debug("Cutting the bar from new supplier bar")

		self.IncrementSupplierBarIndex()
		newCutLength = self.supplierBarLength - cutLength
		cut = Bar(self.supplierBarIndex, currentDate, newCutLength)

		self.StoreOrTrashCut(cut, currentDate)

	def FindBestFitInStockOrUseNewBar(self, currentDate, cutLength):
		# Find the smallest bar in stock that can be used
		bestFitCut = self.cutStock.FindBestCutFitOrGetNewBar(cutLength, currentDate)

		if bestFitCut.length == self.supplierBarLength:
			# If the best fit bar has the length of a supplier bar => use new bar
			self.CutBarFromNewBar(currentDate, cutLength)
		else:
			# Else use cut from stock
			cut = Bar.usingExitingBar(bestFitCut, cutLength, currentDate)
			self.StoreOrTrashCut(cut, currentDate)

	def PrintFinalResults(self):
		cutLength = 0
		cutCount = 0
		stockCount = 0
		stockLength = 0

		logging.info("---------------------")
		logging.info("--- FINAL RESULTS ---")
		logging.info("---------------------")
		supplierLength = self.supplierBarIndex * self.supplierBarLength
		logging.info("{} total supplier length ({} bars bought)".format(supplierLength,
			self.supplierBarIndex))

		for count, bar in enumerate(self.cutTrash.GetCutsList()):
			cutCount = count
			cutLength = cutLength + int(bar.length)
		logging.info("{} total cut length ({} cuts trashed)".format(cutLength, cutCount))

		logging.info("The stock is:")
		for count, bar in enumerate(self.cutStock.GetCutsList()):
			logging.info("    [{}, {}]".format(bar.length, bar.dateIn))
			stockCount = count
			stockLength = cutLength + int(bar.length)
		logging.info("{} total stock length ({} cuts in stock) ".format(stockLength, stockCount))

		waste = 100 * cutLength / supplierLength
		logging.info("Waste = {} / {} = {:.2f}%".format(cutLength, 
			supplierLength, waste))
