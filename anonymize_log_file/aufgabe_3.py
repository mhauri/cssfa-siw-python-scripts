import re
from datetime import datetime, timedelta
import random

def anonymize_log_file(input_file_path, output_file_path):
    # Muster zum Erkennen von Namen, E-Mails, IP-Adressen und Zeitstempeln
    name_pattern = r'\b[A-Z][a-z]*\s[A-Z][a-z]*\b'
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
    time_pattern = r'\d{2}:\d{2}:\d{2}.\d{6}'

    with open(input_file_path, 'r') as file:
        log_data = file.read()

    # Ersetzen der personenbezogenen Daten durch Platzhalter
    log_data = re.sub(name_pattern, 'ANONYMIZED_NAME', log_data)
    log_data = re.sub(email_pattern, 'ANONYMIZED_EMAIL', log_data)
    log_data = re.sub(ip_pattern, 'ANONYMIZED_IP', log_data)
    log_data = re.sub(time_pattern, 'ANONYMIZED_TIME', log_data)

    with open(output_file_path, 'w') as file:
        file.write(log_data)


# Verwendung der Funktion
anonymize_log_file('log.csv', 'output_aufgabe_3.csv')
