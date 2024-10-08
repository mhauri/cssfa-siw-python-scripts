import sqlite3
import pandas as pd
import random
import argparse

# Function to anonymize first names
def anonymize_first_name(name):
    if pd.isnull(name):
        return name
    return f"{name[0]}*********"

# Function to anonymize last names by replacing with a random 10-digit number
def anonymize_last_name():
    return str(random.randint(1000000000, 9999999999))

# Function to reduce date of birth to year
def anonymize_dob(dob):
    if pd.isnull(dob):
        return dob
    return dob.split("-")[0]

# Function to categorize salary
def categorize_salary(salary):
    if pd.isnull(salary):
        return None
    salary = float(salary)
    if salary < 50000:
        return 'low'
    elif salary < 100000:
        return 'medium'
    else:
        return 'high'

# Main function to anonymize the data
def anonymize_data(input_db, output_db):
    # Connect to the original database
    conn = sqlite3.connect(input_db)

    # Load the data from the 't_person' table
    data_query = "SELECT * FROM t_person;"
    data = pd.read_sql(data_query, conn)

    # Apply anonymization
    data['first_name'] = data['first_name'].apply(anonymize_first_name)
    data['last_name'] = data['last_name'].apply(lambda x: anonymize_last_name())
    data['date_of_birth'] = data['date_of_birth'].apply(anonymize_dob)
    data['salary'] = data['salary'].apply(categorize_salary)

    # Drop unnecessary columns: 'username', 'password', 'is_vip'
    data.drop(columns=['username', 'password', 'is_vip'], inplace=True)

    # Connect to the new anonymized database
    new_conn = sqlite3.connect(output_db)

    # Save the anonymized data to the new database
    data.to_sql('t_person_anonymized', new_conn, if_exists='replace', index=False)

    # Close the database connections
    conn.close()
    new_conn.close()

    print(f"Data anonymized successfully and saved to {output_db}!")

# Parse command-line arguments
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Anonymize a database")
    parser.add_argument('input_db', help='Path to the input (original) database')
    parser.add_argument('output_db', help='Path to the output (anonymized) database')

    args = parser.parse_args()

    # Call the anonymization function with the provided arguments
    anonymize_data(args.input_db, args.output:_db)