from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QEvent


class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected = None

    def mousePressEvent(self, a0):
        self.clicked.emit()
        super().mousePressEvent(a0)

    def click(self):
        self.clicked.emit()

class HoverFilter(QObject):
    HoverEnter = pyqtSignal()
    HoverLeft = pyqtSignal()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverEnter:
            self.HoverEnter.emit()
            print("Hovered over button!")
        elif event.type() == QEvent.HoverLeave:
            self.HoverLeft.emit()
            print("Hover left button!")
        return super().eventFilter(obj, event)