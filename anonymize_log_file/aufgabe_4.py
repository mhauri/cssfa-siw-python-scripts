import tkinter as tk
from tkinter import filedialog
import re

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

def select_file():
    file_path = filedialog.askopenfilename(title="Select Log File")
    if file_path:
        output_file_path = file_path.split('.')[0] + '_anonymized.csv'
        anonymize_log_file(file_path, output_file_path)
        display_result(output_file_path)

def display_result(file_path):
    with open(file_path, 'r') as file:
        result = file.read()
    result_window = tk.Toplevel(root)
    result_window.title("Anonymized Log Data")

    text_area = tk.Text(result_window, height=20, width=80)
    text_area.insert(tk.END, result)
    text_area.pack()

# GUI setup
root = tk.Tk()
root.title("Log Anonymizer")

select_button = tk.Button(root, text="Select Log File", command=select_file)
select_button.pack(pady=20)

root.mainloop()
