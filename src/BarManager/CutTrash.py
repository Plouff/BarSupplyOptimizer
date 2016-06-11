"""
@file CutTrash.py
@brief The cut trash

author: Nassim Zga
created: 09/06/16
"""

import logging

from BarManager.Bar import Bar

class BarInTrash:
	"""
	Helper class for bars in trash
	"""
	def __init__(self, length, toTrashDate):
		self.length = length
		self.toTrashDate = toTrashDate

class CutTrash():
		'''
		The cut trash
		'''

		def __init__(self, manager, toThrashLimit):
			'''
			Constructor
			'''
			self.manager = manager
			self.bars = []
			self.toThrashLimit = toThrashLimit

		def GetCutsList(self):
			return self.bars

		def CheckIfGoToTrash(self, bar):
			"""
			Check if the bar can be reused of need to be trashed
			"""
			# If the cut is too small => to thrash
			if bar.length < self.toThrashLimit:
				return True
			else:
				return False

		def SendCutToTrash(self, bar, currentDate):
			"""
			Send the bar to the trash

			Ie. add the bar to the list of trashed bars
			"""
			bar.SetDateOut(currentDate)
			self.bars.append(bar)
			logging.debug("The cut [{}, {}] was thrashed".format(bar.length, 
				bar.dateIn))

