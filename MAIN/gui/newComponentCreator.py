import sys
import os
from jsonHandler import *
from ExtendedComboBox import ExtendedComboBox
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from creatorView import *
import functools

class ComponentGenerator(QDialog):

    def __init__(self):
        super(ComponentGenerator, self).__init__()
        self.parts = read_json_file(JSON_PATH + "/parts.json")
        self.features = read_json_file(JSON_PATH + "/features.json")["Features"]
        self.contents = read_json_file(JSON_PATH + "/contents.json")
        self.createFormGroupBox()
        self.entries = []
        self.dict = {}

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok)
        buttonBox.accepted.connect(self.newAccept)
        cancel = QPushButton("abbrechen")
        cancel.setIcon(QIcon(ICON_PATH+"cancel.png"))
        save = QPushButton("Komponententyp speichern")
        save.setIcon(QIcon(ICON_PATH+"save.png"))
        buttonBox.addButton(cancel, QDialogButtonBox.RejectRole)
        buttonBox.addButton(save, QDialogButtonBox.ActionRole)
        save.clicked.connect(self.save)
        buttonBox.rejected.connect(self.reject)
        self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)
        self.rowCounter = 3
        self.setWindowTitle("Neue Komponente")

    def save(self, custom_parts=None):
        if custom_parts == None or custom_parts == False:
            parts = self.parts
        else:
            parts = custom_parts
        name = self.nameLineEdit.text()
        selfDict = self.writeResult()
        if selfDict is not None:
            if any(part == name for part in parts):
                reply = QMessageBox.question(self, "Komponentenname bereits vorhanden", \
                    "Eine Komponenten mit Namen: " + name + " existiert bereits,"\
                    " soll die Komponente wirklich überschrieben werden?",\
                     QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.No:
                    return
        saveDict = list(selfDict[name][0].keys())
        saveDict.sort()
        parts[name] = {"Eigenschaften": saveDict, "_Eigenschaften":[]}
        if custom_parts == None or custom_parts == False:
            write_json_file(parts, JSON_PATH + "/parts.json")

    def newAccept(self):
        self.writeResult()
        self.accept()

    def writeResult(self):
        name = self.nameLineEdit.text()
        self.dict[name] = [{}]
        if name == "":
            QMessageBox.about(self, "","Bitte geben Sie einen Namen an")
            return None
        else:
            for entry in self.entries:
                if type(entry[2]) == QDoubleSpinBox:
                    self.dict[name][0][entry[0].text()] = {entry[1].currentText(): entry[2].value()}
                else:
                    self.dict[name][0][entry[0].text()] = {entry[1].currentText(): entry[2].currentText()}
        return self.dict

    def getDict(self):
        return self.dict

    def createFormGroupBox(self):
        self.formGroupBox = QGroupBox()
        layout = QGridLayout()
        layout.addWidget(QLabel("<b>Name</b>"),0,2,1,1)
        self.nameLineEdit = QLineEdit()
        layout.addWidget(self.nameLineEdit,0,3,1,2)
        self.featureBox = QComboBox()
        self.featureBox.addItems(list(self.features.keys())+["Inhalt"])
        w1, b1 = self.createAddRemoveButton(alignment=Qt.AlignLeft)
        w2, b2 = self.createAddRemoveButton(alignment=Qt.AlignRight)
        layout.addWidget(QLabel("<b>Eigenschaft hinzufügen</b>"),1,0,1,2)
        layout.addWidget(QLabel("<b>Hinzufügen aller Eigenschaften von</b>"),1,5,1,2)
        layout.addWidget(self.featureBox,2,0,1,1)
        layout.addWidget(w1,2,1,1,1)
        self.componentBox = QComboBox()
        self.componentBox.addItems(list(self.parts.keys()))
        layout.addWidget(self.componentBox,2,6,1,1)
        layout.addWidget(w2,2,5,1,1)

        b1.clicked.connect(self.addFeatureFromComboBox)
        b2.clicked.connect(self.addFeaturesFromComponentBox)

        # layout.addRow(QLabel("Age:"), QSpinBox())
        self.formGroupBox.setLayout(layout)

    def createAddRemoveButton(self, add=True,alignment=Qt.AlignCenter):
        widget = QWidget();
        layout= QHBoxLayout();
        layout.setAlignment( alignment);
        btn_add = QPushButton()
        if add:
            btn_add.setIcon(QIcon(ICON_PATH+"add.png"))
        else:
            btn_add.setIcon(QIcon(ICON_PATH+"remove.png"))
        btn_add.setIconSize(QSize(18,18))
        layout.addWidget(btn_add)
        widget.setLayout(layout)
        return [widget, btn_add]

    def addFeatureFromComboBox(self):
        self.addFeature(self.featureBox.currentText())

    def addFeaturesFromComponentBox(self):
        component = self.componentBox.currentText()
        for feature in self.parts[component]["Eigenschaften"]:
            self.addFeature(feature)

    def addFeature(self, feature):
        if self.entries != []:
            l = [fname for i in range(len(self.entries)) for fname in [self.entries[i][0].text()]]
            if any (name==feature for name in l):
                QMessageBox.about(self, "", feature+" existiert bereits")
                return
        label = QLabel(feature)
        unit = QComboBox()
        if feature in self.features:
            unit.addItems(self.features[feature])
            value = QDoubleSpinBox()
        else: # if == "Inhalt"
            unit.addItems(self.contents["Aggregatszustand"])
            value = QComboBox()
            value.addItems(self.contents["Inhalt"])
        rowCount = self.rowCounter
        widget, button = self.createAddRemoveButton(add=False, alignment=Qt.AlignLeft)
        self.formGroupBox.layout().addWidget(widget, rowCount, 1, 1,1)
        self.formGroupBox.layout().addWidget(label, rowCount, 2, 1,1)
        self.formGroupBox.layout().addWidget(unit, rowCount, 3, 1,1)
        self.formGroupBox.layout().addWidget(value, rowCount, 4, 1,1)
        button.clicked.connect(functools.partial(self.removeFeature,\
                               rowCount))
        self.entries.append([label, unit, value])
        self.rowCounter += 1

    def removeFeature(self, row):
        layout = self.formGroupBox.layout()
        for i in range(4):
            layout.itemAtPosition(row, 1+i).widget().setParent(None)
        self.rowCounter -= 1
        del self.entries[row - 3]
        self.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator = QTranslator(app)
    locale = QLocale.system().name()
    path = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    translator.load('qt_%s' % locale, path)
    app.installTranslator(translator)
    dialog = ComponentGenerator()
    if dialog.exec_():
        print(dialog.getDict())
#sys.exit(dialog.exec_())
