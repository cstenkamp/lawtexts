import jsonHandler
import os
import glob
from PyQt5.QtWidgets import QPushButton, QWidget, QAction, QTableWidget, \
    QVBoxLayout, QMessageBox, QAbstractScrollArea, QTableWidgetItem, QHeaderView, QLabel
from PyQt5.QtCore import pyqtSlot, Qt
from operator import itemgetter

TABLE_HEADER = ["Name", "customerID", "Herstellungsort", "Herstellungsdatum", "Prüfdatum", "", ""]

class centralTable(QWidget):
    def __init__(self, mainWindow):
        super().__init__()
        self.mainWindow = mainWindow
        self.title = 'Central Table'
        self.machines = [[],[]]
        self.orderKey = "name"

        self.create_table()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def create_table(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.get_machines()
        self.tableWidget.setRowCount(len(self.machines[0]))
        self.tableWidget.setColumnCount(len(TABLE_HEADER))
        self.tableWidget.setHorizontalHeaderLabels(TABLE_HEADER)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for row in range(self.tableWidget.rowCount()):
            editBtn = QPushButton(self.tableWidget)
            rmvBtn = QPushButton(self.tableWidget)
            editBtn.setText('Edit')
            editBtn.setToolTip('click to <b>edit</b> this item')
            rmvBtn.setText('Remove')
            rmvBtn.setToolTip('click to <b>remove</b> this item')
            editBtn.clicked.connect(self.btn_edit)
            rmvBtn.clicked.connect(self.btn_remove)
            self.tableWidget.setCellWidget(row, self.tableWidget.columnCount()-2, editBtn)
            self.tableWidget.setCellWidget(row, self.tableWidget.columnCount()-1, rmvBtn)
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.order_list(self.orderKey, False)
        self.fill_table()
        self.tableWidget.resizeColumnsToContents()


    def get_machines(self):
        path = os.path.dirname(os.path.abspath(__file__))
        machinePath = path+"/machines"
        os.chdir(machinePath)
        if os.path.isdir(machinePath):
            machineList = glob.glob("*.json")
            if not machineList:
                return
            else:
                 for file in machineList:
                    json = jsonHandler.read_json_file(file)
                    self.machines[0].append(json)
                    self.machines[1].append(path+"/"+file)
        os.chdir(path)

    def fill_table(self):
        def centerItem(toCenter):
            item = QTableWidgetItem(toCenter)
            item.setTextAlignment(Qt.AlignHCenter)
            return item
        for i in range(len(self.machines[0])):
            self.tableWidget.setItem(i, 0, centerItem(self.machines[0][i]["name"]))
            self.tableWidget.setItem(i, 1, centerItem(self.machines[0][i]["customer_id"]))
            self.tableWidget.setItem(i, 2, centerItem(self.machines[0][i]["location"]))
            self.tableWidget.setItem(i, 3, centerItem(self.machines[0][i]["Herstellungsdatum"]))
            self.tableWidget.setItem(i, 4, centerItem(self.machines[0][i]["Prüfdatum"]))


    def order_list(self, keyItem, descending):
        print(self.machines[1])
        temp = sorted(zip(self.machines[0], self.machines[1]), key=lambda x: x[0][keyItem].lower(), reverse=descending)
        self.machines[0], self.machines[1] = map(list, zip(*temp))

    def reload_list(self):
        self.get_machines()
        self.order_list()
        self.fill_table()


    # start of the button functions
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(
            ), currentQTableWidgetItem.text())


    def btn_edit(self):
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        print("edit: ", self.machines[1][index.row()], index.row(), index.column())


    def btn_remove(self):
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        reply = QMessageBox.question(self, 'Remove item',
                                     "Are you you want to delete this machine?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            print("remove hier: ")

        else:
            print("don't delete")