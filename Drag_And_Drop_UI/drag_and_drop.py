from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton
from canvas import Canvas
from sidebar import Sidebar

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, canvas, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.sidebar = Sidebar(canvas)
        self.canvas = canvas

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.sidebar)
        layout.addWidget(self.canvas)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():
    app = QtWidgets.QApplication([])
    canvas = Canvas()
    window = MainWindow(canvas)
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()