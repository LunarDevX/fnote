import unittest
from unittest import TestCase
import sqlite3
from fnote04 import fnote


class Testfnote(unittest.TestCase):
    """Class to test fnote application"""

    def setUp(self):
        """Set up the connection to a Sqlite database
        in the memory
        """
        # Initalize the class fnote
        self.n = fnote()

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

    def tearDown(self):
        """Tear down the database"""

        self.connection.close()


# Main Program
if __name__ == "__main__":
    unittest.main()
