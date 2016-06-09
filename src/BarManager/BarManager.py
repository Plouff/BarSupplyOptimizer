"""
@file BarManager.py
@brief The bar manager class

author: Nassim Zga
created: 04/06/16
"""

import logging

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
		self.supplierBarCount = 0
		# The stock of bar cuts
		self.cutStock = CutStock(self)
		# The trash of bar cuts
		self.cutTrash = CutTrash(self, toThrashLimit)

	def GetSupplierLength(self):
		return self.supplierBarLength

	def IncrementSupplierBarCount(self):
		self.supplierBarCount = self.supplierBarCount + 1

	def StockIsEmpty(self):
		return self.cutStock.StockIsEmpty()

	def StoreOrTrashCut(self, newCut, newCutDate):
		# If the cut is too small => to thrash
		if self.cutTrash.CheckIfGoToTrash(newCut, newCutDate):
			self.cutTrash.SendCutToTrash(newCut, newCutDate)
		else:
			# Else the bar goes in stock
			self.cutStock.AddCutInStock(newCut, newCutDate)

	def CutBarFromNewBar(self, newCutDate, cutLength):
		logging.debug("Cutting the bar from new supplier bar")
		self.IncrementSupplierBarCount()
		newCut = self.supplierBarLength - cutLength
		self.StoreOrTrashCut(newCut, newCutDate)

	def FindBestFitInStockOrUseNewBar(self, currentDate, cutLength):
		# Find the smallest bar in stock that can be used
		bestFitCut = self.cutStock.FindBestCutFitOrGetNewBar(cutLength, currentDate)

		if bestFitCut.length == self.supplierBarLength:
			# If the best fit bar has the length of a supplier bar => use new bar
			self.CutBarFromNewBar(currentDate, cutLength)
		else:
			# Else use cut from stock
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
