import sqlite3
from time import sleep
from texttable import Texttable
import datetime
import sys
import os


class fnote:
    """
    Simple Post-It Note taking app.
    First build with a simple terminal user interface
    """

    def __init__(self):

        self.logo = "logo.txt"
        self.hyphen = "-" * 40
        self.menu = {"a": self.add_note, "q": self.stop_program}
        self.finished = True

        # Start the program 
        self.start()

    def start(self):
        """Run the program"""

        while self.finished:

            # Clear the terminal cluster
            self.clear_menu()

            # Display the logo
            self.display_ascii(self.logo)

            # Display all current notes
            self.display_notes()
            print()
            sleep(0.50)

            # Display the menu loop
            self.menu_loop()

    def display_ascii(self, path):
        """Display a ascii file"""

        with open(path, "r") as f:
            for line in f:
                print(line.rstrip())
                sleep(0.20)

        print()
        print()

    def menu_loop(self):
        """Display the action menu. Add a new note,
        sort the notes by title, date, tags. Delete a
        note or edit a note
        """

        print()
        print("Menu: ")
        for key, value in self.menu.items():
            print(f"{key}) {value.__doc__}")
        print(self.hyphen)
        choice = input("Action: ")
        for key, value in self.menu.items():
            if choice == key:
                value()

    def stop_program(self):
        """Quit the program."""

        self.finished = False

    def clear_menu(self):
        """Remove the clutter from the terminal window"""

        print()
        os.system("cls" if os.name == "nt" else "clear")

    def add_note(self):
        """Add a new note. Enter Title, Note, Tag."""

        self.clear_menu()
        print("Enter title (press ctrl+D when finished)")
        print(self.hyphen)
        title = sys.stdin.read().strip()
        print()
        sleep(0.50)
        print("Enter note (press ctrl+D when finished)")
        print(self.hyphen)
        note = sys.stdin.read().strip()
        print()
        sleep(0.50)
        print("Enter tag (press crtl+D when finished)")
        print(self.hyphen)
        tag = sys.stdin.read().strip()
        date = self.get_date()
        id_ = self.generate_id()

        self.insertVariableIntoTable(id_, title, date, tag, note)

    def generate_id(self):
        """Generate an id for the table.
        Integer value which starts at 1
        """

        last_id = self.get_last_id()
        re = last_id[0]
        last_id = int(re)
        return last_id + 1

    def get_last_id(self):
        """Get the latest id from the database note"""

        try:
            last_row = ("0",)
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            for row in cursor.execute("SELECT Id FROM overview"):
                last_row = row
            connection.commit()
            cursor.close()
            return last_row

        except sqlite3.Error as e:
            print("Failed the get the last id from table note", e)
        finally:
            if connection:
                connection.close()

    def get_date(self):
        """Get the current date"""

        date = datetime.datetime.now()
        return date.strftime("%x")

    def create_table(self):
        """Create a table with the following columns
        (Title, Date, Tag, Note)
        """

        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            cursor.execute(
                """CREATE TABLE overview (
                    Id text,
                    Title text,
                    Date text,
                    Tag text,
                    Note text
                    )"""
            )
            connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            # print('Table already exists.', e)
            print()
        finally:
            if connection:
                connection.close()

    def insertVariableIntoTable(self, id_, title, date, tag, note):
        """Insert a new note with the following rows
        (id, title, date, tag, note) into the Database
        """

        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            insert_with_param = """INSERT INTO overview
                                (id, title, date, tag, note) 
                                VALUES (?, ?, ?, ?, ?);"""
            data_tuple = (id_, title, date, tag, note)
            cursor.execute(insert_with_param, data_tuple)
            connection.commit()
            cursor.close()

        except sqlite3.Error as e:
            print("Failed to insert Python variable into table", e)
        finally:
            if connection:
                connection.close()

    def display_notes(self):
        """Display all note in from the table note"""

        self.create_table()

        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()

            table = Texttable()
            table.set_cols_align(["c", "c", "c", "c", "c"])
            table.set_cols_valign(["t", "t", "t", "t", "t"])
            table.header(["Id", "Title", "Date", "Tag", "Note"])

            for row in cursor.execute("SELECT * FROM overview"):
                id_, title, date, tag, note = row
                table.add_row([id_, title, date, tag, note])

            print("Overview: ")
            print(table.draw())

        except sqlite3.Error as e:
            print("Failed to display the table.", e)
        finally:
            if connection:
                connection.close()


# Main Program
fnote()
