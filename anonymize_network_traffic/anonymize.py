import argparse
import json
import re
from scapy.all import *
from hashlib import sha1

# Regular expression to match email addresses
email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')


# Function to mask email addresses
def mask_email(packet):
    if packet.haslayer(Raw):
        payload = packet[Raw].load.decode(errors='ignore')
        if email_regex.search(payload):
            masked_payload = email_regex.sub("masked@example.com", payload)
            packet[Raw].load = masked_payload.encode()
    return packet


# Function to anonymize IP addresses
def anonymize_ip(packet, ip_mapping):
    if packet.haslayer(IP):
        # Record original source and destination IP addresses
        original_src = packet[IP].src
        original_dst = packet[IP].dst

        # Anonymize source and destination IP addresses
        packet[IP].src = '.'.join(
            str(int(sha1(packet[IP].src.encode()).hexdigest()[i:i + 2], 16)) for i in range(0, 8, 2))
        packet[IP].dst = '.'.join(
            str(int(sha1(packet[IP].dst.encode()).hexdigest()[i:i + 2], 16)) for i in range(0, 8, 2))

        # Record anonymized source and destination IP addresses
        anonymized_src = packet[IP].src
        anonymized_dst = packet[IP].dst

        # Add to IP mapping
        ip_mapping[original_src] = anonymized_src
        ip_mapping[original_dst] = anonymized_dst

    # Mask email addresses in SMTP traffic
    packet = mask_email(packet)

    return packet


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Anonymize a pcap file.")
    parser.add_argument("filename", help="The name of the pcap file to anonymize.")
    args = parser.parse_args()

    # Read packets from pcap file
    packets = rdpcap(args.filename)

    # Dictionary to record original and anonymized IP addresses
    ip_mapping = {}

    # Anonymize IP addresses in packets and mask email addresses
    anonymized_packets = [anonymize_ip(packet, ip_mapping) for packet in packets]

    # Write anonymized packets to a new pcap file
    wrpcap("anonymized_" + args.filename, anonymized_packets)

    # Save IP mapping to a JSON file
    with open("ip_mapping.json", 'w') as f:
        json.dump(ip_mapping, f)


if __name__ == "__main__":
    main()