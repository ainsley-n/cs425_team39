import unittest
from PyQt5.QtWidgets import QApplication
from Drag_And_Drop_UI.drag_and_drop import MainWindow, Canvas, Sidebar

class TestMainWindow(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])

    def test_main_window_creation(self):
        canvas = Canvas()
        window = MainWindow(canvas)
        self.assertIsNotNone(window)

    def tearDown(self):
        self.app.quit()
        
class TestSidebar(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])

    def test_sidebar_creation(self):
        canvas = Canvas()
        sidebar = Sidebar(canvas)
        self.assertIsNotNone(sidebar)

    def tearDown(self):
        self.app.quit()

if __name__ == '__main__':
    unittest.main()
