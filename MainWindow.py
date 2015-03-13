'''
Arthur Glowacki
APS ANL
3/12/2015
'''
 
import sys
import math
from PyQt4 import QtCore, QtGui
from H5FileWidget import H5FileWidget
 
class MainWindow(QtGui.QMainWindow):
 
	def __init__(self, parent = None):
		QtGui.QMainWindow.__init__(self, parent)
 
		self.frame = QtGui.QFrame()

		self.vl = QtGui.QHBoxLayout()

		self.h5FileWidget = H5FileWidget(self)
		tab_widget = QtGui.QTabWidget()
		tab_widget.addTab(self.h5FileWidget, "HDF5 File")
		#tab_widget.addTab(self.createScanPropsWidget(), "Scan")
		#tab_widget.addTab(self.createVolumePropsWidget(), "Volume")
		self.vl.addWidget(tab_widget)

		self.frame.setLayout(self.vl)
		self.setCentralWidget(self.frame)
 
		self.show()

