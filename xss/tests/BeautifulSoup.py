#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup

url = sys.argv[1]

### function to dynamically extract the parameters:
def extract_parameters_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')
        parameters = [param["name"] for param in soup.find_all('input', {'name': True})]
        return parameters
    except requests.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)
#####################################################

def main():
    print("[+] Starting main function, next parameters should be printed out..")
    parameters = extract_parameters_from_url(url)
    print(parameters)
    print("[+] The End.")

if __name__ == "__main__":
    main()
