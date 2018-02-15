import jsonHandler
import os
import glob
from PyQt5.QtWidgets import QPushButton, QWidget, QAction, QTableWidget, \
    QVBoxLayout, QMessageBox, QAbstractScrollArea, QTableWidgetItem, QHeaderView, QLabel
from PyQt5.QtCore import pyqtSlot, Qt
from operator import itemgetter

TABLE_HEADER = ["Name", "Kundennummer", "Ort", "Herstellungsdatum", "Prüfdatum", "", ""]


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
        self.tableWidget.doubleClicked.connect(self.on_double_click)
        self.tableWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.fill_table()
        self.order_list(self.orderKey[0], self.orderKey[1])
        self.tableWidget.resizeColumnsToContents()


    def get_machines(self):
        """ loads all machines out of the json into the class list """
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
                    self.machines[1].append(machinePath+"/"+file)
        os.chdir(path)

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
        self.machines[0], self.machines[1] = map(list, zip(*temp))
        self.fill_table()
        return 0

    def reload_list(self):
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
        print(self.tableWidget.selectedItems())
        row = self.tableWidget.selectedItems()[0].row()
        self.editWindow = jsonHandler.ItemView([self.machines[0][row],
                                                self.machines[1][row]], self)
        self.editWindow.show()

    def btn_edit(self):
        """ loads a full overview over the respective item - editable """
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        self.editWindow = jsonHandler.ItemView([self.machines[0][index.row()],
                                                      self.machines[1][index.row()]], self, True)
        self.editWindow.show()

    def btn_remove(self):
        """ removes the respective item after a confirmation dialog """
        button = self.sender()
        index = self.tableWidget.indexAt(button.pos())
        item = [self.machines[0][index.row()], self.machines[1][index.row()]]
        reply = QMessageBox.question(self, 'Remove item',
                                     "Are you you want to delete " +
                                     item[0]["Name"] + "?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            # remove the file
            os.remove(item[1])
            self.tableWidget.removeRow(index.row())
            self.machines[0].pop(index.row())
            self.machines[1].pop(index.row())
