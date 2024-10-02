import argparse
import csv
import datetime

# Main function to process the certificates
def process_certificates(csv_file, output_file):
    data = []

    with open(csv_file) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')  # Adjust delimiter to ';' as per the headers
        for row in reader:
            serial = row['Serial']
            valid_till = row['ValidTill']
            issuer = row['Issuer']
            revocation_status = row['Revocation Status']
            signature_algo = row['Signature Algorithm']
            public_key = row['Public Key']
            issues = []

            # Parse the ValidTill field to check for expiration
            valid_till_date = datetime.datetime.strptime(valid_till, '%d.%m.%Y')  # Adjusted date format to '%d.%m.%Y'
            if valid_till_date < datetime.datetime.now():
                issues.append(f"Expired (Valid Till: {valid_till})")

            # Check if the certificate is self-signed (Issuer same as CN)
            if row['Issuer'] == row['CN']:  # CN represents the certificate's subject
                issues.append("Self-signed certificate (Issuer same as CN)")

            # Check for untrusted authority
            trusted_issuers = ['DigiCert', 'GlobalSign', 'Comodo', 'Sectigo', 'QuoVadis', 'Amazon']  # Add more trusted CAs
            if not any(trusted_issuer in issuer for trusted_issuer in trusted_issuers):
                issues.append(f"Untrusted Authority (Issuer: {issuer})")

            # Check for weak algorithms or key lengths
            if 'RSA' in public_key and '1024' in public_key:
                issues.append("Weak Key Length (RSA 1024 bits)")

            # Check for insecure signature algorithm
            if 'sha1' in signature_algo.lower():
                issues.append(f"Insecure Signature Algorithm (SHA-1)")

            # Check revocation status
            if revocation_status.lower() == 'revoked':
                issues.append("Revoked certificate")

            # Append serial and issues only
            formatted_issues = ' | '.join(issues) if issues else 'None'
            data.append([serial, formatted_issues])

    # Write the results to a CSV file
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Serial', 'Issues'])  # Write headers
        writer.writerows(data)  # Write rows

# Set up argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process certificates from a CSV file.')
    parser.add_argument('csv_file', help='Path to the CSV file containing certificate data')
    parser.add_argument('output_file', help='Path to the output CSV file')

    args = parser.parse_args()

    # Call the function with the provided file
    process_certificates(args.csv_file, args.output_file)