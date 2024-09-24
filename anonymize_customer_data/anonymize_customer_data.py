import sqlite3
import pandas as pd

def anonymize_customer_data(db_path, output_csv_path):
    conn = sqlite3.connect(db_path)

    query = """
    SELECT
        t_customer.gender,
        SUBSTR(t_customer.lastname, 1, 2) || '--------' AS lastname,
        CASE 
            WHEN t_customer.birthdate IS NOT NULL THEN SUBSTR(t_customer.birthdate, -4)
            ELSE 'Unknown'
        END AS birthyear,
        SUBSTR(t_location.zip, 1, 2) || '00' AS zip,
        t_customer_status.status
    FROM
        t_customer
    JOIN
        t_location ON t_customer.fk_location = t_location.pk_location
    JOIN
        t_customer_status ON t_customer.fk_customer_status = t_customer_status.pk_customer_status
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    df.to_csv(output_csv_path, index=False)

    print(f"Anonymized data saved to {output_csv_path}")

if __name__ == "__main__":
    db_path = "c3-database-initial.db"  # Replace with your database path
    output_csv_path = "anonymized_customer_data.csv"  # Replace with desired output path
    anonymize_customer_data(db_path, output_csv_path)
