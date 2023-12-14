
import csv
from collections import Counter

def analyze_anonymized_log(filename):
    total_entries = 0
    avg_name_length = 0
    most_common_names = Counter()
    phone_formats = Counter()

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            total_entries += 1

            # Erfassen der Namen und ihrer Längen
            name = row[0]
            avg_name_length += len(name)
            most_common_names[name] += 1

            # Erfassen verschiedener Telefonformate
            phone_format = row[3]
            phone_formats[phone_format] += 1

    avg_name_length /= total_entries if total_entries > 0 else 1
    most_common_names = most_common_names.most_common(5)
    phone_formats = phone_formats.most_common()

    return {
        'total_entries': total_entries,
        'average_name_length': avg_name_length,
        'most_common_names': most_common_names,
        'phone_formats': phone_formats
    }

# Beispielaufruf:
filename = 'log.csv'  # Passe den Dateinamen entsprechend an
statistics = analyze_anonymized_log(filename)

print("Anzahl der Log-Einträge insgesamt:", statistics['total_entries'])
print("Durchschnittliche Länge der Namen:", statistics['average_name_length'])
print("Die häufigsten 5 Namen:", statistics['most_common_names'])
print("Häufigkeit der Telefonformate:", statistics['phone_formats'])
