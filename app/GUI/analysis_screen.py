from PyQt5.QtCore import pyqtSignal, QObject, QAbstractAnimation, QPropertyAnimation, QPoint, QTimer, QMargins, \
    QEasingCurve
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtSql import QSqlQuery, QSqlDatabase
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGraphicsOpacityEffect
from app.GUI.fonts import title_font, text_font, text_style1, title_font2, button_style1a
from data.database import DatabaseManager
from PyQt5 import QtChart


class AnalysisScreen(QWidget):

    goToHomeScreen = pyqtSignal()

    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager
        self.db = DatabaseManager()
        self.income = None
        self.budget_percent = None
        self.loans_percent = None
        self.transportation_percent = None
        self.rent_percent = None
        self.bills_percent = None
        self.utilities_percent = None
        data = self.db.get_percentages(self.screen_manager.name)
        self.set_percent_values(data)
        self.init_ui()

    def init_ui(self):
        self.resize(1920, 1080)

        self.setWindowTitle("Financial Planner")

        self.main_layout = QHBoxLayout(self)
        # create columns
        col1 = self.creat_col1()
        col2 = self.creat_col2()

        # add columns to layout
        self.main_layout.addLayout(col1)
        self.main_layout.addLayout(col2)

        lines = [self.analysis1, self.analysis2, self.analysis3, self.analysis4, self.analysis5]
        # self.setup_lines(lines, 300)

        # separate animations are needed for every line or else it won't work
        self.animations = []
        self.fade_animation(lines, 0)

        self.setLayout(self.main_layout)

    def creat_col1(self):
        col1 = QVBoxLayout(self)

        self.row0 = QHBoxLayout(self)
        title = QLabel("Here is a breakdown of your spending: ")
        title.setFont(title_font2(title))
        title.setAlignment(Qt.AlignLeft)
        self.row0.addWidget(title)
        col1.addLayout(self.row0)
        col1.addSpacing(150)

        self.row1 = QHBoxLayout(self)
        self.analysis1 = QLabel(f"you spend {self.rent_percent}% of your income on rent", self)

        self.row2 = QHBoxLayout(self)
        self.analysis2 = QLabel(f"you spend {self.utilities_percent}% of your income on utilities", self)

        self.row3 = QHBoxLayout(self)
        self.analysis3 = QLabel(f"you spend {self.bills_percent}% of your income on bills", self)

        self.row4 = QHBoxLayout(self)
        self.analysis4 = QLabel(f"you spend {self.transportation_percent}% of your income on transportation", self)

        self.row5 = QHBoxLayout(self)
        self.analysis5 = QLabel(f"you spend {self.loans_percent}% of your income on recurring payments", self)

        # change font in text body
        lines = [self.analysis1, self.analysis2, self.analysis3, self.analysis4, self.analysis5]
        for text in lines:
            text.setFont(text_font(text_style1(text)))

        # add text to row
        rows = [self.row1, self.row2, self.row3, self.row4, self.row5]
        for row, analysis in zip(rows, lines):
            row.addWidget(analysis)

            col1.addLayout(row)
            col1.addSpacing(150)

        return col1

    def creat_col2(self):
        col2 = QVBoxLayout()
        row1 = QHBoxLayout()
        row1.addWidget(self.create_chart())

        row2 = QHBoxLayout(self)
        row2.addStretch(1)
        # buttons
        continue_button = QPushButton("Continue", self)
        continue_button.clicked.connect(self.go_to_home_screen)
        button_style1a(continue_button)
        continue_button.setMaximumWidth(160)
        back_button = QPushButton("Back", self)
        back_button.setMaximumWidth(160)
        button_style1a(back_button)
        row2.addWidget(back_button)
        row2.addWidget(continue_button)

        col2.addLayout(row1)
        col2.addLayout(row2)

        return col2

        # change font in text body

    def set_percent_values(self, data: dict):
        print(f"is this it: {data}")
        self.income = data.get("income")
        self.rent_percent = data.get("rent")
        self.utilities_percent = data.get("utilities")
        self.bills_percent = data.get("bills")
        self.transportation_percent = data.get("transportation")
        self.loans_percent = data.get("loans")
        self.budget_percent = data.get("budget")

    # cascade slide animation from left to right with delay between each line
    def fade_animation(self, lines: [], delay):
        for text in lines:
            opacity_effect = QGraphicsOpacityEffect(self)
            text.setGraphicsEffect(opacity_effect)
            opacity_effect.setOpacity(0.0)

            animation = QPropertyAnimation(opacity_effect, b'opacity')
            animation.setDuration(1000)
            animation.setStartValue(0.0)
            animation.setEndValue(1.0)
            animation.setEasingCurve(QEasingCurve.InOutQuad)

            # delay timer
            timer = QTimer(self)
            timer.setSingleShot(True)
            # Make the label visible and start the animation
            timer.timeout.connect(animation.start)
            timer.start(delay)
            # Store the animation and timer
            self.animations.append((animation, timer))
            delay += 500

    # create lines of text with 150px vertical space between each line
    def setup_lines(self, lines: [], y_pos):
        for text in lines:
            text.move(10, y_pos)
            y_pos += 150

    def create_chart(self):
        self.chart = QtChart.QChart()
        self.series = QtChart.QPieSeries(self.chart)
        self.chart_view = QtChart.QChartView(self.chart, self)

        if self.income != None:  # only create chart after user entered data
            self.pie_slice1 = QtChart.QPieSlice("rent", self.rent_percent)
            self.pie_slice1.setColor(QColor(194, 136, 70))
            self.pie_slice2 = QtChart.QPieSlice("utilities", self.utilities_percent)
            self.pie_slice2.setColor(QColor(63, 159, 159))
            self.pie_slice3 = QtChart.QPieSlice("bills", self.bills_percent)
            self.pie_slice3.setColor(QColor(220, 177, 45))
            self.pie_slice4 = QtChart.QPieSlice("transportation", self.transportation_percent)
            self.pie_slice4.setColor(QColor(136, 113, 160))
            self.pie_slice5 = QtChart.QPieSlice("loans", self.loans_percent)
            self.pie_slice5.setColor(QColor(162, 195, 219))
            self.pie_slice6 = QtChart.QPieSlice("budget", self.budget_percent)
            self.pie_slice6.setColor(QColor(39, 158, 21))

            self.series.append(self.pie_slice1)
            self.series.append(self.pie_slice2)
            self.series.append(self.pie_slice3)
            self.series.append(self.pie_slice4)
            self.series.append(self.pie_slice5)
            self.series.append(self.pie_slice6)

            self.chart.addSeries(self.series)
            self.chart.setBackgroundVisible(False)

            self.chart.legend().setFont(text_font(self.chart.legend()))
            self.chart.legend().setBackgroundVisible(False)
            self.chart.legend().setBorderColor(QColor(0,0,0))
            self.chart.legend().setAlignment(Qt.AlignBottom)

            self.chart_view.setFixedHeight(900)

            self.chart_view.setVisible(True)

            # slice look and animation
            slices = [self.pie_slice1, self.pie_slice2, self.pie_slice3, self.pie_slice4, self.pie_slice5,
                      self.pie_slice6]
            for slice in slices:
                slice.setBorderWidth(2)
                slice.setLabelFont(text_font(slice.labelFont()))
                slice.pressed.connect(lambda sl=slice: self.explode_slice(sl))
                slice.released.connect(lambda sl=slice: self.restored_sliced(sl))

            return self.chart_view

    def explode_slice(self, slice):
        slice.setExploded(True)
        slice.setExplodeDistanceFactor(0.1)
        slice.setLabelVisible(True)

    def restored_sliced(self, slice):
        slice.setExploded(False)
        slice.setLabelVisible(False)

    def go_to_home_screen(self):
        self.goToHomeScreen.emit()