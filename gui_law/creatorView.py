import sys
import os
from jsonHandler import *
from ExtendedComboBox import ExtendedComboBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class CreatorView(QMainWindow):
    """ creates a Widget to create a Machine """
    def __init__(self, parent=None, centralTable = None, jsonFile = None):
        super(CreatorView, self).__init__(parent)
        if parent is not None:
            self.parent = parent
        else:
             self.parent = None
        if centralTable is not None:
            self.centralTable = centralTable
        else:
            self.centralTable = None
        # close previous edit windows
        if self.parent is not None:
            for child in self.parent.children():
                if type(child) == self.__class__:
                    child.close()
        self.setWindowTitle("Machine Creator")
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize(sizeObject.width() / 2, sizeObject.height() / 2)
        self.components = []

        self.ItemCreatorWidget = ItemCreatorWidget(self, centralTable, jsonFile=jsonFile)
        self.setCentralWidget(self.ItemCreatorWidget)
        menuBar = self.menuBar()
        self.initMenubar(menuBar)
        self.show()

    def initMenubar(self, menubar):
        """ adds a Menubar to the Window """
        # todo add functions later
        fileMenu = menubar.addMenu('Datei')
        searchMenu = menubar.addMenu('Suche')
        save = QAction('Speichern', self)
        save.setShortcut('Ctrl+S')
        # lamda necessary in order to make it callable
        save.triggered.connect(lambda: self.ItemCreatorWidget.save_file())
        if self.centralTable is not None:
            save.triggered.connect(lambda: self.centralTable.reload_list())
        saveAs = QAction('Speichern als', self)
        fileMenu.addAction(save)
        fileMenu.addAction(saveAs)
        # TODO add saveAs

    def setJsonFile(self, json):
        self.ItemCreatorWidget.setJsonFile(json)


