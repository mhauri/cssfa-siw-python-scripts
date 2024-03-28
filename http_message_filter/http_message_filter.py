import pyshark
import base64
import sys

def decode_data(encoded_data, encoding):
    try:
        if encoding == 'base32':
            decoded_data = base64.b32decode(encoded_data)
        elif encoding == 'base64':
            decoded_data = base64.b64decode(encoded_data)
        else:
            print(f'Unsupported encoding: {encoding}')
            return None
        return decoded_data.decode('utf-8')
    except Exception as e:
        return None

def filter_http_messages(pcap_file, encoding):
    pcap = pyshark.FileCapture(pcap_file)
    for pkt in pcap:
        try:
            if 'HTTP' in pkt:
                http_layer = pkt['http']
                if hasattr(http_layer, 'file_data'):
                    encoded_data = http_layer.file_data.replace('\r\n', '')
                    decoded_data = decode_data(encoded_data, encoding)
                    if decoded_data:
                        print(f'Decoded data: {decoded_data}')
        except Exception as e:
            pass

if __name__ == "__main__":
    filter_http_messages(sys.argv[1], sys.argv[2])