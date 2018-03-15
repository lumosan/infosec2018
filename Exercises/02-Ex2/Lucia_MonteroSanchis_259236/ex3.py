# This version does not use 'redirect'

import base64
import json
import hmac
#from flask import after_this_request
from flask import current_app
from flask import Flask
from flask import request
#from flask import redirect
from flask import make_response

# Implement the verification function
def superencryption(msg):
    key = "Never send a human to do a machine's job"
    if (len(key) < len(msg)):
        key = key + key[0:len(msg) - len(key)]
    amsg = map(ord, msg)
    akey = map(ord, key[0:len(msg)])
    y = ''.join([chr(v ^ i) for (i,v) in zip(akey, amsg)])
    return base64.b64encode(y.encode('utf-8'))

key = superencryption('lucia.monterosanchis@epfl.ch')

def check_pwd(username, password):
    return (username=='administrator' and str(password)=='42')

def compute_cookie(username, password, type_):
    fields = ",".join([username, '1489662453', 'com402', 'hw2', 'ex3', type_])
    hmac_obj = hmac.new(key, fields.encode('utf-8'))
    cookie = ",".join([fields, hmac_obj.hexdigest()])
    return base64.b64encode(cookie.encode('utf-8'))

def check_cookie(cookie_64):
    cookie = base64.b64decode(cookie_64)
    split_cookie = cookie.decode('utf-8').split(",")
    fields = ",".join(split_cookie[:6])
    type_ = split_cookie[5]
    hmac_rec = split_cookie[6]

    h = hmac.new(key, fields.encode('utf-8'))
    cookie_ok = hmac.compare_digest(hmac_rec, h.hexdigest())
    is_admin = (type_ == 'administrator')

    return cookie_ok, is_admin

# Implement the Flask server
app = Flask(__name__) # this is used when using a single module

@app.route('/ex3/login', methods=['POST'])
def login_app():
    content = request.get_json()
    username = content['user']
    password = content['pass']
    is_admin = check_pwd(username, password)
    if is_admin:
        cookie = compute_cookie(username, password, 'administrator')
    else:
        cookie = compute_cookie(username, password, 'user')

    response = make_response()
    response.set_cookie('LoginCookie', cookie)
    return response

@app.route('/ex3/list', methods=['POST'])
def list_app():
    cookie = request.cookies.get('LoginCookie')
    cookie_ok, is_admin = check_cookie(cookie)
    if (cookie_ok and is_admin):
        return ':D', 200
    elif cookie_ok:
        return ':)', 201
    else:
        return ':(', 403

# run the Flask app
if __name__ == "__main__":
    app.run()