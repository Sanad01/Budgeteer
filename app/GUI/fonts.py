from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QPushButton, QLabel, QInputDialog, QListWidget, QLineEdit, QCheckBox, QTableWidget, \
    QComboBox, QFrame


def title_font(title) -> QFont:
    title.setStyleSheet("""
                        QLabel {
                        color: #00AB2E;
                        font-size: 65px;
                        }
                        """)

def title_font2(title) -> QFont:
    title = QFont("Open Sans", 40, QFont.Bold)
    return title

def text_font(text) -> QFont:
    text = QFont("Roboto", 15)
    return text

def text_font2(text):
    text.setStyleSheet("""
                    QLabel {
                    color: green;
                    font-size: 24px;
                    }
                    """)

def button_style1(button: QPushButton):
    button.setStyleSheet("""
                        QPushButton {
                        background-color: #D8CAB8;
                            color: black;
                            text-align: left;
                            border: none;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 50px;
                            margin: 4px 2px;
                            transition-duration: 0.4s;
                            cursor: pointer;
                        }
                        QPushButton:hover {
                            background-color: #4CAF50; /* Green border */
                            color: black; 
                            width: 30px;
                            border:none;
                        }
                        
                    """)

def button_style1a(button: QPushButton):
    button.setStyleSheet("""
                        QPushButton {
                            background-color: #4CAF50;
                            border: 1px solid black;
                            color: black; /* White text */
                            padding: 5px 20px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 28px;
                            margin: 4px 2px;
                            transition-duration: 0.4s;
                            cursor: pointer;
                        }
                        QPushButton:hover {
                            background-color: green;
                            color: black; 

                            border:none;
                        }
                        QPushButton:pressed {
                            background-color: gold;
                            border: 1px solid black;
                        }
                    """)

def button_style2(button: QPushButton):
    button.setStyleSheet("""
                        QPushButton {
                            background-color: none; 
                            border: none;
                            color: black; 
                            padding: 5px 20px;
                            text-align: center;
                            text-decoration: underline;
                            display: inline-block;
                            font-size: 24px;
                            margin: 30px 15px;
                            transition-duration: 0.4s;
                            cursor: pointer;
                        }
                        QPushButton:hover {
                            background-color: #4CAF50; 
                            color: black; 
                            
                            border:none;
                        }
                    """)

def button_style3(button: QPushButton):
    button.setStyleSheet("""
                        QPushButton {
                            background-color: gold;
                            border: 4px solid black;
                            color: black; /* White text */
                            padding: 5px 5px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 18px;
                            margin: 2px, 2px;
                            transition-duration: 0.4s;
                            cursor: pointer;
                        }
                        QPushButton:hover {
                            background-color: yellow;
                        }
                    """)

def button_style4(button: QPushButton):
    button.setStyleSheet("""
                        QPushButton {
                            background-color: #4CAF50;
                            border: 2px solid black;
                            color: black; 
                            padding: 5px;
                            text-align: center;
                            display: inline-block;
                            font-size: 12px;
                            margin: 2px, 2px;
                            transition-duration: 0.4s;
                            cursor: pointer;
                        }
                        QPushButton:hover {
                            background-color: green;
                        }
                    """)

def text_style1(text: QLabel):
    text.setStyleSheet("""
                        QLabel {
                            color: green;
                            text-align: left;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 35px;
                            margin: 4px 2px;
                            transition-duration: 0.4s;
                            cursor: pointer;
                        }
                    """)

def input_dialog_style1(box: QInputDialog):
    box.setStyleSheet("""
            QDialog {
                background-color: #cccfcd;  
                border: 3px solid black; 
                border-radius: 5px; 
            }
            QLabel {
                background-color: #cccfcd;          
                font-size: 25px;       
            }
            QLineEdit {
                background-color: green;  
                border: 3px solid black;  
                border-radius: 3px;  
                padding: 5px;        
                font-size: 24px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;             
                border: 3px solid green;   
                padding: 10px 20px;        
                border-radius: 3px;         
                font-size: 14px; 
            }
            QPushButton:hover {
                background-color: #45a049;  /* Button background color on hover */
            }
            QPushButton:pressed {
                background-color: #357a38;  /* Button background color on press */
            }
        """)

def list_widget_style(list: QListWidget):
    list.setStyleSheet("""
        QListWidget {
            background-color: #cccfcd;
            border: 4px solid black;  
            padding: 7px;             
            margin: 2px;             
        }
        QListWidget::item:text {
            border: 3px solid black;
            background-color: #4CAF50;
            padding: 7px;
            margin: 2px;
            color: black;
            font-size: 14px;
        }
        QListWidget::item:hover{
        background-color: green;
        }
        QListWidget::item:selected{
        background-color: gold;
        }
    """)

def text_box_style(text_box: QLineEdit):
    text_box.setStyleSheet("""
        QLineEdit {
                background-color: white;  
                border: 4px solid black;  
                border-radius: 5px;  
                padding: 5px;        
                font-size: 40px;
            }
        """)

def check_box(box: QCheckBox):
    box.setStyleSheet("""
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
        }
        QCheckBox::indicator:unchecked {
            background-color: lightgray;
            border: 2px solid gray;
        }
        QCheckBox::indicator:checked {
            background-color: green;
            border: 2px solid darkgreen;
        }
        QCheckBox {
            color: black;
            font-size: 30px;
        }
        """)

def table_style(table: QTableWidget):
    table.setStyleSheet("""
        QTableView {
            border: 2px solid black;
            border-radius: 5px;         
            background-color: rgba(128, 128, 128, 100);  
        }
    
        QTableWidget::item {
            border: 3px solid #BDBDBD;
            border-radius: 4px;
            background-color: #F0F0F0;
            padding: 4px;
            border-style: outset;
            box-shadow: 1px 1px 2px #888888;
        }
        QHeaderView::section { 
            background-color: #4CAF50; 
            color: black;
            font-weight: bold;
        }
        """)

def text_box_style1(text_box: QLineEdit):
    text_box.setStyleSheet("""
        QLineEdit {
                background-color: white;  
                border: 1px solid black;  
                border-radius: 5px;  
                padding: 5px;        
                min-height: 20px;            
                min-width: 30px;            
                font-size: 15px;
            }
        """)

def combobox_style(box: QComboBox):
    box.setStyleSheet("""
        QComboBox {
            background-color: #4CAF50;   
            color: white;
            border: 2px solid #388E3C;  
            padding: 5px;
            border-radius: 5px;
            min-height: 20px;            
            min-width: 30px;            
            font-size: 15px;
        }

        QComboBox:hover {
            background-color: #388E3C;   /* Darker green on hover */
        }

        QComboBox::drop-down {
            background-color: #4CAF50;
            border-left: 2px solid #388E3C; /* Darker green for the drop-down button */
        }

        QComboBox QAbstractItemView {
            background-color: #212121;  /* Dark background for the dropdown list */
            color: white;               /* Text color for the items */
            selection-background-color: gold; /* Gold when selected */
            selection-color: black;      /* Black text when selected */
            border-radius: 5px;
            padding: 5px;
        }

        QComboBox::item {
            padding: 10px;
        }
    """)

def frame_style(frame: QFrame):
    frame.setStyleSheet("""
        QFrame {
        background-color: #F0F0F0;
        border-style: inset;
        box-shadow: 4px 4px 8px #666666;  /* Creates the shadow for a 3D effect */
        }
    
    """)
