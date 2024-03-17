import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import re

# Silence warnings about not verifying Burp's CA certificate.
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

s = requests.session()  # Session object for settings persistence
s.verify = False  # Skip TLS verification due to Burp's CA
s.proxies = {
    "https": "http://127.0.0.1:8080",
    "http": "http://127.0.0.1:8080",
}  # Proxy requests through Burp

url = "http://haas.quoccabank.com"

# Initial GET request
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "http://haas.quoccabank.com/",
}
get_request = "GET /calculator HTTP/1.1\r\n"
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

# Extract cookie from the initial response
cookie_pattern = r"Set-Cookie: session=(.*?);"
cookie_match = re.search(cookie_pattern, response.text)
if cookie_match:
    cookie = cookie_match.group(1)
else:
    print("Cookie not found in initial response!")
    exit()

# Subsequent POST requests with answer-based content-length and updated cookie
while True:
    answer = input("Silahkan masukkan answer: ")

    content_length = 8  # Default for 1-digit answer
    if len(answer) == 2:
        content_length = 9
    elif len(answer) == 3:
        content_length = 10

    got_request = "POST /calculator HTTP/1.1\r\n"
    got_request += "Host: kb.quoccabank.com\r\n"
    got_request += "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r\n"
    got_request += "Accept-Language: en-US,en;q=0.5\r\n"
    got_request += "Referer: http://haas.quoccabank.com\r\n"
    got_request += "Content-Type: application/x-www-form-urlencoded\n"
    got_request += f"Content-Length: {content_length}\r\n"

    # Use response.text for the first request and responses.text for subsequent requests
    got_request += f"Cookie: session={cookie}\r\n"
    got_request += "Origin: http://haas.quoccabank.com\r\n"
    got_request += "Connection: keep-alive\r\n\r\n"
    got_request += f"answer={answer}"
    data = {"requestBox": got_request}
    responses = s.post(url, headers=headers, data=data)
    print(responses.text)
    if responses is None:
        cookie_match = re.search(cookie_pattern, response.text)
    else:
        cookie_match = re.search(cookie_pattern, responses.text)

    if cookie_match:
        cookie = cookie_match.group(1)
    else:
        print("Cookie not found in response!")
        exit()

