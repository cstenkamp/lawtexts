import sys
from PyQt5.QtWidgets import QPushButton, QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

def setColumnWidget(QTableWidget table):
    for column in table