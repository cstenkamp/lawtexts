import sys
import json
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit,\
    QAbstractButton, QDesktopWidget, QGridLayout, QLabel, QAbstractScrollArea,\
    QScrollArea, QToolButton, QMenu, QWidgetAction, QPushButton

EINHEITEN = ["flüssig", "fest", "gasförmig", "c", "bar", "watt", "volt ac", "l", "ml", "k", "g", "mg"]


def read_json_file(jsonFile):
    """ reads the jsonFiles and returns it """
    if not jsonFile.lower().endswith('.json'):
        print("Given File is no json")
        return
    with open(jsonFile, 'r') as f:
        datastor = json.load(f)
        return datastor


class ItemView(QMainWindow):
    """ creates a ItemOverview over the given @item, @edit = readOnly? """
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
    """ creates a scrollable ItemList in which the item entries will be put """
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
        self.scrollContent = QWidget(self.scroll)
        self.grid = QGridLayout()
        self.grid.setSpacing(10)
        self.scrollContent.setLayout(self.grid)

        self.counter = 0

        self.openDict(self.grid, self.item[0])

        self.scroll.setWidget(self.scrollContent)

    def openDict(self, grid, dict_item, intend=0):
        """ recursively puts all the item entries into the ListBox """
        for key in dict_item:
            # handles dictionary entries in the way of recursively loading this
            # function
            self.counter += 1
            font = QFont("Times", 12, weight=QFont.Bold)
            if type(dict_item[key]) is dict:
                if len(dict_item[key]) == 1 and \
                        list(dict_item[key].keys())[0].lower() in EINHEITEN:
                    newKey = list(dict_item[key].keys())[0]
                    keyLabel = QLabel(key)
                    keyLabel.setText(keyLabel.text() + " (" + newKey + ")")
                    keyLabel.setFont(font)
                    grid.addWidget(keyLabel, self.counter, intend)
                    text = QTextEdit(self)
                    text.setText(dict_item[key][newKey])
                    text.setReadOnly(not self.edit)
                    grid.addWidget(text, self.counter, intend + 1)
                else:
                    scrollArea = QScrollArea(self)
                    scrollArea.setWidgetResizable(True)
                    scrollArea.setVisible(False)
                    content = QWidget(scrollArea)
                    nGrid = QGridLayout()
                    nGrid.setSpacing(10)
                    content.setLayout(nGrid)
                    self.openDict(nGrid, dict_item[key], intend)
                    button = dropdownButton(content, grid, self.counter+1, intend+1)
                    button.setText(key)
                    button.setToolTip('click to toggle ' + key)
                    grid.addWidget(button, self.counter, intend)
            else:
                keyLabel = QLabel(key)
                keyLabel.setFont(font)
                # here the entries gets put into the ListBox
                text = QTextEdit(self)
                # in case it's a list put each list entry into the ListBox
                if type(dict_item[key]) is list:
                    toSetText = ""
                    for entry in dict_item[key]:
                        if toSetText == "":
                            toSetText += str(entry)
                        else:
                            toSetText += ("\n" + str(entry))
                    text.setText(toSetText)
                else:
                    text.setText(str(dict_item[key]))
                text.setReadOnly(not self.edit)
                text.setFont(QFont("Times", 12))
                grid.addWidget(keyLabel, self.counter, intend)
                grid.addWidget(text, self.counter, intend + 1)


class dropdownButton(QPushButton):
    def __init__(self, widget, grid, row, column, toggleBoolean=False,):
        super().__init__()
        self.toggle = toggleBoolean
        self.widget = widget
        self.grid = grid
        self.clicked.connect(self.toggle_expand)
        self.row = row
        self.column = column

    def toggle_expand(self):
        if not self.toggle:
            self.grid.addWidget(self.widget, self.row, self.column)
            self.toggle = True
        else:
            self.widget.setParent(None)
            self.toggle = False
