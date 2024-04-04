import argparse
import json
from scapy.all import *

def de_anonymize_ip(packet, ip_mapping):
    if packet.haslayer(IP):
        # De-anonymize source and destination IP addresses
        for original_ip, anonymized_ip in ip_mapping.items():
            if packet[IP].src == anonymized_ip:
                packet[IP].src = original_ip
            if packet[IP].dst == anonymized_ip:
                packet[IP].dst = original_ip

    return packet

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="De-anonymize a pcap file.")
    parser.add_argument("filename", help="The name of the pcap file to de-anonymize.")
    args = parser.parse_args()

    # Read IP mapping from a JSON file
    with open("ip_mapping.json", 'r') as f:
        ip_mapping = json.load(f)

    # Read packets from pcap file
    packets = rdpcap(args.filename)

    # De-anonymize IP addresses in packets
    de_anonymized_packets = [de_anonymize_ip(packet, ip_mapping) for packet in packets]

    # Write de-anonymized packets to a new pcap file
    wrpcap("de_anonymized_" + args.filename, de_anonymized_packets)

if __name__ == "__main__":
    main()