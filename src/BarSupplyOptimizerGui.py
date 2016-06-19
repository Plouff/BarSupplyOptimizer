"""
@file BarSupplyOptimizerGui.py
@brief The Qt GUI of the application

@author Nassim Zga
created 18/06/16
"""

# Import Python modules
import sys
import os
import logging

# Import PyQt modules
from PyQt5 import QtWidgets

# Import application modules
from QtGui import design
from QtGui import helpers
from QtGui.MenuBarManager import MenuBarManager
import BarSupplyOptimizer
from ConfigManager.ConfigManager import InputFileConfig
from ConfigManager.ConfigManager import DetailedRunConfig
from ConfigManager.ConfigManager import OptimizationRunConfig
from ConfigManager.ConfigManager import BarSupplyOptimizerConfig


logging.basicConfig(
	format='%(levelname)s: %(message)s',
	#format='%(asctime)s %(levelname)s: %(message)s',
	level=logging.INFO,
	datefmt='%m/%d/%Y %H:%M:%S')

rootLogger = logging.getLogger()

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

		# Menu bar manager
		self.menuBarManager = MenuBarManager(self)

		# Connect signal and slots
		self.SignalSlotConnection()

	def SignalSlotConnection(self):
		"""
		Connect signal and slot
		"""
		self.chooseInputFileButton.pressed.connect(self.chooseInputFile)
		self.chooseDetailedOutDirButton.pressed.connect(self.chooseDetailedOutputDir)
		self.chooseOutputDirButton.pressed.connect(self.chooseOptimizationOutputDir)
		self.fileMenu.triggered[QtWidgets.QAction].connect(self.menuBarManager.processFileMenu)
		self.launchButton.pressed.connect(self.LaunchSimulation)

	def chooseInputFile(self):
		"""
		Opens a QFileDialog to select the input file
		"""
		filters = "Fichier CSV (*.csv);;Fichier texte (*.txt);;Tous les fichiers (*)"
		inputFile = QtWidgets.QFileDialog.getOpenFileName(
			parent=self, caption='CSV d\'entrée', directory='..', filter=filters,
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
			parent=self, caption='Répertoire de résultats détaillés', directory='..',
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
			parent=self, caption="Répertoire de résultats d'optimization", directory='..',
			options=QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)

		# Update object variable and line edit
		helpers.ValidateDirAndSetLineEdit(self, optimizationOutDir,
			self.detailedOutDir, self.outputDirLineEdit)

	def GetConfig(self):

		if self.optimizationRadioButton.isChecked():
			modeOptimizerEnabled = True
		else:
			modeOptimizerEnabled = False

		logFile = "runGui.log"

		inputFileConfig = InputFileConfig(
			self.inputCsvLineEdit.text(),
			self.dateColumnLineEdit.text(),
			self.lengthColumnLineEdit.text(),
			self.quantityColumnLineEdit.text())

		optimizationRunConfig = OptimizationRunConfig(
			self.supplierBarLengthMinSpinBox.value(),
			self.supplierBarLengthMaxSpinBox.value(),
			self.supplierBarLengthStepSpinBox.value(),
			self.toTrashMinSpinBox.value(),
			self.toTrashMaxSpinBox.value(),
			self.toTrashStepSpinBox.value(),
			self.outputDirLineEdit.text(),
			self.inputCsvLineEdit.text())

		detailedRunConfig = DetailedRunConfig(
			self.supplierBarLengthSpinBox.value(),
			self.toTrashSpinBox.value(),
			self.detailedDirLine.text(),
			self.inputCsvLineEdit.text())

		# Debug
		loggingLevel = logging.INFO

		barConfig = BarSupplyOptimizerConfig(
			inputFileConfig,
			detailedRunConfig,
			optimizationRunConfig,
			modeOptimizerEnabled,
			logFile,
			loggingLevel)
		
		return barConfig


	def LaunchSimulation(self):
		# Config parsing
		barConfig = self.GetConfig()

		# LogFile setup
		fileHandler = logging.FileHandler(filename=barConfig.logFile, mode='w')
		rootLogger.addHandler(fileHandler)

		# Logging level
		if isinstance(barConfig.loggingLevel, str):
			if barConfig.loggingLevel.lower() == "debug":
				rootLogger.setLevel(logging.DEBUG)
			else:
				rootLogger.setLevel(logging.INFO)
		elif isinstance(barConfig.loggingLevel, int):
			rootLogger.setLevel(barConfig.loggingLevel)
		else:
			rootLogger.setLevel(logging.INFO)

		# Input bar CSV reader
		inputDataDic = BarSupplyOptimizer.ReadInputCsv(barConfig)

		# Simulations
		BarSupplyOptimizer.LaunchSimulation(barConfig, inputDataDic)

def main():
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow()
	mainWindow.show()
	app.exec_()

if __name__ == '__main__':
	main()
