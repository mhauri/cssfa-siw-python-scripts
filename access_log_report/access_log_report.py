import collections
import matplotlib.pyplot as plt
import yaml
import sys


# Function to parse the log file and count HTTP status codes
def parse_log_file(log_file):
    try:
        with open(log_file, 'r') as f:
            # Initialize a counter for status codes
            status_code_counter = collections.Counter()

            # Process each line in the log file
            for line in f:
                try:
                    # Split the line to extract the status code (9th element)
                    parts = line.split()
                    status_code = parts[8]
                    # Increment the counter for the status code
                    status_code_counter[status_code] += 1
                except IndexError:
                    print(f"Error parsing line: {line}")
                    continue

            return status_code_counter
    except FileNotFoundError:
        print(f"Error: Log file {log_file} not found.")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


# Function to save results as YAML
def save_results_as_yaml(status_code_counter, yaml_file):
    sorted_status_code_list = sorted(status_code_counter.items())

    with open(yaml_file, 'w') as f:
        yaml.dump(dict(sorted_status_code_list), f, default_flow_style=False)
    print(f"Results saved to {yaml_file}")


# Function to generate a pie chart of status codes
def generate_pie_chart(status_code_counter, image_file):
    labels = []
    sizes = []

    # Prepare labels and sizes for the pie chart
    total_count = sum(status_code_counter.values())
    for status, count in status_code_counter.items():
        labels.append(f"{status} ({count / total_count:.2%})")
        sizes.append(count)

    # Create a pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.2f%%', startangle=90)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the pie chart as an image
    plt.savefig(image_file)
    plt.close()
    print(f"Pie chart saved to {image_file}")


# Main function to execute the entire process
def main():
    if len(sys.argv) < 2:
        print("Usage: python access_log_report.py <log_file>")
        sys.exit(1)

    log_file = sys.argv[1]
    yaml_output = 'results.yml'
    image_output = 'statuscode.png'

    # Parse the log file
    status_code_counter = parse_log_file(log_file)

    if status_code_counter:
        # Save results as YAML
        save_results_as_yaml(status_code_counter, yaml_output)

        # Generate pie chart
        generate_pie_chart(status_code_counter, image_output)


if __name__ == "__main__":
    main()
