import sys
import json
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTextEdit

def read_json_file(jsonFile):
    if not jsonFile.lower().endswith('.json'):
        print("Given File is no json")
        return
    with open(jsonFile, 'r') as f:
        datastor = json.load(f)
        return datastor

class ItemView(QMainWindow):
    def __init__(self, item, parent=None):
        super(ItemView, self).__init__(parent)
        self.item = item
        self.text = QTextEdit(self)
        self.init_ui()

        self.show()

    def init_ui(self):

        self.setWindowTitle(self.item[0]["name"])
