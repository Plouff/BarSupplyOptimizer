"""
@file helpers.py
@brief helpers

author: Nassim Zga
created: 19 juin 2016
"""

import os
# Import PyQt modules
from PyQt5 import QtWidgets
from email._header_value_parser import ValueTerminal

def ValidateDirAndSetLineEdit(parent, dirPath, storageVariable, lineEdit):
	if dirPath:
		if os.path.isdir(dirPath):
			storageVariable = dirPath
			lineEdit.setText(dirPath)
		else:
			msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
				"Erreur", "Répertoire incorrect :\n{}".format(dirPath),
				QtWidgets.QMessageBox.Ok, parent=parent)
			msgBox.show()

def ValidateFileAndSetLineEdit(parent, filePath, storageVariable, lineEdit):
	if filePath:
		if os.path.isfile(filePath):
			storageVariable = filePath
			lineEdit.setText(filePath)
		else:
			msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
				"Erreur", "Fichier incorrect :\n{}".format(filePath),
				QtWidgets.QMessageBox.Ok, parent=parent)
			msgBox.show()

def GetValidatedFilePathForSave(parent, filePath):
	"""
	Check if file can be written

	@return A tuple (filePath, error) as (str, bool)
	"""
	storageVariable = ""
	error = True
	if filePath:
		if os.path.exists(filePath):
			if os.access(filePath, os.W_OK):
				storageVariable = filePath
				error = False
		else:
			dirname = os.path.dirname(filePath)
			if os.access(dirname, os.W_OK):
				storageVariable = filePath
				error = False

		if not storageVariable:
			msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
				"Erreur", "Impossible d'écrire :\n{}".format(filePath),
				QtWidgets.QMessageBox.Ok, parent=parent)
			msgBox.show()

	return (storageVariable, error)

def GetValidatedFilePathForRead(parent, filePath):
	"""
	Check if file can be written
	
	@return A tuple (filePath, error) as (str, bool)
	"""
	storageVariable = ""
	error = True
	if filePath:
		if os.path.exists(filePath):
			if os.access(filePath, os.R_OK):
				storageVariable = filePath
				error = False
		else:
			dirname = os.path.dirname(filePath)
			if os.access(dirname, os.R_OK):
				storageVariable = filePath
				error = False

		if not storageVariable:
			msgBox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Critical,
				"Erreur", "Impossible de lire :\n{}".format(filePath),
				QtWidgets.QMessageBox.Ok, parent=parent)
			msgBox.show()

	return (storageVariable, error)


def SetIntToWidgetFromSettings(widget, settings, key):
	"""
	Set int value to a widget
	
	@attention: This function assumes the section is opened:
	self.settings.beginGroup("currentGroup")
	"""
	value = settings.value(key)
	if value:
		widget.setValue(int(value))
	else:
		widget.setValue(0)

def SetStringToWidgetFromSettings(widget, settings, key):
	"""
	Set int value to a widget
	
	@attention: This function assumes the section is opened:
	self.settings.beginGroup("currentGroup")
	"""
	value = settings.value(key)
	if value:
		widget.setText(value)
	else:
		widget.setText("")