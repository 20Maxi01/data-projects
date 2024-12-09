import logging


def create_table(cursor, table_name, df):
    try:
        column_definitions = []
        for i, column in enumerate(df.columns):
            if i < 4:  # First four columns as NVARCHAR(50)
                column_definitions.append(f"[{column}] NVARCHAR(50)")
            else:  # Remaining columns as NVARCHAR(9)
                column_definitions.append(f"[{column}] NVARCHAR(9)")

        create_table_query = f"CREATE TABLE {table_name} ({', '.join(column_definitions)});"

        # Drop the table if it exists
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
        cursor.execute(create_table_query)
        logging.info(f"Table '{table_name}' created successfully.")
    except Exception as e:
        logging.error(f"Failed to create table: {e}")
        raise


def insert_data(cursor, table_name, df):
    try:
        insert_query = f"INSERT INTO {table_name} ({', '.join([f'[{col}]' for col in df.columns])}) VALUES ({', '.join(['?' for _ in df.columns])})"

        for index, row in df.iterrows():
            cursor.execute(insert_query, tuple(row))
        logging.info(f"Data successfully inserted into table '{table_name}'.")
    except Exception as e:
        logging.error(f"Failed to insert data: {e}")
        raise
