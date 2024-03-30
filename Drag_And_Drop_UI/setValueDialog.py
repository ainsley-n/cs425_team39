from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QPushButton

class SetValueDialog(QDialog):
    def __init__(self, parent=None):
        super(SetValueDialog, self).__init__(parent)
        self.setWindowTitle("Set Value")
        
        self.label = QLabel("Enter a value:")
        self.value_input = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.value_input)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def get_value(self):
        input_text = self.value_input.text().strip()
        
        # Check if the input is a valid float or if it's empty
        try:
            return float(input_text)
        except ValueError:
            return input_text if input_text else None
        