import sqlite3

conn = sqlite3.connect('vehicle_info.db')
cursor = conn.cursor()

# Create the table
cursor.execute('''
CREATE TABLE IF NOT EXISTS vehicle_info (
    vehicle_number TEXT PRIMARY KEY,
    owner_name TEXT NOT NULL,
    phone_number TEXT NOT NULL
)
''')

# Insert the data
data = [
    ("OD07N9936", "Deepak Kumar Rauta", "+91 6372757074")
]

cursor.executemany('''
INSERT OR REPLACE INTO vehicle_info (vehicle_number, owner_name, phone_number)
VALUES (?, ?, ?)
''', data)

# Commit and close
conn.commit()
conn.close()

print("Database updated successfully!")
