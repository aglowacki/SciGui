'''
Arthur Glowacki
APS ANL
03/12/2015
'''

import sys
from MainWindow import MainWindow
from PyQt4 import QtCore, QtGui

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

