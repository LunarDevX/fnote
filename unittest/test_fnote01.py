import unittest
from unittest import TestCase
import sqlite3
from fnote06 import fnote
import os
from create_database import *


class Testfnote(unittest.TestCase):
    """Class to test fnote application"""

    def setUp(self):
        """Set up the connection to a Sqlite database
        in the memory
        """
        # Initalize the class fnote
        self.n = fnote()

        # Create temporary test.db
        create_database()

        # Initialize table name
        self.table_name = "test.db"

        # Connect to a temporary database
        self.connection = sqlite3.connect(self.table_name)
        self.cursor = self.connection.cursor()

        self.connection.commit()

    def test_get_title_database(self):
        """Test whether the title is correct with a given id."""

        title = self.n.get_title_database(self.table_name, "1")
        self.assertEqual("title_test01", title)

    def test_get_note_database(self):
        """Test whether the note is correct with a given id."""

        note = self.n.get_note_database(self.table_name, "1")
        self.assertEqual("note_test01", note)

    def test_get_tag_database(self):
        """Test whether the tag os correct with a given id."""

        tag = self.n.get_tag_database(self.table_name, "1")
        self.assertEqual("tag_test01", tag)

    def test_insertVariableIntoTable(self):
        """Test whether a new note is added succesfully"""

        test_add = ("4", "add_title", "add_date", "add_tag", "add_note")
        test_insert = self.n.insertVariableIntoTable(
            self.table_name, "4", "add_title", "add_date", "add_tag", "add_note"
        )

        for row in self.cursor.execute("SELECT * FROM overview"):
            last_row = row
        self.connection.commit()

        self.assertEqual(test_add, last_row)

    def test_update_database(self):
        """Test whethter the database is updated correctly"""

        # Update note with id 3
        update_note = ("3", "update_title", "date_test03", "update_tag", "update_note")

        count = 0
        for row in self.cursor.execute("SELECT * FROM overview"):
            id_, title, date, tag, note = row
            if id_ == "3":
                old_row = row
        self.connection.commit()

        self.n.update_database(
            self.table_name, "update_title", "update_note", "update_tag", "3"
        )

        self.assertNotEqual(update_note, old_row)

    def test_check_id_in_database(self):
        """Test whether the function returns True correctly"""

        self.assertTrue(self.n.check_id_in_database(self.table_name, "1"))
        self.assertFalse(self.n.check_id_in_database(self.table_name, "5"))

    def test_get_last_id(self):
        """Test whether the last id from the table is returned correctly"""

        self.assertEqual(self.n.get_last_id(self.table_name), ("3",))

    def test_generate_id(self):
        """Test whether the id is correct"""

        self.assertEqual(self.n.generate_id(("3",)), 4)

    def test_delete_note_database(self):
        """Test whether a note is deleted"""

        for row in self.cursor.execute("SELECT * FROM overview"):
            old_last_row = row
        self.connection.commit()

        # Delete note with id 3
        self.n.delete_note_database(self.table_name, "3")

        for row in self.cursor.execute("SELECT * FROM overview"):
            new_last_row = row
        self.connection.commit()

        self.assertNotEqual(old_last_row, new_last_row)

    def test_search_tag_table(self):
        """Test whethter the right tag will be returned"""

        # Create list based on the table overview
        check_list = []
        for row in self.cursor.execute("SELECT * FROM overview"):
            id_, title, date, tag, note = row
            check_list.append([id_, title, date, tag, note])

        # First search tag
        search_tag01 = "test"
        result01 = self.n.search_tag_table(self.table_name, search_tag01)

        # Second search tag
        search_tag02 = "Clouds"
        result02 = self.n.search_tag_table(self.table_name, search_tag02)

        self.assertEqual(result01, check_list)
        self.assertEqual(result02, [])

    def tearDown(self):
        """Tear down the database"""

        self.connection.close()

        # Delete test.db
        os.remove("test.db")


# Main Program
if __name__ == "__main__":
    unittest.main()
