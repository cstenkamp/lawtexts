import sys
import json
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit,\
    QAbstractButton, QDesktopWidget, QGridLayout, QLabel, QAbstractScrollArea, QScrollArea

EINHEITEN = ["flüssig", "fest", "gasförmig", "c", "bar", "watt", "volt ac", "l", "ml", "k", "g", "mg"]


def read_json_file(jsonFile):
    if not jsonFile.lower().endswith('.json'):
        print("Given File is no json")
        return
    with open(jsonFile, 'r') as f:
        datastor = json.load(f)
        return datastor


class ItemView(QMainWindow):
    def __init__(self, item, parent=None, edit=False):
        super(ItemView, self).__init__(parent)
        self.setCentralWidget(ItemList(item, edit))
        self.parent = parent
        self.item = item
        # close previous edit windows
        if self.parent is not None:
            for child in self.parent.children():
                if type(child) == self.__class__:
                    child.close()
        self.init_ui()

        self.show()

    def init_ui(self):
        self.setWindowTitle(self.item[0]["name"])
        sizeObject = QDesktopWidget().screenGeometry(-1)
        self.resize(sizeObject.width() / 2, sizeObject.height() / 2)


class ItemList(QWidget):
    def __init__(self, item, edit):
        super(ItemList, self).__init__()
        self.item = item
        self.edit = edit
        self.init_ui()

    def init_ui(self):
        self.listBox = QVBoxLayout(self)
        self.setLayout(self.listBox)
        self.scroll = QScrollArea(self)
        self.listBox.addWidget(self.scroll)
        self.scroll.setWidgetResizable(True)
        #self.scroll.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.scrollContent = QWidget(self.scroll)
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.scrollContent.setLayout(self.grid)

        self.counter = 0
        self.openDict(self.item[0])
        self.scroll.setWidget(self.scrollContent)

    def openDict(self, dict_item, intend=0):
        for key in dict_item:
            self.counter += 1
            keyLabel = QLabel(key)
            keyLabel.setFont(QFont("Times", weight=QFont.Bold))
            self.grid.addWidget(keyLabel, self.counter, intend)
            if type(dict_item[key]) is dict:
                if len(dict_item[key]) == 1 and list(dict_item[key].keys())[0].lower() in EINHEITEN:
                    newKey = list(dict_item[key].keys())[0]
                    keyLabel.setText(keyLabel.text() + " (" + newKey + ")")
                    text = QTextEdit(self)
                    text.setText(dict_item[key][newKey])
                    text.setReadOnly(not self.edit)
                    self.grid.addWidget(text, self.counter, intend + 1)
                else:
                    self.openDict(dict_item[key], intend + 1)
            else:
                text = QTextEdit(self)
                if type(dict_item[key]) is list:
                    text.setText(dict_item[key][0])
                else:
                    text.setText(str(dict_item[key]))
                text.setReadOnly(not self.edit)
                self.grid.addWidget(text, self.counter, intend + 1)