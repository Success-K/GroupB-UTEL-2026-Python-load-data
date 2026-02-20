import pandas as pd
from sqlalchemy import create_engine

# ---- DATABASE CONNECTION ----
username = "root"
password = "andrew"
host = "localhost"
port = "3306"
database = "retail_sales_dw"

engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)

# ---- YOUR QUERIES ----
queries = {
    "Revenue_by_Product": """
        SELECT p.name, SUM(s.total_amount) AS rev
        FROM sales s
        JOIN product p ON s.product_id = p.product_id
        GROUP BY 1
        ORDER BY 2 DESC;
    """,

    "Monthly_Revenue": """
        SELECT d.year, d.month, SUM(s.total_amount) AS monthly_revenue
        FROM sales s
        JOIN date_dim d ON s.date_id = d.date_id
        GROUP BY d.year, d.month
        ORDER BY d.year, d.month;
    """,

    "Revenue_by_Age_Group": """
        SELECT c.age_group, SUM(s.total_amount) AS revenue
        FROM sales s
        JOIN customer c ON s.customer_id = c.customer_id
        GROUP BY c.age_group
        ORDER BY revenue DESC;
    """,

    "Avg_Purchase_per_Customer": """
        SELECT c.name AS customer_name, AVG(s.total_amount) AS avg_purchase_value
        FROM sales s
        JOIN customer c ON s.customer_id = c.customer_id
        GROUP BY c.name
        ORDER BY avg_purchase_value DESC;
    """,

    "Sales_by_District": """
        SELECT l.district, SUM(s.total_amount) AS total_sales
        FROM sales s
        JOIN location l ON s.location_id = l.location_id
        GROUP BY l.district
        ORDER BY total_sales DESC;
    """
}

# ---- EXPORT TO EXCEL ----
output_file = "Group-B-Sales-report.xlsx"

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    for sheet_name, query in queries.items():
        df = pd.read_sql(query, engine)
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"All reports exported successfully to {output_file}")
