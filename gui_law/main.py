import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget, \
        QDesktopWidget
from centralTable import CentralTable
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
        fileMenu = menubar.addMenu('File')
        editMenu = menubar.addMenu('Edit')
        viewMenu = menubar.addMenu('View')
        searchMenu = menubar.addMenu('Search')
        toolsMenu = menubar.addMenu('Tools')
        helpMenu = menubar.addMenu('Help')





if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mainWindow()
    sys.exit(app.exec_())
