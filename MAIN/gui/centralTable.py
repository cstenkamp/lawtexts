import jsonHandler
import os
import glob
from creatorView import *
from jsonHandler import ORDER, MACHINE_PATH
from PyQt5.QtWidgets import QPushButton, QWidget, QAction, QTableWidget, \
    QVBoxLayout, QMessageBox, QAbstractScrollArea, QTableWidgetItem,\
    QHeaderView, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from operator import itemgetter
from ItemView import ItemView

TABLE_HEADER = ORDER[0:5] + ["", "", ""]

sys.path.insert(0,os.path.join(os.getcwd(),'logic/'))
from mainLogic import MainLogic

class CentralTable(QWidget):
    """ A class to create a table where all machines will be presented in an
        easy overview """
    def __init__(self, mainWindow):
        """ initialises the Window for the Table """
        super().__init__()
        self.mainWindow = mainWindow
        self.title = 'Central Table'
        self.machines = [[],[]]
        self.orderKey = ["Name", False]
        self.logic = None

        self.create_table()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def create_table(self):
        """ initialises the QTableWidgets and its cells """
        # Create table
        self.tableWidget = QTableWidget()
        self.get_machines()
        self.order_list(self.orderKey[0], self.orderKey[1])
        self.tableWidget.setRowCount(len(self.machines[0]))
        self.tableWidget.setColumnCount(len(TABLE_HEADER))
        self.tableWidget.setHorizontalHeaderLabels(TABLE_HEADER)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for row in range(self.tableWidget.rowCount()):
            self.add_remove_edit_check_btns(row)
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_double_click)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.fill_table()
        self.order_list(self.orderKey[0], self.orderKey[1])
        self.tableWidget.resizeColumnsToContents()

    def add_remove_edit_check_btns(self, row):
        editBtn = QPushButton(self.tableWidget)
        rmvBtn = QPushButton(self.tableWidget)
        checkBtn = QPushButton(self.tableWidget)
        editBtn.setIcon(QIcon(ICON_PATH + "edit.png"))
        editBtn.setToolTip('hier klicken um diese Maschine zu <b>bearbeiten</b>')
        editBtn.setIconSize(QSize(24, 24))
        rmvBtn.setIcon(QIcon(ICON_PATH + "trash.png"))
        rmvBtn.setIconSize(QSize(24, 24))
        rmvBtn.setToolTip('hier klicken um diese Maschine zu <b>löschen</b>')
        checkBtn.setIcon(QIcon(ICON_PATH + "law.png"))
        checkBtn.setIconSize(QSize(24, 24))
        checkBtn.setToolTip('hier klicken um diese Maschine auf zutreffende Richtlinien zu <b>überprüfen</b>')
        editBtn.clicked.connect(self.btn_edit)
        rmvBtn.clicked.connect(self.btn_remove)
        checkBtn.clicked.connect(self.btn_check)
        self.tableWidget.setCellWidget(row, self.tableWidget.columnCount()-3, checkBtn)
        self.tableWidget.setCellWidget(row, self.tableWidget.columnCount()-2, editBtn)
        self.tableWidget.setCellWidget(row, self.tableWidget.columnCount()-1, rmvBtn)

    def get_machines(self):
        """ loads all machines out of the json into the class list """
        #path = os.path.dirname(os.path.abspath(__file__))
        #machinePath = path+"/machines"
        machinePath = MACHINE_PATH
        os.chdir(machinePath)
        if os.path.isdir(machinePath):
            machineList = glob.glob("*.json")
            if not machineList:
                return
            else:
                 for file in machineList:
                    json = jsonHandler.read_json_file(file)
                    self.machines[0].append(json)
                    self.machines[1].append(machinePath+"/"+file)
        #os.chdir(path)

    def fill_table(self):
        """ adds the machines of the class list into the cells """
        # todo make the Header changeable by the user
        def centerItem(toCenter):
            item = QTableWidgetItem(toCenter)
            item.setTextAlignment(Qt.AlignHCenter)
            return item
        for i in range(len(self.machines[0])):
            self.tableWidget.setItem(i, 0, centerItem(self.machines[0][i]["Name"]))
            self.tableWidget.setItem(i, 1, centerItem(self.machines[0][i]["Kundennummer"]))
            self.tableWidget.setItem(i, 2, centerItem(self.machines[0][i]["Ort"]))
            self.tableWidget.setItem(i, 3, centerItem(self.machines[0][i]["Herstellungsdatum"]))
            self.tableWidget.setItem(i, 4, centerItem(self.machines[0][i]["Prüfdatum"]))


    def order_list(self, keyItem="Name", descending=False):
        """ orders list depending on the keyItem and depending on descending """
        order = [keyItem, descending]
        self.orderKey = order
        temp = sorted(zip(self.machines[0], self.machines[1]), key=lambda x: x[0][keyItem].lower(), reverse=descending)
        if len(self.machines[0]) > 0:
            self.machines[0], self.machines[1] = map(list, zip(*temp))
        self.fill_table()
        return 0

    def reload_list(self):
        """ reloads the list and all releated machines """
        oldRowCount = self.tableWidget.rowCount()
        del self.machines
        self.machines = [[],[]]
        self.get_machines()
        self.tableWidget.setRowCount(len(self.machines[0]))
        if oldRowCount < len(self.machines[0]):
            "we are here"
            for row in range(len(self.machines[0])-oldRowCount):
                self.add_remove_edit_check_btns(oldRowCount+row)
        self.order_list(self.orderKey[0], self.orderKey[1])

    # start of the button functions
    @pyqtSlot()
    def on_double_click(self):
        """ loads a full overview over the respective item read-only """
        '''
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(
            ), currentQTableWidgetItem.text())
        '''
        row = self.tableWidget.selectedItems()[0].row()
        self.editWindow = ItemView([self.machines[0][row], self.machines[1][row]], self)
        self.editWindow.show()

    def btn_edit(self):
        """ loads a full overview over the respective item - editable """
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        machineFile = self.machines[0][index.row()]
        machinePath = self.machines[1][index.row()]
        htmlPath = machinePath.split('.json')[0]+'.html'
        logic = MainLogic(machineFile,htmlPath)
        self.newCreatorView = CreatorView(self.mainWindow, centralTable = self,\
                                    jsonFile = machineFile, path = machinePath)
        self.newCreatorView.show()

    def btn_remove(self):
        """ removes the respective item after a confirmation dialog """
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        item = [self.machines[0][index.row()], self.machines[1][index.row()]]
        reply = QMessageBox.question(self, 'Maschine löschen',
                                     "Wollen Sie " +
                                     item[0]["Name"] + " wirklich löschen?", QMessageBox.Yes |
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            # remove the file
            os.remove(item[1])
            self.tableWidget.removeRow(index.row())
            self.machines[0].pop(index.row())
            self.machines[1].pop(index.row())

    def btn_check(self):
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        machineFile = self.machines[0][index.row()]
        machinePath = self.machines[1][index.row()]
        resFileName = machineFile['Name']+'.html'
        resPath = os.path.join(os.getcwd(),resFileName)
        self.logic = MainLogic(machineData=machineFile,filePath=resPath)
        CreatorView.start_check(machineFile,logic=self.logic)