class ItemCreatorWidget(QTreeWidget):
    """ The widget for creating new machines """
    def __init__(self, parent=None, centralTable = None, jsonFile = None):
        self.parent = parent
        self.centralTable = centralTable
        QTreeWidget.__init__(self)
        self.setHeaderLabels(["Feature", "Einheit", "Wert"])
        self.model = QStandardItemModel()
        self.setSelectionMode(QAbstractItemView.NoSelection)
        if jsonFile is None:
            self.jsonFile = {"Name":"", "Kundennummer":"", "Ort":"", \
                "Herstellungsdatum":"2000", "Prüfdatum":"2000", "Komponenten":{},\
                 "Verwendungszwecke":[], "Verwendungsorte": [], "Kommentare": []}
        else:
            self.jsonFile = jsonFile
        self.createStartEntries(self.model)
        if jsonFile is not None:
            self.loadJson()
        self.itemClicked.connect(self.item_changed)
        self.model.dataChanged.connect(self.item_changed)
        self.itemChanged.connect(self.item_changed)

    def createStartEntries(self, model):
        """ creates all the required fields and buttons in order to create a machine """
        self.minEntries = ORDER[0:5]
        self.parts = read_json_file(JSON_PATH + "/parts.json")
        self.features = read_json_file(JSON_PATH + "/features.json")["Features"]
        self.contents = read_json_file(JSON_PATH + "/contents.json")
        self.purposes = read_json_file(JSON_PATH + "/_purposes.json")
        self.sites = read_json_file(JSON_PATH + "/sites.json")
        self.firstComponent = self.boolObject(True)
        self.firstVZweck = self.boolObject(True)
        self.firstVOrt = self.boolObject(True)
        self.firstComment = self.boolObject(True)

        for entry in self.minEntries:
            tmp = QTreeWidgetItem(["placeHolder"]) # required in order to put costom widgets at the right position
            self.addTopLevelItem(tmp)
            if "datum" in entry:
                dateEdit = QDateEdit(QDate(int(self.jsonFile[entry]),1,1))
                dateEdit.setDisplayFormat("dd.MM.yyyy")
                CustomTreeWidgetItems(self, [entry, dateEdit], [0,2], placeHolder = tmp)

            else:
                CustomTreeWidgetItems(self, [entry, QLineEdit(self.jsonFile[entry])], [0,2], placeHolder = tmp)

        tooltip = "Hier klicken um eine neue Komponente zu erstellen"
        self.combo = ExtendedComboBox(self)
        self.combo.setInsert(False)
        self.combo.addItems(list(self.parts.keys()))
        self.btn_comp, self.addComponents = self.QTreeAddButtonMenu("Komponente +", self.combo, tooltip)
        self.btn_comp.clicked.connect(lambda: self.addExtComboBoxEdit(\
            list(self.parts.keys()), self.combo, \
            self.firstComponent, self.addComponents, "Komponenten") )

        vZweckCombo = ExtendedComboBox(self)
        list_keys = list(self.purposes.keys())
        list_keys.sort()
        vZweckCombo.addItems(list_keys)
        self.btn_vZweck, self.addVZweck = self.QTreeAddButtonMenu("Verwendungszwecke +", vZweckCombo)
        self.btn_vZweck.clicked.connect(lambda: self.addExtComboBoxEdit(\
            list(self.purposes.keys()), vZweckCombo, \
            self.firstVZweck, self.addVZweck, "Verwendungszwecke") )

        vOrtCombo = ExtendedComboBox(self)
        list_keys = list(self.sites.keys())
        list_keys.sort()
        vOrtCombo.addItems(list_keys)
        self.btn_vOrt, self.addVOrt = self.QTreeAddButtonMenu("Verwendungsorte +", vOrtCombo)
        self.btn_vOrt.clicked.connect(lambda: self.addExtComboBoxEdit(\
            list(self.sites.keys()), vOrtCombo, \
            self.firstVOrt, self.addVOrt, "Verwendungsorte") )

        self.btn_comment, self.addComment = self.addCommentEdit()

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

    def loadJson(self):
        """ loads the json parts with childs into the widget """
        keys = ["Komponenten", "Verwendungszwecke", \
                "Verwendungsorte", "Kommentare"]
        first_list = [self.firstComponent, self.firstVZweck, \
                      self.firstVOrt, self.firstComment]
        add_list = [self.addComponents, self.addVZweck, \
                    self.addVOrt, self.addComment]
        for i in range(len(keys)):
            cur_dict = self.jsonFile[keys[i]]
            first = first_list[i]
            if cur_dict == []:
                continue
            first.setBool(False)
            parent = QTreeWidgetItem([keys[i]])
            first.setParent(parent)
            index = self.indexOfTopLevelItem(add_list[i])
            self.insertTopLevelItem(index, parent)
            parent.setExpanded(True)
            if keys[i] is not "Komponenten":
                text_list = self.jsonFile[keys[i]]
                text_list.sort()
                for text in text_list:
                    tmpLineEdit = QLineEdit()
                    tmpLineEdit.setText(text)
                    tmpLineEdit.setReadOnly(True)
                    placeHolder = QTreeWidgetItem([""])
                    parent.addChild(placeHolder)
                    CustomTreeWidgetItems(self, [tmpLineEdit],[2], connect=False, placeHolder=placeHolder)
            else:
                comp_list = list(self.jsonFile[keys[i]].keys())
                comp_list.sort()
                for component in comp_list:
                    self.openComponentCreator(component, parent, self.jsonFile[keys[i]][component])

    def addCommentEdit(self, parent=None):
        """ adds a QLineEdit + Button in order to add comments """
        lineEdit = QLineEdit()
        btn, addLineEdit = self.QTreeAddButtonMenu("Kommentare +", lineEdit)
        btn.clicked.connect(lambda: self.addExtComboBoxEdit([], lineEdit, \
                            self.firstComment, addLineEdit, "Kommentare") )
        return btn, addLineEdit

    def QTreeAddButtonMenu(self, buttonText, widget, tooltip = None):
        """ adds a Button to the QTree and returns the buton and the TreeWidget """
        button = QPushButton()
        button.setText(buttonText)
        button.setMinimumSize(175,10)
        button.setToolTip(tooltip)

        item = CustomTreeWidgetItems(self, [button, widget],[0,2], connect=False)
        return [button, item]

    class boolObject():
        """ stores a boolean value and an attached Widget """
        def __init__(self, boolToObj):
            self.bool = boolToObj
            self.parent = None
        def getBool(self):
            return self.bool
        def setBool(self, boolToSet):
            self.bool = boolToSet
        def setParent(self, parent):
            self.parent = parent
        def getParent(self):
            return self.parent

    def addExtComboBoxEdit(self, listDic, exComboBox, first, addBtn, key ):
        """ adds an (extended) ComboBox to the view """
        if type(exComboBox) is ExtendedComboBox:
            purpose = exComboBox.currentText()
            if not exComboBox.insert and purpose not in listDic:
                exComboBox.setCurrentText("")
                exComboBox.showPopup() # if empty test load the popup
                return
        elif type(exComboBox) is QLineEdit:
            purpose = exComboBox.text()
            if purpose is "":
                return
            else:
                exComboBox.setText("")
        # creates the parent entry in the Qtree
        if first.getBool():
            first.setBool(False)
            parent = QTreeWidgetItem([key])
            first.setParent(parent)
            index = self.indexOfTopLevelItem(addBtn)
            self.insertTopLevelItem(index, parent)
            parent.setExpanded(True)
        else:
            parent = first.getParent()

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

    def openComponentCreator(self, component, parent, valueDict=None):
        """ adds components to the view """
        self.jsonFile["Komponenten"][component] = {}
        component_features = self.parts[component]["Eigenschaften"]
        component_features.sort()
        item = QTreeWidgetItem([component])
        parent.addChild(item)
        item.setExpanded(True)
        for i in range(len(component_features)):
            tmp = QTreeWidgetItem(["placeHolder"])
            item.addChild(tmp)
            feature_keys = list(self.features.keys())
            feature_keys.sort()
            if valueDict is not None:
                curValue = valueDict[component_features[i]]
                keyOFcurValue = list(curValue.keys())
            if component_features[i] in feature_keys:
                cur_feature = self.features[component_features[i]]
                spinBox = QDoubleSpinBox()
                if valueDict is None:
                    spinBox.setValue( 0 )
                else:
                    spinBox.setValue(curValue[keyOFcurValue[0]])
                spinBox.setMaximum(99999.99)
                spinBox.setMinimumSize(25,10)
                unitBox = QComboBox()
                unitBox.addItems(cur_feature)
                if valueDict is not None:
                    unitBox.setCurrentText(keyOFcurValue[0])
                else:
                    self.jsonFile["Komponenten"][component][component_features[i]] = {cur_feature[0]:float(0)}
                CustomTreeWidgetItems(self, [str(component_features[i]), unitBox, spinBox], range(3), placeHolder=tmp)

            elif component_features[i] == "Inhalt":
                contentBox = QComboBox()
                contentBox.addItems(self.contents["Inhalt"])
                unitBox = QComboBox()
                unitBox.addItems(self.contents["Aggregatszustand"])
                if valueDict is not None:
                    unitBox.setCurrentText(keyOFcurValue[0])
                    contentBox.setCurrentText(curValue[keyOFcurValue[0]])
                parent.addChild(tmp)
                self.jsonFile["Komponenten"][component][component_features[i]] = {unitBox.currentText(): contentBox.currentText()}
                CustomTreeWidgetItems(self,[str(component_features[i]),unitBox, contentBox],range(3), placeHolder=tmp)

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

    def item_changed(self, item, _NotWorking):
        """ writes the changed item at the right position into the jsonFile """
        parItem = item
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
            try:
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
            except IndexError:
                pass # required for uninted indexError for fields which are not used

    def save_file(self):
        """ writes the jsonFile to disk """
        if any(self.jsonFile[key] == "" for key  in self.minEntries) \
            or  self.jsonFile["Komponenten"] == {}:
            minEntriesBold = ["<b>"+str(x)+",</b>" for x in self.minEntries]
            requiredFields = "\n"+ "\n".join(str(x) for x in minEntriesBold)
            QMessageBox.about(self, "", "Bitte fügen Sie <b>mindestenes eine Komponente</b> hinzu"\
                "und füllen Sie mindestens folgende Felder aus:" + requiredFields)

        else:
            self.start_check()
            fileName = MACHINE_PATH + self.jsonFile["Name"]
            if os.path.isfile(fileName+".json"):
                reply = QMessageBox.question(self, "Dateiname existiert bereits", \
                    "Der Dateiname " + self.jsonFile["Name"] + " existiert bereits,"\
                    " soll die Datei überschrieben werden? \n  Andernfalls wird eine neue Datei erzeugt",\
                     QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    i = 1
                    while os.path.isfile(fileName+".json"):
                        fileName += str(i)
                        i += 1
            write_json_file(self.jsonFile, fileName)
            if self.centralTable is not None:
                self.centralTable.reload_list()

    def start_check(self):
        """ Constantins Part goes here """
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
