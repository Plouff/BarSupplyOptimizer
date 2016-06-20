from PyQt5 import QtWidgets
import logging

class QPlainTextEditLogger(logging.Handler):
	def __init__(self, parent):
		super().__init__()


class MyDialog(QtWidgets.QDialog, QPlainTextEditLogger):
	def __init__(self, parent=None):
		super().__init__()

if (__name__ == '__main__'):
	app = None
	if (not QtWidgets.QApplication.instance()):
		app = QtWidgets.QApplication([])
	dlg = MyDialog()
	dlg.show()
	dlg.raise_()
	if (app):
		app.exec_()