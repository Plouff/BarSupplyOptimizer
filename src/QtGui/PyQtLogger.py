"""
@file PyQtLogger.py
@brief The PyQtLogger
From https://stackoverflow.com/questions/24469662/how-to-redirect-logger-output-into-pyqt-text-widget

author: Nassim Zga
created: 20 juin 2016
"""

import sys
from PyQt5 import QtCore, QtWidgets
import logging

class QtHandler(logging.Handler):
	def __init__(self):
		logging.Handler.__init__(self)
	def emit(self, record):
		record = self.format(record)
		if record: XStream.stdout().write('%s\n'%record)
		# originally: XStream.stdout().write("{}\n".format(record))


logger = logging.getLogger(__name__)
handler = QtHandler()
handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class XStream(QtCore.QObject):
	_stdout = None
	_stderr = None
	messageWritten = QtCore.pyqtSignal(str)
	def flush( self ):
		pass
	def fileno( self ):
		return -1
	def write( self, msg ):
		if ( not self.signalsBlocked() ):
			# NZ:
			# Was self.messageWritten.emit(msg)
			# But append adds extra \n so we need to remove them
			self.messageWritten.emit(msg.split('\n')[0])

	@staticmethod
	def stdout():
		if ( not XStream._stdout ):
			XStream._stdout = XStream()
			sys.stdout = XStream._stdout
		return XStream._stdout

	@staticmethod
	def stderr():
		if ( not XStream._stderr ):
			XStream._stderr = XStream()
			sys.stderr = XStream._stderr
		return XStream._stderr

class MyDialog(QtWidgets.QDialog):
	def __init__( self, parent = None ):
		super(MyDialog, self).__init__(parent)

		self._console = QtWidgets.QTextBrowser(self)
		self._button  = QtWidgets.QPushButton(self)
		self._button.setText('Test Me')

		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(self._console)
		layout.addWidget(self._button)
		self.setLayout(layout)

		# NZ:
		# Was XStream.stderr().messageWritten.connect( self._console.insertPlainText )
		# But append enables autoscroll to bottom
		XStream.stdout().messageWritten.connect( self._console.append )
		XStream.stderr().messageWritten.connect( self._console.append )

		self._button.clicked.connect(self.test)

	def test( self ):
		logger.debug('debug message')
		logger.info('info message')
		logger.warning('warning message')
		logger.error('error message')
		print('Old school hand made print message')

if ( __name__ == '__main__' ):
	app = None
	if ( not QtWidgets.QApplication.instance() ):
		app = QtWidgets.QApplication([])
	dlg = MyDialog()
	dlg.show()
	if ( app ):
		app.exec_()