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
        self.scroll.verticalScrollBar()
        self.scroll.horizontalScrollBar()
        self.scroll.setWidgetResizable(False)
        self.scroll.setMinimumSize(200,200)
        self.scrollContent = QTableWidget(self.scroll)
        #self.scrollContent.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.setCentralWidget(self.scroll)
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.scrollContent.setLayout(self.grid)
        self.scroll.setWidget(self.scrollContent)

        self.counter = 0

    def restart(self):
        self.__init__()

    def doStuff(self):
        for i in range(10):
            test = QTextBrowser()
            test.setText("Test")
            self.addDropDownWidget(test)
        self.scrollContent.resizeColumnsToContents()

    def addDropDownWidget(self, widget):
        DropdownButton(widget, self)
        self.counter += 1

class DropdownButton(QPushButton):
    def __init__(self, widget, itemList, show=True):
        super(DropdownButton, self).__init__()
        self.widget = widget
        self.setText("Test")
        self.itemList = itemList
        self.show = show
        self.itemList.grid.addWidget(self)
        self.clicked.connect(self.toggle_expand)

    def toggle_expand(self):
        grid = self.itemList.grid
        widgetList = []
        if not self.show:
            self.widget.setParent(None)
        else:
            index = grid.indexOf(self)
        while self.itemList.grid.itemAt(0) is not None:
            item = grid.takeAt(0)
            widgetList.append(item.widget())
        if self.show:
            widgetList.insert(index+1, self.widget)
        index = 0
        for entry in widgetList:
            grid.addWidget(entry)
        self.show = not self.show



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    window = ItemList()
    window.doStuff()
    window.show()
    sys.exit(app.exec_())
