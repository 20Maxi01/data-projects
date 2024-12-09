# SQL Import Automation Tool

This project provides a solution for importing Excel files into a Microsoft SQL Server database. The code was developed to address limitations and issues encountered with SQL Server Integration Services (SSIS) and dynamic bulk inserts when handling Excel files with more than 255 columns.

---

## **Background**

### **Challenges Addressed**
1. **SSIS and Excel Import Limitations**:
   - SSIS struggles to import Excel files with more than 255 columns due to legacy design constraints. For example:
     - [SQL Server Central Post](https://www.sqlservercentral.com/forums/topic/ssis-importing-excel-spreadsheet-with-more-than-255-columns)
     - [Microsoft Q&A](https://learn.microsoft.com/en-gb/answers/questions/1611021/importing-xlsx-with-more-than-255-columns-to-ssms)
   - Workarounds like splitting files into smaller chunks can be tedious and error-prone.

2. **Dynamic Bulk Insert Issues**:
   - Attempts to dynamically generate and execute `BULK INSERT` statements for large files often result in string truncation errors, even when using `NVARCHAR(MAX)`. For example:
     - [Stack Overflow Discussion](https://stackoverflow.com/questions/4833549/nvarcharmax-still-being-truncated)

### **Solution**
The python script:
- Connects to the SQl Server Instance using the proviced
- Dynamically creates SQL tables based on the structure of the input Excel file. Thy dynamic statement has no column limitation compared to SSIS.
- Converts all data to string format to ensure compatibility. Adjustements can be made using the column index.
- Automates the entire workflow for seamless integration into existing pipelines.

---

## **System Setup**

This project was tested and developed using the following setup:
1. **SQL Server via Docker**:
   - The [Azure SQL Edge](https://hub.docker.com/r/microsoft/azure-sql-edge) Docker image was used to host SQL Server.

2. **Azure Data Studio**:
   - Azure Data Studio was used to manage and query the database. It can be downloaded here:
     [Download Azure Data Studio](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?view=sql-server-ver16&tabs=win-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall)

3. **ODBC Driver**:
   - The [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16) was installed for database connectivity.

---



## **Installation & Prerequisites**
- Python 3.8 or higher
- [Microsoft ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16)
- Docker with [Azure SQL Edge](https://hub.docker.com/r/microsoft/azure-sql-edge)
- [Azure Data Studio](https://learn.microsoft.com/en-us/azure-data-studio/download-azure-data-studio?view=sql-server-ver16&tabs=win-install%2Cwin-user-install%2Credhat-install%2Cwindows-uninstall%2Credhat-uninstall)
- ```bash 
  pip install -r requirements.txt
  
## **Executing the script**
The script can be executed using the command line in your project directory. Arguments that are passed via the command line override the env-file variables. 
For further information run python main.py --help.
```
python main.py --help

usage: main.py [-h] --file_path FILE_PATH --target_table TARGET_TABLE [--db_name DB_NAME] [--db_driver DB_DRIVER] [--db_server DB_SERVER] [--db_username DB_USERNAME] [--db_password DB_PASSWORD] [--db_encrypt DB_ENCRYPT]

SQL Import Automation Tool

options:
  -h, --help            show this help message and exit
  --file_path FILE_PATH
                        Mandatory: Path to the input file (.csv or .xlsx)
  --target_table TARGET_TABLE
                        Mandatory: Target table name in SQL Server
  --db_name DB_NAME     Database name in SQL Server (overrides .env if provided)
  --db_driver DB_DRIVER
                        ODBC Driver (e.g., 'ODBC Driver 18 for SQL Server')
  --db_server DB_SERVER
                        SQL Server address (e.g., 'localhost,1433')
  --db_username DB_USERNAME
                        Username for SQL Server authentication
  --db_password DB_PASSWORD
                        Password for SQL Server authentication
  --db_encrypt DB_ENCRYPT
                        Encryption option for SQL Server (e.g., 'no')

Example usage: python main.py --file_path /path/to/file.xlsx --target_table TargetTableName --db_name MyDatabase
```
