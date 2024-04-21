import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QFont, QFontDatabase


def main():
    # Create an instance of QApplication
    app = QApplication(sys.argv)

    # Create a window
    window = QWidget()
    window.setWindowTitle('Circuit Circus!')
    
    window.setStyleSheet("background-color: #1C2366")
    window.setGeometry(100, 100, 1600, 300) 

    # Load the font from a file
    font_path = 'Drag_And_Drop_UI/fonts/brasika.otf' 
    font_id = QFontDatabase.addApplicationFont(font_path)
    
    # Check if the font was loaded successfully
    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        # Create a label widget
        label = QLabel('Circuit Circus!', parent=window)
        label.move(150, 150)
        
        # Set the font of the label
        font = QFont(font_family)
        font.setPointSize(40)
        label.setFont("Arial")
        
        # Set the color of the label text
        label.setStyleSheet("color: #FDE66C; border-style: outset; border-width: 2px; border-color: beige;")

        # Show the window
        window.show()
    else:
        print("Font loading failed.")

    # Start the event loop
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
