import argparse
import logging
import os
from db_connection import DatabaseConnection
from file_processor import FileProcessor
from table_operations import create_table, insert_data
from dotenv import load_dotenv, find_dotenv


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )


def main():
    setup_logging()

    # Load environment variables from .env
    load_dotenv(find_dotenv())

    # CLI Argument Parsing
    parser = argparse.ArgumentParser(
        description="SQL Import Automation Tool",
        epilog="Example usage: python main.py --file_path /path/to/file.xlsx --target_table TargetTableName --db_name MyDatabase"
    )
    parser.add_argument('--file_path', type=str, required=True,
                        help="Mandatory: Path to the input file (.csv or .xlsx)")
    parser.add_argument('--target_table', type=str, required=True, help="Mandatory: Target table name in SQL Server")
    parser.add_argument('--db_name', type=str, help="Database name in SQL Server (overrides .env if provided)")
    parser.add_argument('--db_driver', type=str, help="ODBC Driver (e.g., 'ODBC Driver 18 for SQL Server')")
    parser.add_argument('--db_server', type=str, help="SQL Server address (e.g., 'localhost,1433')")
    parser.add_argument('--db_username', type=str, help="Username for SQL Server authentication")
    parser.add_argument('--db_password', type=str, help="Password for SQL Server authentication")
    parser.add_argument('--db_encrypt', type=str, help="Encryption option for SQL Server (e.g., 'no')")
    args = parser.parse_args()

    # Retrieve or override environment variables
    db_driver = args.db_driver or os.getenv("DB_DRIVER")
    db_server = args.db_server or os.getenv("DB_SERVER")
    db_name = args.db_name or os.getenv("DB_NAME")
    db_username = args.db_username or os.getenv("DB_USERNAME")
    db_password = args.db_password or os.getenv("DB_PASSWORD")
    db_encrypt = args.db_encrypt or os.getenv("DB_ENCRYPT")

    # Debugging logs for connection variables
    #logging.info(f"Using DB_DRIVER={db_driver}")
    #logging.info(f"Using DB_SERVER={db_server}")
    #logging.info(f"Using DB_NAME={db_name}")
    #logging.info(f"Using DB_USERNAME={db_username}")
    #logging.info(f"Using DB_PASSWORD={db_password}")
    #logging.info(f"Using DB_ENCRYPT={db_encrypt}")

    # Validate mandatory variables
    if not all([db_driver, db_server, db_name, db_username, db_password, db_encrypt]):
        logging.error("Missing required database configuration. Ensure all values are provided via CLI or .env file.")
        exit()

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
        conn_str = (
            f"DRIVER={{{db_driver}}};"
            f"SERVER={db_server};"
            f"DATABASE={db_name};"
            f"UID={db_username};"
            f"PWD={db_password};"
            f"Encrypt={db_encrypt};"
        )
        db = DatabaseConnection(conn_str)
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
