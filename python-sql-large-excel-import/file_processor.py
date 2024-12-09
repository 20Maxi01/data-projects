import pandas as pd
import os
import logging

class FileProcessor:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        try:
            if self.file_path.endswith('.xlsx'):
                logging.info(f"Reading Excel file: {self.file_path}")
                df = pd.read_excel(self.file_path, engine='openpyxl')#, encoding='utf-8-sig') CHECK why encoding fails
            elif self.file_path.endswith('.csv'):
                logging.info(f"Reading CSV file: {self.file_path}")
                df = pd.read_csv(self.file_path, delimiter=';', encoding='utf-8-sig')
            else:
                raise ValueError("Unsupported file type. Please provide a .csv or .xlsx file.")
            logging.info("File read successfully.")
            return df
        except Exception as e:
            logging.error(f"Failed to read file: {e}")
            raise
