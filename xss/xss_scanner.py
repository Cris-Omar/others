#!/usr/bin/env python3
import sys
import requests
###### Configuration ###### set a variable for the xss_test.txt file
xss_test_strings_path = './xss_test.txt'
###########################

###### Argument Parsing ###### Check if there are min. 2 parameters inputs (Url & parameters)
if len(sys.argv) != 3:
  print("[-] Require exactly 2 Parameters.")
  exit()
url = sys.argv[1]
parameters = sys.argv[2].split(",")
###########################

############ Function ######## this function returns a list containing the lines of the file
def load_xss_test_strings(filename):
  with open(filename) as f:
    content = f.readlines() # Reads all the lines from the file and stores them into the variable "content"
  content = [line.strip() for line in content] # Removes Newline-Character
  return content
##########################

########### main function #### If the programm doenst stop because of insuficient parameters, it will be start here with some prints to be sure it is starting..
def main():
  print("[+] Starting Scanner")
  print("[+] Loading XSS Test-Strings")
##############
############## setting variable to take the list of lines from the external file..
  xss_test_strings = load_xss_test_strings(xss_test_strings_path)
############## starting the Test:
  print("[+] Testing for XSS.")
  
  for xss_test_string in xss_test_strings:
    for parameter in parameters:
        
        # create a dictonary to hold parameters
        data = {}
        # the parameter entered by the user is assosiated to the each xss_test_string
        data[parameter] = xss_test_string
        # here the url and parameters are send by POST request aaaand stored in the response variable
        response = requests.post(url, data = data)
        # decoding of the bytes to Unicode String 
        if xss_test_string in response.content.decode("utf-8"): 
          print("[!] XSS Vulnerability in parameter " + parameter + " detected.")
          print("[!] The test string was: " + xss_test_string)
        else:
          print("[+] All good. No XSS Vulnerability in parameter " + parameter + " detected.")
# check if this script is the main programm or not
if __name__ == "__main__":
  main()