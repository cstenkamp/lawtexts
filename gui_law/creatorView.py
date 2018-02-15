import sys
import os
import jsonHandler
from ExtendedComboBox import ExtendedComboBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

MY_PATH = os.path.abspath(os.path.dirname(__file__))
JSON_PATH = os.path.abspath(os.path.join(MY_PATH, os.pardir)) + "/python_code/Main/json/"

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

class ItemCreatorWidget(QTreeWidget):
    """ The widget for creating new machines """
    def __init__(self):
        QTreeWidget.__init__(self)
        self.setHeaderLabels(["Feature", "Wert"])

        self.createStartEntries(self.model)

    def createStartEntries(self, model):
        self.jsonFile = {"Name":"", "Kundennummer":"", "Ort":"", "Herstellungsdatum":"", "Prüfdatum":""}
        for entry in list(self.jsonFile.keys()):
            featureValuePair = QTreeWidgetItem([entry, ""])
            self.addTopLevelItem(featureValuePair)
        ## TODO delete later
        tooltip = "Hier klicken um eine neue Komponente zu erstellen"
        button = QPushButton()
        button.setText( "Komponent +")
        button.clicked.connect( self.openComponentCreator )
        # tmp0 = CustomTreeWidgetItem(self, button, position = 0)

        self.combo = ExtendedComboBox()

        self.parts = jsonHandler.read_json_file(JSON_PATH + "/parts.json")
        self.combo.addItems(list(self.parts.keys()))
        # tmp1 = CustomTreeWidgetItem(self, combo)
        CustomTreeWidgetItems(self, [button, self.combo])
        # self.addTopLevelItems([tmp0, tmp1])

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

    def openComponentCreator(self):
        print(self.combo.currentText())
        # if "Komponenten" not in list(self.jsonFile.keys())
        # self.compCreator = ComponentCreatorWidget()


class CustomTreeWidgetItem( QTreeWidgetItem ):
    """ Creates a custom QTreeWidgetItem out of the given widget """
    def __init__( self, parent, widget, position = 1):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeWidgetItem, self ).__init__( parent )
        parent.setItemWidget( self, position, widget )

class CustomTreeWidgetItems( QTreeWidgetItem ):
    """ Creates a custom QTreeWidgetItem out of the given widget """
    def __init__( self, parent, widgets, startingPos = 0):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeWidgetItems, self ).__init__( parent )
        for i in range(len(widgets)):
            parent.setItemWidget( self, startingPos + i, widgets[i] )
        # parent.addTopLevelItems(treeWidgets)

class ComponentCreatorWidget(QWidget):
    """ The widget for creating new Components """
    def __init__(self):
        QWidget.__init__(self)




if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = CreatorView()
    window.show()
    sys.exit(app.exec_())
