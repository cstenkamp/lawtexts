import sys
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CreatorView(QMainWindow):
    """ creates a ItemOverview over the given @item, @edit = readOnly? """
    def __init__(self, parent=None):
        super(CreatorView, self).__init__(parent)
        self.parent = parent
        # close previous edit windows
        if self.parent is not None:
            for child in self.parent.children():
                if type(child) == self.__class__:
                    child.close()
        self.setWindowTitle("Machine Creator")
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize(sizeObject.width() / 2, sizeObject.height() / 2)

        self.ItemCreatorWidget = ItemCreatorWidget()
        self.setCentralWidget(self.ItemCreatorWidget)

        self.show()

class ItemCreatorWidget(QWidget):
    """ The widget for creating new machines """
    def __init__(self):
        QWidget.__init__(self)
        self.treeView = QTreeView()
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.treeView.customContextMenuRequested.connect(self.openMenu)
        # self.treeView.setRootIsDecorated(False)
        self.treeView.setAlternatingRowColors(True)

        self.model = QStandardItemModel()

        layout = QHBoxLayout()
        layout.addWidget(self.treeView)
        self.setLayout(layout)
        self.treeView.setModel(self.model)
        # self.model.dataChanged.connect(self.item_changed)
        self.model.setHorizontalHeaderLabels(["Feature", "Wert"])

        self.createStartEntries(self.model)

    def createStartEntries(self, model):
        self.jsonFile = {"Name":"", "Kundennummer":"", "Ort":"", "Herstellungsdatum":"", "Prüfdatum":""}
        for entry in list(self.jsonFile.keys()):
            featureValuePair = [QStandardItem(entry), QStandardItem("")]
            model.appendRow(featureValuePair)
        addComponentBtn = QPushButton(self.ItemCreatorWidget)
        addComponentBtn.setToolTip("Hier klicken um eine neue Komponente zu erstellen")
        addComponentBtn.clicked.connect(self.ComponentCreatorWidget())

        for i in range(self.model.columnCount()):
            self.treeView.resizeColumnToContents(i)

class ComponentCreatorWidget(QWidget):
    """ The widget for creating new Components """
    def __init__(self):
        QWidget.__init__(self)
        



if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = CreatorView()
    window.show()
    sys.exit(app.exec_())
