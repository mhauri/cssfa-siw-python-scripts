import hashlib
import sys
import os

def calculate_sha1(file_path):
    """Calculate the SHA-1 hash of a file."""
    sha1 = hashlib.sha1()

    with open(file_path, 'rb') as f:
        while True:
            data = f.read(8192)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()

def validate_checksums(file_list):
    """Validate the checksums of a list of files."""
    with open(file_list, 'r') as f:
        for line in f:
            checksum, file_path = line.strip().split(' ', 1)

            if not os.path.exists(file_path):
                print(f"File {file_path} does not exist.")
                continue

            calculated_checksum = calculate_sha1(file_path)

            if calculated_checksum == checksum:
                print(f"Checksum for {file_path} is VALID.")
            else:
                print(f"Checksum for {file_path} is INVALID. Calculated: {calculated_checksum}, Expected: {checksum}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <file_list>")
        sys.exit(1)

    file_list = sys.argv[1]
    validate_checksums(file_list)