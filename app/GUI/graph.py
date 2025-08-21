from datetime import datetime, date
import json
import matplotlib.dates as mdates
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class GraphScreen(QWidget):
    BackToHome = pyqtSignal()

    def __init__(self, screen_manager, user_id):
        super().__init__()
        self.screen_manager = screen_manager
        self.user_id = user_id

        layout = QVBoxLayout(self)

        # Matplotlib Figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

    def update_graph(self):
        # Fetch JSON data from DB
        json_data = self.fetch_json_from_db()
        if not json_data:
            QMessageBox.information(self, "No Data", "No spending data found for this user.")
            return

        # Parse JSON into dates and amounts
        dates, amounts = self.parse_spending(json_data)

        # Clear previous plot
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        # Plot spending trend
        ax.plot(dates, amounts, marker='o', linestyle='-', color='blue')
        ax.set_title("Spending Trend")
        ax.set_xlabel("Date")
        ax.set_ylabel("Amount Spent")
        ax.grid(True)

        # Format x-axis for dates
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        self.figure.autofmt_xdate()  # rotates date labels nicely

        self.canvas.draw()

    def fetch_json_from_db(self):
        query = QSqlQuery(self.screen_manager.db.db)  # pass the actual QSqlDatabase
        query.prepare("SELECT json_expenses FROM answers WHERE name = :user_id")
        query.bindValue(":user_id", self.user_id)
        if not query.exec_():
            print("Query failed:", query.lastError().text())
            return None

        if query.next():
            json_text = query.value(0)
            if json_text:
                import json
                return json.loads(json_text)
        return None

    @staticmethod
    def parse_spending(data):
        daily_totals = {}

        for year, months in data.items():
            for month, days in months.items():
                for day, entries in days.items():
                    total = 0
                    # entries = [Category, Amount, Note, Category, Amount, Note, ...]
                    for i in range(1, len(entries), 3):
                        try:
                            total += float(entries[i])
                        except (ValueError, IndexError):
                            continue

                    # Use datetime.date to avoid time duplicates
                    date_obj = date(int(year), int(month), int(day))
                    daily_totals[date_obj] = total

        # Sort by date
        sorted_dates = sorted(daily_totals.keys())
        amounts = [daily_totals[d] for d in sorted_dates]

        return sorted_dates, amounts