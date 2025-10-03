import sqlite3
import pandas as pd
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, "sales.db")

# Connect to the database (or create one)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create the sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    product TEXT,
    category TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Insert sample data
data = [
    ("2025-01-01", "Laptop", "Electronics", 2, 4500.00),
    ("2025-01-02", "Mouse", "Accessories", 5, 150.00),
    ("2025-01-03", "Keyboard", "Accessories", 3, 200.00),
    ("2025-01-04", "Monitor", "Electronics", 1, 1200.00),
    ("2025-01-05", "Printer", "Peripherals", 2, 800.00)
]

cursor.executemany("INSERT INTO sales (date, product, category, quantity, price) VALUES (?, ?, ?, ?, ?)", data)
conn.commit()

# Load data from SQL into pandas
df = pd.read_sql_query("SELECT * FROM sales", conn)

# Create total revenue column
df["revenue"] = df["quantity"] * df["price"]

# General statistics
print(df.describe())

# Total revenue by category
revenue_by_category = df.groupby("category")["revenue"].sum()
print(revenue_by_category)

# Dashboard with pandas
import matplotlib.pyplot as plt
import seaborn as sns

# Bar chart - Revenue by category
plt.figure(figsize=(8,5))
sns.barplot(x=revenue_by_category.index, y=revenue_by_category.values)
plt.title("Revenue by Category")
plt.xlabel("Category")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.show()

# Close connection
conn.close()
