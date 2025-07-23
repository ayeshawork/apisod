import mysql.connector
from mysql.connector import Error

def create_database_on_second_server(host, port, user, password, db_name):
    """
    Connects to a MySQL server on a specified port and creates a new database.

    Args:
        host (str): The hostname or IP address of the MySQL server.
        port (int): The port number of the MySQL server.
        user (str): The username to connect with (e.g., 'root').
        password (str): The password for the specified user.
        db_name (str): The name of the database to create.

    Returns:
        bool: True if the database was created successfully or already exists, False otherwise.
    """
    connection = None
    cursor = None
    try:
        # Establish a connection to the MySQL server without specifying a database initially
        # This is because we want to create a database, not connect to an existing one yet.
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )

        if connection.is_connected():
            print(f"Successfully connected to MySQL server on {host}:{port}")
            cursor = connection.cursor()

            # SQL query to create the database
            # Using IF NOT EXISTS prevents an error if the database already exists
            create_db_query = f"CREATE DATABASE IF NOT EXISTS {db_name}"

            # Execute the query
            cursor.execute(create_db_query)
            print(f"Database '{db_name}' created successfully or already exists on {host}:{port}.")
            return True
        else:
            print(f"Failed to connect to MySQL server on {host}:{port}.")
            return False

    except Error as e:
        print(f"Error creating database '{db_name}' on {host}:{port}: {e}")
        return False
    finally:
        # Close the cursor and connection in the finally block to ensure they are always closed
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()
            print(f"MySQL connection to {host}:{port} closed.")

if __name__ == "__main__":
    # --- Configuration for your second MySQL server ---
    # IMPORTANT: Replace these with your actual second server details.
    # The port should be the one you configured for your second MySQL instance (e.g., 3307).
    second_server_config = {
        'host': 'localhost',
        'port': 3306,  # <--- Make sure this is the port of your second MySQL server
        'user': 'root',
        'password': 'apisodai@123' # <--- CHANGE THIS PASSWORD
    }

    database_name_to_create = 'my_new_database_on_server2' # <--- Name of the database you want to create

    print(f"Attempting to create database '{database_name_to_create}' on the second MySQL server...")
    success = create_database_on_second_server(
        second_server_config['host'],
        second_server_config['port'],
        second_server_config['user'],
        second_server_config['password'],
        database_name_to_create
    )

    if success:
        print("\nDatabase creation process completed.")
    else:
        print("\nDatabase creation process failed.")

    # You can try creating another database or the same one to see the "already exists" message
    # print("\nAttempting to create another database...")
    # create_database_on_second_server(
    #     second_server_config['host'],
    #     second_server_config['port'],
    #     second_server_config['user'],
    #     second_server_config['password'],
    #     'another_db_on_server2'
    # )
