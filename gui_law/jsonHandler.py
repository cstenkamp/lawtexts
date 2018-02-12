import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

EINHEITEN = ["flüssig", "fest", "gasförmig", "c", "bar", "watt", "volt ac", \
            "l", "ml", "k", "g", "mg"]


def read_json_file(jsonFile):
    """ reads the jsonFiles and returns it """
    if not jsonFile.lower().endswith('.json'):
        print("Given File is no json")
        return
    with open(jsonFile, 'r') as f:
        datastor = json.load(f)
        return datastor


class ItemView(QMainWindow):
    """ creates a ItemOverview over the given @item, @edit = readOnly? """
    def __init__(self, item, parent=None, edit=False):
        super(ItemView, self).__init__(parent)
        self.parent = parent
        self.item = item
        self.edit = edit
        # close previous edit windows
        if self.parent is not None:
            for child in self.parent.children():
                if type(child) == self.__class__:
                    child.close()
        self.setWindowTitle(self.item[0]["name"])
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize(sizeObject.width() / 2, sizeObject.height() / 2)

        self.ItemWidget = ItemViewWidget(self.item[0], self.edit)
        self.setCentralWidget(self.ItemWidget)

        self.show()


class ItemViewWidget(QWidget):
    def __init__(self, data, edit):
        QWidget.__init__(self)
        self.data = data
        self.edit = edit
        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.openMenu)
        #self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)
        if not self.edit:
            self.treeView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.model = QStandardItemModel()

        layout = QHBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)
        self.treeView.setModel(self.model)
        self.model.setHorizontalHeaderLabels(["Feature", "Wert"])

        self.addItems(self.model, self.data)

    def addItems(self, parent, dict_item):

        for key in dict_item:
            item = QStandardItem(key)
            newParent = item
            # self.model.setData(self.model.index(0, 1), "test")
            if type(dict_item[key]) is list:
                string = ""
                for entry in dict_item[key]:
                    if string is not "":
                        string += "\n"
                    string += entry
                item2 = QStandardItem(string)
                parent.appendRow([item, item2])

            elif type(dict_item[key]) is dict and len(dict_item[key]) == 1 and \
                    list(dict_item[key].keys())[0].lower() in EINHEITEN:
                    einheit = list(dict_item[key].keys())[0]
                    item2 = str(dict_item[key][einheit]) + " (" + einheit +")"
                    item2 = QStandardItem(item2)
                    parent.appendRow([item, item2])

            elif type(dict_item[key]) is dict:
                parent.appendRow(item)
                self.addItems(item, dict_item[key])

            else:
                item2 = QStandardItem(dict_item[key])
                parent.appendRow([item, item2])
        for i in range(self.model.columnCount()):
            self.treeView.resizeColumnToContents(i)

    def openMenu(self, position):
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:
            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1
            # todo implement for editing in viewView only
            '''
            menu = QMenu()
            if level == 0:
                menu.addAction(self.tr("Edit Feature"))
            elif level == 1:
                menu.addAction(self.tr("Edit Wert"))
            action = menu.exec_(self.treeView.viewport().mapToGlobal(position))
            '''
