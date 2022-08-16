import sqlite3


def create_database():
    """Creates a database for testing the class fnote"""

    try:
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()

        # Create Table overview
        cmd = "CREATE TABLE overview (id text, title text, date text, tag text, note text);"
        cursor.execute(cmd)

        # Insert test data1
        cmd = """INSERT INTO overview (id, title, date, tag, note) 
            VALUES ('1', 'title_test01', 'date_test01', 'tag_test01', 'note_test01');
            """
        cursor.execute(cmd)

        # Insert test data2
        cmd = """INSERT INTO overview (id, title, date, tag, note) 
            VALUES ('2', 'title_test002', 'date_test02', 'tag_test02', 'note_test02');
            """
        cursor.execute(cmd)

        # Insert test data3
        cmd = """INSERT INTO overview (id, title, date, tag, note) 
            VALUES ('3', 'title_test03', 'date_test03', 'tag_test03', 'note_test03');
            """
        cursor.execute(cmd)
        connection.commit()
        cursor.close()

    except sqlite3.Error as e:
        print("Failed in methof create_databse.", e)

    finally:
        if connection:
            connection.close()


def display_table():
    """Display the table"""

    try:
        connection = sqlite3.connect("test.db")
        cursor = connection.cursor()
        cmd = "SELECT * FROM overview;"
        for row in cursor.execute(cmd):
            print(row)
    except sqlite3.Error as e:
        print("Cannot display table rows.", e)
    finally:
        if connection:
            connection.close()


# Main program
