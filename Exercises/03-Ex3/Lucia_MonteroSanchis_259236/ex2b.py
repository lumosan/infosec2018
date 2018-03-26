# 1. Read file
with open("hw3_ex2.txt") as f:
    content = f.readlines()
# you may also want to remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]

# 2. Get strings for this exercise
ex2b = content[12:22]

import string

# 3. Generate set of possible characters
chars = string.digits + string.ascii_lowercase + string.ascii_uppercase

# 4. Define rules
def change(string, nb):
    if nb == 0:
        return string.title()
    elif nb == 1:
        return string.replace("e", "3").replace("E", "3")
    elif nb == 2:
        return string.replace("o", "0").replace("O", "0")
    else:
        return string.replace("i", "1").replace("I", "1")

# Dictionary to store found passwords
found_pwd = {}

# 5. Load dictionary
import bz2

dictionary = set()
with bz2.open("rockyou.txt.bz2", "rt", encoding="ISO-8859-1") as bz_file:
    for line in bz_file:
        word = line.rstrip()
        if all(char in chars for char in word):
            dictionary.add(word)

# 6. Iterate through the dictionary, applying all possible modifications
import hashlib

for w in dictionary:
    for w_0 in [w, change(w, 0)]:
        for w_1 in [w_0, change(w_0, 1)]:
            for w_2 in [w_1, change(w_1, 2)]:
                for w_3 in [w_2, change(w_2, 3)]:
                    # check if w_3 is in passwords
                    h_w = hashlib.sha256(w_3.encode('utf-8')).hexdigest()
                    if h_w in ex2b:
                        found_pwd[h_w] = w_3
                        print(w_3)
                    if len(found_pwd) >= 10:
                        break
                if len(found_pwd) >= 10:
                    break
            if len(found_pwd) >= 10:
                break
        if len(found_pwd) >= 10:
            break
    if len(found_pwd) >= 10:
        break

# 7. Save file with the found passwords
f = open('solutions/2b.txt','w')
f.write(found_pwd[ex2b[0]])
for k in ex2b[1:]:
    f.write(', ')
    f.write(found_pwd[k])
f.close()
