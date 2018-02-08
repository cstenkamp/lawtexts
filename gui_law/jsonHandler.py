import sys
import json
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit,\
    QAbstractButton, QDesktopWidget, QGridLayout, QLabel, QAbstractScrollArea,\
    QScrollArea, QToolButton, QMenu, QWidgetAction, QPushButton, QTableWidget,\
    QTextBrowser, QScrollBar, QSizePolicy

EINHEITEN = ["flüssig", "fest", "gasförmig", "c", "bar", "watt", "volt ac", \
            "l", "ml", "k", "g", "mg"]


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
        self.parent = parent
        self.item = item
        self.edit = edit
        # close previous edit windows
        if self.parent is not None:
            for child in self.parent.children():
                if type(child) == self.__class__:
                    child.close()
        self.setWindowTitle(self.item[0]["name"])
        self.sizeObject = QDesktopWidget().screenGeometry(-1)

        self.scroll = QScrollArea(self)
        self.scroll.setWidgetResizable(True)
        self.setMinimumSize(self.sizeObject.width() / 2,\
                            self.sizeObject.height() / 2)
        self.scrollContent = QWidget()
        self.grid = QVBoxLayout(self.scrollContent)
        self.scroll.setWidget(self.scrollContent)
        self.setCentralWidget(self.scroll)

        self.openDict(self.scrollContent, self.grid, self.item[0])

        self.show()

    def openDict(self, table, grid, dict_item, intend=0):
        """ recursively puts all the item entries into the ListBox """
        for key in dict_item:
            # handles dictionary entries in the way of recursively loading this
            # function
            font = QFont("Times", 12, weight=QFont.Bold)
            if type(dict_item[key]) is dict:

                if len(dict_item[key]) == 1 and \
                        list(dict_item[key].keys())[0].lower() in EINHEITEN:
                    newKey = list(dict_item[key].keys())[0]
                    keyLabel = QLabel(key)
                    keyLabel.setText(keyLabel.text() + " (" + newKey + ")")
                    keyLabel.setFont(font)
                    grid.addWidget(keyLabel)
                    text = QTextEdit(self)
                    text.setText(dict_item[key][newKey])
                    text.setReadOnly(not self.edit)
                    grid.addWidget(text)
                else:
                    scrollArea = QScrollArea(self)
                    scrollArea.setWidgetResizable(True)
                    scrollArea.setVisible(False)
                    content = QWidget()
                    nGrid = QVBoxLayout(content)

                    self.openDict(content, nGrid, dict_item[key], intend)
                    scrollArea.setWidget(content)

                    DropdownButton(scrollArea, key, grid)

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
                grid.addWidget(keyLabel)
                grid.addWidget(text)


class DropdownButton(QPushButton):
    def __init__(self, widget, key, grid, toggle = False):
        super(DropdownButton, self).__init__()
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.widget = widget
        self.setText(key)
        self.grid = grid
        self.toggle = toggle
        self.grid.addWidget(self)
        self.clicked.connect(self.toggle_expand)

    def test_stuff(self):
        for i in range(10):
            test = QTextBrowser()
            test.setText("Test")
            DropdownButton(test, "test", self.grid)

    def toggle_expand(self):
        i = 0
        if type(self.widget) is QScrollArea:
            while self.widget.widget().layout().itemAt(i) is not None:
                i += 1
        if not self.toggle:
            index = self.grid.indexOf(self)
            widgetList = []
            while self.grid.itemAt(0) is not None:
                item = self.grid.takeAt(0)
                widgetList.append(item.widget())
            if not self.toggle:
                widgetList.insert(index + 1, self.widget)
            for entry in widgetList:
                self.grid.addWidget(entry)
            self.grid.setStretch(index, 5)
            self.widget.setVisible(True)

        else:
            self.widget.setParent(None)
            widgetList = []
            while self.grid.itemAt(0) is not None:
                item = self.grid.takeAt(0)
                widgetList.append(item.widget())
            for entry in widgetList:
                self.grid.addWidget(entry)
        self.toggle = not self.toggle
