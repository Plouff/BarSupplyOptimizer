"""
@file MenuBarManager.py
@brief The menu bar manager

author: Nassim Zga
created: 19 juin 2016
"""

# Import PyQt modules
from PyQt5 import QtWidgets, QtCore
from QtGui import helpers

configIniFile="BarSupplyOptimizerGui.ini"

class MenuBarManager():
	'''
	The menu bar manager
	'''

	def __init__(self, parent):
		'''
		Constructor
		'''
		self.parent = parent
		# GUI settings persistence
		self.settings = self.GetNewSettings(configIniFile)

	def processFileMenu(self, action):
		if action == self.parent.openSettingsAction:
			self.OpenSettings()

		if action == self.parent.saveSettingsAction:
			self.SaveSettings()

	def GetNewSettings(self, settingsPath):
		settings = QtCore.QSettings(settingsPath, QtCore.QSettings.IniFormat, self.parent)
		settings.setFallbacksEnabled(False)
		return settings

	def OpenSettings(self):
		"""
		Open a QFileDialog to save the settings
		"""
		# Open QFileDialog to get .ini path
		settingsPath = QtWidgets.QFileDialog.getOpenFileName(
			parent=self.parent, caption='Chargement de la configuration',
			directory='.', filter='Fichier de configuration (*.ini)')
		settingsPath = settingsPath[0]

		# Write only the user selected a file
		if settingsPath:
			# Validate path
			(settingsPath, error) = helpers.GetValidatedFilePathForRead(self.parent, settingsPath)
			if not error:
				# Read and apply config
				self.settings = self.GetNewSettings(settingsPath)
				self.ApplyGuiSettings()

	def SaveSettings(self):
		"""
		Open a QFileDialog to save the settings
		"""
		# Open QFileDialog to get .ini path
		settingsPath = QtWidgets.QFileDialog.getSaveFileName(
			parent=self.parent, caption='Sauvergarde de la configuration',
			directory='.', filter='Fichier de configuration (*.ini)')
		settingsPath = settingsPath[0]

		# Write only the user selected a file
		if settingsPath:
			# Validate path
			(settingsPath, error) = helpers.GetValidatedFilePathForSave(self.parent, settingsPath)
			if not error:
				# Create and write config
				self.settings = self.GetNewSettings(settingsPath)
				self.WriteSettings()


	def ApplyGuiSettings(self):
		self.settings.beginGroup("inputFileGroup")
		self.parent.inputCsvLineEdit.setText(self.settings.value("inputCsvLineEdit"))
		self.parent.nameColumnLineEdit.setText(self.settings.value("nameColumnLineEdit"))
		self.parent.lengthColumnLineEdit.setText(self.settings.value("lengthColumnLineEdit"))
		self.parent.quantityColumnLineEdit.setText(self.settings.value("quantityColumnLineEdit"))
		self.settings.endGroup()

		self.settings.beginGroup("optimizationGroup")
		helpers.SetIntToWidgetFromSettings(self.parent.supplierBarLengthMinSpinBox,
			self.settings, "supplierBarLengthMinSpinBox")
		helpers.SetIntToWidgetFromSettings(self.parent.supplierBarLengthMaxSpinBox,
			self.settings, "supplierBarLengthMaxSpinBox")
		helpers.SetIntToWidgetFromSettings(self.parent.supplierBarLengthStepSpinBox,
			self.settings, "supplierBarLengthStepSpinBox")
		helpers.SetIntToWidgetFromSettings(self.parent.toTrashMinSpinBox,
			self.settings, "toTrashMinSpinBox")
		helpers.SetIntToWidgetFromSettings(self.parent.toTrashMaxSpinBox,
			self.settings, "toTrashMaxSpinBox")
		helpers.SetIntToWidgetFromSettings(self.parent.toTrashStepSpinBox,
			self.settings, "toTrashStepSpinBox")
		helpers.SetStringToWidgetFromSettings(self.parent.outputDirLineEdit,
			self.settings, "outputDirLineEdit")
		self.settings.endGroup()

		self.settings.beginGroup("detailedSimGroup")
		helpers.SetIntToWidgetFromSettings(self.parent.supplierBarLengthSpinBox,
			self.settings, "supplierBarLengthSpinBox")
		helpers.SetIntToWidgetFromSettings(self.parent.toTrashSpinBox,
			self.settings, "toTrashSpinBox")
		helpers.SetStringToWidgetFromSettings(self.parent.detailedDirLine,
			self.settings, "detailedDirLine")
		self.settings.endGroup()

	def WriteSettings(self):
		self.settings.beginGroup("inputFileGroup")
		self.settings.setValue("inputCsvLineEdit", self.parent.inputCsvLineEdit.text())
		self.settings.setValue("nameColumnLineEdit", self.parent.nameColumnLineEdit.text())
		self.settings.setValue("lengthColumnLineEdit", self.parent.lengthColumnLineEdit.text())
		self.settings.setValue("quantityColumnLineEdit", self.parent.quantityColumnLineEdit.text())
		self.settings.endGroup()

		self.settings.beginGroup("optimizationGroup")
		self.settings.setValue("supplierBarLengthMinSpinBox", self.parent.supplierBarLengthMinSpinBox.value())
		self.settings.setValue("supplierBarLengthMaxSpinBox", self.parent.supplierBarLengthMaxSpinBox.value())
		self.settings.setValue("supplierBarLengthStepSpinBox", self.parent.supplierBarLengthStepSpinBox.value())
		self.settings.setValue("toTrashMinSpinBox", self.parent.toTrashMinSpinBox.value())
		self.settings.setValue("toTrashMaxSpinBox", self.parent.toTrashMaxSpinBox.value())
		self.settings.setValue("toTrashStepSpinBox", self.parent.toTrashStepSpinBox.value())
		self.settings.setValue("outputDirLineEdit", self.parent.outputDirLineEdit.text())
		self.settings.endGroup()

		self.settings.beginGroup("detailedSimGroup")
		self.settings.setValue("supplierBarLengthSpinBox", self.parent.supplierBarLengthSpinBox.value())
		self.settings.setValue("toTrashSpinBox", self.parent.toTrashSpinBox.value())
		self.settings.setValue("detailedDirLine", self.parent.detailedDirLine.text())
		self.settings.endGroup()
