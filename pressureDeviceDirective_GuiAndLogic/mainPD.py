import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from jsonParser import PARSER as jParser 

from pressureGraphs import pressureGraphs, loadGraphImage

from numpy import argmin as argmin
from numpy import any as npany

class BaseWindow(QWidget):
	def __init__(self):
		super(BaseWindow,self).__init__()

		self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

		self.mainLayout = QVBoxLayout()
		self.mainLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
		self.setLayout(self.mainLayout)

	def addCheckBox(self,text, connection, parentLayout):
		layout = QHBoxLayout()
		parentLayout.addLayout(layout)
		checkBox = QCheckBox(text)
		checkBox.clicked.connect(connection)
		layout.addWidget(checkBox)
		return checkBox



	def addLabelBox(self,labelName,unitLabel, connection, parentLayout):
		layout = QHBoxLayout()
		parentLayout.addLayout(layout)
		label = QLabel(labelName)
		label.setFixedWidth(80)
		layout.addWidget(label)
		lineEdit = QLineEdit('0')
		lineEdit.setFixedWidth(80)
		lineEdit.editingFinished.connect(lambda: connection(lineEdit.text()))
		layout.addWidget(lineEdit)
		layout.addWidget(QLabel(unitLabel))
		return lineEdit


	def addQCombo(self,labelName, items, connection, parentLayout,returnLabel=False):
		layout = QHBoxLayout()
		parentLayout.addLayout(layout)
		label = QLabel(labelName)
		label.setFixedWidth(80)
		layout.addWidget(label)
		items = sorted(items)
		selectionMenu = QComboBox()
		for s in items:
			selectionMenu.addItem(s)
		selectionMenu.activated.connect(connection)
		layout.addWidget(selectionMenu)
		if not returnLabel:
			return selectionMenu 
		else:
			return selectionMenu, label


	def addQMenu(self,labelName, items, connection, parentLayout,checkable=True):
		layout = QHBoxLayout()
		parentLayout.addLayout(layout)
		label = QLabel(labelName)
		label.setFixedWidth(80)
		layout.addWidget(label)
		items = sorted(items)
		selectionMenu = QMenu()
		for s in items:
			a = selectionMenu.addAction(s)
			a.triggered.connect(connection)
			a.setCheckable(checkable)
		specificationMenuButton = QPushButton('')
		specificationMenuButton.setMenu(selectionMenu)
		layout.addWidget(specificationMenuButton)
		return specificationMenuButton

	def addButton(self,buttonText, connection, parentLayout,fixedWidth=True):
		button = QPushButton(buttonText)
		if fixedWidth:
			button.setFixedWidth(150)
		parentLayout.addWidget(button)
		button.clicked.connect(connection)
		return button 

	def print(self,s=None):
		pass

class BaseWindowPlus(BaseWindow):
	def __init__(self,parent,name='bw'):
		super(BaseWindowPlus,self).__init__()

		self.topLayout = QVBoxLayout()
		self.topLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)		

		self.topBox = QGroupBox()
		self.topBox.setLayout(self.topLayout)
		self.mainLayout.addWidget(self.topBox)

		self.headerLayout = QHBoxLayout()
		self.headerLayout.setAlignment(Qt.AlignRight | Qt.AlignTop)		
		self.topLayout.addLayout(self.headerLayout)

		self.parent = parent 
		self.name = name
		self.label = QLabel(self.name)
		self.headerLayout.addWidget(self.label)
		self.headerLayout.addStretch(0)
		self.setMaximumWidth(500)
		self.setSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum)

	def addDelButton(self,parent_list):
		self.delButton = self.addButton('x',lambda: self.deleteFrom(parent_list),self.headerLayout)
		self.delButton.setFixedWidth(10)

	def deleteFrom(self,parent_list):
		self.deleteLater()
		parent_list.remove(self)

	def addContentLayout(self):
		self.contentLayout = QVBoxLayout()
		self.contentLayout.setAlignment(Qt.AlignLeft|Qt.AlignTop)
		self.mainLayout.addLayout(self.contentLayout)

