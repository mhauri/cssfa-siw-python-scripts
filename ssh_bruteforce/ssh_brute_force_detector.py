#!/usr/bin/env python3
import systemd.journal
from collections import defaultdict
import re

def main():
    print("[+] Starting SSH Brute Force Detector.")

    # Create a dictionary to store IP addresses and their corresponding failed login attempts
    failed_attempts = defaultdict(int)

    with systemd.journal.Reader() as journal:
        # seek to the end of the journal to get new entries
        journal.seek_tail()
        journal.get_previous()

        while True:
            try:
                # read and print log entries
                for entry in journal:
                    if 'sshd' in entry.get('SYSLOG_IDENTIFIER', ''):
                        # Check if the log entry indicates a failed login attempt
                        if 'Failed password' in entry.get('MESSAGE', ''):
                            # Extract the IP address from the log entry
                            ip_address = extract_ip_address(entry['MESSAGE'])
                            # Increment the count of failed login attempts for this IP address
                            failed_attempts[ip_address] += 1

                            # If the number of failed attempts from this IP address exceeds a certain threshold, print a warning
                            if failed_attempts[ip_address] > 5:
                                print(f"[!] Detected SSH brute force attack from IP address {ip_address}!")

            except KeyboardInterrupt:
                print("[+] Stopping SSH Brute Force Detector.")
                break


def extract_ip_address(log_message):
  pattern = re.compile(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})')
  match = pattern.search(log_message)
  if match:
    return match.group(0)
  return None


if __name__ == "__main__":
    main()