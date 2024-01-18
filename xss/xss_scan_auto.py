#!/usr/bin/env python3
import sys
import requests
from bs4 import BeautifulSoup

###### Configuration ###### set a variable for the xss_test.txt file
xss_test_strings_path = './xss_test.txt'
###########################

###### Argument Parsing ###### Check if there are min. 1 parameters input (Url)
if len(sys.argv) != 2:
    print("[-] Require exactly 1 Parameter (URL).")
    exit()

url = sys.argv[1]
#############

############ Function ######## this function returns a list containing the lines of the file
def load_xss_test_strings(filename):
    with open(filename) as f:
      content = f.readlines() # Reads all the lines from the file and stores them into the variable "content"
    content = [line.strip() for line in content] # Removes Newline-Character
    return content
##########################

### function to dynamically extract the parameters:
def extract_parameters_from_url(url):
    try:
        #send http GET request to the "url"
        response = requests.get(url)
        # Check if the request was successful
        response.raise_for_status()
        #parse response
        soup = BeautifulSoup(response.content, 'html.parser')
        #find all name attributes and extract their value..
        parameters = [param["name"] for param in soup.find_all('input', {'name': True})]
        #return list of parameters
        return parameters
    #error handling:
    except requests.RequestException as e:
        # If an exception occurs during the request (e.g., network issues), print an error message
        print(f"Error: {e}")
        #exit code with non zero status to indicate an error
        sys.exit(1)
#####################################################

########### main function #### If the programm doenst stop because of insuficient parameters, it will be start here with some prints to be sure it is starting..
def main():
    print("[+] Starting Scanner")
    print("[+] Extracting Parameters from the URL")
    ############## setting variable to take the the parameters of the "extract_parameters_from_url" function
    parameters = extract_parameters_from_url(url)

    print("[+] Loading XSS Test-Strings")
    ############## setting variable to take the list of lines from the external file..
    xss_test_strings = load_xss_test_strings(xss_test_strings_path)

    print("[+] Testing for XSS.")
    for xss_test_string in xss_test_strings:
        for parameter in parameters:
            # create a dictonary to hold parameters
            data = {}
            # the parameter entered by the user is assosiated to the each xss_test_string
            data[parameter] = xss_test_string
            # here the url and parameters are send by POST request aaaand stored in the response variable
            response = requests.post(url, data=data)

            # decoding of the bytes to Unicode String 
            if xss_test_string in response.content.decode("utf-8"):
                print("[!] XSS Vulnerability in parameter " + parameter + " detected.")
                print("[!] The test string was: " + xss_test_string)
            else:
                print("[+] All good. No XSS Vulnerability in parameter " + parameter + " detected.")

# check if this script is the main programm or not
if __name__ == "__main__":
    main()