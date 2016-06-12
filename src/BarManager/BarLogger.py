"""
@file D:/Developpements/Eclipse_Workspaces/BarSupplyOptimizer/src/BarManager/BarLogger.py
@brief 

author: Nassim Zga
created: 12 juin 2016
"""

class BarLogger():
	'''
	Bar logger class
	'''


	def __init__(self, manager):
		'''
		Constructor
		'''
		self.manager = manager
		self.bars = []

	def UpdateWithBar(self, bar):
		if bar.index >= len(self.bars):
			self.bars.append(bar)

	def UpdateWithListOfBars(self, bars):
		for bar in bars:
			self.UpdateWithBar(bar)

	def GetBars(self):
		return self.bars