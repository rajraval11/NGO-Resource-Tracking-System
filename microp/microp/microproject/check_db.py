import sqlite3

# Connect to the database
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:")
for table in tables:
    print(table[0])

# Optionally, show data in each table
for table in tables:
    table_name = table[0]
    print(f"\nData in {table_name}:")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No data")

conn.close()
