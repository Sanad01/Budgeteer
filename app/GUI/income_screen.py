from PyQt5.QtWidgets import QWidget, QCheckBox, QSizePolicy, QGraphicsOpacityEffect, QRadioButton, QButtonGroup, \
    QDateEdit
from PyQt5.QtCore import pyqtSignal, QObject, QPoint, QPropertyAnimation, QEasingCurve, QDate
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QIntValidator

from app.GUI.fonts import check_box, title_font, text_box_style, button_style1a, calendar_style, date_box_style
from data.database import DatabaseManager


class IncomeScreen(QWidget):
    goBack = pyqtSignal()
    contToAnalysis = pyqtSignal()

    def __init__(self, screen_manager):
        super().__init__()
        self.screen_manager = screen_manager
        self.update_signal = pyqtSignal(int)  # for updating values in self.category
        self.animations = []
        self.category = {
            "income": 0,
            "rent": 0,
            "utilities": 0,
            "bills": 0,
            "transportation": 0,
            "loans": 0
        }
        self.pay_type = None
        self.expenses = 0
        self.db = DatabaseManager()
        self.init_ui()


    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        question1 = QLabel("How much do you make per paycheck after taxes?", self)
        question2 = QLabel("How much do you pay for rent?", self)
        question3 = QLabel("How much do you pay for utilities? (electric, gas)", self)
        question4 = QLabel("How much do you spend on bills? (internet, phone bill, subscription)", self)
        question5 = QLabel("How much do you spend on transportation? (gas, bus fare)", self)
        question6 = QLabel("How much do you spend on recurring payments? (debt, insurance, child support)", self)
        question7 = QLabel("When was your last paycheck?", self)

        self.questions = [question1, question2, question3, question4, question5, question6, question7]
        self.question_number = 0

        self.box1 = QLineEdit(self)
        self.box2 = QLineEdit(self)
        self.box3 = QLineEdit(self)
        self.box4 = QLineEdit(self)
        self.box5 = QLineEdit(self)
        self.box6 = QLineEdit(self)
        # user chooses date
        self.box7 = QDateEdit(self)
        self.box7.setCalendarPopup(True)
        self.box7.setDate(QDate.currentDate())
        self.box7.setMaximumDate(QDate.currentDate())

        #date styles
        date_box_style(self.box7)
        calendar_style(self.box7.calendarWidget())

        self.text_boxes = [self.box1, self.box2, self.box3, self.box4, self.box5, self.box6, self.box7]

        self.row1 = QHBoxLayout(self)
        self.row1.setAlignment(Qt.AlignCenter)

        for question in self.questions:
            question.setVisible(False)
            title_font(question)
            self.row1.addWidget(question)

        self.row2 = QHBoxLayout(self)
        self.row2.setAlignment(Qt.AlignCenter)

        int_validator = QIntValidator(0, 999999999)
        for box in self.text_boxes:
            box.setFixedWidth(400)
            box.setFixedHeight(int(self.height() / 6))
            if box != self.box7:
                box.setValidator(int_validator)
                box.textEdited.connect(lambda text, text_box=box: self.screen_manager.add_comma(text_box, text))
                text_box_style(box)
            box.setAlignment(Qt.AlignCenter)
            box.setVisible(False)
            self.row2.addWidget(box)

        self.box1.setVisible(True)

        self.row4 = QHBoxLayout(self)

        self.button_group = QButtonGroup()
        self.weekly_radio = QRadioButton("Weekly")
        self.biweekly_radio = QRadioButton("Biweekly")
        self.button_group.addButton(self.weekly_radio)
        self.button_group.addButton(self.biweekly_radio)

        self.row4.addStretch(1)
        self.row4.addWidget(self.weekly_radio)
        self.row4.addWidget(self.biweekly_radio)
        self.row4.addStretch(1)


        self.row3 = QHBoxLayout(self)
        self.next = QPushButton("Next", self)
        button_style1a(self.next)
        self.next.clicked.connect(self.next_button)
        # self.next.move(self.screen_manager.width() - 10, self.screen_manager.height() - 10)
        self.back = QPushButton("Back", self)
        button_style1a(self.back)
        self.back.clicked.connect(self.back_button)
        # self.back.move(self.next.pos().x() - self.next.width(), self.next.pos().y())

        self.continue_button = QPushButton("Continue", self)
        button_style1a(self.continue_button)
        self.continue_button.clicked.connect(self.cont_button_function)
        self.continue_button.setVisible(False)

        self.row3.addWidget(self.back)
        self.row3.addWidget(self.next)
        self.row3.addWidget(self.continue_button)

        main_layout.addStretch(1)
        main_layout.addLayout(self.row1)
        main_layout.addSpacing(50)
        main_layout.addLayout(self.row2)
        main_layout.addSpacing(30)
        main_layout.addLayout(self.row4)
        main_layout.addStretch(1)
        main_layout.addLayout(self.row3)

        question1.setVisible(True)
        # fade for first question before pressing next
        self.fade_animation(question1)
        self.fade_animation(self.box1)
        self.setLayout(main_layout)

    def next_button(self):
        if self.animation is None or self.animation.state() == QPropertyAnimation.Stopped:
            if self.text_boxes[self.question_number].text() == '':
                if self:
                    QMessageBox.warning(self, "Input Error", "Please enter a $ amount")
                    return 0
            else:
                income = int(self.text_boxes[0].text().replace(',', ''))
                if self.pay_type == "Weekly":
                    income *= 4
                elif self.pay_type == "Biweekly":
                    income *= 2

                if self.question_number != 0:  # calculate expenses without adding the income]
                    self.calculate_expenses()
                    if self.expenses > income:
                        # do not add current text box value to expenses
                        self.expenses -= int(self.text_boxes[self.question_number].text().replace(',', ''))
                        QMessageBox.warning(self, "you are in debt",
                                            "according to the numbers you entered you are losing money"
                                            " monthly, if this is the case this app will not help you!")

                        return 0

                if self.question_number == 0:
                    # save pay type
                    selected_button = self.button_group.checkedButton()
                    if selected_button:
                        self.pay_type = selected_button.text()
                    else:
                        QMessageBox.warning(self, "pay type can't be empty", "please choose weekly or bi-weekly")
                        return 0

                    self.weekly_radio.setVisible(False)
                    self.biweekly_radio.setVisible(False)

                self.questions[self.question_number].setVisible(False)
                self.text_boxes[self.question_number].setVisible(False)
                self.question_number += 1
                self.questions[self.question_number].setVisible(True)
                self.fade_animation(self.questions[self.question_number])
                self.text_boxes[self.question_number].setVisible(True)
                self.fade_animation(self.text_boxes[self.question_number])

            if self.question_number == len(self.questions) - 1:
                self.next.setVisible(False)
                self.continue_button.setVisible(True)

    def back_button(self):
        if self.animation is None or self.animation.state() == QPropertyAnimation.Stopped:
            if self.question_number > 1:
                self.expenses -= int(self.text_boxes[self.question_number - 1].text().replace(',', ''))
                self.continue_button.setVisible(False)
                self.next.setVisible(True)
                self.questions[self.question_number].setVisible(False)
                self.text_boxes[self.question_number].setVisible(False)
                self.question_number -= 1
                # radio buttons
                if self.question_number == 0:
                    self.weekly_radio.setVisible(True)
                    self.biweekly_radio.setVisible(True)
                    self.fade_animation(self.weekly_radio)
                    self.fade_animation(self.biweekly_radio)

                self.questions[self.question_number].setVisible(True)
                self.fade_animation(self.questions[self.question_number])
                self.text_boxes[self.question_number].setVisible(True)
                self.fade_animation(self.text_boxes[self.question_number])
            else:
                self.go_back()

    def fade_animation(self, text: QLabel):
        opacity_effect = QGraphicsOpacityEffect(self)
        text.setGraphicsEffect(opacity_effect)
        opacity_effect.setOpacity(0.0)

        self.animation = QPropertyAnimation(opacity_effect, b'opacity')
        self.animation.setDuration(1300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.animations.append(self.animation) # prevent garbage collection of animation
        self.animation.start()

    def go_back(self):
        self.goBack.emit()
        # if user backs out of income_screen clear all text boxes
        for box in self.text_boxes:
            if box.text() != '':
                box.clear()

    def insert_answers_into_db(self, data: dict):
        query = QSqlQuery()

        # Calculate budget
        if self.pay_type == "Weekly":
            data["income"] *= 4
        elif self.pay_type == "Biweekly":
            data["income"] *= 2
        budget = data["income"] - self.expenses

        print(f"this is your expenses: {self.expenses}")
        print(f"this is the budget {budget}")

        query.prepare('''
               UPDATE answers SET 
                income = :income,
                pay_type = :pay_type,
                rent = :rent,
                utilities = :utilities,
                bills = :bills,
                transportation = :transportation,
                loans = :loans,
                budget = :budget
                WHERE name = :name
                ''')
        query.bindValue(':name', self.screen_manager.name)
        query.bindValue(':income', data.get('income'))
        query.bindValue(':pay_type', self.pay_type)
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

        self.insert_date_into_db()


    def emit_cont_signal(self):
        self.contToAnalysis.emit()

    def cont_button_function(self):
        text_boxes = [self.box1.text(), self.box2.text(), self.box3.text(), self.box4.text(), self.box5.text(),
                      self.box6.text()]



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

        self.emit_cont_signal()


    def calculate_expenses(self):
        self.expenses += int(self.text_boxes[self.question_number].text().replace(',', ''))
        print(f"what is this {self.expenses}")

    def insert_date_into_db(self):
        date_str = self.box7.date().toString("yyyy-MM-dd")

        query = QSqlQuery()

        query.prepare('''
        UPDATE answers SET last_paycheck = :last_paycheck
        WHERE name = :name
        ''')
        query.bindValue(':name', self.screen_manager.name)
        query.bindValue(':last_paycheck', date_str)

        if not query.exec_():
            # Detailed error handling
            error = query.lastError()
            print(f"Error inserting data: {error.text()}")
            print(f"SQL query: {query.executedQuery()}")
        else:
            print("Date for paycheck inserted successfully.")
