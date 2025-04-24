import sys
from PyQt5.QtWidgets import QApplication
from app.GUI.screen_manager import ScreenManager

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen_manager = ScreenManager()
    screen_manager.run()
