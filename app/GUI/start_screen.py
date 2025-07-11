import sys
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QPropertyAnimation, QRect, QTimer
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QInputDialog, QMessageBox, \
    QListWidget, QSpacerItem, QSizePolicy, QApplication
from PyQt5.QtGui import QPixmap, QIcon, QFont

from app.GUI.fonts import title_font, text_font, list_widget_style, button_style1a, button_style3
from app.methods.methods import play_music
from app.GUI.fonts import button_style1, input_dialog_style1
from data.database import DatabaseManager
from custom_widgets import HoverFilter


class StartScreen(QWidget):
    goToIncome = pyqtSignal()  # create signal for transition to income screen

    def __init__(self, screen_manager):
        super().__init__()
        self.db = DatabaseManager()
        self.screen_manager = screen_manager
        self.name = None
        self.init_ui()

        # self.music_player = play_music()
        # self.music_player.play()

    def init_ui(self):
        self.setWindowTitle("Financial Planner")

        main_layout = QHBoxLayout()

        col1 = self.create_col1()
        self.create_col2()
        #col3 = self.create_col3()

        # Add columns to the main layout
        main_layout.addLayout(col1)
        #main_layout.addLayout(col3)

        self.setLayout(main_layout)

    def create_col1(self):
        col1 = QVBoxLayout()

        row1 = QHBoxLayout()
        row2 = QHBoxLayout()
        row3 = QHBoxLayout()
        row4 = QHBoxLayout()

        # Start button
        self.start_button = QPushButton("-  Start New Plan")
        self.start_button.clicked.connect(self.list_cancel)
        self.start_button.clicked.connect(self.show_input_dialog)  # closes load plan list if open
        self.hover_filter2 = HoverFilter()
        # self.start_button.installEventFilter(self.hover_filter2)
        # self.hover_filter2.HoverEnter.connect(lambda: self.expand_button_animation(self.start_button))

        row1.addWidget(self.start_button)
        row1.addStretch(1)

        # load plan button
        self.load_plan_button = QPushButton("-  Load Plan")

        row2.addWidget(self.load_plan_button)

        row2.addStretch(1)

        # settings button
        settings_button = QPushButton("-  Settings")
        row3.addWidget(settings_button)
        row3.addStretch(1)

        # exit button
        exit_button = QPushButton("-  Exit")
        exit_button.clicked.connect(sys.exit)
        row4.addWidget(exit_button)
        row4.addStretch(1)

        buttons = [self.start_button, self.load_plan_button, settings_button, exit_button]
        relative_font_size = max(10, self.screen_manager.screen_size[1] // 35)
        for button in buttons:
            button_style1(button)
            button.setMinimumSize(self.screen_manager.screen_size[0] // 5, self.screen_manager.screen_size[1] // 13)
            font = QFont()
            font.setPointSize(relative_font_size)
            button.setFont(font)

        col1.addStretch(1)
        rows = [row1, row2, row3, row4]
        for row in rows:
            col1.addLayout(row)
            col1.addSpacing(60)
        col1.addStretch(1)

        self.create_list()
        print(self.plan_name_list)
        if self.plan_name_list:
            self.load_plan_button.clicked.connect(self.show_list)
        else:
            self.load_plan_button.clicked.connect(
                lambda: QMessageBox.about(self, "No plan available", "There are no plans to load"))

        return col1

    def create_col2(self):
        intro_text = QLabel("BUDGETEER", self)
        title_font(intro_text)
        relative_font_size = max(10, self.screen_manager.screen_size[1] // 15)
        font = QFont()
        font.setPointSize(relative_font_size)
        intro_text.setFont(font)
        x = ((self.screen_manager.screen_size[0] - intro_text.sizeHint().width()) // 2)
        y = 30  # arbitrary vertical offset
        intro_text.move(x, y)
        intro_text.show()

    def create_col3(self):
        col3 = QVBoxLayout()

        # Image
        row2 = QHBoxLayout()
        image_label = QLabel(self)
        pixmap = QPixmap('C:/Users/sanad/planner/logo.png')
        scaled_pixmap = pixmap.scaled(1200, 1200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        row2.addWidget(image_label)

        # Add the image row to column 2
        col3.addLayout(row2)

        return col3

    """
    def create_load_list(self):
        # set the Qlist position to be next to load button
        x = self.screen_manager.screen_size[0] * 0.3125
        y = self.screen_manager.screen_size[1] * 10.8
        button_pos = self.get_button_pos(self.load_plan_button)
        self.plan_name_list.move(button_pos.x() + x, button_pos.y() - y + self.load_plan_button.height())

        # move select, cancel buttons relative to the pos of the Qlist
        list_pos = self.plan_name_list.pos()
        self.select_button.move(int(list_pos.x() + self.plan_name_list.width() / 2) - 2,
                                list_pos.y() + self.plan_name_list.height() - 9)
        self.cancel_button.move(int(list_pos.x()) + 2, list_pos.y() + self.plan_name_list.height() - 9)
    """


    # create an input dialog when the user presses start new plan
    def show_input_dialog(self):
        self.input_dialog = QInputDialog(self)
        self.input_dialog.setWindowFlags(self.input_dialog.windowFlags() | Qt.FramelessWindowHint) # remove window frame
        self.input_dialog.setWindowTitle("plan name")
        self.input_dialog.setLabelText("enter a name for your plan: ")
        input_dialog_style1(self.input_dialog)
        if self.input_dialog.exec_() == QInputDialog.Accepted:
            self.screen_manager.name = self.input_dialog.textValue()
            if self.screen_manager.name:  # Check if the user entered text
                print("name entered")
                self.go_to_income_screen()
            else:
                self.show_input_dialog()

    # emits the signal to transition
    def go_to_income_screen(self):
        self.goToIncome.emit()


    def create_list(self):
        self.plan_name_list = QListWidget(self)

        list_widget_style(self.plan_name_list)
        self.plan_name_list.setMinimumWidth(self.screen_manager.screen_size[0] // 5)
        self.plan_name_list.setMinimumHeight(self.screen_manager.screen_size[0] // 5)

        relative_font_size = max(10, self.screen_manager.screen_size[1] // 45)
        font = QFont()
        font.setPointSize(relative_font_size)
        self.plan_name_list.setFont(font)
        self.create_list_buttons()
        self.plan_name_list.hide()

        # Delay the position logic until after layout is complete
        QTimer.singleShot(0, self.position_list)

        # unpack list of plan names and a dict that contains plan names and income values
        name_list, _ = self.db.fetch_plan()
        self.plan_name_list.addItems(name_list)

        self.plan_name_list.setSelectionMode(QListWidget.SingleSelection)
        self.plan_name_list.setVisible(False)

        # set the Qlist position to be next to load button

    def position_list(self):

        x = self.screen_manager.screen_size[0] * 0.25

        button_pos = self.get_button_pos(self.load_plan_button)
        print("Button global position:", button_pos)
        print(button_pos.x())
        self.plan_name_list.move(button_pos.x() + int(x), button_pos.y())

        # move select, cancel buttons relative to the pos of the Qlist
        list_pos = self.plan_name_list.pos()
        self.select_button.move(int(list_pos.x() + self.plan_name_list.width() / 2) - 2,
                                list_pos.y() + self.plan_name_list.height() - 9)
        self.cancel_button.move(int(list_pos.x()) + 2, list_pos.y() + self.plan_name_list.height() - 9)

    def show_list(self):
        self.plan_name_list.setVisible(True)
        self.select_button.setVisible(True)
        self.cancel_button.setVisible(True)

    def get_button_pos(self, button: QPushButton):
        return button.pos()

    def create_list_buttons(self):
        self.select_button = QPushButton("select", self)
        self.select_button.setFixedSize(int(self.plan_name_list.width()/2), 40)
        button_style3(self.select_button)
        self.select_button.clicked.connect(self.list_select)

        self.cancel_button = QPushButton("cancel", self)
        self.cancel_button.setFixedSize(int(self.plan_name_list.width()/2), 40)
        self.cancel_button.clicked.connect(self.list_cancel)
        button_style3(self.cancel_button)

        self.cancel_button.setVisible(False)
        self.select_button.setVisible(False)

    def list_cancel(self):
        self.plan_name_list.setVisible(False)
        self.cancel_button.setVisible(False)
        self.select_button.setVisible(False)

    # returns the selected value from the list as text
    def get_name_from_list(self):
        item = self.plan_name_list.currentItem()
        if item:
            self.screen_manager.name = item.text()
            print(item.text())
            return item.text()
        return None

    def list_select(self, plan_name):
        _, plan_dict = self.db.fetch_plan()
        plan_name = self.get_name_from_list()
        if plan_name:
            if plan_dict[plan_name]:
                print(f'income is not 0, it is {plan_dict[plan_name]}')
                self.screen_manager.go_to_home_screen()
            else:
                print("income is zero")
                self.screen_manager.go_to_questions()

        # hide list after transitioning to another screen
        self.list_cancel()

    def button_width(self, button: QPushButton):
        button.setFixedWidth(button.sizeHint().width() + 50)

    def expand_button_animation(self, button: QPushButton):
        button_pos = self.get_button_pos(button)
        animation = QPropertyAnimation(button, b"size")
        animation.setDuration(200)
        animation.setStartValue(button.size().width())
        animation.setEndValue(button.size().width()+20)
        animation.start()


