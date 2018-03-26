# Read file
with open("hw3_ex2.txt") as f:
    content = f.readlines()

# remove whitespace characters at the end of each line
content = [x.strip() for x in content]

# Get strings for this exercise
ex2a = content[1:11]

import string

# Generate set of possible characters
chars = string.digits + string.ascii_lowercase

import itertools
import hashlib

# Dictionary to store the found passwords
found_pwd = {}

# Check all possible combinations of characters
for length in range(4,7):
    for w in map(''.join, itertools.product(*[chars]*length)):
        # get hash
        hashed_w = hashlib.sha256(w.encode('utf-8')).hexdigest()
        # compare
        if hashed_w in ex2a:
            found_pwd[hashed_w] = w
            print(w)
        if len(found_pwd) >= 10:
            break
    if len(found_pwd) >= 10:
        break

# Save file with the found passwords
f = open('solutions/2a.txt','w')
f.write(found_pwd[ex2a[0]])
for k in ex2a[1:]:
    f.write(', ')
    f.write(found_pwd[k])
f.close()