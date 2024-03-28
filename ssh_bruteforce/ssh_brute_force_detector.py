#!/usr/bin/env python3
import systemd.journal
from collections import defaultdict
import re
import time


def main():
    TRESHOLD = 2
    RELAX_AFTER_SECONDS = 10

    print("[+] Starting SSH Brute Force Detector.")

    # Create a dictionary to store IP addresses and their corresponding failed login attempts and the time of the last attempt
    failed_attempts = defaultdict(lambda: {'count': 0, 'time': time.time()})

    with systemd.journal.Reader() as journal:
        # seek to the end of the journal to get new entries
        journal.seek_tail()
        journal.get_previous()

        while True:
            try:
                for entry in journal:
                    if 'sshd' in entry.get('SYSLOG_IDENTIFIER', ''):
                        if 'Failed password' in entry.get('MESSAGE', ''):
                            ip_address = extract_ip_address(entry['MESSAGE'])

                            # Check if more than 10 seconds have passed since the last failed attempt
                            if time.time() - failed_attempts[ip_address]['time'] > RELAX_AFTER_SECONDS:
                                failed_attempts[ip_address]['count'] = 0

                            failed_attempts[ip_address]['count'] += 1
                            failed_attempts[ip_address]['time'] = time.time()


                            print(failed_attempts)
                            if failed_attempts[ip_address]['count'] > TRESHOLD:
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