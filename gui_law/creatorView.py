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
        self.components = []

        self.ItemCreatorWidget = ItemCreatorWidget()
        self.setCentralWidget(self.ItemCreatorWidget)

        self.show()

class ItemCreatorWidget(QTreeWidget):
    """ The widget for creating new machines """
    def __init__(self):
        QTreeWidget.__init__(self)
        self.setHeaderLabels(["Feature", "Einheit", "Wert"])
        self.model = QStandardItemModel()
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.createStartEntries(self.model)

    def createStartEntries(self, model):
        self.jsonFile = {"Name":"", "Kundennummer":"", "Ort":"", "Herstellungsdatum":"", "Prüfdatum":""}
        self.parts = jsonHandler.read_json_file(JSON_PATH + "/parts.json")
        self.features = jsonHandler.read_json_file(JSON_PATH + "/features.json")["Features"]
        self.contents = jsonHandler.read_json_file(JSON_PATH + "/contents.json")

        for entry in list(self.jsonFile.keys()):
            tmp = QTreeWidgetItem(["placeHolder"])
            self.addTopLevelItem(tmp)
            CustomTreeWidgetItems(self, [entry,QLineEdit()],[0,2],placeHolder = tmp)
        self.firstComponent = True
        tooltip = "Hier klicken um eine neue Komponente zu erstellen"
        button = QPushButton()
        button.setText( "Komponent +")
        button.setMinimumSize(25,10)
        button.clicked.connect( self.openComponentCreator )
        # tmp0 = CustomTreeWidgetItem(self, button, position = 0)

        self.combo = ExtendedComboBox(self)
        self.combo.addItems(list(self.parts.keys()))
        # tmp1 = CustomTreeWidgetItem(self, combo)
        self.addComponents = CustomTreeWidgetItems(self, [button, self.combo],[0,2])
        # self.addTopLevelItems([tmp0, tmp1])

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

    def openComponentCreator(self):
        component = self.combo.currentText()
        if component not in self.parts:
            self.combo.setCurrentText("")
            self.combo.showPopup()
            return
        if self.firstComponent:
            self.firstComponent = False
            self.compItem = QTreeWidgetItem(["Komponenten"])
            index = self.indexOfTopLevelItem(self.addComponents)
            self.insertTopLevelItem(index, self.compItem)
            self.compItem.setExpanded(True)
            self.jsonFile[component] = {}
        component_features = self.parts[component]["Eigenschaften"]
        item = QTreeWidgetItem([component])
        self.compItem.addChild(item)
        item.setExpanded(True)
        for feature in component_features:
            self.jsonFile[component][feature] = ""
            tmp = QTreeWidgetItem(["placeHolder"])
            item.addChild(tmp)
            if feature in list(self.features.keys()):
                cur_feature = self.features[feature]
                spinBox = QSpinBox()
                spinBox.setValue( 0 )
                spinBox.setMinimumSize(25,10)
                unitBox = ExtendedComboBox()
                unitBox.addItems(cur_feature)
                CustomTreeWidgetItems(self, [str(feature), unitBox, spinBox], range(3), placeHolder=tmp)

            elif feature == "Inhalt":
                contentBox = ExtendedComboBox()
                contentBox.addItems(self.contents["Inhalt"])
                unitBox = ExtendedComboBox()
                unitBox.addItems(self.contents["Aggregatszustand"])
                self.compItem.addChild(tmp)
                CustomTreeWidgetItems(self,[str(feature),unitBox, contentBox],range(3), placeHolder=tmp)

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)
        print(self.jsonFile)
'''
class featureCreatorWidget(QTreeWidget):
    def __init__(self, parent, cur_feature)
'''


class CustomTreeWidgetItem( QTreeWidgetItem ):
    """ Creates a custom QTreeWidgetItem out of the given widget """
    def __init__( self, treeWidget, widget, position = 1, placeHolder = None):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeWidgetItem, self ).__init__( treeWidget )
        if placeHolder is None:
            treeWidget.setItemWidget( self, position, widget )
        else:
            treeWidget.setItemWidget( placeHolder, position, widget)

class CustomTreeWidgetItems( QTreeWidgetItem ):
    """ Creates a custom QTreeWidgetItem out of the given widget """
    def __init__( self, treeWidget, widgets, position, placeHolder= None):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeWidgetItems, self ).__init__( treeWidget )
        for i in range(len(widgets)):
            if placeHolder is None:
                if type(widgets[i]) is str:
                    self.setText( position[i], widgets[i] )
                else:
                    treeWidget.setItemWidget( self, position[i], widgets[i] )
            else:
                if type(widgets[i]) is str:
                    placeHolder.setText( position[i], widgets[i] )
                else:
                    treeWidget.setItemWidget( placeHolder, position[i], widgets[i] )

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = CreatorView()
    window.show()
    sys.exit(app.exec_())
