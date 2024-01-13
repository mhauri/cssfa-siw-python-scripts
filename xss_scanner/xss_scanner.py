import requests
import sys
from bs4 import BeautifulSoup


def test_xss(url, payloads_file):
    # Read the payloads from the file
    with open(payloads_file, 'r') as f:
        payloads = [line.strip() for line in f]

    # Get the page content
    response = requests.get(url)

    # Create a Beautiful Soup object and find the form
    soup = BeautifulSoup(response.text, 'html.parser')
    forms = soup.find_all('form')

    for form in forms:
        # Find all input fields in the form
        inputs = form.find_all('input')
        fields = [input.get('name') for input in inputs]

        # Get the action attribute of the form (this is the submit URL)
        action = form.get('action')

        for field in fields:
            for payload in payloads:
                r = requests.post(url + action, data={field: payload})

                if payload in r.text:
                    print(f'XSS Vulnerability detected in {field} with payload: {payload}')


if __name__ == "__main__":
    url = sys.argv[1]  # The first command line argument is the URL
    payloads_file = sys.argv[2]  # The second command line argument is the payloads file

    test_xss(url, payloads_file)