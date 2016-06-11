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

		def __init__(self, supplierBarIndex, dateIn, length):
			'''
			Constructor
			'''
			self.supplierBarIndex = supplierBarIndex
			self.dateIn = dateIn
			self.length = length

		@classmethod
		def usingExitingBar(cls, bar, lengthRequired, currentDate):
			remainingLength = bar.length - lengthRequired
			return cls(bar.supplierBarIndex, currentDate, remainingLength)

		def SetDateOut(self, dateOut):
			self.dateOut = dateOut