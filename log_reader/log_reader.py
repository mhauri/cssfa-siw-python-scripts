import sys
from collections import Counter, OrderedDict
import matplotlib.pyplot as plt
import yaml

def read_log_file(log_file):
    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()
            status_codes = []
            for line in lines:
                status_code = line.split()[8]  # Extracting status code from the log line
                status_codes.append(status_code)

            status_code_counts = Counter(status_codes)
            ordered_status_codes = OrderedDict(sorted(status_code_counts.items()))

            # Generate the pie chart
            labels = []
            sizes = []
            for code, count in ordered_status_codes.items():
                labels.append(f"Status Code {code}")
                sizes.append(count)

            # Calculating percentages
            total_requests = sum(sizes)
            percentages = [(count / total_requests) * 100 for count in sizes]

            # Round percentages to two decimals
            rounded_percentages = [round(percent, 2) for percent in percentages]

            # Plotting the pie chart
            plt.figure(figsize=(8, 6))
            plt.pie(sizes, labels=labels, autopct=lambda p: '{:.2f}%'.format(p))
            plt.title('Percentage Share of Status Codes')

            # Save the chart as statuscode.png
            plt.savefig('statuscode.png')
            plt.show()

            # Print ordered list of status codes and their counts
            print("Ordered list of status codes and their counts:")
            status_code_list = []
            for idx, (code, count) in enumerate(ordered_status_codes.items()):
                status_code_list.append({'status_code': f"Status Code {code}", 'count': count, 'percentage': rounded_percentages[idx]})
                print(f"{labels[idx]}: {rounded_percentages[idx]}%")

            # Prepare data for YAML
            status_code_list = []
            for idx, (code, count) in enumerate(ordered_status_codes.items()):
                status_code_data = {
                    int(code): rounded_percentages[idx]
                }
                status_code_list.append(status_code_data)

            # Write ordered key-value pairs to YAML file
            with open('results.yaml', 'w') as yaml_file:
                yaml.dump(status_code_list, yaml_file, default_flow_style=False)

    except FileNotFoundError:
        print("File not found! Please provide a valid file path.")
    except IOError:
        print("Error reading the file. Please check file permissions or path.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the path to the log file as an argument.")
    else:
        log_file_path = sys.argv[1]
        read_log_file(log_file_path)
