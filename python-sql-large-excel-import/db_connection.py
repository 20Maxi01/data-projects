import os
import pyodbc
from dotenv import load_dotenv, find_dotenv
import logging

class DatabaseConnection:
    def __init__(self, conn_str=None):
        load_dotenv(find_dotenv())

        self.db_driver = os.getenv("DB_DRIVER")
        self.db_server = os.getenv("DB_SERVER")
        self.db_name = os.getenv("DB_NAME")
        self.db_username = os.getenv("DB_USERNAME")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_encrypt = os.getenv("DB_ENCRYPT")

        self.conn_str = conn_str or (
            f"DRIVER={{{self.db_driver}}};"
            f"SERVER={self.db_server};"
            f"DATABASE={self.db_name};"
            f"UID={self.db_username};"
            f"PWD={self.db_password};"
            f"Encrypt={self.db_encrypt};"
        )

    def get_connection(self):
        try:
            connection = pyodbc.connect(self.conn_str)
            logging.info("Database connection successful.")
            return connection
        except pyodbc.Error as ex:
            logging.error("Database connection failed.")
            for err in ex.args:
                logging.error(err)
            raise