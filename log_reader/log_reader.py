import sys
from collections import Counter, OrderedDict
import matplotlib.pyplot as plot

chart_colors = [
    '#1f77b4',
    '#ff7f0e',
    '#2ca02c',
    '#d62728',
    '#9467bd',
    '#8c564b',
    '#e377c2',
    '#7f7f7f',
    '#bcbd22',
    '#17becf',
    '#aec7e8',
    '#ffbb78'
]

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
            plot.figure(figsize=(8, 8))
            plot.pie(sizes, colors=chart_colors, labels=labels, autopct=lambda p: '{:.2f}%'.format(p))
            plot.title('Percentage Share of Status Codes')

            # Save the chart as statuscode.png
            plot.savefig('statuscode.png')
            plot.show()

            # Print ordered list of status codes and their counts
            print("Ordered list of status codes and their counts:")
            for idx, (code, count) in enumerate(ordered_status_codes.items()):
                print(f"{labels[idx]}: {rounded_percentages[idx]}%")
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
