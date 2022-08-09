import sqlite3
from time import sleep
from texttable import Texttable
import datetime
import sys
import os
import readline


class fnote:
    """
    Simple Post-It Note taking app.
    First build with a simple terminal user interface
    """

    def __init__(self):

        self.logo = "logo.txt"
        self.hyphen = "-" * 50
        self.menu = {
            "a": self.add_note,
            "d": self.delete_note,
            "e": self.edit_note,
            "s": self.search_for_tag,
            "q": self.stop_program,
        }
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
        note or edit a note.
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

    def multi_input(self, txt=""):
        """Simple user input with multiple lines to create and edit
        note, title, tag
        """

        try:
            # Hold all user inputs
            words = []
            # Append the given string
            if len(txt) != 0:
                words.append(txt)
            finalstr = ""

            # Initialize the loop
            while True:
                word = input()
                if not word:
                    break
                else:
                    words.append(word)
        except KeyboardInterrupt:
            return
        finally:
            if len(words) != 0:
                final_str = "\n".join(words)
                return final_str
            else:
                quit

    def add_note(self):
        """Add a new note. Enter title, note, tag."""

        # Initialize the window
        self.clear_menu()

        # Add title
        print("Enter title (press <<Enter>>  when finished)")
        print(self.hyphen)
        title = input()

        # Add note
        print()
        sleep(0.50)
        print("Enter note (press <<Enter>> when line is empty)")
        print(self.hyphen)
        note = self.multi_input()

        # Add tag
        print()
        sleep(0.50)
        print("Enter comma-separated tag (press <<Enter>> when finished)")
        print(self.hyphen)
        tag = input()

        # Safe note?
        print()
        sleep(0.50)
        print("Do you want to save the note? (y/n): ")
        answer = input().lower().strip()
        date = self.get_date()
        id_ = self.generate_id()

        if answer == "y":
            self.insertVariableIntoTable(id_, title, date, tag, note)

    def search_for_tag(self):
        """Search table for one tag."""

        print(self.hyphen)
        print("Enter one search tag (press <<Enter>> when finished)")
        tag = input().lower().strip()
        draw_list = self.search_tag_table(tag)

        # Check if draw_list is empty
        if len(draw_list) != 0:
            self.clear_menu()
            print(self.hyphen)
            print("Overview: ")
            print(self.hyphen)
            print(f"search tag: {tag}")
            sleep(0.50)
            print()
            print()
            self.draw_table(draw_list)
            print()
            print()
            sleep(0.50)
            print("Press <<Enter>> to get to the homescreen.")
            input()
        else:
            print(self.hyphen)
            print("Tag does not exist.")
            sleep(1.50)

    def search_tag_table(self, search_tag):
        """Search the table for a given tag"""

        try:
            draw_list = []
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            for row in cursor.execute("SELECT * FROM overview;"):
                id_, title, date, tag, note = row
                tmp_list = []
                tmp_tag = tag.split(",")
                for item in tmp_tag:
                    item = item.lower().strip()
                    tmp_list.append(item)
                if search_tag in tmp_list:
                    draw_list.append([id_, title, date, tag, note])
            connection.commit()
            cursor.close()
            return draw_list
        except sqlite3.Error as e:
            print(e)
            sleep(4.0)
        finally:
            if connection:
                cursor.close()

    def delete_note(self):
        """Delete saved note."""

        # Check if id is in database
        note_id = self.edit_get_note_id()
        if self.check_id_in_database(note_id):
            print(self.hyphen)
            print("Do you want to delete this note? (y/n)")
            answer = input().lower().strip()
            if answer == "y":
                self.delete_note_database(note_id)
        else:
            print(self.hyphen)
            print("Note does not exist.")
            sleep(1.50)

    def draw_table(self, L=[]):
        """Draw table with module Texttable"""

        table = Texttable()
        table.set_cols_align(["c", "c", "c", "c", "c"])
        table.set_cols_valign(["t", "t", "t", "t", "t"])
        table.header(["Id", "Title", "Date", "Tag", "Note"])
        for row in L:
            table.add_row(row)
        print(table.draw())

    def delete_note_database(self, table_id):
        """Delete note with given id from the table overview"""

        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            insert_state = "DELETE FROM overview WHERE Id = ?;"
            cursor.execute(insert_state, [table_id])
            connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print("Could not delete note from table.", e)
            sleep(4.0)
        finally:
            if connection:
                cursor.close()

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
            sleep(4.0)
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
            sleep(4.0)
        finally:
            if connection:
                connection.close()

    def display_notes(self):
        """Display all note in from the table note"""

        self.create_table()
        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            L = []
            for row in cursor.execute("SELECT * FROM overview"):
                id_, title, date, tag, note = row
                L.append([id_, title, date, tag, note])

            # Draw Table
            print("Overview: ")
            self.draw_table(L)

        except sqlite3.Error as e:
            print("Failed to display the table.", e)
            sleep(4.0)
        finally:
            if connection:
                connection.close()

    def edit_note(self):
        """Edit a saved note. Edit title, note and tag."""

        # Ćheck if id is in database
        note_id = self.edit_get_note_id()
        if self.check_id_in_database(note_id):
            # Get the current title, note and tag
            title = self.get_title_database(note_id)
            note = self.get_note_database(note_id)
            tag = self.get_tag_database(note_id)

            # Initialize terminal window
            self.clear_menu()

            # Edit Title
            print("Edit title (press <<Enter>> when finished)")
            print(self.hyphen)
            new_title = self.rlinput(title)

            # Edit Note
            print()
            sleep(0.50)
            print("Edit note (press <<Enter>> when line is empty)")
            print(self.hyphen)
            tmp_note = self.rlinput(note)
            new_note = self.multi_input(tmp_note)

            # Edit Tag
            print()
            sleep(0.50)
            print("Edit tag (press <<Enter>> when finished)")
            print(self.hyphen)
            new_tag = self.rlinput(tag)

            # Save changes?
            print()
            sleep(0.50)
            print("Do you want to save your changes? (y/n): ")
            answer = input().lower().strip()

            # Update the databse
            if answer == "y":
                self.update_database(new_title, new_note, new_tag, note_id)
        else:
            print()
            print("Note does not exist.")
            sleep(1.50)

    def check_id_in_database(self, table_id):
        """Return True if the given id is in database.
        Return False if given id is not in database.
        """

        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            for row in cursor.execute("SELECT * FROM overview"):
                id_, title, date, tag, note = row
                if id_ == table_id:
                    return True
            connection.commit()
            cursor.close()
            return False
        except sqlite3.Error as e:
            print("Error in method: check_id_in_database.", e)
        finally:
            if connection:
                connection.close()

    def update_database(self, new_title, new_note, new_tag, id_):
        """Update the database overview. Update Title, Tag and Note."""

        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            insert_stat = """UPDATE overview 
                        SET Title = ?, Note = ?, Tag = ? 
                        WHERE Id = ?;"""
            values = (new_title, new_note, new_tag, id_)
            cursor.execute(insert_stat, values)
            connection.commit()
            cursor.close()
        except sqlite3.Error as e:
            print("Could not update the database.", e)
        finally:
            if connection:
                connection.close()

    def rlinput(self, prefill=""):
        """Display the "old note" and edit it."""

        readline.set_startup_hook(lambda: readline.insert_text(prefill))
        try:
            return input()
        finally:
            readline.set_startup_hook()

    def get_title_database(self, table_id):
        """Get the current title from the database overview."""

        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            for row in cursor.execute("SELECT * FROM overview"):
                id_, title, date, tag, note = row
                if id_ == table_id:
                    tmp_title = title
            connection.commit()
            cursor.close()
            return tmp_title
        except sqlite3.Error as e:
            print("Could not return title", e)
            sleep(4.0)
        finally:
            if connection:
                connection.close()

    def get_note_database(self, table_id):
        """Get the current title from the database overview."""

        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            for row in cursor.execute("SELECT * FROM overview"):
                id_, title, date, tag, note = row
                if id_ == table_id:
                    tmp_note = note
            connection.commit()
            cursor.close()
            return tmp_note
        except sqlite3.Error as e:
            print("Could not return note", e)
            sleep(4.0)
        finally:
            if connection:
                connection.close()

    def get_tag_database(self, table_id):
        """Get the current title from the database overview."""

        try:
            connection = sqlite3.connect("note.db")
            cursor = connection.cursor()
            for row in cursor.execute("SELECT * FROM overview"):
                id_, title, date, tag, note = row
                if id_ == table_id:
                    tmp_tag = tag
            connection.commit()
            cursor.close()
            return tmp_tag
        except sqlite3.Error as e:
            print("Could not return tag", e)
            sleep(4.0)
        finally:
            if connection:
                connection.close()

    def edit_get_note_id(self):
        """Get the note id one wants to edit"""
        print(self.hyphen)
        note_id = input("Type the id of the note: ").lower().strip()
        # note_id = input()

        return note_id


# Main Program
fnote()