class MainWindow(BaseWindow):
	def __init__(self):
		super(MainWindow,self).__init__()
		self.setGeometry(100,100,400,300)

		# upper part with buttons etc
		self.topFrame = QFrame()
		self.topLayout = QHBoxLayout()
		self.topLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
		self.topFrame.setLayout(self.topLayout)
		self.mainLayout.addWidget(self.topFrame)
		# button to create groups/single products
		self.groupButton = self.addButton('neue Gerätegruppe', self.addGroup, self.topLayout)
		
		# bottom layout
		self.bottomLayout = QHBoxLayout()
		self.bottomLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

		self.bottomBox = QGroupBox()
		self.bottomBox.setLayout(self.bottomLayout)

		self.scroller = QScrollArea()
		self.scroller.setWidget(self.bottomBox)
		self.scroller.setWidgetResizable(True)

		self.mainLayout.addWidget(self.scroller)

		self.groups = []

	def addGroup(self):
		n = 'Gerätegruppe: {0}'.format(str(len(self.groups)+1))
		group = DeviceGroup(self,n)
		self.groups.append(group)
		self.bottomLayout.addWidget(group)

class DeviceGroup(BaseWindowPlus):
	def __init__(self,parent,name='DeviceGroup'):
		super(DeviceGroup,self).__init__(parent,name=name)

		self.json = {}
		self.addDelButton(self.parent.groups)
		self.roleMenu,roleLabel = self.addQCombo('als Wirtschaftsakteur:', 
												['Hersteller','Bevollmächtigter','Händler','Einführer'],
												  self.setRole, self.topLayout, returnLabel=True)
		roleLabel.setFixedWidth(120)
		self.role = 'Hersteller'
		self.roleMenu.setCurrentText(self.role)
		self.analyseButton = self.addButton('Gerätegruppe bewerten', self.anaylse, self.topLayout)
		#self.delButton = self.addButton('Gerätegruppe entfernen', lambda: self.deleteFrom(self.parent.groups), self.topLayout)
		self.button = self.addButton('neues Druckgerät', self.addDevice, self.topLayout)
		self.devices = []

	def addDevice(self):
		self.intrfc = addingInterface(self)

	def addContainer(self):
		device = PressureContainer(self)
		self.devices.append(device)
		self.topLayout.addWidget(device)

	def addPipe(self):
		device = PressurePipe(self)
		self.devices.append(device)
		self.topLayout.addWidget(device)

	def addSafetyDevice(self):
		device = SafetyDevice(self)
		self.devices.append(device)
		self.topLayout.addWidget(device)

	def addPressureCooker(self):
		device = PressureCooker(self)
		self.devices.append(device)
		self.topLayout.addWidget(device)

	def addFireExtinguisher(self):
		device = FireExtinguisher(self)
		self.devices.append(device)
		self.topLayout.addWidget(device)

	def addBreathingGas(self):
		device = BreathingGas(self)
		self.devices.append(device)
		self.topLayout.addWidget(device)

	def anaylse(self):
		l = PressureLogic()
		R=l.checkGroup(self)
		self.rw = ResultWindow(self,R)
		self.rw.show()

	def setRole(self):
		self.role = self.roleMenu.currentText()



class addingInterface(BaseWindow):
	def __init__(self,parent,name=''):
		super(addingInterface,self).__init__()
		#self.setGeometry(100,100,850,300)
		self.parent = parent

		self.addButton('Druckbehälter', self.addContainer, self.mainLayout)
		self.addButton('Rohrleitung', self.addPipe, self.mainLayout)
		#self.addButton('Sicherheitsbauteil', self.addSafetyDevice, self.mainLayout)
		self.addButton('Schnellkochtopf', self.addPressureCooker, self.mainLayout)
		self.addButton('Feuerlöscher', self.addFireExtinguisher, self.mainLayout)
		self.addButton('Atemschutzflasche', self.addBreathingGas, self.mainLayout)

		self.show()

	def addContainer(self):
		self.parent.addContainer()
		self.deleteLater()

	def addPipe(self):
		self.parent.addPipe()
		self.deleteLater()

	def addSafetyDevice(self):
		self.parent.addSafetyDevice()
		self.deleteLater()

	def addPressureCooker(self):
		self.parent.addPressureCooker()
		self.deleteLater()

	def addFireExtinguisher(self):
		self.parent.addFireExtinguisher()
		self.deleteLater()

	def addBreathingGas(self):
		self.parent.addBreathingGas()
		self.deleteLater()

