import sqlite3
import pandas as pd

# Function to anonymize customer data and save as CSV
def anonymize_customer_data(db_path, output_csv_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)

    # Updated SQL query to extract the last 4 digits of the birthdate as the year
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

    # Execute the query and load the results into a Pandas DataFrame
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # Save the anonymized data to a CSV file
    df.to_csv(output_csv_path, index=False)

    print(f"Anonymized data saved to {output_csv_path}")

# Example usage
if __name__ == "__main__":
    db_path = "c3-database-initial.db"  # Replace with your database path
    output_csv_path = "anonymized_customer_data.csv"  # Replace with desired output path
    anonymize_customer_data(db_path, output_csv_path)
