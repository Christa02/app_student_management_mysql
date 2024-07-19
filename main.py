from PyQt6.QtWidgets import (QApplication, QLineEdit, QPushButton, QTableWidgetItem, QMainWindow, QTableWidget,
                             QDialog, QVBoxLayout, QComboBox, QMessageBox, QToolBar, QLabel, QGridLayout)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt
import mysql.connector
import sys


class DatabaseConnection:
    def __init__(self, host="localhost", user="root", password="NewPassword", database="school"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def connect(self):
        connection = mysql.connector.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        return connection


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Student Management System")
        self.setGeometry(100, 100, 600, 400)

        # Create actions
        add_student_action = QAction(QIcon("icons/add.png"), '&Add Student', self)
        add_student_action.triggered.connect(self.insert)
        search_action = QAction(QIcon("icons/search.png"), '&Search', self)
        search_action.triggered.connect(self.search)
        about_action = QAction('&About', self)
        about_action.triggered.connect(self.about)

        # Create menubar
        menubar = self.menuBar()
        menubar.setStyleSheet("background-color: lightblue;")
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(add_student_action)
        file_menu.setStyleSheet("background-color: lightgrey;")
        help_menu = menubar.addMenu('&Help')
        help_menu.addAction(about_action)
        help_menu.setStyleSheet("background-color: lightgrey;")
        edit_menu = menubar.addMenu('&Edit')
        edit_menu.addAction(search_action)
        edit_menu.setStyleSheet("background-color: lightgrey;")

        # Create table
        self.table = QTableWidget()
        self.table.setColumnCount(4)  # Set number of columns
        # Create table header
        self.table.setHorizontalHeaderLabels(['Id', 'Name', 'Course', 'Mobile'])  # Set column header labels
        self.table.verticalHeader().setVisible(False)  # Hiding the vertical header
        header = self.table.horizontalHeader()  # Setting header background color
        header.setStyleSheet("background-color: #f0f0f0; color: black; font-weight: bold;")
        # Create table selection
        self.table.setSelectionMode(QTableWidget.SelectionMode.MultiSelection)  # Set multiple selection
        self.table.setStyleSheet("QTableWidget::item:selected { background-color: lightgrey; }")  # Changed the color
        # Create toolbar and add two buttons
        self.toolBar = QToolBar()
        self.toolBar.setFloatable(True)
        self.toolBar.setMovable(True)
        self.addToolBar(self.toolBar)
        self.toolBar.setStyleSheet("background-color: #f0f0f0; color: black; font-weight: bold;")
        self.toolBar.addAction(add_student_action)
        self.toolBar.addAction(search_action)

        # Create statusbar
        self.statusBar = self.statusBar()
        self.statusBar.setStyleSheet("background-color: #f0f0f0; color: black; font-weight: bold;")
        self.table.cellClicked.connect(self.on_cell_clicked)

        self.setCentralWidget(self.table)

    def load_data(self):
        connection = DatabaseConnection().connect()
        self.table.setRowCount(0)
        cursor = connection.cursor()
        cursor.execute("SELECT * from students")
        result = cursor.fetchall()
        result_list = list(result)
        for row_number, row_data in enumerate(result_list):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        connection.close()

    def on_cell_clicked(self):
        selected_items = self.table.selectedItems()
        for item in selected_items:
            button = self.statusBar.findChild(QPushButton)
            if button is None:
                self.edit_button = QPushButton(text="Edit Record", parent=self)
                self.edit_button.setStyleSheet("""QPushButton{border:1px solid #ccc; border-radius: 10px; padding: 8px;
                                                            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);}""")
                self.edit_button.clicked.connect(self.edit)
                self.statusBar.addWidget(self.edit_button)

                self.delete_button = QPushButton(text="Delete Record", parent=self)
                self.delete_button.setStyleSheet("""QPushButton{border:1px solid #ccc; border-radius: 10px; padding: 8px;
                                                            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);}""")
                self.delete_button.clicked.connect(self.delete)
                self.statusBar.addWidget(self.delete_button)

    def insert(self):
        insert = InsertDialog()
        insert.exec()

    def search(self):
        search = SearchDialog()
        search.exec()

    def about(self):
        about = AboutMessageBox()
        about.exec()

    def edit(self):
        edit = EditDialog()
        edit.exec()
            
    def delete(self):
        delete = DeleteDialog()
        delete.exec()


class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: white; color: black;")
        self.setWindowTitle("Insert Student Data")
        self.resize(300, 300)  # Width, Height

        self.name_input = QLineEdit()
        self.name_input.setFixedHeight(30)
        self.name_input.setStyleSheet("""QLineEdit{border:2px solid #ccc; border-radius: 3px;
                                                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); }""")
        self.name_input.setPlaceholderText('Name')

        self.course_input = QComboBox()
        self.course_input.setFixedHeight(30)
        course_options = ["Math", "Physics", "Biology", "Astronomy"]
        self.course_input.addItems(course_options)
        self.course_input.setStyleSheet(
            '''
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                background: white;
                selection-background-color: lightgray;
            }
            '''
        )

        self.mobile_input = QLineEdit()
        self.mobile_input.setFixedHeight(30)
        self.mobile_input.setStyleSheet("""QLineEdit{border:2px solid #ccc; border-radius: 3px;
                                                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); }""")
        self.mobile_input.setPlaceholderText('Mobile')

        self.button = QPushButton(text="Register", parent=self)
        self.button.setStyleSheet("""QPushButton{border:1px solid #ccc; border-radius: 10px; padding: 8px;
                                                    background-color: blue;
                                                    color: white;
                                                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);}""")
        self.button.clicked.connect(self.on_register_button_clicked)

        # Create a vertical layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.course_input)
        layout.addWidget(self.mobile_input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_register_button_clicked(self):
        name = self.name_input.text()
        course = self.course_input.currentText()
        mobile = self.mobile_input.text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students (name, course, mobile) VALUES (%s, %s, %s)", (name, course, mobile))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()


class SearchDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: white; color: black;")
        self.setWindowTitle("Search Student Data")
        self.resize(300, 300)  # Width, Height

        self.name_input = QLineEdit()
        self.name_input.setFixedHeight(30)
        self.name_input.setStyleSheet("""QLineEdit{border:2px solid #ccc; border-radius: 3px;
                                                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); }""")
        self.name_input.setPlaceholderText('Name')
        self.name_input.textChanged.connect(self.on_name_changed)  # Unselect rows of table when name is changed

        self.button = QPushButton(text="Search", parent=self)
        self.button.setStyleSheet("""QPushButton{border:1px solid #ccc; border-radius: 10px; padding: 8px;
                                                    background-color: blue;
                                                    color: white;
                                                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);}""")
        self.button.clicked.connect(self.on_search_button_clicked)

        # Create a vertical layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_search_button_clicked(self):
        name = self.name_input.text()
        items = window.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            window.table.selectRow(item.row())

    def on_name_changed(self):
        window.table.clearSelection()


class AboutMessageBox(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: white; color: black;")
        self.setWindowTitle("About")
        content = """This app was created during the course "The Python Mega Course". 
Feel free to modify and rescue this app."""
        self.setText(content)


class EditDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: white; color: black;")
        self.setWindowTitle("Edit Student Data")
        self.resize(300, 300)  # Width, Height

        current_row = window.table.currentRow()

        # Get ID of row
        self.student_id = window.table.item(current_row, 0)

        # Load student name
        student_name = window.table.item(current_row, 1).text()
        self.name_input = QLineEdit(student_name)
        self.name_input.setFixedHeight(30)
        self.name_input.setStyleSheet("""QLineEdit{border:2px solid #ccc; border-radius: 3px;
                                                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); }""")
        self.name_input.setPlaceholderText('Name')

        # Load course name
        course_name = window.table.item(current_row, 2).text()
        self.course_input = QComboBox()
        self.course_input.setFixedHeight(30)
        course_options = ["Math", "Physics", "Biology", "Astronomy"]
        self.course_input.addItems(course_options)
        self.course_input.setCurrentText(course_name)
        self.course_input.setStyleSheet(
            '''
            QComboBox {
                border: 2px solid #ccc;
                border-radius: 3px;
                padding: 1px 18px 1px 3px;
                background: white;
                selection-background-color: lightgray;
            }
            '''
        )

        # Load mobile number
        mobile = window.table.item(current_row, 3).text()
        self.mobile_input = QLineEdit(mobile)
        self.mobile_input.setFixedHeight(30)
        self.mobile_input.setStyleSheet("""QLineEdit{border:2px solid #ccc; border-radius: 3px;
                                                        box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2); }""")
        self.mobile_input.setPlaceholderText('Mobile')

        self.button = QPushButton(text="Update", parent=self)
        self.button.setStyleSheet("""QPushButton{border:1px solid #ccc; border-radius: 10px; padding: 8px;
                                                    background-color: blue;
                                                    color: white;
                                                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);}""")
        self.button.clicked.connect(self.on_button_update_clicked)

        # Create a vertical layout for the dialog
        layout = QVBoxLayout()
        layout.addWidget(self.name_input)
        layout.addWidget(self.course_input)
        layout.addWidget(self.mobile_input)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def on_button_update_clicked(self):
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = %s, course = %s, mobile = %s WHERE id = %s;",
                       (self.name_input.text(),
                        self.course_input.currentText(),
                        self.mobile_input.text(),
                        self.student_id.text()))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()


class DeleteDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("background-color: white; color: black;")
        self.setWindowTitle("Delete Student Data")

        confirmation_label = QLabel("Are you sure you want to delete ?")

        self.yes_button = QPushButton(text="Yes", parent=self)
        self.yes_button.setStyleSheet("""QPushButton{border:1px solid #ccc; border-radius: 10px; padding: 8px;
                                                    background-color: blue;
                                                    color: white;
                                                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);}""")
        self.yes_button.clicked.connect(self.on_yes_button_clicked)

        self.no_button = QPushButton(text="No", parent=self)
        self.no_button.setStyleSheet("""QPushButton{border:1px solid #ccc; border-radius: 10px; padding: 8px;
                                                    background-color: white;
                                                    color: black;
                                                    box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);}""")
        self.no_button.clicked.connect(self.on_no_button_clicked)

        # Create a vertical layout for the dialog
        layout = QGridLayout()
        layout.addWidget(confirmation_label, 0, 0, 1, 2)
        layout.addWidget(self.yes_button, 1, 0)
        layout.addWidget(self.no_button, 1, 1)

        self.setLayout(layout)

    def on_yes_button_clicked(self):
        current_row = window.table.currentRow()
        print("current_row", current_row)
        # Get ID of row
        student_id = window.table.item(current_row, 0).text()
        connection = DatabaseConnection().connect()
        cursor = connection.cursor()
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        connection.commit()
        cursor.close()
        connection.close()
        window.load_data()
        success_message = QMessageBox.information(self, 'Success', 'The record was deleted successfully!')
        success_message.setIcon(QMessageBox.Icon.Information)
        self.close()

    def on_no_button_clicked(self):
        self.close()


app = QApplication(sys.argv)
window = MainWindow()
window.setStyleSheet("background-color: white; color: black;")
window.show()
window.load_data()
app.exec()
