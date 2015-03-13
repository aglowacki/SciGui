'''
Arthur Glowacki
APS ANL
3/12/2015
'''
 
from PyQt4 import QtCore, QtGui
import h5py
import time

class H5FileWidget(QtGui.QWidget):
 
	def __init__(self, parent = None):
		QtGui.QWidget.__init__(self, parent)
 
		self.mutex = QtCore.QMutex()

		self.hFile = None
		self.dataLayout = []

		self.layout = self.createLayout()
		self.setLayout(self.layout)

	def createLayout(self):
		self.treeView = QtGui.QTreeView()
		self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.treeView.customContextMenuRequested.connect(self.openMenu)

		self.model = QtGui.QStandardItemModel()
		self.treeView.setModel(self.model)

		self.model.setHorizontalHeaderLabels([self.tr("File:")])

		self.btnLoadFile = QtGui.QPushButton('Load HDF')
		self.btnLoadFile.clicked.connect(self.onLoadFile)

		self.loadProgressBar = QtGui.QProgressBar(self)
		self.loadProgressBar.setRange(0,100)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.btnLoadFile)
		layout.addWidget(self.treeView)
		layout.addWidget(self.loadProgressBar)
		return layout

	def addItems(self, parent, elements):
		#print 'p',parent,': e',elements
		for text, children in elements:
			#print 't',text,': c',children
			item = QtGui.QStandardItem(text)
			parent.appendRow(item)
			if children:
				self.addItems(item, children)

	def openMenu(self, position): 
		indexes = self.treeView.selectedIndexes()
		if len(indexes) > 0:
			level = 0
			index = indexes[0]
			while index.parent().isValid():
				index = index.parent()
				level += 1

		menu = QtGui.QMenu()
		if level == 0:
			menu.addAction(self.tr("Edit person"))
		elif level == 1:
			menu.addAction(self.tr("Edit object/container"))
		elif level == 2:
			menu.addAction(self.tr("Edit object"))

		menu.exec_(self.treeView.viewport().mapToGlobal(position))

	def clearFileTree(self):
		print 'TODO:'

	def onLoadProgress(self, i):
		self.loadProgressBar.setValue(i)

	def onFinishLoad(self):
		self.btnLoadFile.setEnabled(True)
		#self.fileTree.setEnabled(True)
		print 'Finished loading file'

	def onLoadFile(self):
		#self.startLoadTime = time.time()
		#self.btnLoadFile.setEnabled(False)
		#self.fileTree.setEnabled(False)
		#self.clearFileTree()
		self.loadProgressBar.setValue(0)

		self.hFileName = QtGui.QFileDialog.getOpenFileName(self, 'Open file', '', 'HDF5 (*.h5)')
		print 'Opening',self.hFileName
		self.runLoadFile()

	def runLoadFile(self):
		try:
			print 'opening file',self.hFileName
			self.hFile = h5py.File(str(self.hFileName), 'r')
			self.model.setHorizontalHeaderLabels([self.tr("File:"+str(self.hFileName))])
			self.dataLayout = self.loadGroups(self.hFile)
			#print 'dataLayout = ',self.dataLayout
			self.addItems(self.model, self.dataLayout)
		except:
			print 'Error loading file',self.hFileName

		#data = [  ("Alice", [  ("Keys", []),  ("Purse", [  ("Cellphone", [])   ])   ]),  ("Bob", [  ("Wallet", [  ("Credit card", []), ("Money", [])  ])  ])   ]
	def loadGroups(self, parent):
		gList = []
		#print 'parent', parent
		for key in parent.keys():
			#print 'key',key
			val = parent[key]
			#print 'val = ',val
			if type(val) == h5py.Group:
				gList += [(str(key), self.loadGroups(val)) ]
			if type(val) == h5py.Dataset:
				gList += [(str(key), [])]
		return gList
