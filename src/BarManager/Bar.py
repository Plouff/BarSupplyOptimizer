"""
@file Bar.py
@brief The bar class

author: Nassim Zga
created: 09/06/16
"""

class Bar():
	'''
	The bar class
	'''
	staticBarIndex = 0

	def __init__(self, supplierBarIndex, length, dateIn, isVirtual=False):
		'''
		Constructor
		'''
		self.dateIn = dateIn
		self.length = length
		self.supplierBarIndex = supplierBarIndex
		self.index = Bar.staticBarIndex
		# Increment static bar index only if the bar is not "virtual"
		if not isVirtual:
			Bar.staticBarIndex = Bar.staticBarIndex + 1
		self.dateOut = None
		self.InStockOrInTrash = None

	@classmethod
	def usingExitingBar(cls, bar, lengthRequired, currentDate):
		remainingLength = bar.length - lengthRequired
		return cls(bar.supplierBarIndex, remainingLength, currentDate)

	@classmethod
	def virtualBar(cls, supplierBarIndex, lengthRequired, currentDate):
		return cls(supplierBarIndex, lengthRequired, currentDate, isVirtual=True)