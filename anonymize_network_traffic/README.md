# Installation
```commandline
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 
```

# Usage

## Anonymize Network Traffic
```commandline
python3 anonymize.py network_traffic_non_anonymized.pcap
```

## De-Anonymize Network Traffic
```commandline
python3 deanonymize.py network_traffic_non_anonymized.pcap
```