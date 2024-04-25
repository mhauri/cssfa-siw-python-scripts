#!/usr/bin/env python3
import sys
import json
import argparse
from datetime import datetime


def process_logs(access_file, forensics_file):
    with open(access_file, 'r') as access, open(forensics_file, 'r') as forensics:
        # Process forensics log file
        forensics_data = [json.loads(line) for line in forensics]

        # Process access log file
        for l in access:
            try:
                # Process line of access.log file here
                parts = l.split(' ')
                timestamp = datetime.strptime(parts[3][1:], '%d/%m/%Y:%H:%M:%S %z').isoformat()
                request_parts = parts[5][1:].split(' ')
                obj = {
                    'requestId': parts[0],
                    'remoteAddress': parts[1],
                    'timestamp': timestamp,
                    'method': request_parts[0],
                    'url': request_parts[1],
                    'version': request_parts[2][:-1],
                    'responseCode': int(parts[6]),
                    'responseSize': int(parts[7]) if parts[7] != '-' else 0,
                }
                # Match with forensics data
                for entry in forensics_data:
                    if entry['requestId'] == obj['requestId']:
                        # Convert headers into a dictionary of lists
                        entry_headers = {k: [v] for k, v in (h.split(':') for h in entry['headers'].split('\n'))}
                        obj['requestHeaders'] = entry_headers
                        break
                # Write to output.json
                with open('output.json', 'a') as output:
                    output.write(json.dumps(obj) + '\n')
            except Exception as e:
                print(f"Error {e} on line {l}", file=sys.stderr)
                sys.exit(1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process web application log files.')
    parser.add_argument('-a', '--access', help='the acces log file to parse', default='access.log')
    parser.add_argument('-f', '--forensics', help='the forensics log file to parse', default='forensics.json')

    args = parser.parse_args()

    process_logs(args.access, args.forensics)
