# Lucia Montero Sanchis
# Information Security and Privacy, EPFL 2018

import json
from flask import request

# Implement the hash function
import bcrypt
def get_hash(msg):
    return bcrypt.hashpw(msg.encode('utf-8'), bcrypt.gensalt())

# Implement a simple Flask application
from flask import Flask
app = Flask(__name__) # this is used when using a single module

# decorator tells what URL the function should trigger
@app.route('/hw4/ex2', methods=['POST'])
def hello_world():
    try:
        content = request.get_json()
        return get_hash(content['pass']), 200
    except Exception:
        return traceback.format_exc()

# run the Flask app
if __name__ == "__main__":
    app.run()