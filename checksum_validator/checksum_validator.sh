#!/bin/bash

# File containing checksums and file paths
file_list=$1

# Check if file list is provided
if [ -z "$file_list" ]; then
    echo "Please provide a file list as a parameter."
    exit 1
fi

# Check if file list exists
if [ ! -f "$file_list" ]; then
    echo "File $file_list does not exist."
    exit 1
fi

# Read each line of the file
while read -r line; do
    # Split the line into checksum and file path
    checksum=$(echo $line | cut -d ' ' -f 1)
    file_path=$(echo $line | cut -d ' ' -f 2-)

    if [ ! -f "$file_path" ]; then
        echo "File $file_path does not exist."
        continue
    fi

    # Calculate the checksum of the file
    calculated_checksum=$(sha1sum "$file_path" | cut -d ' ' -f 1)

    if [ "$calculated_checksum" == "$checksum" ]; then
        echo "Checksum for $file_path is VALID."
    else
        echo "Checksum for $file_path is INVALID. Calculated: $calculated_checksum, Expected: $checksum"
    fi
done < "$file_list"