import mysql.connector
from faker import Faker

fake=Faker()
print("MySQL Connector/Python is installed and ready to use.")

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="apisodai@123"
)

#print(mydb)
mycursor = conn.cursor()
mycursor.execute("SHOW DATABASES")
for x in mycursor:
    print(x)
mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")

mycursor.execute("USE mydatabase")

mycursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        address VARCHAR(255)
    )
""")
sql = "INSERT INTO customers (name, address) VALUES (%s, %s)"
for _ in range(10):
    name = fake.name()
    address = fake.address().replace('\n', ', ')  
    mycursor.execute(sql, (name, address))

# Commit changes and close connection
conn.commit()
print("10 random customers inserted.")

mycursor.execute("SELECT * FROM customers")
myresult = mycursor.fetchall()
for x in myresult:
    print(x)

print(len(myresult), "was inserted.")   

# mycursor.execute("delete from customers")
# conn.commit()


mycursor.close()
conn.close()


