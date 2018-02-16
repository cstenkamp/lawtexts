import sys
import os
from jsonHandler import *
from ExtendedComboBox import ExtendedComboBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CreatorView(QMainWindow):
    """ creates a ItemOverview over the given @item, @edit = readOnly? """
    def __init__(self, parent=None, centralTable = None):
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

        self.ItemCreatorWidget = ItemCreatorWidget(self, centralTable)
        self.setCentralWidget(self.ItemCreatorWidget)
        menuBar = self.menuBar()
        self.initMenubar(menuBar)

        self.show()

    def initMenubar(self, menubar):
        """ adds a Menubar to the mainWindow """
        # todo add functions later
        fileMenu = menubar.addMenu('Datei')
        searchMenu = menubar.addMenu('Suche')
        save = QAction('Speichern', self)
        save.setShortcut('Ctrl+S')
        # lamda necessary in order to make it callable
        save.triggered.connect(lambda: self.ItemCreatorWidget.save_file())
        # save.triggered.connect(lambda: self.parent.reload_list())
        saveAs = QAction('Speichern als', self)
        fileMenu.addAction(save)
        fileMenu.addAction(saveAs)
        # TODO add saveAs


class ItemCreatorWidget(QTreeWidget):
    """ The widget for creating new machines """
    def __init__(self, parent=None, centralTable = None):
        self.parent = parent
        self.centralTable = centralTable
        QTreeWidget.__init__(self)
        self.setHeaderLabels(["Feature", "Einheit", "Wert"])
        self.model = QStandardItemModel()
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.createStartEntries(self.model)
        # self.itemClicked.connect(self.item_changed)
        # self.model.dataChanged.connect(self.item_changed)
        self.itemChanged.connect(self.item_changed)

    def createStartEntries(self, model):
        self.jsonFile = {"Name":"", "Kundennummer":"", "Ort":"", "Herstellungsdatum":"2000", \
                         "Prüfdatum":"2000", "Komponenten":{}, "Verwendungszwecke":[], "Verwendungsorte": []}
        self.minEntries = ORDER[0:5]
        self.parts = read_json_file(JSON_PATH + "/parts.json")
        self.features = read_json_file(JSON_PATH + "/features.json")["Features"]
        self.contents = read_json_file(JSON_PATH + "/contents.json")
        self.purposes = read_json_file(JSON_PATH + "/_purposes.json")
        self.sites = read_json_file(JSON_PATH + "/sites.json")
        self.firstComponent = self.boolObject(True)
        self.firstVZweck = self.boolObject(True)
        self.firstVOrt = self.boolObject(True)

        for entry in self.minEntries:
            tmp = QTreeWidgetItem(["placeHolder"])
            self.addTopLevelItem(tmp)
            if "datum" in entry:
                dateEdit = QDateEdit()
                dateEdit.setDisplayFormat("dd.MM.yyyy")
                CustomTreeWidgetItems(self, [entry, dateEdit], [0,2], placeHolder = tmp)

            else:
                CustomTreeWidgetItems(self, [entry, QLineEdit()], [0,2], placeHolder = tmp)

        tooltip = "Hier klicken um eine neue Komponente zu erstellen"
        self.combo = ExtendedComboBox(self)
        self.combo.setInsert(False)
        self.combo.addItems(list(self.parts.keys()))
        btn, self.addComponents = self.QTreeAddButtonMenu("Komponente +", self.combo, tooltip)
        btn.clicked.connect(lambda: self.addExtComboBoxEdit(\
            list(self.parts.keys()), self.combo, \
            self.firstComponent, self.addComponents, "Komponenten") )

        self.vZweckCombo = ExtendedComboBox(self)
        list_keys = list(self.purposes.keys())
        list_keys.sort()
        self.vZweckCombo.addItems(list_keys)
        btn, self.addVZweck = self.QTreeAddButtonMenu("Verwendungszwecke +", self.vZweckCombo)
        btn.clicked.connect(lambda: self.addExtComboBoxEdit(\
            list(self.purposes.keys()), self.vZweckCombo, \
            self.firstVZweck, self.addVZweck, "Verwendungszwecke") )

        self.vOrtCombo = ExtendedComboBox(self)
        list_keys = list(self.sites.keys())
        list_keys.sort()
        self.vOrtCombo.addItems(list_keys)
        btn, self.addVOrt = self.QTreeAddButtonMenu("Verwendungsorte +", self.vOrtCombo)
        btn.clicked.connect(lambda: self.addExtComboBoxEdit(\
            list(self.sites.keys()), self.vOrtCombo, \
            self.firstVOrt, self.addVOrt, "Verwendungsorte") )

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

    def QTreeAddButtonMenu(self, buttonText, widget, tooltip = None):
        button = QPushButton()
        button.setText(buttonText)
        button.setMinimumSize(175,10)
        button.setToolTip(tooltip)

        item = CustomTreeWidgetItems(self, [button, widget],[0,2], connect=False)
        return [button, item]

    class boolObject():
        def __init__(self, boolToObj):
            self.bool = boolToObj
        def getBool(self):
            return self.bool
        def setBool(self, boolToSet):
            self.bool = boolToSet

    def addExtComboBoxEdit(self, listDic, exComboBox, first, addBtn, key ):
        purpose = exComboBox.currentText()
        if not exComboBox.insert and purpose not in listDic:
            exComboBox.setCurrentText("")
            exComboBox.showPopup()
            return
        if first:
            first.setBool(False)
            parent = QTreeWidgetItem([key])
            index = self.indexOfTopLevelItem(addBtn)
            self.insertTopLevelItem(index, parent)
            parent.setExpanded(True)

        if key is not "Komponenten":
            self.jsonFile[key].append(purpose)
            tmpLineEdit = QLineEdit()
            tmpLineEdit.setText(purpose)
            tmpLineEdit.setReadOnly(True)
            placeHolder = QTreeWidgetItem([""])
            parent.addChild(placeHolder)
            CustomTreeWidgetItems(self, [tmpLineEdit],[2], connect=False, placeHolder=placeHolder)
        else:
            self.openComponentCreator(purpose, parent)

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

    def openComponentCreator(self, component, parent):
        self.jsonFile["Komponenten"][component] = {}
        component_features = self.parts[component]["Eigenschaften"]
        item = QTreeWidgetItem([component])
        parent.addChild(item)
        item.setExpanded(True)
        for feature in component_features:
            tmp = QTreeWidgetItem(["placeHolder"])
            item.addChild(tmp)
            if feature in list(self.features.keys()):
                cur_feature = self.features[feature]
                spinBox = QDoubleSpinBox()
                spinBox.setValue( 0 )
                spinBox.setMaximum(99999.99)
                spinBox.setMinimumSize(25,10)
                unitBox = QComboBox()
                unitBox.addItems(cur_feature)
                self.jsonFile["Komponenten"][component][feature] = {cur_feature[0]:0}
                CustomTreeWidgetItems(self, [str(feature), unitBox, spinBox], range(3), placeHolder=tmp)

            elif feature == "Inhalt":
                contentBox = QComboBox()
                contentBox.addItems(self.contents["Inhalt"])
                unitBox = QComboBox()
                unitBox.addItems(self.contents["Aggregatszustand"])
                parent.addChild(tmp)
                self.jsonFile["Komponenten"][component][feature] = {unitBox.currentText(): contentBox.currentText()}
                CustomTreeWidgetItems(self,[str(feature),unitBox, contentBox],range(3), placeHolder=tmp)

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

    def item_changed(self, item, _NotWorking):
        parItem= item
        parentList = []
        while parItem.parent() is not None:
            parItem = parItem.parent()
            parentList.append(parItem.text(0))

        if type(item) is CustomTreeWidgetItems:
            nonTreeWidgets, pos = item.widgets_and_position()
            key = nonTreeWidgets[0]
            unit = None
            valueAt = 1
            if 1 in pos:
                unit = nonTreeWidgets[1].currentText()
                valueAt += 1
            value = None
            if type(nonTreeWidgets[valueAt]) is QLineEdit:
                value = nonTreeWidgets[valueAt].text()
            elif type(nonTreeWidgets[valueAt]) is QDoubleSpinBox:
                value = nonTreeWidgets[valueAt].value()
            elif type(nonTreeWidgets[valueAt]) is QComboBox:
                value = nonTreeWidgets[valueAt].currentText()
            elif type(nonTreeWidgets[valueAt]) is QDateEdit:
                value = str(nonTreeWidgets[valueAt].date().year())
            json = self.jsonFile
            while parentList != []:
                json = json[parentList.pop()]
            if unit is None:
                json[key]=value
            else:
                json[key] = {unit:value}

    def save_file(self):
        if any(self.jsonFile[key] == "" for key  in self.minEntries) or "Komponenten" not in self.jsonFile:
            minEntriesBold = ["<b>"+str(x)+",</b>" for x in self.minEntries]
            requiredFields = "\n"+ "\n".join(str(x) for x in minEntriesBold)
            QMessageBox.about(self, "", "Bitte fügen Sie <b>mindestenes eine Komponente</b> hinzu"\
                "und füllen Sie mindestens folgende Felder aus:" + requiredFields)

        else:
            self.start_check()
            fileName = MACHINE_PATH + self.jsonFile["Name"]
            i = 1
            while os.path.exists(fileName):
                fileName += str(i)
                i += 1
            write_json_file(self.jsonFile, fileName)
            if self.centralTable is not None:
                self.centralTable.reload_list()

    def start_check(self):
        print("creatorView.py Methodenname: startCheck")
        print("this method is currently called when the user tries to save the file")


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
    def __init__( self, treeWidget, widgets, position, placeHolder= None, connect = True):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeWidgetItems, self ).__init__( treeWidget )
        self.widgets = widgets
        self.parent = None
        self.position = position
        for i in range(len(widgets)):
            if placeHolder is None:
                placeHolder = self
            else:
                self.parent = lambda: placeHolder.parent()
            if type(widgets[i]) is str:
                placeHolder.setText( position[i], widgets[i] )
            else:
                treeWidget.setItemWidget( placeHolder, position[i], widgets[i] )
                if connect:
                    if type(widgets[i]) is QLineEdit:
                        widgets[i].textChanged.connect(lambda: self.emitDataChanged())
                    elif type(widgets[i]) is QDoubleSpinBox:
                        widgets[i].valueChanged.connect(lambda: self.emitDataChanged())
                    elif type(widgets[i]) is QComboBox:
                        widgets[i].currentTextChanged.connect(lambda: self.emitDataChanged())
                    elif type(widgets[i]) is QDateEdit:
                        widgets[i].dateChanged.connect(lambda: self.emitDataChanged())

    def widgets_and_position(self):
        return [self.widgets, self.position]
    def parent(self):
        return self.parent


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = CreatorView()
    window.show()
    sys.exit(app.exec_())
