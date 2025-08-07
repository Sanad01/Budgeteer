import datetime

from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QEvent


class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None, paycheck_date=None, paycheck_dates=None):
        super().__init__(parent)
        self.selected = None
        self.paycheck_date = paycheck_date
        self.paycheck_dates = paycheck_dates or []
        
        self.label = QLabel(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.update_appearance()

    def mousePressEvent(self, a0):
        self.clicked.emit()
        super().mousePressEvent(a0)

    def click(self):
        self.clicked.emit()

    def update_appearance(self):
        if not self.paycheck_date:
            return

        # Convert string from DB to datetime.date
        date_obj = datetime.datetime.strptime(self.paycheck_date, "%Y-%m-%d").date()

        if self.paycheck_date in self.paycheck_dates:
            self.setStyleSheet("background-color: lightgreen; border: 1px solid green;")
            self.label.setText(f"💲 {date_obj.strftime('%b %d')}")
        else:
            self.setStyleSheet("background-color: lightgray; border: 1px solid #ccc;")
            self.label.setText(date_obj.strftime('%b %d'))


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



