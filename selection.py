from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets
from PySide2 import shiboken2
from pymxs import runtime as rt
import MaxPlus
import csv


def seleccionar_lifts():
	dictionary_result = read_csv('archivo1.txt')
	print(dictionary_result)
	nombres = []
	for row in dictionary_result:
		nombres.append(row['UOM'])
		
	#nombres = ["AH3W2CW07", "AH3W3CW10"]
	nodes_selection(nombres)
	
def seleccionar_2_lifts():
	dictionary_result = read_csv('archivo2.txt')
	print(dictionary_result)
	nombres = []
	for row in dictionary_result:
		nombres.append(row['UOM'])
	nodes_selection(nombres)
	
def seleccionar_3_lifts():
	dictionary_result = read_csv('archivo3.txt')
	print(dictionary_result)
	nombres = []
	for row in dictionary_result:
		nombres.append(row['UOM'])
	nodes_selection(nombres)

class PyMaxDockWidget(QtWidgets.QDockWidget):
	def __init__(self, parent=None):
		super(PyMaxDockWidget, self).__init__(parent)
		self.setWindowFlags(QtCore.Qt.Tool)
		self.initUI()
		self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
		
	def initUI(self):
		main_layout = QtWidgets.QVBoxLayout()
		label = QtWidgets.QLabel("Click to select lifts according to defects")
		main_layout.addWidget(label)
		# Select lifts with 1 defect
		seleccionar_btn = QtWidgets.QPushButton("Select lifts: 1 defect")
		seleccionar_btn.clicked.connect(seleccionar_lifts)
		main_layout.addWidget(seleccionar_btn)
		
		# Select lifts with 2 defects
		seleccionar2_btn = QtWidgets.QPushButton("Select lifts: 2 defects")
		seleccionar2_btn.clicked.connect(seleccionar_2_lifts)
		main_layout.addWidget(seleccionar2_btn)
		
		# Select lifts with more than 3 defects
		seleccionar3_btn = QtWidgets.QPushButton("Select lifts: > 3 defects")
		seleccionar3_btn.clicked.connect(seleccionar_3_lifts)
		main_layout.addWidget(seleccionar3_btn)
		
		widget = QtWidgets.QWidget()
		widget.setLayout(main_layout)
		self.setWidget(widget)
		self.resize(250, 100)
		

def read_csv(filename):
	data = []
	with open(filename, mode='r') as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			data.append(row)
		return data
				
def nodes_selection(node_list):
	nodos = MaxPlus.INodeTab()
	for c in MaxPlus.Core.GetRootNode().Children:
		if c.Name in node_list:
			print(c.Name)
			nodos.Append(c)
	MaxPlus.SelectionManager.ClearNodeSelection()
	MaxPlus.SelectionManager.SelectNodes(nodos)
	

	
	
def main():
	#rt.resetMaxFile(rt.name('noPrompt'))
	# Cast the main window HWND to a QMainWindow for docking
	# First, get the QWidget corresponding to the Max windows HWND:
	main_window_qwdgt = QtWidgets.QWidget.find(rt.windows.getMAXHWND())
	# Then cast it as a QMainWindow for docking purposes:
	main_window = shiboken2.wrapInstance(shiboken2.getCppPointer(main_window_qwdgt)[0], QtWidgets.QMainWindow)
	w = PyMaxDockWidget(parent=main_window)
	w.setFloating(True)
	w.show()
	

if __name__ == '__main__':
	main()
			
	
