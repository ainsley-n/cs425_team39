from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton



class Wire(QtWidgets.QGraphicsLineItem):
    def __init__(self, start_pos, end_pos, parent=None):
        super(Wire, self).__init__(parent)
        self.setLine(QtCore.QLineF(start_pos, end_pos))
        self.setPen(QtGui.QPen(QtGui.QColor("black"), 2))
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        