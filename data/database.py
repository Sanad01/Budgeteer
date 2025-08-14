from datetime import datetime, timedelta
import sys

from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox
import json

class DatabaseManager:

    def __init__(self, screen_manager):
        self.create_connection()
        self.create_answers_table()
        self.create_expense_table()
        self.create_totals_table()
        self.create_dates_table()
        self.screen_manager = screen_manager
        # self.print_table_schema()
        self.plan_dict = {}
        self.fetch_plan()
        self.reset()
        print(self.plan_dict)

    def create_connection(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName("C:/Users/sanad/Documents/GitHub/financial-planner/general_info.db")
        if not self.db.open():
            QMessageBox.Critical(None, "Error", "Could not open your db")
            sys.exit(1)
        else:
            print("Database connected successfully.")

    def create_answers_table(self):
        query = QSqlQuery()

        # query.exec_("DROP TABLE IF EXISTS answers")

        query.exec_('''CREATE TABLE IF NOT EXISTS answers
                               (name TEXT NULL PRIMARY KEY, income REAL, pay_type TEXT NULL, rent REAL, utilities REAL,
                                bills REAL, transportation REAL, loans REAL,
                                budget REAL, json_expenses TEXT)''')

    '''
    @staticmethod
    def print_table_schema():
        query = QSqlQuery()
        query.exec_("PRAGMA table_info(answers);")
        while query.next():
            column_id = query.value(0)
            column_name = query.value(1)
            column_type = query.value(2)
            is_not_null = query.value(3)
            default_value = query.value(4)
            is_primary_key = query.value(5)
            print(f"Column ID: {column_id}, Name: {column_name}, Type: {column_type}, "
                  f"Not Null: {is_not_null}, Default: {default_value}, Primary Key: {is_primary_key}")
                  '''

    def create_expense_table(self):
        query = QSqlQuery()

        # query.exec_("DROP TABLE IF EXISTS expenses")

        query.exec_('''CREATE TABLE IF NOT EXISTS expenses
                                       (name TEXT NULL PRIMARY KEY, category TEXT NULL, amount REAL)''')

    def create_totals_table(self):
        query = QSqlQuery()

        # query.exec_("DROP TABLE IF EXISTS totals")

        query.exec_('''
        CREATE TABLE IF NOT EXISTS totals (
            name TEXT PRIMARY KEY,
            total REAL DEFAULT 0,
            monthly REAL DEFAULT 0,
            yearly REAL DEFAULT 0,
            daily_avg REAL DEFAULT 0,
            monthly_avg REAL DEFAULT 0,
            yearly_avg REAL DEFAULT 0
        )
    ''')

    def create_dates_table(self):
        query = QSqlQuery()

        # query.exec_("DROP TABLE IF EXISTS paycheck_dates")

        query.exec_('''
        CREATE TABLE IF NOT EXISTS paycheck_dates (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES answers(name)
        )
    ''')

    def get_percentages(self, plan_name):
        query = QSqlQuery()
        query.prepare('''SELECT income, rent, utilities, bills, transportation, loans, budget 
                             FROM answers WHERE name = :name ORDER BY rowid DESC''')

        # Bind the parameter value
        query.bindValue(':name', plan_name)

        # Execute the query
        if query.exec_():
            if query.next():
                print("Data retrieved successfully")
                income = query.value(0)

                if income is not None:
                    print(f"this the income: {income}, rent: {query.value(1)}, util: {query.value(2)}"
                          f"bills {query.value(3)}, transportation: {query.value(4)}, loans: {query.value(5)}"
                          f"budget: {query.value(6)}")
                    print(query.value(1))
                    return {
                        "income": income,
                        "rent": query.value(1),
                        "utilities": query.value(2),
                        "bills": query.value(3),
                        "transportation": query.value(4),
                        "loans": query.value(5),
                        "budget": query.value(6)
                    }

                else:
                    print("Income is None or zero, cannot calculate percentages")
            else:
                print("No data found")
        return {}

    def insert_plan_name(self, name):
        query = QSqlQuery()

        try:
            self.db.transaction()

            query.prepare('''INSERT INTO answers (name)
                             VALUES (?)''')
            query.addBindValue(name)
            if not query.exec_():
                raise Exception("Insert into table1 failed")

            query.prepare('''INSERT INTO expenses (name)
                             VALUES (?)''')
            query.addBindValue(name)
            if not query.exec_():
                raise Exception("Insert into table2 failed")

            query.prepare('''INSERT INTO totals
                (name) VALUES (?)''')
            query.addBindValue(name)
            if not query.exec_():
                raise Exception("Insert into table3 failed")

            query.prepare('''INSERT INTO paycheck_dates (user_id)
                                                     VALUES (?)''')
            query.addBindValue(name)
            if not query.exec_():
                raise Exception("Insert into dates failed")

            if not self.db.commit():
                raise Exception("Commit failed")

            print("Data inserted successfully")

        except Exception as e:
            self.db.rollback()
            print(f"An error occurred: {e}")


    # for loading a plan
    def fetch_plan(self):
        query = QSqlQuery()
        names = []
        if query.exec_("SELECT name, income FROM answers ORDER BY rowid DESC"):
            while query.next():
                name = query.value(0)
                income = query.value(1)
                self.plan_dict[name] = income
                names.append(name)

        else:
            print("failed to fetch name")
            # return a list of plan names and a dict that contains names and income values
        return names, self.plan_dict

    def close_connection(self):
        if self.db.isOpen():
            self.db.close()
            QSqlDatabase.removeDatabase(QSqlDatabase.defaultConnection)
            print("Database connection closed.")

    def insert_money_spent(self, plan_name, category, amount):
        query = QSqlQuery()

        try:
            self.db.transaction()

            query.prepare("UPDATE expenses SET category = ?, amount = ? WHERE name = :name")

            query.addBindValue(category)
            query.addBindValue(amount)
            query.bindValue(':name', plan_name)

            if not query.exec_():
                raise Exception("Insert into table2 failed")

            if not self.db.commit():
                raise Exception("Commit failed")

            print("Data inserted successfully")

        except Exception as e:
            self.db.rollback()
            print(f"An error occurred: {e}")


    def calc_total(self, amount, plan_name):
        query = QSqlQuery()
        query.prepare("UPDATE totals SET total = total + :amount WHERE name = :name")
        query.bindValue(":amount", amount)
        query.bindValue(":name", plan_name)

        if not query.exec_():
            print("Error updating total:", query.lastError().text())
            return

        query.prepare("UPDATE totals SET monthly = monthly + :amount WHERE name = :name")
        query.bindValue(":amount", amount)
        query.bindValue(":name", plan_name)

        if not query.exec_():
            print("Error updating total:", query.lastError().text())
            return

        query.prepare("UPDATE totals SET yearly = yearly + :amount WHERE name = :name")
        query.bindValue(":amount", amount)
        query.bindValue(":name", plan_name)

        if not query.exec_():
            print("Error updating total:", query.lastError().text())
            return

    def get_total(self, plan_name):
        query = QSqlQuery()
        query.prepare("SELECT total FROM totals WHERE name = :name")
        query.bindValue(':name', plan_name)

        if not query.exec_():
            print("Error retrieving total:", query.lastError().text())
            return None

        if query.next():
            return query.value(0)  # Index 0 = first column ("total")

        return None

    def get_monthly_total(self, plan_name):
        query = QSqlQuery()
        query.prepare("SELECT monthly FROM totals WHERE name = :name")
        query.bindValue(':name', plan_name)

        if not query.exec_():
            print("Error retrieving total:", query.lastError().text())
            return None

        if query.next():
            return query.value(0)  # Index 0 = first column ("total")

        return None

    def generate_paycheck_dates(self, last_date_str, interval_type):
        last_date = datetime.strptime(last_date_str, '%Y-%m-%d')
        delta = timedelta(days=7) if interval_type == "Weekly" else timedelta(days=14)

        end_of_month = last_date.replace(day=28) + timedelta(days=4)
        end_of_month = end_of_month.replace(day=1) - timedelta(days=1)

        new_dates = []
        next_date = last_date + delta

        while next_date <= end_of_month:
            new_dates.append(next_date.strftime('%Y-%m-%d'))
            next_date += delta

        return new_dates

    def insert_generated_dates(self, user_id, date_list):
        query = QSqlQuery()
        query.exec_("PRAGMA foreign_keys = ON")

        for date_str in date_list:
            query.prepare('''
                INSERT INTO paycheck_dates (user_id, date)
                VALUES (:user_id, :date)
            ''')
            query.bindValue(':user_id', user_id)
            query.bindValue(':date', date_str)

            if not query.exec_():
                print("Error inserting", date_str, ":", query.lastError().text())

    def get_pay_dates(self, user_id):
        now = datetime.now()
        year = now.year
        month = now.month
        query = QSqlQuery()
        query.exec_("PRAGMA foreign_keys = ON")

        year_month = f"{year}-{month:02d}"

        query.prepare('''
                SELECT date FROM paycheck_dates
                WHERE user_id = :user_id
                AND date LIKE :year_month || '%'
            ''')
        query.bindValue(':user_id', user_id)
        query.bindValue(':year_month', year_month)

        if not query.exec_():
            print("Query failed:", query.lastError().text())
            return []

        dates = []
        while query.next():
            date_str = query.value(0)  # get the 'date' column
            dates.append(date_str)

        return dates

    def reset(self):
        today = datetime.today()

        if today.day == 1:
            self.zero_month(self.screen_manager.name)
            # generate new dates at the beginning of each month
            new_dates = self.get_pay_dates(self.screen_manager.name)
            self.insert_generated_dates(self.screen_manager.name, new_dates)

        if today.month == 1 and today.day == 1:
            self.zero_year(self.screen_manager.name)

    def zero_month(self, name):
        query = QSqlQuery()

        query.prepare("UPDATE totals SET monthly = 0 WHERE name = :name")
        query.bindValue(":name", name)

        if not query.exec_():
            print("Error zeroing month:", query.lastError().text())
            return

    def zero_year(self, name):
        query = QSqlQuery()

        query.prepare("UPDATE totals SET yearly = 0 WHERE name = :name")
        query.bindValue(":name", name)

        if not query.exec_():
            print("Error zeroing year:", query.lastError().text())
            return

    def calc_avg_spending(self, name):
        today = datetime.today()

        # get how many months user has used app from paycheck_dates table
        query0 = QSqlQuery()
        query0.prepare("""
            SELECT COUNT(DISTINCT strftime('%m', date))
            FROM paycheck_dates
            WHERE user_id = :name
        """)
        query0.bindValue(":user_id", name)

        if not query0.exec_():
            print("Error counting months:", query0.lastError().text())
            return

        if query0.next():
            months_count = query0.value(0) or 1
        else:
            months_count = 1

        # --- Get monthly spending ---
        query1 = QSqlQuery()
        query1.prepare("SELECT monthly FROM totals WHERE name = :name")
        query1.bindValue(":name", name)

        if not query1.exec_() or not query1.next():
            print("Error getting monthly spending:", query1.lastError().text())
            return

        monthly_spending = query1.value(0) or 0.0
        daily_average = round((monthly_spending / today.day), 2)

        # --- Get yearly spending ---
        query2 = QSqlQuery()
        query2.prepare("SELECT yearly FROM totals WHERE name = :name")
        query2.bindValue(":name", name)

        if not query2.exec_() or not query2.next():
            print("Error getting yearly spending:", query2.lastError().text())
            return

        yearly_spending = query2.value(0) or 0.0
        monthly_average = round((yearly_spending / months_count), 2)

        # --- Update ---
        query3 = QSqlQuery()
        query3.prepare("""
                UPDATE totals
                SET daily_avg = ?, monthly_avg = ?
                WHERE name = ?
            """)
        query3.addBindValue(daily_average)
        query3.addBindValue(monthly_average)
        query3.addBindValue(name)

        if not query3.exec_():
            print("Error updating averages:", query3.lastError().text())

    def get_averages(self, name):
        query = QSqlQuery()

        query.prepare("""
            SELECT daily_avg, monthly_avg
            FROM totals
            WHERE name = :name
        """)
        query.bindValue(":name", name)

        if not query.exec_():
            print("Error getting averages:", query.lastError().text())
            return None, None

        if query.next():  # Move to the first row
            daily_avg = query.value(0) or 0.0
            monthly_avg = query.value(1) or 0.0
            return daily_avg, monthly_avg
        else:
            return 0.0, 0.0