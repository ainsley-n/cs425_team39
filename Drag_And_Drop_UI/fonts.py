import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QFontDatabase
from PyQt5.QtGui import QFont




def getFont(font_path):
    try:
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            print(f"Failed to load font at: {font_path}")
            return None
        else:
            font_family = QFontDatabase.applicationFontFamilies(font_id).at(0)
            return QFont(font_family)
    except Exception as e:
        print(f"An error occurred while loading the font: {e}")
        return None


def main():
    # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Create a window
    window = QWidget()
    window.setWindowTitle('Circuit Circus!')
    
    window.setStyleSheet("background-color: #1C2366")
    window.setGeometry(100, 100, 1600, 300) 


    # Create a label widget
    label = QLabel('Circuit Circus!', parent=window)
    label.move(150, 150)
    
    font = getFont('Drag_And_Drop_UI/fonts/brasika.otf')
    font.setPointSize(40)
    label.setFont(font)
        
    # Set the color of the label text
    label.setStyleSheet("color: #FDE66C; border-style: outset; border-width: 2px; border-color: beige;")

    # Show the window
    window.show()

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
