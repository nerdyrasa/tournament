#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


class DB:

    def __init__(self, db_conn_str="dbname=tournament"):
        """
        Creates a database connection
        with the connection string provided
        :param str db_conn_str: Contains the database connection string with a
        default value when no argument is passed
        """
        self.conn = psycopg2.connect(db_conn_str)

    def cursor(self):
        """
        Returns the current cursor of the database
        """
        return self.conn.cursor()

    def execute(self, sql_query_string, and_close=False):
        """
        Executes SQL queries
        :param str sql_query_string: Contain the query string to be executed
        :param bool and_close: If true, closes the database connection after
        executing and commiting the SQL Query
        """
        cursor = self.cursor()
        cursor.execute(sql_query_string)
        if and_close:
            self.conn.commit()
            self.close()
        return {"conn": self.conn, "cursor": cursor if not and_close else None}

    def insert(self, sql_query_string, data, and_close=False):
        """
        Executes SQL queries
        :param str sql_query_string: Contains the query string to be
        :param bool and_close: If true, closes the database connetion
        after executing and committing the SQL query
        """
        cursor = self.cursor()
        cursor.execute(sql_query_string, data)
        if and_close:
            self.conn.commit()
            self.close()
        return {"conn": self.conn, "cursor": cursor if not and_close else None}

    def close(self):
        """
        Closes the current database connection
        """
        return self.conn.close()
