import sys
import os
from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget
from centralTable import centralTable
from screeninfo import get_monitors

class mainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.centralTable = centralTable(self)
        self.setCentralWidget(self.centralTable)

        self.initUI()

    def initUI(self):
        self.statusBar()
        # center window
        self.title = 'Prototyp LawText'
        self.setWindowTitle(self.title)
        self.resize(get_monitors()[0].width / 2, get_monitors()[0].height / 2)
        # set window in center
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

        menubar = self.menuBar()

        self.initMenubar(menubar)
        self.show()

    # todo do the actual menu
    def initMenubar(self, menubar):
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
