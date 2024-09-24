import csv
import json
import sys
import os


# Function to anonymize the IP by masking the last byte
def anonymize_ip(ip_address):
    ip_parts = ip_address.split('.')
    ip_parts[-1] = 'xxx'
    return '.'.join(ip_parts)


# Function to partially anonymize the email address
def anonymize_email(email):
    local_part, domain = email.split('@')
    parts = local_part.split('.')
    anonymized_parts = [p[0] + '*' * (len(p) - 1) for p in parts]
    anonymized_local = '.'.join(anonymized_parts)
    return anonymized_local + '@' + domain


# Function to process the input JSON file and write to a CSV
def process_json_to_csv(input_file, output_file):
    if not os.path.exists(input_file):
        print(f"Error: The file {input_file} does not exist.")
        return

    try:
        # Open the output CSV file for writing
        with open(output_file, mode='w', newline='') as csvfile:
            fieldnames = ['Order ID', 'Anonymized Email', 'Anonymized IP', 'ZIP Code', 'Order Date']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Read and process each JSON object
            with open(input_file, 'r') as jsonfile:
                for line in jsonfile:
                    order = json.loads(line)
                    user_info = order['user']

                    # Extract and process the relevant data
                    anonymized_ip = anonymize_ip(order['ip'])
                    anonymized_email = anonymize_email(user_info['mail'])
                    zip_code = user_info['address'].split('\n')[-1].split(' ')[0]
                    order_date = order['date']

                    # Write the anonymized data to the CSV file
                    writer.writerow({
                        'Order ID': order['id'],
                        'Anonymized Email': anonymized_email,
                        'Anonymized IP': anonymized_ip,
                        'ZIP Code': zip_code,
                        'Order Date': order_date
                    })
        print(f"Processing complete. Output saved to {output_file}")
    except Exception as e:
        print(f"Error processing file: {e}")


# Main function
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python anonymize_orders.py <input_json_file> <output_csv_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        process_json_to_csv(input_file, output_file)