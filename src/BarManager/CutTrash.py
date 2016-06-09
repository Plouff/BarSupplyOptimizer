"""
@file CuTrash.py
@brief The cut trash

author: Nassim Zga
created: 09/06/16
"""

import logging

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
			self.cuts = []
			self.toThrashLimit = toThrashLimit

		def GetCutsList(self):
			return self.cuts

		def CheckIfGoToTrash(self, newCut, newCutDate):
			"""
			Check if the bar can be reused of need to be trashed
			"""
			# If the cut is too small => to thrash
			if newCut < self.toThrashLimit:
				return True
			else:
				return False

		def SendCutToTrash(self, newCut, newCutDate):
			"""
			Send the bar to the trash
			
			Ie. add the bar to the list of trashed bars
			"""
			self.cuts.append(BarInTrash(newCut, newCutDate))
			logging.debug("The cut [{}, {}] was thrashed".format(newCut,
				 newCutDate))

