from datetime import datetime, date

from PyQt5.QtWidgets import QFrame, QLabel, QVBoxLayout
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QEvent


class ClickableFrame(QFrame):
    clicked = pyqtSignal()

    def __init__(self, parent=None, frame_date=None, paycheck_dates=None):
        super().__init__(parent)
        self.selected = None
        self.pay_date = None
        self.day = frame_date

        today = datetime.today()
        self.date = frame_date
        self.date = date(today.year, today.month, frame_date)

        self.paycheck_dates = [
            datetime.strptime(d, "%Y-%m-%d").date() if isinstance(d, str) else d
            for d in (paycheck_dates or [])
        ]

        self.label = QLabel(self)
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)  # center text horizontally & vertically
        self.label.setStyleSheet("""
            color: #E8C523;
            font-size: 18pt;
            font-weight: bold;
        """)
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
        if not self.date:
            return

        # Convert string from DB to datetime.date
        #date_obj = datetime.strptime(self.date, "%Y-%m-%d").date()

        if self.date in self.paycheck_dates:
            self.pay_date = True
            self.setStyleSheet("background-color: #1AC91D;")
            self.label.setText(f"$")



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



