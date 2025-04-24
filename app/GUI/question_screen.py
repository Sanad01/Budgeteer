import sys

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QIntValidator
from app.GUI.fonts import button_style1a, text_font, text_box_style, text_font2
from data.database import DatabaseManager


class QuestionScreen(QWidget):
    goBack = pyqtSignal()  # create signal to transition back to start screen
    cont = pyqtSignal()  # create signal to transition to analysis screem

    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager
        self.category = {
            "income": 0,
            "rent": 0,
            "utilities": 0,
            "bills": 0,
            "transportation": 0,
            "loans": 0
        }
        self.db = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Questions Window")
        self.resize(1920, 1080)
        self.master_layout = QVBoxLayout()

        self.questions = [
            "What is your monthly income after taxes? (avg if wages)",
            "How much do you pay for rent?",
            "How much do you pay for utilities? (electric, gas, etc...)",
            "How much do you spend on bills? (internet, phone bill, subscription)",
            "How much do you spend on transportation? (gas, bus fare, etc...)",
            "How much do you spend on recurring payments? (loans, debt, insurance, child support, etc...)",
        ]
        # widget and row setup
        row1 = QHBoxLayout()
        question1 = QLabel(self.questions[0])
        question1.setFont(text_font(question1))
        row2 = QHBoxLayout()
        row2.setAlignment(Qt.AlignLeft)
        self.box1 = QLineEdit()
        self.box_setup(self.box1)
        text_box_style(self.box1)
        self.box1.textEdited.connect(lambda text, box=self.box1: self.screen_manager.add_comma(box, text))
        money_sign1 = QLabel("$")
        text_font2(money_sign1)

        row3 = QHBoxLayout()
        question2 = QLabel(self.questions[1])
        question2.setFont(text_font(question2))
        row4 = QHBoxLayout()
        row4.setAlignment(Qt.AlignLeft)
        self.box2 = QLineEdit()
        self.box_setup(self.box2)
        text_box_style(self.box2)
        self.box2.textEdited.connect(lambda text, box=self.box2: self.screen_manager.add_comma(box, text))
        money_sign2 = QLabel("$")
        text_font2(money_sign2)

        row5 = QHBoxLayout()
        question3 = QLabel(self.questions[2])
        question3.setFont(text_font(question3))
        row6 = QHBoxLayout()
        row6.setAlignment(Qt.AlignLeft)
        self.box3 = QLineEdit()
        self.box_setup(self.box3)
        text_box_style(self.box3)
        self.box3.textEdited.connect(lambda text, box=self.box3: self.screen_manager.add_comma(box, text))
        money_sign3 = QLabel("$")
        text_font2(money_sign3)

        row7 = QHBoxLayout()
        question4 = QLabel(self.questions[3])
        question4.setFont(text_font(question4))
        row8 = QHBoxLayout()
        row8.setAlignment(Qt.AlignLeft)
        self.box4 = QLineEdit()
        self.box_setup(self.box4)
        text_box_style(self.box4)
        self.box4.textEdited.connect(lambda text, box=self.box4: self.screen_manager.add_comma(box, text))
        money_sign4 = QLabel("$")
        text_font2(money_sign4)

        row9 = QHBoxLayout()
        question5 = QLabel(self.questions[4])
        question5.setFont(text_font(question5))
        row10 = QHBoxLayout()
        row10.setAlignment(Qt.AlignLeft)
        self.box5 = QLineEdit()
        self.box_setup(self.box5)
        text_box_style(self.box5)
        self.box5.textEdited.connect(lambda text, box=self.box5: self.screen_manager.add_comma(box, text))
        money_sign5 = QLabel("$")
        text_font2(money_sign5)

        row11 = QHBoxLayout()
        question6 = QLabel(self.questions[5])
        question6.setFont(text_font(question6))
        row12 = QHBoxLayout()
        row12.setAlignment(Qt.AlignLeft)
        self.box6 = QLineEdit()
        self.box_setup(self.box6)
        text_box_style(self.box6)
        self.box6.textEdited.connect(lambda text, box=self.box6: self.screen_manager.add_comma(box, text))
        money_sign6 = QLabel("$")
        text_font2(money_sign6)

        # add widgets to rows
        row1.addWidget(question1)
        row2.addWidget(self.box1)
        row2.addWidget(money_sign1)

        row3.addWidget(question2)
        row4.addWidget(self.box2)
        row4.addWidget(money_sign2)

        row5.addWidget(question3)
        row6.addWidget(self.box3)
        row6.addWidget(money_sign3)

        row7.addWidget(question4)
        row8.addWidget(self.box4)
        row8.addWidget(money_sign4)

        row9.addWidget(question5)
        row10.addWidget(self.box5)
        row10.addWidget(money_sign5)

        row11.addWidget(question6)
        row12.addWidget(self.box6)
        row12.addWidget(money_sign6)

        rows = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10, row11, row12]
        # add rows to layout
        for row in rows:
            self.master_layout.addLayout(row)

        last_row = QHBoxLayout()
        # buttons on the bottom
        continue_button = QPushButton("Continue")
        button_style1a(continue_button)
        back_button = QPushButton("Back")
        button_style1a(back_button)

        continue_button.clicked.connect(self.continue_button)
        back_button.clicked.connect(self.go_back)

        last_row.addWidget(back_button)
        last_row.addWidget(continue_button)

        self.master_layout.addLayout(last_row)
        self.setLayout(self.master_layout)

    # emit the transition signal
    def go_back(self):
        self.goBack.emit()

    def contin(self):
        self.cont.emit()

    def insert_answers_into_db(self, data: dict):
        query = QSqlQuery()

        # Calculate budget
        expenses = sum(value for category, value in data.items() if category != "income")
        budget = data["income"] - expenses
        if expenses > data["income"]:
            QMessageBox.warning(self, "you are in debt", "according to the numbers you entered you are losing money"
                                                         " monthly, if this is the case this app will not help you!")
            return 0

        print(f"this is your expenses: {expenses}")
        print(f"this is the budget {budget}")

        query.prepare('''
               INSERT INTO answers (
                   name, 
                   income, 
                   rent, 
                   utilities, 
                   bills, 
                   transportation, 
                   loans, 
                   budget
               ) VALUES (
                   :name, 
                   :income, 
                   :rent, 
                   :utilities, 
                   :bills, 
                   :transportation, 
                   :loans, 
                   :budget
               )
           ''')
        query.bindValue(':name', self.screen_manager.name)
        query.bindValue(':income', data.get('income'))
        query.bindValue(':rent', data.get('rent'))
        query.bindValue(':utilities', data.get('utilities'))
        query.bindValue(':bills', data.get('bills'))
        query.bindValue(':transportation', data.get('transportation'))
        query.bindValue(':loans', data.get('loans'))
        query.bindValue(':budget', budget)

        if not query.exec_():
            # Detailed error handling
            error = query.lastError()
            print(f"Error inserting data: {error.text()}")
            print(f"SQL query: {query.executedQuery()}")
        else:
            print("Data inserted successfully.")

    def continue_button(self):
        text_boxes = [self.box1.text(), self.box2.text(), self.box3.text(), self.box4.text(), self.box5.text(),
                      self.box6.text()]
        # check if any text boxes are empty and display warning if they are
        if any(text == "" for text in text_boxes):
            QMessageBox.warning(self, "Input Error", "One or more fields are missing!")
            return
        # store the values inserted into each text box as integer values into self.categories
        keys = self.category.keys()
        for key, text in zip(keys, text_boxes):
            self.category[key] = int(text.replace(",", ""))
        print(f"this is the income {self.category['income']}")
        print(self.category)
        if self.insert_answers_into_db(self.category) == 0:
            return

        self.percent = self.db.get_percentages(self.screen_manager.name)

        if self.percent:
            self.income = self.percent["income"]
            self.budget_percent = self.percent["budget"]
            self.loans_percent = self.percent["loans"]
            self.transportation_percent = self.percent["transportation"]
            self.rent_percent = self.percent["rent"]
            self.bills_percent = self.percent["bills"]
            self.utilities_percent = self.percent["utilities"]
        else:
            self.income = self.budget_percent = self.loans_percent = self.transportation_percent = None
            self.rent_percent = self.bills_percent = self.utilities_percent = None

        self.contin()

    def box_setup(self, text_box: QLineEdit):
        text_box.setMaximumWidth(200)
        text_box.setAlignment(Qt.AlignLeft)
        text_box.setFont(text_font(text_box))
        int_validator = QIntValidator(0, 999999999)
        text_box.setValidator(int_validator)

        return text_box



