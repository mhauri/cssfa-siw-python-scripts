import pandas as pd
from datetime import timedelta

def process_auth_log(log_file_path, output_file_path):
    # Define the format for the log fields
    columns = ['Date', 'Time', 'SessionID', 'Username', 'HTTP_Verb', 'URL', 'Status_Code', 'User_Agent']

    # Read the log file into a DataFrame
    log_data = pd.read_csv(log_file_path, sep=' ', names=columns, header=None)

    # Combine Date and Time into a single column for easier handling
    log_data['Timestamp'] = pd.to_datetime(log_data['Date'] + ' ' + log_data['Time'], format='%Y-%m-%d %H:%M:%S')

    # Drop unnecessary columns for analysis
    log_data = log_data.drop(columns=['Date', 'Time', 'User_Agent', 'Status_Code'])

    # Initialize a dictionary to track session data
    sessions = {}

    # Iterate over the log data to process each row
    for index, row in log_data.iterrows():
        session_id = row['SessionID']
        username = row['Username']
        timestamp = row['Timestamp']
        verb = row['HTTP_Verb']
        url = row['URL']

        # Handle login (POST to /auth/)
        if verb == 'POST' and url == '/auth/':
            if session_id not in sessions:
                # New session initiated
                sessions[session_id] = {
                    'SessionID': session_id,
                    'User': username,
                    'StartTime': timestamp,
                    'EndTime': timestamp,
                    'Reason': 'TIMEOUT',  # Assume TIMEOUT by default
                }

        # Handle refresh (PUT to /auth/)
        elif verb == 'PUT' and url == '/auth/':
            if session_id in sessions:
                # Update the end time for the session
                sessions[session_id]['EndTime'] = timestamp

        # Handle logout (POST to /logout/)
        elif verb == 'POST' and url == '/logout/':
            if session_id in sessions:
                # Update the end time and reason for logout
                sessions[session_id]['EndTime'] = timestamp
                sessions[session_id]['Reason'] = 'LOGOUT'

    # After iterating, add the timeout buffer for sessions that have not explicitly logged out
    timeout_buffer = timedelta(minutes=2.5)
    for session in sessions.values():
        if session['Reason'] == 'TIMEOUT':
            session['EndTime'] += timeout_buffer

    # Create a DataFrame from the session data
    session_report = pd.DataFrame(list(sessions.values()),
                                  columns=['SessionID', 'User', 'StartTime', 'EndTime', 'Reason'])

    # Export to CSV with the required columns
    session_report.to_csv(output_file_path, index=False,
                          columns=['SessionID', 'User', 'StartTime', 'EndTime', 'Reason'])
    return session_report

def process_session_report():
    # Load the uploaded session report
    session_report_path = 'session_report.csv'

    # Read the CSV file into a DataFrame
    session_report = pd.read_csv(session_report_path)

    # Convert StartTime and EndTime to datetime format
    session_report['StartTime'] = pd.to_datetime(session_report['StartTime'], format='%Y-%m-%d %H:%M:%S')
    session_report['EndTime'] = pd.to_datetime(session_report['EndTime'], format='%Y-%m-%d %H:%M:%S')

    # Calculate session duration
    session_report['Duration'] = session_report['EndTime'] - session_report['StartTime']

    # Answer the questions
    num_sessions = len(session_report)
    shortest_session = session_report['Duration'].min()
    longest_session = session_report['Duration'].max()
    logout_percentage = (session_report[session_report['Reason'] == 'LOGOUT'].shape[0] / num_sessions) * 100

    print(f"Number of valid sessions: {num_sessions}")
    print(f"Shortest session: {shortest_session}")
    print(f"Longest session: {longest_session}")
    print(f"Percentage of sessions logged out explicitly: {logout_percentage:.2f}%")


log_file_path = 'auth.log'  # Replace with the path to your log file
output_file_path = 'session_report.csv'
session_report = process_auth_log(log_file_path, output_file_path)
process_session_report()