class PressureContainer(BaseWindowPlus):
	def __init__(self,parent,name='Druckbehälter'):
		super(PressureContainer,self).__init__(parent,name=name)

		self.addDelButton(self.parent.devices)
		
		self.checkBoxWater = self.addCheckBox('Zur Erzeugung von Dampf oder Heißwasser.',self.addManualHeating, self.topLayout)

		self.placeholderLayout = QHBoxLayout()		
		self.placeholderLayout.setAlignment(Qt.AlignLeft|Qt.AlignTop)
		self.topLayout.addLayout(self.placeholderLayout)

		self.addChamberButton = self.addButton('Druckkammer hinzufügen', self.addChamber, self.topLayout)
		#self.deleteChamberButton = self.addButton('Druckbehälter entfernen', lambda: self.deleteFrom(self.parent.devices), self.topLayout)

		self.chambers = []
		self.addChamber()

	def addManualHeating(self):
		if self.checkBoxWater.isChecked():
			self.checkBoxHeating = self.addCheckBox('Beheizt',self.print, self.placeholderLayout)
			self.checkBoxHeatingManual = self.addCheckBox('Handbeschickung des Brennstoffes',self.print, self.placeholderLayout)
		else:
			self.checkBoxHeating.deleteLater()
			self.checkBoxHeatingManual.deleteLater()
		

	def addChamber(self):
		chamber = PressureChamber(self)
		self.chambers.append(chamber)
		self.topLayout.addWidget(chamber)


class PressurePipe(BaseWindowPlus):
	def __init__(self,parent,name='Rohrleitung'):
		super(PressurePipe,self).__init__(parent,name=name)

		self.addDelButton(self.parent.devices)

		self.pressue_panel = self.addLabelBox('Druck',	'bar',self.print,self.topLayout)
		self.temperature_panel = self.addLabelBox('Temperatur','C',self.print,self.topLayout)
		self.checkBoxPressure = self.addCheckBox('Dampfdruck des Inhalts liegt bei der\nzulässigen maximalen Temperatur\nbei mehr als 0.5 bar.',self.print, self.topLayout)
		self.checkBoxPressure.clicked.connect(self.print)
		self.dn_panel =  self.addLabelBox('Nennweite',	'DN',self.print,self.topLayout)
		self.length_panel =  self.addLabelBox('Länge',	'm',self.print,self.topLayout)

		self.contents = []
		self.addContent()


	def addContent(self):
		content = ContentPanel(self,'Inhalt')
		self.contents.append(content)
		self.topLayout.addWidget(content)


class SafetyDevice(BaseWindowPlus):
	def __init__(self,parent,name='Sicherheitsbauteil'):
		super(SafetyDevice,self).__init__(parent,name=name)
		self.addDelButton(self.parent.devices)


class PressureCooker(BaseWindowPlus):
	def __init__(self,parent,name='Schnellkochtopf'):
		super(PressureCooker,self).__init__(parent,name=name)
		self.addDelButton(self.parent.devices)

class FireExtinguisher(BaseWindowPlus):
	def __init__(self,parent,name='Feuerlöscher'):
		super(FireExtinguisher,self).__init__(parent,name=name)
		self.addDelButton(self.parent.devices)

class BreathingGas(BaseWindowPlus):
	def __init__(self,parent,name='Atemschutzflasche'):
		super(BreathingGas,self).__init__(parent,name=name)
		self.addDelButton(self.parent.devices)


class PressureChamber(BaseWindowPlus):
	def __init__(self,parent,name='Druckkammer'):
		super(PressureChamber,self).__init__(parent,name=name)

		self.addDelButton(self.parent.chambers)

		self.addContentButton = self.addButton('Inhalt hinzufügen', self.addContent, self.topLayout)
		
		self.pressue_panel = self.addLabelBox('Druck',	'bar',self.print,self.topLayout)
		self.temperature_panel = self.addLabelBox('Temperatur','C',self.print,self.topLayout)
		self.volume_panel =  self.addLabelBox('Volumen',	'liter',self.print,self.topLayout)
		self.checkBoxPressure = self.addCheckBox('Dampfdruck des Inhalts liegt bei der\nzulässigen maximalen Temperatur\nbei mehr als 0.5 bar.',self.print, self.topLayout)
		
		self.contents = []

		self.addContent()

	def addContent(self):
		content = ContentPanel(self)
		self.contents.append(content)
		self.topLayout.addWidget(content)


