import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from centralTable import CentralTable
from creatorView import CreatorView
import functools
# from screeninfo import get_monitors


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.CentralTable = CentralTable(self)
        self.setCentralWidget(self.CentralTable)
        self.initUI()

    def initUI(self):
        """ initialises the mainWindow at the center to half the size of the
            resolution """
        self.statusBar()
        # center window
        self.title = 'Prototyp LawText'
        self.setWindowTitle(self.title)
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize(sizeObject.width() / 2, sizeObject.height() / 2)
        # set window in center
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        menubar = self.menuBar()

        self.initMenubar(menubar)
        self.show()

    def initMenubar(self, menubar):
        """ adds a Menubar to the mainWindow """
        # todo add functions later
        fileMenu = menubar.addMenu('Datei')
        editMenu = menubar.addMenu('Bearbeiten')
        viewMenu = menubar.addMenu('Ansicht')
        searchMenu = menubar.addMenu('Suche')
        toolsMenu = menubar.addMenu('Werkzeuge')
        helpMenu = menubar.addMenu('Hilfe')

        newMachine = QAction('Maschine hinzufügen', self)
        newMachine.setShortcut("Ctrl+N")
        newMachine.triggered.connect(lambda: self.create_CreatorView())
        fileMenu.addAction(newMachine)

        refresh = QAction('Erneut Laden', self)
        refresh.setShortcut("F5")
        refresh.triggered.connect(lambda: self.CentralTable.reload_list())
        editMenu.addAction(refresh)

        #orderMenus
        features = ["Name", "Kundennummer", "Ort", "Herstellungsdatum", "Prüfdatum"]
        orderMDescF = viewMenu.addMenu('Sortiere aufsteigend')
        orderMDescT = viewMenu.addMenu('Sortiere absteigend')
        self.fill_order_menu(features, orderMDescF, False)
        self.fill_order_menu(features, orderMDescT, True)

    def fill_order_menu(self, features, menu, descending):
        for i in range(len(features)):
            action = QAction(features[i], self)
            action.triggered.connect(functools.partial(self.CentralTable.order_list, features[i], descending))
            menu.addAction(action)

    def create_CreatorView(self):
        self.creatorView = CreatorView(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
