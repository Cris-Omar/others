#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup

xss_test_strings_path = './xss_test.txt'

if len(sys.argv) != 2:
    print("[-] Require exactly 1 Parameter (URL).")
    exit()

url = sys.argv[1]

def load_xss_test_strings(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [line.strip() for line in content]    # Removes Newline-Character
    return content



### function to dynamically extract the parameters:
def extract_parameters_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract parameters from query string
    parameters = [param["name"] for param in soup.find_all('input', {'name': True})]

    return parameters
#####################################################



def main():
    print("[+] Starting Scanner")
    print("[+] Extracting Parameters from the URL")

    parameters = extract_parameters_from_url(url)

    print("[+] Loading XSS Test-Strings")
    xss_test_strings = load_xss_test_strings(xss_test_strings_path)

    print("[+] Testing for XSS.")
    for xss_test_string in xss_test_strings:
        for parameter in parameters:
            # add parameters
            data = {}
            data[parameter] = xss_test_string
            response = requests.post(url, data=data)

            # parsing the response
            if xss_test_string in response.content.decode("utf-8"):
                print("[!] XSS Vulnerability in parameter " + parameter + " detected.")
                print("[!] The test string was: " + xss_test_string)
            else:
                print("[+] All good. No XSS Vulnerability in parameter " + parameter + " detected.")

if __name__ == "__main__":
    main()
