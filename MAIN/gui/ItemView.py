import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from jsonHandler import *

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
        self.setWindowTitle(self.item[0]["Name"])
        menubar = self.menuBar()
        self.initMenubar(menubar)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize(sizeObject.width() / 2, sizeObject.height() / 2)

        self.ItemWidget = ItemViewWidget(self.item[0], self.item[1], self.edit)
        self.setCentralWidget(self.ItemWidget)

        self.show()

    def initMenubar(self, menubar):
        """ adds a Menubar to the mainWindow """
        # todo add functions later
        fileMenu = menubar.addMenu('Datei')
        #searchMenu = menubar.addMenu('Search')

        save = QAction('Speichern', self)
        save.setShortcut('Ctrl+S')
        # lamda necessary in order to make it callable
        save.triggered.connect(lambda: write_json_file(self.item[0], self.item[1]))
        save.triggered.connect(lambda: self.parent.reload_list())
        saveAs = QAction('Speichern als', self)
        fileMenu.addAction(save)
        fileMenu.addAction(saveAs)
        # TODO add saveAs


class ItemViewWidget(QWidget):
    def __init__(self, data, path, edit):
        QWidget.__init__(self)
        self.data = data
        self.path = path
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
        self.model.dataChanged.connect(self.item_changed)
        self.model.setHorizontalHeaderLabels(["Feature", "Wert"])

        self.addItems(self.model, self.data)

    def item_changed(self, index, index2, roles):
        if index.isValid():
            newData = index2.data()
            key = index.sibling(index.row(), 0).data()
            parentList = []
            item = self.data
            while index2.parent().isValid():
                index2 = index2.parent()
                parentList.append(index2.data())
            if parentList is not []:
                while len(parentList) > 0:
                    item = item[parentList.pop()]
            item[key] = newData


    def addItems(self, parent, dict_item):
        order_list = list(dict_item.keys())
        if all(entries in ORDER for entries in list(dict_item.keys())):
            order_list = ORDER
        elif all(entries in ORDER+ ["Kommentare"] for entries in list(dict_item.keys())):
            order_list = ORDER + ["Kommentare"]
        else:
            order_list.sort()
        for key in order_list:
            item = QStandardItem(key)
            item.setEditable(False)
            newParent = item

            # self.model.setData(self.model.index(0, 1), "test")
            if type(dict_item[key]) is list:
                # in case of it being a component
                if len(dict_item[key]) > 0 and type(dict_item[key][0]) is dict:
                        for entry in dict_item[key]:
                            item = QStandardItem(key)
                            item.setEditable(False)
                            parent.appendRow(item)
                            self.addItems(item, entry)
                # in case of it being "Verwenungszweck/ort, Kommentar"
                else:
                    parent.appendRow(item)
                    string = ""
                    for entry in dict_item[key]:
                        item.appendRow([QStandardItem(""), QStandardItem(entry)])
                    self.treeView.setExpanded(item.index(), True)
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
