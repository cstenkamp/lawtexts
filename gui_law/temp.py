import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


def read_json_file(jsonFile):
    """ reads the jsonFiles and returns it """
    if not jsonFile.lower().endswith('.json'):
        print("Given File is no json")
        return
    with open(jsonFile, 'r') as f:
        datastor = json.load(f)
        return datastor


class Window(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize(sizeObject.width() / 2, sizeObject.height() / 2)
        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)

        self.model = QStandardItemModel()
        self.addItems(self.model, data)
        self.treeView.setModel(self.model)

        self.model.setHorizontalHeaderLabels([self.tr("Object")])

        layout = QVBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)

    def addItems(self, parent, dict_item):

        for key in dict_item:
            item = QStandardItem(key)
            parent.appendRow(item)
            newParent = item
            if type(dict_item[key]) is dict:
                self.addItems(item, dict_item[key])
            elif type(dict_item[key]) is list:
                item = QStandardItem(str(dict_item[key]))
                newParent.appendRow(item)
            else:
                item = QStandardItem(dict_item[key])
                newParent.appendRow(item)

    def openMenu(self, position):
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
            menu = QMenu()
            # todo Change
            if level == 0:
                menu.addAction(self.tr("Edit person"))
            elif level == 1:
                menu.addAction(self.tr("Edit object/container"))
            elif level == 2:
                menu.addAction(self.tr("Edit object"))
            menu.exec_(self.treeView.viewport().mapToGlobal(position))


if __name__ == "__main__":

    data = read_json_file(\
        "/home/nilus/Projects/lawtexts/gui_law/machines/bMachine.json")
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
