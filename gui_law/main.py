import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from centralTable import CentralTable
from creatorView import CreatorView
from jsonHandler import ICON_PATH
import functools
# from screeninfo import get_monitors


class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralTable = CentralTable(self)
        self.setCentralWidget(self.centralTable)
        self.initUI()

    def initUI(self):
        """ initialises the mainWindow at the center to half the size of the
            resolution """
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
        toolbar = self.addToolBar('Edit')
        toolbar.setIconSize(QSize(32,32))
        self.initMenubar(menubar, toolbar)

        self.show()

    def initMenubar(self, menubar, toolbar):
        menubarRight = QMenuBar()

        """ adds a Menubar to the mainWindow """
        # todo add functions later
        fileMenu = menubar.addMenu('Datei')
        editMenu = menubar.addMenu('Bearbeiten')
        viewMenu = menubar.addMenu('Ansicht')
        searchMenu = menubar.addMenu('Suche')
        # toolsMenu = menubar.addMenu('Werkzeuge')
        # helpMenu = menubar.addMenu('Hilfe')
        newMachine = QAction('Maschine hinzufügen', self)
        newMachine.triggered.connect(lambda: self.create_CreatorView())
        newMachine.setShortcut("Ctrl+N")
        fileMenu.addAction(newMachine)
        newMachine_2 = QAction(QIcon(ICON_PATH+"add.png"), '', self)
        newMachine_2.setIcon
        newMachine_2.setToolTip("Maschine hinzufügen")
        newMachine_2.triggered.connect(lambda: self.create_CreatorView())
        # menubarRight.addAction(newMachine_2)
        toolbar.addAction(newMachine_2)
        menubar.setCornerWidget(toolbar)
        menubar.adjustSize()
        # menubar.setCornerWidget(menubar)

        refresh = QAction('Erneut Laden', self)
        refresh.setShortcut("F5")
        refresh.triggered.connect(lambda: self.centralTable.reload_list())
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
            action.triggered.connect(functools.partial(self.centralTable.order_list, features[i], descending))
            menu.addAction(action)

    def create_CreatorView(self):
        self.creatorView = CreatorView(self, centralTable = self.centralTable)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = QTranslator(app) # no idea if it works due to my system set to english
    locale = QLocale.system().name()
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator.load('qt_%s' % locale, path)
    app.installTranslator(translator)
    ex = mainWindow()
    sys.exit(app.exec_())
