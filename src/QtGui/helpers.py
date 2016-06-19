"""
@file helpers.py
@brief helpers

author: Nassim Zga
created: 19 juin 2016
"""

import os
# Import PyQt modules
from PyQt5 import QtWidgets

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
				"Erreur", "Répertoire incorrect :\n{}".format(filePath),
				QtWidgets.QMessageBox.Ok, parent=parent)
			msgBox.show()