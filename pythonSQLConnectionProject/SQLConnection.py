import pandas as pd
import os
import pyodbc  # Ensure pyodbc is imported
from dotenv import load_dotenv, find_dotenv

# make sure the environment variables get loaded on mac
os.environ["ODBCSYSINI"] = "/opt/homebrew/etc"
os.environ["ODBCINI"] = "/opt/homebrew/etc/odbc.ini"

#print(f"ODBCSYSINI={os.environ['ODBCSYSINI']}")
#print(f"ODBCINI={os.environ['ODBCINI']}")

try:
    print("Loading .env file")
    load_dotenv(find_dotenv())  # Make sure this path is correct
    print("Loaded .env file\n")
    
    # Retrieve connection details from environment variables
    db_driver = os.getenv("DB_DRIVER")
    db_server = os.getenv("DB_SERVER")
    db_name = os.getenv("DB_NAME")
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_encrypt = os.getenv("DB_ENCRYPT")

    # output to ensure environment variables are loaded
    print(f"DB_DRIVER={db_driver}")
    print(f"DB_SERVER={db_server}")
    print(f"DB_NAME={db_name}")
    print(f"DB_USERNAME={db_username}")
    print(f"DB_PASSWORD={db_password}")
    print(f"DB_ENCRYPT={db_encrypt}")
    
    # set up final connection string
    conn_str = (
        f"DRIVER={{{db_driver}}};"
        f"SERVER={db_server};"
        f"DATABASE={db_name};"
        f"UID={db_username};"
        f"PWD={db_password};"
        f"Encrypt={db_encrypt};"
    )
except Exception as e:
    print(f"Error loading .env file: {e}")

# Test the connection
try:
    conn = pyodbc.connect(conn_str)
    print("Connection to SQL Server successful!")
except pyodbc.Error as ex:
    print("Connection failed:")
    for err in ex.args:
        print(err)
    exit()


# Define the Excel file path
excel_file = 'SQL_Personalplan_Test.xlsx'  # Replace with your actual file path


# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file, engine='openpyxl')

df.head()

# Ensure connection is successful before proceeding
if 'conn' in locals() and conn is not None:
    try:
        cursor = conn.cursor()
        print("Connection verified. Proceeding with table creation...")
    except Exception as e:
        print(f"Connection is not active: {e}")
        exit()
else:
    print("Connection not established. Exiting...")
    exit()

# Define the table name
table_name = "Personalplan_Import"

# Ensure all columns in the DataFrame are converted to strings
df = df.astype(str)

# Generate SQL CREATE TABLE statement
column_definitions = []
for i, column in enumerate(df.columns):
    if i < 4:  # First three columns as NVARCHAR(50)
        column_definitions.append(f"[{column}] NVARCHAR(50)")
    else:  # Remaining columns as NVARCHAR(9)
        column_definitions.append(f"[{column}] NVARCHAR(9)")

create_table_query = f"CREATE TABLE {table_name} ({', '.join(column_definitions)});"

# Execute the CREATE TABLE statement
try:
    cursor.execute(f"DROP TABLE IF EXISTS {table_name};")  # Drop the table if it exists
    cursor.execute(create_table_query)
    conn.commit()
    print(f"Table '{table_name}' created successfully!")
except Exception as e:
    print(f"Failed to create table: {e}")
    exit()

# Insert DataFrame rows into the table
insert_query = f"INSERT INTO {table_name} ({', '.join([f'[{col}]' for col in df.columns])}) VALUES ({', '.join(['?' for _ in df.columns])})"

try:
    for index, row in df.iterrows():
        cursor.execute(insert_query, tuple(row))
    conn.commit()
    print(f"Data successfully inserted into table '{table_name}'")
except Exception as e:
    print(f"Failed to insert data: {e}")
    exit()

# Close the connection
cursor.close()
conn.close()
print("Database connection closed.")
