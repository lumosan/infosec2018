import os
import sys
import populate
from flask import g
from flask import Flask, current_app
from flask import render_template, request, jsonify
import pymysql


app = Flask(__name__)
username = "root"
password = "root"
database = "hw4_ex3"

## This method returns a list of messages in a json format such as
## [
##  { "name": <name>, "message": <message> },
##  { "name": <name>, "message": <message> },
##  ...
## ]
## If this is a POST request and there is a parameter "name" given, then only
## messages of the given name should be returned.
## If the POST parameter is invalid, then the response code must be 500.
@app.route("/messages", methods=["GET","POST"])
def messages():
    with db.cursor() as cursor:
        cursor.execute("SELECT name, message FROM messages")
        res = cursor.fetchall()
        json = [{"name": e[0], "message": e[1]} for e in res]

        if request.method == "POST":
            content = request.args
            if len(content) == 0:
                return jsonify(json), 200
            if len(content) == 1:
                name = content.get("name")
                if name is None:
                    return "", 500
                else:
                    return jsonify([e for e in json if e["name"] == name]), 200
            else:
                return "", 500
        else:
            return jsonify(json), 200

        #cursor.close()


## This method returns the list of users in a json format such as
## { "users": [ <user1>, <user2>, ... ] }
## This methods should limit the number of users if a GET URL parameter is given
## named limit. For example, /users?limit=4 should only return the first four
## users.
## If the parameter given is invalid, then the response code must be 500.
@app.route("/users",methods=["GET"])
def contact():
    with db.cursor() as cursor:
        cursor.execute("SELECT name FROM users")
        res = cursor.fetchall()
        # remove duplicates or not?
        users = list(set([e[0] for e in res]))
        content = request.args

        if len(content) == 0:
            json = {"users": users}
            return jsonify(json), 200
        if len(content) == 1:
            limit = content.get("limit")
            if limit is None:
                return "", 500
            else:
                try:
                    lim = int(limit)
                    if lim >= 0:
                        #what happens if limit larger than nb of users?
                        lim = min(len(users), lim)
                        json = {"users": users[:lim]}
                        return jsonify(json), 200
                    else:
                        return "", 500
                except ValueError:
                    return "", 500
        else:
            return "", 500

        #cursor.close()


if __name__ == "__main__":
    seed = "randomseed"
    if len(sys.argv) == 2:
        seed = sys.argv[1]

    db = pymysql.connect("localhost",
                username,
                password,
                database)
    with db.cursor() as cursor:
        populate.populate_db(seed, cursor)
        db.commit()
    print("[+] database populated")

    app.run(host="0.0.0.0", port=80)