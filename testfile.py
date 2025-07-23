import mysql.connector
from mysql.connector import Error

def transfer_table(source_db_config, dest_db_config, table_name):
    source_conn = None
    dest_conn = None
    try:
        # Connect to the source database
        source_conn = mysql.connector.connect(**source_db_config)
        if source_conn.is_connected():
            print(f"Connected to source database: {source_db_config['database']} on port {source_db_config['port']}")
            source_cursor = source_conn.cursor()

            # Connect to the destination database
            dest_conn = mysql.connector.connect(**dest_db_config)
            if dest_conn.is_connected():
                print(f"Connected to destination database: {dest_db_config['database']} on port {dest_db_config['port']}")
                dest_cursor = dest_conn.cursor()

                # 1. Get CREATE TABLE statement from source
                source_cursor.execute(f"SHOW CREATE TABLE {table_name}")
                create_table_sql = source_cursor.fetchone()[1]

                # Optional: Modify the CREATE TABLE statement if needed (e.g., remove AUTO_INCREMENT)
                # For simplicity, we'll use it as is.
                # If the table already exists in destination, you might want to DROP it first
                # dest_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")

                # 2. Create table in destination database
                print(f"Creating table '{table_name}' in destination...")
                dest_cursor.execute(create_table_sql)
                print(f"Table '{table_name}' created in destination.")

                # 3. Read data from source table
                print(f"Reading data from '{table_name}' in source...")
                source_cursor.execute(f"SELECT * FROM {table_name}")
                rows = source_cursor.fetchall()
                columns = [i[0] for i in source_cursor.description]

                if rows:
                    # 4. Insert data into destination table
                    print(f"Inserting {len(rows)} rows into '{table_name}' in destination...")
                    placeholders = ', '.join(['%s'] * len(columns))
                    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
                    dest_cursor.executemany(insert_sql, rows)
                    dest_conn.commit()
                    print(f"Successfully transferred {len(rows)} rows to '{table_name}'.")
                else:
                    print(f"No data found in table '{table_name}' to transfer.")

            else:
                print("Failed to connect to destination database.")
    except Error as e:
        print(f"Error transferring table: {e}")
    finally:
        if source_conn and source_conn.is_connected():
            source_cursor.close()
            source_conn.close()
            print("Source database connection closed.")
        if dest_conn and dest_conn.is_connected():
            dest_cursor.close()
            dest_conn.close()
            print("Destination database connection closed.")

if __name__ == "__main__":
    # --- Configuration for your two MySQL servers ---
    # (e.g., if using Docker, port 3306 and 3307 might map to container port 3306)

    source_db_config = {
        'host': 'localhost',
        'port': 3306,  
        'user': 'root',
        'password': 'apisodai@123', 
        'database': 'mydatabase'  # Change this to your source database name
    }

    dest_db_config = {
        'host': 'localhost',
        'port': 3306,  # Port for your second MySQL server
        'user': 'root',
        'password': 'apisodai@123', # Change this
        'database': 'my_new_database_on_server2' # Change this
    }

    table_to_transfer = 'customer_records' # Replace with the actual table name you want to transfer

    transfer_table(source_db_config, dest_db_config, table_to_transfer)