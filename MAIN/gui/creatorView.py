import sys
import os
from newComponentCreator import *
from jsonHandler import *
from ExtendedComboBox import ExtendedComboBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from customerDialog import *
from PyQt5.QtWidgets import *
import functools

sys.path.insert(0,os.path.join(os.getcwd(),'logic'))
from mainLogic import MainLogic 

TEXT_GENERATE =  "generiere neue Komponente"

class CreatorView(QMainWindow):
    """ creates a Widget to create a Machine """
    def __init__(self, parent=None, centralTable = None, jsonFile = None, path=None):
        super(CreatorView, self).__init__(parent)

        self.path = path 
        self.parent = None
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
        self.initMenubar(menuBar, path)
        self.show()

    def initMenubar(self, menubar, path):
        """ adds a Menubar to the Window """
        # todo add functions later
        fileMenu = menubar.addMenu('Datei')
        # searchMenu = menubar.addMenu('Suche')
        save = QAction('Speichern', self)
        save.setShortcut('Ctrl+S')
        # lamda necessary in order to make it callable
        save.triggered.connect(lambda: self.ItemCreatorWidget.save_file(path))
        if self.centralTable is not None:
            save.triggered.connect(lambda: self.centralTable.reload_list())
        saveAs = QAction('Speichern als', self)
        fileMenu.addAction(save)
        toolbar = self.addToolBar('Auf zutreffende Richtlinien überprüfen')
        toolbar.setIconSize(QSize(32,32))
        check = QAction(QIcon(ICON_PATH+"law.png"), '', self)
        check.setIcon
        check.setToolTip("Richtlinien auf dieser Maschine überprüfen")
        check.triggered.connect(functools.partial(CreatorView.start_check, \
                self.ItemCreatorWidget.jsonFile, True, self.ItemCreatorWidget))
        toolbar.addAction(check)
        fileMenu.addAction(saveAs)
        menubar.setCornerWidget(toolbar)
        menubar.adjustSize()
        # TODO add saveAs

    def setJsonFile(self, json):
        self.ItemCreatorWidget.setJsonFile(json)



    @staticmethod
    def start_check(jsonFile, finishCheckRequired=False, creatorWidget = None, logic=None):
        # init file to save check results:
        
        if finishCheckRequired and creatorWidget is not None:
            if not creatorWidget.finishCheck():
                return
        logic.start()
        #customerDialog = CustomerDialog()
        #result = customerDialog.exec_()
        #if result:
        #    role = customerDialog.getRole()
        #    del customerDialog
        #    print(role)
        #
        #    """ Constantins Part goes here jsonFile is the machine"""
        #    print("creatorView.py Methodenname: startCheck")
        #    print("this method is currently called when the user tries to save the file")


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
                "Herstellungsdatum":"2000-01-01", "Prüfdatum":"2000-01-01", "Komponenten":{},\
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
                date = self.jsonFile[entry].split('-')
                dateEdit = QDateEdit(QDate(int(date[0]),int(date[1]),int(date[2])))
                dateEdit.setDisplayFormat("dd.MM.yyyy")
                CustomTreeWidgetItems(self, [entry, dateEdit], [0,2], placeHolder = tmp)

            else:
                CustomTreeWidgetItems(self, [entry, QLineEdit(self.jsonFile[entry])], [0,2], placeHolder = tmp)

        tooltip = "Hier klicken um eine neue Komponente zu erstellen"
        self.combo = ExtendedComboBox(self)
        self.combo.setInsert(False)
        self.combo.addItems(list(self.parts.keys())+[TEXT_GENERATE])
        self.btn_comp, self.addComponents = self.QTreeAddButtonMenu("Komponente", self.combo, tooltip)
        self.btn_comp.clicked.connect(functools.partial(self.addExtComboBoxEdit,
            list(self.parts.keys())+[TEXT_GENERATE], self.combo, \
            self.firstComponent, self.addComponents, "Komponenten") )

        vZweckCombo = ExtendedComboBox(self)
        list_keys = list(self.purposes.keys())
        list_keys.sort()
        vZweckCombo.addItems(list_keys)
        self.btn_vZweck, self.addVZweck = self.QTreeAddButtonMenu("Verwendungszwecke", vZweckCombo)
        self.btn_vZweck.clicked.connect(lambda: self.addExtComboBoxEdit(\
            list(self.purposes.keys()), vZweckCombo, \
            self.firstVZweck, self.addVZweck, "Verwendungszwecke") )

        vOrtCombo = ExtendedComboBox(self)
        list_keys = list(self.sites.keys())
        list_keys.sort()
        vOrtCombo.addItems(list_keys)
        self.btn_vOrt, self.addVOrt = self.QTreeAddButtonMenu("Verwendungsorte", vOrtCombo)
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
                    if keys[i] is not "Kommentare":
                        tmpLineEdit.setReadOnly(True)
                    placeHolder = QTreeWidgetItem([""])
                    parent.addChild(placeHolder)
                    btn_del, widget = self.del_or_addFeature_button()
                    delCustom = CustomTreeWidgetItems(self,\
                        [widget,tmpLineEdit],[1,2], connect=True, placeHolder=placeHolder, comment=True)
                    btn_del.clicked.connect(functools.partial(self.del_item, delCustom))
            else:
                comp_list = list(self.jsonFile[keys[i]].keys())
                comp_list.sort()
                for component in comp_list:
                    for compOfSameType in self.jsonFile[keys[i]][component]:
                        shortedenedDict = compOfSameType
                        self.openComponentCreator(component, parent, shortedenedDict)

    def addCommentEdit(self, parent=None):
        """ adds a QLineEdit + Button in order to add comments """
        lineEdit = QLineEdit()
        btn, addLineEdit = self.QTreeAddButtonMenu("Kommentare", lineEdit)
        btn.clicked.connect(lambda: self.addExtComboBoxEdit([], lineEdit, \
                            self.firstComment, addLineEdit, "Kommentare") )
        return btn, addLineEdit

    def QTreeAddButtonMenu(self, buttonText, widget, tooltip = None):
        """ adds a Button to the QTree and returns the buton and the TreeWidget """
        button = QToolButton()
        button.setText(buttonText)
        button.setIcon(QIcon(ICON_PATH + "add.png"))
        button.setIcon(QIcon(ICON_PATH + "add.png"))
        button.setMinimumSize(175,10)
        button.setToolTip(tooltip)
        button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        item = CustomTreeWidgetItems(self, [button, widget],[0,2], connect=False)
        return [button, item]

    def del_or_addFeature_button(self, feature=False):
        widget = QWidget();
        layout= QHBoxLayout();
        layout.setAlignment( Qt.AlignCenter );
        btn_del = QPushButton()
        if not feature:
            btn_del.setToolTip("Hier klicken um dieses Element zu löschen")
            btn_del.setIcon(QIcon(ICON_PATH+"trash.png"))
        else:
            btn_del.setToolTip("Hier klicken um eine Eigenschaft hinzuzufügen")
            btn_del.setIcon(QIcon(ICON_PATH+"add.png"))
        btn_del.setIconSize(QSize(18,18))
        btn_del.setFixedSize(64,24)
        layout.addWidget(btn_del);
        widget.setLayout(layout);
        return [btn_del, widget]

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
                exComboBox.showPopup() # if empty text load the popup
                return
            if purpose == TEXT_GENERATE:
                dialog = ComponentGenerator()
                reply = dialog.exec_()
                # if not accepted
                if reply == 0:
                    return
                else:
                    newDict = dialog.getDict() # get the created component dict
                    dialog.save(custom_parts=self.parts) # saves the dict to the current partsDict
                    component = list(newDict.keys())[0]
                    # set the corresponding entries in the custom boolean class
                    if self.firstComponent.getBool():
                        self.firstComponent.setBool(False)
                        parent = QTreeWidgetItem(["Komponenten"])
                        index = self.indexOfTopLevelItem(self.addComponents)
                        self.insertTopLevelItem(index, parent)
                        self.firstComponent.setParent(parent)
                        parent.setExpanded(True)
                    parent = self.firstComponent.getParent()
                    # add the component the same way it is done in loadJson
                    self.openComponentCreator(component, parent, valueDict=newDict[component] )
                    # reload the itemList and set it to the same generiere neue Komponente entry
                    self.combo.clear()
                    self.combo.addItems(list(self.parts.keys())+[TEXT_GENERATE])
                    self.combo.setCurrentIndex(self.combo.count()-1)
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
            if key is not "Kommentare":
                tmpLineEdit.setReadOnly(True)
            placeHolder = QTreeWidgetItem([""])
            parent.addChild(placeHolder)
            btn_del, widget = self.del_or_addFeature_button()
            delCustom = CustomTreeWidgetItems(self, [widget,tmpLineEdit],[1,2], connect=True, placeHolder=placeHolder, comment=True)
            btn_del.clicked.connect(functools.partial(self.del_item, delCustom))
        else:
            if purpose == TEXT_GENERATE:
                return
            self.openComponentCreator(purpose, parent)

        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

    def openComponentCreator(self, component, parent, valueDict=None):
        """ adds components to the view """
        if component not in self.jsonFile["Komponenten"] and valueDict is None:
            self.jsonFile["Komponenten"][component] = []
        component_features = self.parts[component]["Eigenschaften"]
        if valueDict is None:
            component_features = self.parts[component]["Eigenschaften"]
        else:
            component_features = list(valueDict.keys())
        component_features.sort()
        btn_del, widget = self.del_or_addFeature_button()
        btn_add_feature, widget2 = self.del_or_addFeature_button(True)
        item = QTreeWidgetItem([component])
        parent.addChild(item)
        self.setItemWidget(item, 1, widget)
        self.setItemWidget(item, 2, widget2)
        btn_del.clicked.connect(functools.partial(self.del_item, item))
        btn_add_feature.clicked.connect(functools.partial(self.add_feature, item))
        item.setExpanded(True)
        newCompList = {}
        for i in range(len(component_features)):
            tmp = QTreeWidgetItem(["placeHolder"])
            item.addChild(tmp)
            feature_keys = list(self.features.keys())
            feature_keys.sort()
            if valueDict is not None:
                curValue = valueDict[component_features[i]]
                if type(curValue) is dict:
                    keyOFcurValue = list(curValue.keys())
                # else:
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
                if valueDict is not None: # in case an existing json File is loaded
                    unitBox.setCurrentText(keyOFcurValue[0])
                else:
                    #TODO implement this change everywhere else as well
                    newCompList[component_features[i]] = {cur_feature[0]:float(0)}
                CustomTreeWidgetItems(self, [str(component_features[i]), unitBox, spinBox], range(3), placeHolder=tmp)

            elif component_features[i] == "Inhalt":
                contentBox = QComboBox()
                contentBox.addItems(self.contents["Inhalt"])
                unitBox = QComboBox()
                unitBox.addItems(self.contents["Aggregatszustand"])
                if valueDict is not None: # in case an existing json File is loaded
                    unitBox.setCurrentText(keyOFcurValue[0])
                    contentBox.setCurrentText(curValue[keyOFcurValue[0]])
                else:
                    newCompList[component_features[i]] = {unitBox.currentText(): contentBox.currentText()}
                parent.addChild(tmp)
                # self.jsonFile["Komponenten"][component].append([component_features[i]: {unitBox.currentText(): contentBox.currentText()}])
                CustomTreeWidgetItems(self,[str(component_features[i]),unitBox, contentBox],range(3), placeHolder=tmp)
            else:
                CustomTreeWidgetItems(self, [component_features[i], QLineEdit(curValue)], [0,2], placeHolder = tmp, comment=True)

        if valueDict is None:
            self.jsonFile["Komponenten"][component].append(newCompList)
        for i in range(self.columnCount()):
            self.resizeColumnToContents(i)

    def item_changed(self, item, _NotWorking):
        """ writes the changed item at the right position into the jsonFile """
        parItem = item
        parentList = []
        try:
            while parItem.parent() is not None:
                parItem = parItem.parent()
                parentList.append(parItem.text(0))
        except RecursionError:
            return #needed to handle empty fields in custromtreeWidgets

        if type(item) is CustomTreeWidgetItems:
            nonTreeWidgets, pos = item.widgets_and_position()
            key = nonTreeWidgets[0]
            unit = None
            if not item.isComment():
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
                        value = nonTreeWidgets[valueAt].date().toString(Qt.ISODate)
                    json = self.jsonFile
                    while parentList != []:
                        json = json[parentList.pop()]
                    if unit is None:
                        json[key]=value
                    else:
                        super_parent = item.parent().parent()
                        ind = [i for i in range(super_parent.childCount()) if super_parent.child(i) == item.parent()][0]
                        json[ind][key] = {unit:value}
                except IndexError:
                    return # required for uninted indexError for fields which are not used
            else:
                parent = item.parent()
                if parent.parent() is None:
                    # change the edited comment in the jsonFile
                    value = nonTreeWidgets[0].text()
                    key = "Kommentare"
                    old_list = self.jsonFile[key]
                    # check what's the index of the comment in order to edit the right one at the jsonFile
                    list_index = [i for i in range(parent.childCount()) if parent.child(i) == item.get_placeHolder()]
                    self.jsonFile[key][list_index[0]] = value
                else: # one of the added components
                    widgets, position = item.widgets_and_position()
                    value = widgets[1].text()
                    index = parent.parent().indexOfChild(parent)
                    parent_key = parent.text(0)
                    indicesOfItemType = [i for i in range(parent.parent().childCount())\
                                if parent.parent().child(i).text(0) == parent.text(0)]
                    indexInJson = indicesOfItemType.index(index)
                    self.jsonFile[parent.parent().text(0)][parent.text(0)][indexInJson][key] = value

    def del_item(self,item):
        if type(item) is CustomTreeWidgetItems:
            parent = item.parent()
            index = [i for i in range(parent.childCount()) if parent.child(i) == item.get_placeHolder()][0]
            parent.takeChild(index)
            widgets, positions = item.widgets_and_position()
            self.jsonFile[parent.text(0)].remove(widgets[1].text())
        elif type(item ) is QTreeWidgetItem:
            parent = item.parent()
            index = parent.indexOfChild(item)
            parent_key = parent.text(0)
            item_key = item.text(0)
            indicesOfItemType = [i for i in range(parent.childCount()) if parent.child(i).text(0) == item_key]
            indexInJson = indicesOfItemType.index(index)
            parent.takeChild(index)
            del self.jsonFile[parent_key][item_key][indexInJson]
            if len(indicesOfItemType) == 1:
                self.jsonFile[parent_key].pop(item_key)

    def add_feature(self, item):
        text, ok = QInputDialog.getText(self, 'Eigenschaft hinzufügen', 'Name der Eigenschaft:')
        if not ok:
           return
        parent = item.parent()
        index = parent.indexOfChild(item)
        indicesOfItemType = [i for i in range(parent.childCount()) if parent.child(i).text(0) == item.text(0)]
        indexInJson = indicesOfItemType.index(index)
        tmp = QTreeWidgetItem(["placeHolder"])
        item.addChild(tmp)
        lineE01 = QLineEdit()
        CustomTreeWidgetItems(self, [str(text), lineE01], [0,2], placeHolder=tmp, connect=True, comment=True)

    def finishCheck(self):
        """ checks if all required fields are filled out """
        if any(self.jsonFile[key] == "" for key  in self.minEntries) \
            or  self.jsonFile["Komponenten"] == {}:
            minEntriesBold = ["<b>"+str(x)+",</b>" for x in self.minEntries]
            requiredFields = "\n"+ "\n".join(str(x) for x in minEntriesBold)
            QMessageBox.about(self, "", "Bitte fügen Sie <b>mindestenes eine Komponente</b> hinzu"\
                "und füllen Sie mindestens folgende Felder aus:" + requiredFields)
            return False
        else:
            return True

    def save_file(self, path):
        """ writes the jsonFile to disk """
        if self.finishCheck():
            # CreatorView.start_check()
            if path == None:
                fileName = os.path.join(MACHINE_PATH,self.jsonFile["Name"])
            else:
                fileName = path.replace(".json", "")
            if os.path.isfile(fileName+".json"):
                cancel = QPushButton("abbrechen")
                cancel.setIcon(QIcon(ICON_PATH+"cancel.png"))
                save = QPushButton("als neue Datei speichern")
                save.setIcon(QIcon(ICON_PATH+"save.png"))
                overwrite = QPushButton("überschreiben")
                overwrite.setIcon(QIcon(ICON_PATH+"overwrite.png"))
                box = QMessageBox()
                box.setIcon(QMessageBox.Question)
                box.setWindowTitle("Komponentenname bereits vorhanden")
                box.setText("Die Datei " + fileName + " existiert bereits,"\
                " soll die Datei überschrieben werden?")
                box.addButton(save, QMessageBox.NoRole)
                box.addButton(overwrite, QMessageBox.YesRole)
                box.addButton(cancel, QMessageBox.DestructiveRole)
                reply = box.exec_()
                if reply == 2:
                    return
                if reply == QMessageBox.Rejected:
                    i = 1
                    while os.path.isfile(fileName+".json"):
                        fileName += str(i)
                        i += 1
            write_json_file(self.jsonFile, fileName)
            if self.centralTable is not None:
                self.centralTable.reload_list()


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
    def __init__( self, treeWidget, widgets, position, placeHolder= None, connect = True, comment=False):
        ## Init super class ( QtGui.QTreeWidgetItem )
        super( CustomTreeWidgetItems, self ).__init__( treeWidget )
        self.widgets = widgets
        self.parent = None
        self.position = position
        self.comment = comment
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
        self.placeHolder = placeHolder

    def widgets_and_position(self):
        return [self.widgets, self.position]

    def parent(self):
        return self.parent

    def isComment(self):
        return self.comment

    def get_placeHolder(self):
        return self.placeHolder


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = CreatorView()
    window.show()
    sys.exit(app.exec_())
