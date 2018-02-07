from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QHBoxLayout, QToolButton, QMenu, QTextBrowser,\
    QWidgetAction, QWidget, QApplication, QPushButton, QScrollArea, QVBoxLayout,\
    QGridLayout, QMainWindow, QAbstractScrollArea, QTableWidget


class ItemList(QMainWindow):
    """ creates a scrollable ItemList in which the item entries will be put """
    def __init__(self):
        super(ItemList, self).__init__()
        self.setLayout(QVBoxLayout())
        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.scroll.setMinimumSize(500,250)
        self.scrollContent = QTableWidget(self.scroll)
        #self.scrollContent.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setCentralWidget(self.scroll)
        self.grid = QGridLayout()
        self.scrollContent.setLayout(self.grid)
        self.scroll.setWidget(self.scrollContent)

        self.counter = 0

    def restart(self):
        self.__init__()

    def doStuff(self):
        for i in range(3):
            test = QTextBrowser()
            test.setText("Test")
            self.addDropDownWidget(test)
        self.scrollContent.resizeColumnsToContents()

    def addDropDownWidget(self, widget):
        DropdownButton(widget, self)
        self.counter += 1

class DropdownButton(QPushButton):
    def __init__(self, widget, itemList, toggle = False):
        super(DropdownButton, self).__init__()
        self.widget = widget
        self.setText("Test")
        self.itemList = itemList
        self.toggle = toggle
        self.itemList.grid.addWidget(self)
        self.clicked.connect(self.toggle_expand)

    def toggle_expand(self):
        grid = self.itemList.grid
        if not self.toggle:
            index = grid.indexOf(self)
            widgetList = []
            while grid.itemAt(0) is not None:
                item = grid.takeAt(0)
                widgetList.append(item.widget())
            widgetList.insert(index+1, self.widget)
            index = 0
            for entry in widgetList:
                index += 1
                grid.addWidget(entry, index, 0)
            # self.widget.setParent(self)
        else:
            self.widget.setParent(None)
            widgetList = []
            while self.itemList.grid.itemAt(0) is not None:
                item = grid.takeAt(0)
                widgetList.append(item.widget())
            for entry in widgetList:
                self.itemList.grid.addWidget(entry)
            self.resize(self.sizeHint())
            self.widget.resize(self.widget.sizeHint())
            self.itemList.resize(self.itemList.sizeHint())
        self.toggle = not self.toggle



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ItemList()
    window.doStuff()
    window.show()
    sys.exit(app.exec_())
