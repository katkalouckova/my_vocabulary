import mysql.connector


class Database:
    """
    A class for storage and manipulation of czech-english dictionary.
    Instance attributes:
        *
    """

    def __init__(self):
        self.my_db = mysql.connector.connect(
            host='localhost',
            user='mv_app',
            passwd='1234567890.',
            database='my_vocabulary',
            autocommit=True
            )

    def get_cursor(self):
        """
        Returns object of class MySQLCursor. This object enables working
        with database.
        :return: MySQLCursor
        """

        return self.my_db.cursor()

    def get_cursor_tuples(self):
        """
        Returns object of class MySQLCursor. This object enables working
        with database (returns rows as named tuples).
        :return:
        """

        return self.my_db.cursor(named_tuple=True)
