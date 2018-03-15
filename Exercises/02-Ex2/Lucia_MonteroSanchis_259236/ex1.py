import base64
import json
from flask import request

# Implement the verification function
def superencryption(msg):
    key = "Never send a human to do a machine's job"
    if (len(key) < len(msg)):
        key = key + key[0:len(msg) - len(key)]
    amsg = map(ord, msg)
    akey = map(ord, key[0:len(msg)])
    y = ''.join([chr(v ^ i) for (i,v) in zip(akey, amsg)])
    return base64.b64encode(y.encode('ascii'))

def check_pwd(username, password):
    enc = superencryption(username)
    return enc == password.encode('ascii')


# Implement a simple Flask application
from flask import Flask
app = Flask(__name__) # this is used when using a single module

# decorator tells what URL the function should trigger
@app.route('/hw2/ex1', methods=['POST'])
def hello_world():
    try:
        content = request.get_json()
        res = check_pwd(content['user'], content['pass'])
        if res:
            # correct
            return ':)', 200
        else:
            # incorrect
            return ':(', 400
    except Exception:
        return traceback.format_exc()

# run the Flask app
if __name__ == "__main__":
    app.run()