class ContentPanel(BaseWindowPlus):
	def __init__(self,parent,name='Inhalt'):
		super(ContentPanel,self).__init__(parent,name=name)

		self.addDelButton(self.parent.contents)

		self.jparser = jParser()

		self.contents = self.jparser.parse('jsons/contents.json')['Inhalt']+['--andere--']
		self.c_states = self.jparser.parse('jsons/contents.json')['Aggregatszustand']+['--andere--']
		self.c_features = self.jparser.parse('jsons/contents.json')['Eigenschaften']

		self.content = self.addQCombo('Inhalt', self.contents, self.print, self.topLayout)
		self.contentState = self.addQCombo('Aggregatszustand\nd. Inhalts', self.c_states, self.print, self.topLayout)
		self.contentFeatures = self.addQMenu('Eigenschaften\nd. Inhalts', self.c_features, self.print, self.topLayout)
		
class PressureLogic():
	def __init__(self):
		pass 


	def checkPressureContainer(self,container):
		# for each of the pressure chambers on the container:
		chamber_results = []
		chamber_vols = []
		chamber_pressures = []
		for chamber in container.chambers:
			temperature = float(chamber.temperature_panel.text())
			pressure = float(chamber.pressue_panel.text())
			volume = float(chamber.volume_panel.text())
			chamber_vols.append(volume)
			chamber_pressures.append(pressure)
			# if pressure is too low, PD doesn't apply
			if pressure < .5:
				chamber_results.append(False)
			# if device is for water heating, larger than 2L and hotter than 110C
			elif container.checkBoxWater.isChecked() and (volume>2) and (temperature>110):
				chamber_results.append(5)
			elif container.checkBoxWater.isChecked() and (temperature>110) \
				and container.checkBoxHeating.isChecked():
				chamber_results.append(90)
			# otherwise check each content
			else:
				content_results = []
				for C in chamber.contents:
					# infos about content
					content = C.content.currentText()
					state = C.contentState.currentText()
					features = [a.text() for a in C.contentFeatures.menu().actions() if a.isChecked()]
					# for gasses, steams or and fluids with high steam pressure
					if state in ['gasförmig','verflüssigtes Gas','unter Druck gelöstes Gas','Dampf']\
						or (state=='flüssig' and chamber.checkBoxPressure.isChecked()):
						# if any of the features are checked, it's a fluid of group 1
						if len(features)>0:
							if ((volume>1) and ((pressure*volume)>25)) or (pressure>200):
								content_results.append(1)
							else:
								content_results.append(100)
						# if no features are checked, it's a fluid of group 2
						else:
							if ((volume>1) and ((pressure*volume)>50)) or (pressure>1000):
								content_results.append(2)
							else:
								content_results.append(100)
					# for fluids 
					elif (state == 'flüssig') and (not chamber.checkBoxPressure.isChecked()):
						# if any of the features are checked, it's a fluid of group 1
						if len(features)>0:
							if ((volume>1) and ((pressure*volume)>200)) or (pressure>500):
								content_results.append(3)
							else:
								content_results.append(100)
						# if no features are checked, it's a fluid of group 2
						else:
							if ((pressure>10) and ((pressure*volume)>10000)) or (pressure>1000):
								content_results.append(4)
							else:
								content_results.append(100)
					else:
						content_results.append(False)
				# take the content with the highest rating (lowest number) and apply it to the whole chamber
				content_results = [a for a in content_results if type(a) is int]
				if len(content_results)==0:
					chamber_results.append(False)
				else:
					content_results = min(content_results)
					chamber_results.append(content_results)
		# again, take the highest result (lowest number) over all chambers
		chamber_pressures = [b for a,b in zip(chamber_results,chamber_pressures) if type(a) is int]
		chamber_vols = [b for a,b in zip(chamber_results,chamber_vols) if type(a) is int]
		chamber_results = [a for a in chamber_results if type(a) is int]
		if len(chamber_results)==0:
			return False
		else:
			chamber_vols = chamber_vols[argmin(chamber_results)]
			chamber_pressures = chamber_pressures[argmin(chamber_results)]
			chamber_results = min(chamber_results)
			return chamber_results,chamber_vols,chamber_pressures

	def checkPressurePipe(self,pipe):
		pressure = float(pipe.pressue_panel.text())
		DN = float(pipe.dn_panel.text())
		if pressure < .5:
			return False
		content_results = []
		for C in pipe.contents:
			content = C.content.currentText()
			state = C.contentState.currentText()
			features = [a.text() for a in C.contentFeatures.menu().actions() if a.isChecked()]
			if (state in ['gasförmig','verflüssigtes Gas','unter Druck gelöstes Gas','Dampf'])\
					or (state=='flüssig' and pipe.checkBoxPressure.isChecked()):
				if len(features)>0:
					# fluids of group 1
					if DN > 25:
						content_results.append(6)
					else:
						content_results.append(100)
				else:
					# fluids of group 2
					if (DN>32)  and ((pressure*DN)>1000):
						content_results.append(7)
					else:
						content_results.append(100)
			elif (state == 'flüssig') and (not pipe.checkBoxPressure.isChecked()):
				if len(features)>0:
					if (DN > 25) and ((pressure*DN)>2000):
						content_results.append(8)
					else:
						content_results.append(100)
				else:
					if (pressure>10) and (DN>200) and ((pressure*DN)>5000):
						content_results.append(9)
					else:
						content_results.append(100)
			else:
				content_results.append(False)
		# take the content with the highest rating (lowest number) and apply it to the whole chamber
		content_results = [a for a in content_results if type(a) is int]
		if len(content_results)==0:
			return False
		else:
			content_results = min(content_results)
			return content_results


	def checkDevice(self,device):
		# if device is pressure cooker
		if type(device) is PressureCooker:
			return 5
		elif type(device) is FireExtinguisher:
			return 2
		elif type(device) is BreathingGas:
			return 2
		elif type(device) is PressureContainer:
			return self.checkPressureContainer(device)
		elif type(device) is PressurePipe:
			return self.checkPressurePipe(device)

	def checkGroup(self,group):
		R = []
		for device in group.devices:
			r = self.checkDevice(device)
			R.append(r)
			print(r)
		return R




