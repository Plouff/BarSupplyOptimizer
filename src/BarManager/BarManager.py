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
from BarManager.BarLogger import BarLogger

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
		# The bar logger
		self.barLogger = BarLogger(self)

	def GetSupplierLength(self):
		return self.supplierBarLength

	def GetSupplierBarIndex(self):
		return self.supplierBarIndex

	def GetLoggerList(self):
		return self.barLogger.GetBars()
	
	def IncrementSupplierBarIndex(self):
		self.supplierBarIndex = self.supplierBarIndex + 1

	def StockIsEmpty(self):
		return self.barStock.StockIsEmpty()

	def StoreOrTrashCut(self, bar, currentDate):
		"""
		Store or trash a cut

		return a Bar object
		"""
		bar.dateIn = currentDate

		# If the cut is too small => to thrash
		if self.barTrash.CheckIfGoToTrash(bar):
			bar.InStockOrInTrash = "Trash"
			bar.dateOut = currentDate
			self.barTrash.SendBarToTrash(bar)
		else:
			# Else the bar goes in stock
			bar.InStockOrInTrash = "Stock"
			self.barStock.AddCutInBarStock(bar)

	def CutBarFromNewBar(self, currentDate, cutLength):
		logging.debug("Cutting the bar from new supplier bar")

		self.IncrementSupplierBarIndex()
		newCutLength = self.supplierBarLength - cutLength
		cut = Bar(self.supplierBarIndex, newCutLength, currentDate)

		self.StoreOrTrashCut(cut, currentDate)

		return cut

	def CutWithBestFitInStockOrNewBar(self, currentDate, cutLength):
		# Find the smallest bar in stock that can be used
		bestFitCut = self.barStock.FindBestCutFitOrGetNewBar(cutLength, currentDate)

		if bestFitCut.length == self.supplierBarLength:
			# If the best fit bar has the length of a supplier bar => use new bar
			cut = self.CutBarFromNewBar(currentDate, cutLength)
			return [cut]
		else:
			# Else use bar from stock
			bestFitCut.dateOut = currentDate
			cut = Bar.usingExitingBar(bestFitCut, cutLength, currentDate)
			self.StoreOrTrashCut(cut, currentDate)
			return [bestFitCut, cut]

	def ProcessBar(self, currentDate, cutLength):
		bar = None
		if self.StockIsEmpty():
			# If stock is empty use supplier new bar
			bar = self.CutBarFromNewBar(currentDate, cutLength)
			self.barLogger.UpdateWithBar(bar)
		else:
			# If the stock is not empty try to find the best fit bar in the stock
			bars = self.CutWithBestFitInStockOrNewBar(currentDate, cutLength)
			self.barLogger.UpdateWithListOfBars(bars)


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
			stockLength = stockLength + int(bar.length)
		logging.info("{} total stock length ({} bars in stock) ".format(stockLength, stockedBarCount))

		waste = 100 * trashLength / supplierLength
		logging.info("Waste = {} / {} = {:.2f}%".format(trashLength, 
			supplierLength, waste))
