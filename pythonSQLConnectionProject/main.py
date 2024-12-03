import argparse
import logging
import os
from db_connection import DatabaseConnection
from file_processor import FileProcessor
from table_operations import create_table, insert_data


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def main():
    setup_logging()

    # CLI Argument Parsing
    parser = argparse.ArgumentParser(description="SQL Import Automation Tool")
    parser.add_argument('file_path', type=str, help="Path to the input file (.csv or .xlsx)")
    parser.add_argument('target_table', type=str, help="Target table name in SQL Server")
    args = parser.parse_args()

    file_path = args.file_path
    target_table = args.target_table

    # Validate file extension
    if not (file_path.endswith('.csv') or file_path.endswith('.xlsx')):
        logging.error("File must be a .csv or .xlsx")
        return

    try:
        # Process input file
        processor = FileProcessor(file_path)
        df = processor.read_file()

        # Connect to database
        db = DatabaseConnection()
        conn = db.get_connection()

        try:
            cursor = conn.cursor()

            # Create table
            create_table(cursor, target_table, df)

            # Insert data
            insert_data(cursor, target_table, df)

            # Commit changes
            conn.commit()

            logging.info(f"Data successfully imported into table '{target_table}'")
        except Exception as e:
            logging.error(f"Error during database operations: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()
            logging.info("Database connection closed.")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()