class RWPanel(QWidget):
	def __init__(self,parentLayout):
		super(RWPanel,self).__init__()
		self.parentLayout = parentLayout
		self.mainLayout = QVBoxLayout()
		self.mainLayout.setContentsMargins(0,0,0,0)
		self.mainLayout.setSpacing(0)
		self.setLayout(self.mainLayout)

		self.topLayout = QVBoxLayout()
		self.topLayout.setContentsMargins(0,0,0,0)
		#self.topLayout.setSpacing(0)
		self.box = QGroupBox()
		self.box.setContentsMargins(50,20,0,0)
		self.box.setLayout(self.topLayout)

		self.mainLayout.addWidget(self.box)
		self.parentLayout.addWidget(self)
		self.hide()

	def toggle(self):
		if self.isVisible():
			self.hide()
		else:
			self.show()




class ResultWindow(BaseWindow):
	def __init__(self,group,results,graphId=None):
		super(ResultWindow,self).__init__()

		self.scrollLayout = QVBoxLayout()
		self.scrollLayout.setAlignment(Qt.AlignLeft|Qt.AlignTop)

		self.scrollBox = QGroupBox()
		self.scrollBox.setLayout(self.scrollLayout)

		self.scrollLayout.setSpacing(0)

		self.scroller = QScrollArea()
		self.scroller.setWidget(self.scrollBox)
		self.scroller.setWidgetResizable(True)

		self.mainLayout.addWidget(self.scroller)

		# duties
		self.dutiesLayout = QVBoxLayout()
		self.dutiesLayout.setContentsMargins(0,0,0,0)
		self.scrollLayout.addLayout(self.dutiesLayout)
		self.dutiesWidget = RWPanel(self.scrollLayout)
		self.dutiesButton = self.addButton('Pflichten',self.dutiesWidget.toggle, self.dutiesLayout,fixedWidth=False)
		self.dutiesButton.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)
		path = os.path.join(os.getcwd(),'html','duties',group.role+'.html')
		with open(path) as f:
			html = f.readlines()
			html = ''.join(html)
		htmlView = QWebEngineView()
		htmlView.setHtml(html)
		self.dutiesWidget.topLayout.addWidget(htmlView)


		# for each device make a dropdown layout
		self.groupsLayout = QVBoxLayout()
		#self.groupsLayout.setContentsMargins(0,0,0,0)
		self.scrollLayout.addLayout(self.groupsLayout)
		self.groupsWidget = RWPanel(self.scrollLayout)
		self.groupsButton = self.addButton('Druckgeräte',self.groupsWidget.toggle, self.groupsLayout,fixedWidth=False)
		self.groupsButton.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Minimum)

		for device,result  in zip(group.devices,results):
			if not result:
				pressure = 0
				volume_DN = 0
			elif type(device) is PressurePipe:
				pressure = float(device.pressue_panel.text())
				volume_DN = float(device.dn_panel.text())
				result = result
			elif type(result) is tuple:
				volume_DN = float(result[1])
				pressure = float(result[2])
				result = result[0]
			deviceLayout = QVBoxLayout()
			#deviceLayout.setContentsMargins(0,0,0,0)
			self.groupsWidget.topLayout.addLayout(deviceLayout)
			deviceWidget = RWPanel(self.groupsWidget.topLayout)
			deviceButton = self.addButton(device.name,deviceWidget.toggle, deviceLayout,fixedWidth=False)

			# graphs
			graphsLayout = QVBoxLayout()
			deviceWidget.topLayout.addLayout(graphsLayout)
			graphsWidget = RWPanel(deviceWidget.topLayout)
			graphsButton = self.addButton('Diagramme',graphsWidget.toggle, graphsLayout,fixedWidth=False)
			im = self.loadGraphImage(result)
			if not im is None:
				graphsWidget.topLayout.addWidget(im)
			else:
				html = '<h1>Trifft nicht zu!</h1>'
				htmlView = QWebEngineView()
				htmlView.setHtml(html)
				graphsWidget.topLayout.addWidget(htmlView)
				
			# common
			commonLayout = QVBoxLayout()
			deviceWidget.topLayout.addLayout(commonLayout)
			commonWidget = RWPanel(deviceWidget.topLayout)
			commonButton = self.addButton('Grundlegende Anforderungen',commonWidget.toggle, commonLayout,fixedWidth=False)
			if result == 100:
				html = '<h1>Nach in dem Land gängigen Ingeneurspraktiken herstellens. Kein CE Kennzeichen anbringen!</h1>'
			elif not result:
				html = '<h1>Trifft nicht zu!</h1>'
			elif result in [1,2,3,4,5,6,7,8,9,90]:
				path = os.path.join(os.getcwd(),'html','basic_safety_demands','basic_safety_demands.html')
				with open(path) as f:
					html = f.readlines()
					html = ''.join(html)
			htmlView = QWebEngineView()
			htmlView.setHtml(html)
			commonWidget.topLayout.addWidget(htmlView)

			# modules
			modulesLayout = QVBoxLayout()
			deviceWidget.topLayout.addLayout(modulesLayout)
			modulesWidget = RWPanel(deviceWidget.topLayout)
			modulesButton = self.addButton('Module',modulesWidget.toggle, modulesLayout,fixedWidth=False)
			moduleHtml = self.getModule(result,device,volume_DN,pressure)
			htmlView = QWebEngineView()
			modulesWidget.topLayout.addWidget(htmlView)
			htmlView.setHtml(moduleHtml)
		self.show()

	def getModule(self,result,device,volume_DN,pressure):
		if not result:
			return '<h1>Trifft nicht zu</h1>'
		else:
			graph = pressureGraphs[result-1]
			category = graph(volume_DN,pressure)
			if category == 'I':
				names = ['A.html']
			elif category == 'II':
				names = ['A2.html']#['A2.html','D1.html','E1.html']
			elif category == 'III':
				names = ['B_Entwurfsmuster.html','D.html']
			elif category == 'IV':
				names = ['B_Baumuster.html','D.html']
			elif category == 'Artikel 4, Absatz 3':
				names = None
			html = ''
			for name in names:
				if names is None:
					html = '<h1>Nach in dem Land gängigen Ingeneurspraktiken herstellens. Kein CE Kennzeichen anbringen!</h1>'
				else:
					module_path = os.path.join(os.getcwd(),'html','modules',name)
					with open(module_path) as f:
						module = f.readlines()
						module = '\n'.join(module)
						html += module
			return html 


	def loadGraphImage(self,result):
		if result:
			if result==90:
				return None
			elif result == 100:
				return None
			else:
				p = os.path.join(os.getcwd(),'diagrams','d'+str(result)+'.jpg')
				label = QLabel()
				pixmap = QPixmap(p)
				label.setPixmap(pixmap)
				return label 




if __name__ == '__main__':
	app = QApplication(sys.argv)
	mw = MainWindow()
	mw.show()
	sys.exit(app.exec_())
	#rw = ResultWindow()
	#rw.show()