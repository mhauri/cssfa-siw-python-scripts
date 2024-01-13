import requests
import sys

def check_file_or_directory(url, file_path):
    with open(file_path, 'r') as file:
        files_or_directories = [line.strip() for line in file]

    for file_or_directory in files_or_directories:
        response = requests.get(url + '/' + file_or_directory)

        if response.status_code == 200:
            print(f"The file or directory {file_or_directory} exists")
        elif response.status_code == 403:
            print(f"The file or directory {file_or_directory} exists (403)")
        else:
            print(f"Received status code {response.status_code} when checking {file_or_directory}")

if __name__ == "__main__":
    url = sys.argv[1]  # Replace with your URL
    file_path = sys.argv[2]  # Replace with your file path

    check_file_or_directory(url, file_path)