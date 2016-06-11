"""
@file BarManager.py
@brief The bar manager class

author: Nassim Zga
created: 04/06/16
"""

import logging

from BarManager.Bar import Bar
from BarManager.BarStock import BarStock
from BarManager.BarTrash import BarTrash

class BarManager:
	"""
	The Bar Manager

	It handles the cut of bars using supplier bars or bars from stock
	"""
	def __init__(self, toThrashLimit, supplierBarLength):
		self.toThrashLimit = toThrashLimit
		self.supplierBarLength = supplierBarLength
		self.supplierBarIndex = 0
		# The stock of bar cuts
		self.barStock = BarStock(self)
		# The trash of bar cuts
		self.barTrash = BarTrash(self, toThrashLimit)

	def GetSupplierLength(self):
		return self.supplierBarLength

	def GetSupplierBarIndex(self):
		return self.supplierBarIndex

	def IncrementSupplierBarIndex(self):
		self.supplierBarIndex = self.supplierBarIndex + 1

	def StockIsEmpty(self):
		return self.barStock.StockIsEmpty()

	def StoreOrTrashCut(self, bar, currentDate):
		# If the cut is too small => to thrash
		if self.barTrash.CheckIfGoToTrash(bar):
			self.barTrash.SendBarToTrash(bar, currentDate)
		else:
			# Else the bar goes in stock
			bar.dateIn = currentDate
			self.barStock.AddCutInBarStock(bar)

	def CutBarFromNewBar(self, currentDate, cutLength):
		logging.debug("Cutting the bar from new supplier bar")

		self.IncrementSupplierBarIndex()
		newCutLength = self.supplierBarLength - cutLength
		cut = Bar(self.supplierBarIndex, currentDate, newCutLength)

		self.StoreOrTrashCut(cut, currentDate)

	def FindBestFitInStockOrUseNewBar(self, currentDate, cutLength):
		# Find the smallest bar in stock that can be used
		bestFitCut = self.barStock.FindBestCutFitOrGetNewBar(cutLength, currentDate)

		if bestFitCut.length == self.supplierBarLength:
			# If the best fit bar has the length of a supplier bar => use new bar
			self.CutBarFromNewBar(currentDate, cutLength)
		else:
			# Else use bar from stock
			bestFitCut.SetDateOut(currentDate)
			cut = Bar.usingExitingBar(bestFitCut, cutLength, currentDate)
			self.StoreOrTrashCut(cut, currentDate)

	def PrintFinalResults(self):
		trashLength = 0
		trashedBarCount = 0
		stockedBarCount = 0
		stockLength = 0

		logging.info("---------------------")
		logging.info("--- FINAL RESULTS ---")
		logging.info("---------------------")
		supplierLength = self.supplierBarIndex * self.supplierBarLength
		logging.info("{} total supplier length ({} bars bought)".format(supplierLength,
			self.supplierBarIndex))

		for count, bar in enumerate(self.barTrash.GetBarsList()):
			trashedBarCount = count
			trashLength = trashLength + int(bar.length)
		logging.info("{} total length trashed ({} cuts trashed)".format(trashLength, trashedBarCount))

		logging.info("The stock is:")
		for count, bar in enumerate(self.barStock.GetBarsList()):
			logging.info("    [{}, {}]".format(bar.length, bar.dateIn))
			stockedBarCount = count
			stockLength = trashLength + int(bar.length)
		logging.info("{} total stock length ({} bars in stock) ".format(stockLength, stockedBarCount))

		waste = 100 * trashLength / supplierLength
		logging.info("Waste = {} / {} = {:.2f}%".format(trashLength, 
			supplierLength, waste))
