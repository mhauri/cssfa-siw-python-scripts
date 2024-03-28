import re
import time
import sqlite3
import json
from datetime import datetime

def parse_log_line(line):
    pattern = r'(?P<session_id>\S+) -- (?P<remote_addr>\S+) - - \[(?P<timestamp>.+)\] "(?P<http_method>\S+) (?P<http_uri>\S+) HTTP/1.1" (?P<http_status>\d+) (?P<http_response_size>\d+)'
    match = re.search(pattern, line)

    if match:
        data = match.groupdict()

        # Convert timestamp to Unix timestamp
        timestamp_str = data['timestamp']
        timestamp_obj = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
        data['timestamp'] = str(int(time.mktime(timestamp_obj.timetuple())))

        return data

    return None

def get_username_from_db(session_id, db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT username FROM user_sessions WHERE id = ?", (session_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return None

def extract_data_from_log_file(file_path, db_path):
    with open(file_path, 'r') as file:
        for line in file:
            data = parse_log_line(line)
            if data:
                data['user'] = get_username_from_db(data['session_id'], db_path)
                print(json.dumps(data, indent=4))
# Call the function with the path to your log file and SQLite database
extract_data_from_log_file('data.log', 'data.db')