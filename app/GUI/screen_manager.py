import sys

from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QMainWindow
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QPropertyAnimation, Qt, QAbstractAnimation, pyqtSignal
from PyQt5 import QtWidgets
from data.database import DatabaseManager
from PyQt5.uic import loadUi

from app.GUI.start_screen import StartScreen
from app.GUI.analysis_screen import AnalysisScreen
from app.GUI.income_screen import IncomeScreen
from app.GUI.home_screen import HomeScreen
from app.GUI.question_screen import QuestionScreen


class ScreenManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.move(800, 200)
        self.app = QApplication(sys.argv)
        self.setStyleSheet("background-color: #D8CAB8;")
        self.start_screen = StartScreen(self)
        self.income_screen = None
        self.question_screen = QuestionScreen(self)
        self.analysis_screen = None
        self.home_screen = None
        self.db = DatabaseManager()
        self.name = None

        # place each screen in a QStackedWidget
        self.widget = QtWidgets.QStackedWidget()
        self.widget.addWidget(self.start_screen)
        self.widget.addWidget(self.question_screen)

        self.setCentralWidget(self.widget)
        self.widget.setFixedHeight(1080)
        self.widget.setFixedWidth(1920)

        # signals for screen transitions
        self.start_screen.goToIncome.connect(self.go_to_income_screen)

    def go_to_income_screen(self):
        if self.income_screen is None:
            self.income_screen = IncomeScreen(self)

        self.widget.addWidget(self.income_screen)
        self.income_screen.contToAnalysis.connect(self.go_to_analysis)
        self.widget.setCurrentWidget(self.income_screen)
        self.income_screen.goBack.connect(self.go_to_start_screen)

    def go_to_questions(self):
        self.widget.setCurrentWidget(self.question_screen)

    def go_to_analysis(self):
        # makes sure to init only after the table is updated
        if self.analysis_screen is None:
            self.analysis_screen = AnalysisScreen(self)

        self.widget.addWidget(self.analysis_screen)
        self.analysis_screen.goToHomeScreen.connect(self.go_to_home_screen)
        self.widget.setCurrentWidget(self.analysis_screen)

    def go_to_home_screen(self):
        # makes sure to init only after the table is updated
        if self.home_screen is None:
            self.home_screen = HomeScreen(self)

        self.widget.addWidget(self.home_screen)
        self.widget.setCurrentWidget(self.home_screen)

    def go_to_start_screen(self):
        self.widget.setCurrentWidget(self.start_screen)

    def get_selected_name(self, selected_name):
        self.name = selected_name
        return self.name

    # add comma between every three nums
    def add_comma(self, box, text):
        text = text.replace(",", "")

        try:
            number = int(text)

            # Format the number with commas
            formatted_text = '{:,}'.format(number)
        except ValueError:
            # If the conversion fails, use the original text
            formatted_text = text

        box.blockSignals(True)  # stops textChanges from emitting a signal when adding a comma
        box.setText(formatted_text)
        box.blockSignals(False)

    # execute program
    def run(self):
        self.show()
        self.app.exec_()

