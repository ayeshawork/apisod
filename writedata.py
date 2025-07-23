import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from urllib.parse import quote_plus
import pymysql # Recommended for SQLAlchemy MySQL connections

fake = Faker()

def generate_random_data(num_records=100):
    data = []
    for _ in range(num_records):
        customer_name = fake.name()
        product = fake.word(ext_word_list=['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Webcam', 'Headphones', 'Speaker', 'Printer', 'Scanner', 'Router'])
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80).strftime('%Y-%m-%d')        
        address = fake.address().replace('\n', ', ')
        qty_purchased = random.randint(1, 10)

        data.append({
            'customerName': customer_name,
            'Product': product,
            'dob': dob,
            'address': address,
            'qtyPurchased': qty_purchased
        })
    return data

records = generate_random_data(100)
df = pd.DataFrame(records)

# print("Generated Customer Data Table (first 10 rows):")
# print(df.head(10).to_markdown(index=False))

# --- MySQL Database Integration ---
# IMPORTANT: Replace with your actual MySQL database credentials and details
DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = quote_plus('apisodai@123')  # encode special characters like '@'
print(DB_PASSWORD)  # For debugging, remove in production   
DB_NAME = 'mydatabase' # Ensure this database exists or will be created
DB_TABLE_NAME = 'customer_records' # Name of the table to create/insert into

try:
    # Create a SQLAlchemy engine to connect to MySQL
    # Ensure you have 'pymysql' installed: pip install pymysql
    # Or 'mysql-connector-python': pip install mysql-connector-python   
    # For mysql-connector-python, the connection string would be:
    # f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

    # Write the DataFrame to the MySQL table
    # if_exists='replace' will drop the table if it exists and recreate it.
    # if_exists='append' will append new rows to an existing table.
    # index=False prevents Pandas from writing the DataFrame index as a column in MySQL.
    df.to_sql(name=DB_TABLE_NAME, con=engine, if_exists='replace', index=False)

    print(f"\nSuccessfully wrote {len(df)} records to MySQL table '{DB_TABLE_NAME}' in database '{DB_NAME}'.")

except ImportError:
    print("\nError: 'pymysql' or 'mysql-connector-python' not found.")
    print("Please install it using: pip install pymysql (or pip install mysql-connector-python)")
except Exception as e:
    print(f"\nAn error occurred while writing to MySQL: {e}")
finally:
    # Dispose the engine to close the connection (important for resource management)
    if 'engine' in locals() and engine:
        engine.dispose()
        print("Database connection closed.")

# You can also save this DataFrame to a CSV file if needed:
# df.to_csv('customer_data.csv', index=False)
# print("\nData saved to customer_data.csv")
