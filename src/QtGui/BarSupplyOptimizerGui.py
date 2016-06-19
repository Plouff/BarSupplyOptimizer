"""
@file BarSupplyOptimizerGui.py
@brief The Qt GUI of the application

@author Nassim Zga
created 18/06/16
"""

import sys
import os
# Import PyQt modules
from PyQt5 import QtWidgets

import design
import helpers

class MainWindow(QtWidgets.QMainWindow, design.Ui_MainWindow):
	"""
	The main window of the GUI
	"""
	def __init__(self, parent=None):
		"""
		Constructor
		
		It calls parent mainWindow setupUi to initialize the window from the .ui
		"""
		super(MainWindow, self).__init__(parent)
		self.setupUi(self)
		self.inputFile = ""
		self.detailedOutDir = ""
		self.optimizationOutDir = ""

		# Connect signal and slots
		self.SignalSlotConnection()

	def SignalSlotConnection(self):
		"""
		Connect signal and slot
		"""
		self.chooseInputFileButton.pressed.connect(self.chooseInputFile)
		self.chooseDetailedOutDirButton.pressed.connect(self.chooseDetailedOutputDir)
		self.chooseOutputDirButton.pressed.connect(self.chooseOptimizationOutputDir)

	def chooseInputFile(self):
		"""
		Opens a QFileDialog to select the input file
		"""
		filters = "Fichier CSV (*.csv);;Fichier texte (*.txt);;Tous les fichiers (*)"
		inputFile = QtWidgets.QFileDialog.getOpenFileName(
			parent=self, caption='CSV d\'entrée', directory='.', filter=filters,
			initialFilter=None, options=QtWidgets.QFileDialog.DontResolveSymlinks)

		# Extract input file
		inputFile = inputFile[0]
		# Update object variable and line edit
		if os.path.isfile(inputFile):
			self.inputFile = inputFile
			self.inputCsvLineEdit.setText(inputFile)


	def chooseDetailedOutputDir(self):
		"""
		Opens a QFileDialog to select the detailed results directory
		"""
		detailedOutDir = QtWidgets.QFileDialog.getExistingDirectory(
			parent=self, caption='Répertoire de résultats détaillés', directory='.',
			options=QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)

		# Update object variable and line edit
		if os.path.isdir(detailedOutDir):
			self.detailedOutDir = detailedOutDir
			self.detailedDirLine.setText(detailedOutDir)

	def chooseOptimizationOutputDir(self):
		"""
		Opens a QFileDialog to select the optimization results directory
		"""
		optimizationOutDir = QtWidgets.QFileDialog.getExistingDirectory(
			parent=self, caption="Répertoire de résultats d'optimization", directory='.',
			options=QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)

		# Update object variable and line edit
		helpers.ValidateDirAndSetLineEdit(self, optimizationOutDir,
			self.detailedOutDir, self.outputDirLineEdit)

def main():
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.show()
	app.exec_()

if __name__ == '__main__':
	main()
