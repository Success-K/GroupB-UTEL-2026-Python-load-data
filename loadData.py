import csv
import mysql.connector

# ----------------------------
# DATABASE CONNECTION
# ----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="andrew",   # <-- CHANGE THIS
    database="retail_sales_dw"    # <-- CHANGE THIS
)

cursor = conn.cursor()


# ----------------------------
# GENERIC LOAD FUNCTION
# ----------------------------
def load_table(csv_file, table_name):
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Skip header row
        
        placeholders = ', '.join(['%s'] * len(headers))
        query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({placeholders})"
        
        for row in reader:
            cursor.execute(query, row)

    conn.commit()
    print(f"{table_name} loaded successfully!")


# ----------------------------
# LOAD TABLES (DIMENSIONS FIRST)
# ----------------------------
# load_table('Product.csv', 'product')
# load_table('customer.csv', 'customer')
load_table('location.csv', 'location')
# load_table('date_dim.csv', 'date_dim')
load_table('sales.csv', 'sales')


# ----------------------------
# CLOSE CONNECTION
# ----------------------------
cursor.close()
conn.close()

print("All data loaded successfully!")
