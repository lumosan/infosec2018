# 1. Read file
with open("hw3_ex2.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

# 2. Get data for this exercise
ex2c_s = [c.split(", ")[0] for c in content[23:]]
ex2c_p = [c.split(", ")[1] for c in content[23:]]

import string

# 3. Generate set of possible characters
chars = string.digits + string.ascii_lowercase + string.ascii_uppercase

# 4. Load dictionary
import bz2

dictionary = set()
with bz2.open("rockyou.txt.bz2", "rt", encoding="ISO-8859-1") as bz_file:
    for line in bz_file:
        word = line.rstrip()
        if all(char in chars for char in word):
            dictionary.add(word)

# Dictionary to store found passwords
found_pwd = {}

# 6. Iterate through the dictionary
# append all possible salts, then hash and compare to the pwds
import hashlib

for w in dictionary:
    for s in ex2c_s:
        w_s = w+s
        h_w = hashlib.sha256(w_s.encode('utf-8')).hexdigest()
        if h_w in ex2c_p:
            found_pwd[h_w] = w
            print(w)
        if len(found_pwd) >= 10:
            break
    if len(found_pwd) >= 10:
        break

# 7. Save file with the found passwords
f = open('solutions/2c.txt','w')
f.write(found_pwd[ex2c_p[0]])
for k in ex2c_p[1:]:
    f.write(', ')
    f.write(found_pwd[k])
f.close()