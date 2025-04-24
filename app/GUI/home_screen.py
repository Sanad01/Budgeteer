import json
import os.path

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QTableWidget, \
    QDateEdit, QComboBox, QLineEdit, QTableWidgetItem
from PyQt5.QtWidgets import QHeaderView
from PyQt5.QtGui import QFont, QIntValidator
import calendar
from datetime import datetime

from data.database import DatabaseManager
from custom_widgets import ClickableFrame
from app.GUI.fonts import table_style, text_box_style1, combobox_style, button_style4, frame_style


class HomeScreen(QWidget):

    def __init__(self, screen_manager):
        super().__init__()
        self.db = DatabaseManager()
        self.screen_manager = screen_manager
        self.init_json()
        self.tables = []
        self.data = {}
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.addSpacing(int(self.screen_manager.height()/13))
        outer_frame = QFrame(self)
        outer_frame.setFrameShape(QFrame.Panel)  # Set the frame shape to Box (border around the frame)
        outer_frame.setStyleSheet("background-color: #A1662F;")

        inner_frame = QFrame(outer_frame)
        inner_frame.setFrameShape(QFrame.Panel)  # Set the frame shape to Box (border around the frame)
        inner_frame.setStyleSheet("background-color: white;")
        self.grid = QGridLayout(inner_frame)
        self.create_calendar()

        # first row
        calendar_frame_layout = QVBoxLayout(outer_frame)
        calendar_frame_layout.addWidget(inner_frame)
        outer_frame.setLayout(calendar_frame_layout)

        row1 = QHBoxLayout(self)
        row1.addSpacing(int(self.screen_manager.width()/3))  # Add stretchable space
        row1.addWidget(outer_frame)
        row1.addSpacing(int(self.screen_manager.width()/3))  # Add stretchable space

        # second row
        row2 = QHBoxLayout(self)
        row2.addSpacing(int(self.screen_manager.width()/3))
        self.dropdown = QComboBox(self)
        self.dropdown.addItems(["Food", "Groceries", "shopping", "other"])
        combobox_style(self.dropdown)

        self.amount = QLineEdit(self)
        self.amount.setPlaceholderText("Enter amount here")
        text_box_style1(self.amount)
        int_validator = QIntValidator(0, 999999999)
        self.amount.setValidator(int_validator)
        self.amount.textEdited.connect(lambda text=self.amount.text(), text_box=self.amount:
                                       self.screen_manager.add_comma(text_box, text))

        self.description = QLineEdit(self)
        self.description.setPlaceholderText("Enter description here")
        text_box_style1(self.description)

        row2.addWidget(self.dropdown)
        row2.addWidget(self.amount)
        row2.addWidget(self.description)
        row2.addSpacing(int(self.screen_manager.width()/3))

        # third row
        row3 = QHBoxLayout(self)
        row3.addSpacing(int(self.screen_manager.width()/3))

        self.add_button = QPushButton("Add Expense", self)
        self.add_button.clicked.connect(self.insert_json_info)
        button_style4(self.add_button)

        self.delete_button = QPushButton("Delete Expense", self)
        button_style4(self.delete_button)

        row3.addWidget(self.add_button)
        row3.addWidget(self.delete_button)
        row3.addSpacing(int(self.screen_manager.width()/3))

        # fourth row
        row4 = QHBoxLayout(self)
        row4.addSpacing(int(self.screen_manager.width()/3))

        table_columns = 3
        table_rows = 10
        for i in range(32):
            table = QTableWidget(table_rows, table_columns, self)
            table.setHorizontalHeaderLabels(["Category", "Amount", "Description"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.adjust_table_height(table)
            table.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            table.verticalHeader().setVisible(False)
            table_style(table)
            if i != datetime.today().day:
                table.hide()
            else:
                self.restore_table_info(table, str(i))  # restore db data as soon as home_screen is open
                table.show()
            self.tables.append(table)
            row4.addWidget(table)

        row4.addSpacing(int(self.screen_manager.width()/3))

        main_layout.addLayout(row1)
        main_layout.addSpacing(50)
        main_layout.addLayout(row2)
        main_layout.addLayout(row3)
        main_layout.addLayout(row4)
        self.setLayout(main_layout)

    def on_frame_click(self, frame, *args):
        for i, box in enumerate(self.calendar_boxes):
            if hasattr(box, 'selected') and box.selected:  # don't affect the day labels (Sun, Mon...)
                box.setStyleSheet("background-color: white;")
                self.tables[i].clear()
                self.tables[i].hide()
                self.tables[i].setHorizontalHeaderLabels(["Category", "Amount", "Description"])  # don't clear header
                box.selected = False
        frame.selected = True
        frame.setStyleSheet("background-color: gray;")


    def create_calendar(self):
        self.calendar_boxes = []
        for i in range(31):
            frame = ClickableFrame(self)
            frame.setMaximumSize(90, 90)
            frame.setFrameShape(QFrame.StyledPanel)
            frame.clicked.connect(lambda qframe=frame: self.on_frame_click(qframe))
            frame.clicked.connect(self.show_day_table)
            frame_layout = QHBoxLayout(frame)
            day_num = QLabel(str(i+1), frame)
            day_num.setAlignment(Qt.AlignTop)
            frame_layout.addWidget(day_num)
            if i == datetime.today().day:
                frame.click()  # select the frame corresponding to the current daty of the month
            self.calendar_boxes.append(frame)
            print(f"this is the size of calendar_boxes{len(self.calendar_boxes)}")

        self.create_day_labels()

        now = datetime.now()
        current_year = now.year
        current_month = now.month
        days_in_month = calendar.monthrange(current_year, current_month)[1]
        print(f"these are the days in this month {days_in_month}")

        # Get the first day of the month (0 = Monday, 6 = Sunday)
        first_day_of_month = calendar.monthrange(current_year, current_month)[0]

        day_counter = 0

        for row in range(1, 7):
            for col in range(7):
                if row == 1 and col < first_day_of_month:
                    continue  # Skip the cells before the first day of the month
                if day_counter < days_in_month:
                    self.grid.addWidget(self.calendar_boxes[day_counter], row, col)
                    day_counter += 1


    # shows the table for the relevant day of the month
    def show_day_table(self):
        for i, frame in enumerate(self.calendar_boxes):
            if frame.selected:
                self.tables[i].show()
                self.restore_table_info(self.tables[i], str(i))


    def adjust_table_height(self, table: QTableWidget):
        row_height = 0
        for row in range(table.rowCount()):
            row_height += table.rowHeight(row)

        header_height = table.horizontalHeader().height()
        total_height = row_height + header_height
        table.setFixedHeight(total_height)

    def create_day_labels(self):
        # font for day labels
        font = QFont()
        font.setBold(True)
        font.setPointSize(14)

        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        for i, day in enumerate(days):
            day_label = QLabel(day, self)
            day_label.setFont(font)
            day_label.setMaximumHeight(50)
            day_label.setStyleSheet("background-color: #bf0404;"
                                    "border: 1px solid white;")
            day_label.setFrameShape(QFrame.Panel)
            day_label.setFrameShadow(QFrame.Raised)
            day_label.setAlignment(Qt.AlignCenter)
            day_label.resize(self.calendar_boxes[1].width(), self.calendar_boxes[1].height())
            self.grid.addWidget(day_label, 0, i)

    def insert_json_info(self):
        # Fetch category, amount, and description from UI
        category = self.dropdown.currentText()
        amount = str(self.amount.text().replace(',', ''))
        description = str(self.description.text())
        inserted_data = [category, amount, description]

        # Initialize current date
        year = str(datetime.today().year)
        month = str(datetime.today().month)
        day = None

        for i, frame in enumerate(self.calendar_boxes):
            if frame.selected:
                day = str(i)
                break

        if day is None:
            print("No day selected!")
            return


        # Fetch existing json_expenses from the database for the given name
        query = QSqlQuery()
        query.prepare("SELECT json_expenses FROM answers WHERE name = :name")
        query.bindValue(":name", self.screen_manager.name)

        if query.exec_() and query.next():
            json_expenses_str = query.value(0)
            if json_expenses_str:
                data = json.loads(json_expenses_str)  # Convert JSON string back to Python dict
            else:
                data = {}
        else:
            print("Error fetching data:", query.lastError().text())
            data = {}

        if day not in data[year][month]:
            data[year][month][day] = []

        # Add the new entry to the existing data
        data[year][month][day].append(category)
        data[year][month][day].append(amount)
        data[year][month][day].append(description)

        updated_json_expenses = json.dumps(data, indent=4, sort_keys=True)

        # Update the database with the new json_expenses data
        update_query = QSqlQuery()
        update_query.prepare("UPDATE answers SET json_expenses = :json_expenses WHERE name = :name")
        update_query.bindValue(":json_expenses", updated_json_expenses)
        update_query.bindValue(":name", self.screen_manager.name)

        if not update_query.exec_():
            print("Error updating json_expenses:", update_query.lastError().text())

        # update the qtable with the data entered
        self.update_table(data, year, month, day)

    def update_table(self, data: dict, year: str, month: str, day: str):
        category = self.dropdown.currentText()
        amount = str(self.amount.text().replace(',', ''))
        description = str(self.description.text())
        inserted_data = [category, amount, description]

        current_table = None
        for i, table in enumerate(self.tables):
            if table.isVisible():
                current_table = table
                break
            else:
                current_table = None

        row_count = current_table.rowCount()
        col_count = current_table.columnCount()

        for row in range(row_count):
            if current_table.item(row, 0) is None:  # Find the first empty row
                for col in range(col_count):
                    if col < len(data[year][month][day]):
                        item = QTableWidgetItem(inserted_data[col])
                        current_table.setItem(row, col, item)
                break  # Exit after filling the first empty row

    def restore_table_info(self, table: QTableWidget, day: str):
        year = str(datetime.today().year)
        month = str(datetime.today().month)

        query = QSqlQuery()
        query.prepare("SELECT json_expenses FROM answers WHERE name = :name")
        query.bindValue(":name", self.screen_manager.name)

        data = {}
        if query.exec_() and query.next():
            json_expenses_str = query.value(0)
            data = json.loads(json_expenses_str)  # Convert JSON string back to Python dict

        if data and year in data and month in data[year] and day in data[year][month]:
            row_count = table.rowCount()
            col_count = table.columnCount()
            items_count = 0

            for row in range(row_count):
                if items_count < len(data[year][month][day]):
                    for col in range(col_count):
                        if col < 3:
                            item = QTableWidgetItem(data[year][month][day][items_count])
                            table.setItem(row, col, item)
                            items_count += 1
                        else:
                            break


    def init_json(self):
        year = str(datetime.today().year)
        month = str(datetime.today().month)

        query = QSqlQuery()
        query.prepare("SELECT json_expenses FROM answers WHERE name = :name")
        query.bindValue(":name", self.screen_manager.name)

        if query.exec_() and query.next():
            json_expenses_str = query.value(0)
            if json_expenses_str:
                data = json.loads(json_expenses_str)  # Convert JSON string back to Python dict
            else:
                data = {}
        else:
            print("Error fetching data:", query.lastError().text())
            data = {}

        if year not in data:
            data[year] = {}
        if month not in data[year]:
            data[year][month] = {}

        updated_json_expenses = json.dumps(data, indent=4, sort_keys=True)

        update_query = QSqlQuery()
        update_query.prepare("UPDATE answers SET json_expenses = :json_expenses WHERE name = :name")
        update_query.bindValue(":json_expenses", updated_json_expenses)
        update_query.bindValue(":name", self.screen_manager.name)

        if not update_query.exec_():
            print("Error updating json_expenses:", update_query.lastError().text())


