# Implement the pwd encryption function
import asyncio
import websockets
import binascii
import base64
import hashlib

def superencryption(msg):
    key = "Never send a human to do a machine's job"
    if (len(key) < len(msg)):
        key = key + key[0:len(msg) - len(key)]
    amsg = map(ord, msg)
    akey = map(ord, key[0:len(msg)])
    y = ''.join([chr(v ^ i) for (i,v) in zip(akey, amsg)])
    return base64.b64encode(y.encode('utf8'))

U = b'lucia.monterosanchis@epfl.ch'
p = superencryption(U.decode())

# provided functions to encode and decode an integer
# (used for all numbers A, B, salt)
def encoding(i):
    """int to str"""
    buff = i.to_bytes((i.bit_length() + 7) // 8, 'big')
    str_to_send = binascii.hexlify(buff).decode()
    return str_to_send

def decoding(msg_received):
    """str to int"""
    buff = binascii.unhexlify(msg_received)
    i = int.from_bytes(buff, 'big')
    return i

# ----

def int2bytes(i):
    """int to bytes"""
    buff = i.to_bytes((i.bit_length() + 7) // 8, 'big')
    return buff

def bytes2str(buff):
    """bytes to str"""
    return binascii.hexlify(buff).decode()

def str2bytes(i):
    """str to bytes"""
    buff = binascii.unhexlify(i)
    return buff

def bytes2int(buff):
    """bytes to int"""
    return int.from_bytes(buff, 'big')

# parameters
def H(x):
    assert(type(x) == bytes)
    hash_object = hashlib.sha256(x)
    hex_dig = hash_object.hexdigest()
    return str2bytes(hex_dig)

channel_str = "ws://com402.epfl.ch/hw2/ws"

# create websocket client
async def hello():
    async with websockets.connect(channel_str) as websocket:
        await websocket.send(U.decode())

        # define parameters
        N_str = ("EEAF0AB9ADB38DD69C33F80AFA8FC5E86072618775FF3C0B9EA2314C9C2"
            "56576D674DF7496EA81D3383B4813D692C6E0E0D5D8E250B98BE48E495C"
            "1D6089DAD15DC7D7B46154D6B6CE8EF4AD69B15D4982559B297BCF1885C"
            "529F566660E57EC68EDBC3C05726CC02FD4CBF4976EAA9AFD5138FE8376"
            "435B9FC61D2FC0EB06E3")
        N_int = int(N_str, 16)
        g_int = 2

        s_rec = await websocket.recv()
        s_int = decoding(s_rec)
        print("{} = {}".format("s", s_int))

        a_int = 65476
        A_int = pow(g_int, a_int, N_int)
        A_rec = encoding(A_int)
        await websocket.send(A_rec)
        print("{} = {}".format("A", A_int))

        B_rec = await websocket.recv()
        B_int = decoding(B_rec)
        print("{} = {}".format("B", B_int))

        u = H(int2bytes(A_int) + int2bytes(B_int))
        print('u = {}'.format(bytes2int(u)))
        x = H(str2bytes(s_rec) + H(U + b":" + p))
        print('x = {}'.format(bytes2int(x)))
        S_int = pow(B_int - pow(g_int, bytes2int(x), N_int),
            a_int + bytes2int(u) * bytes2int(x), N_int)

        final_msg = bytes2str(H(str2bytes(A_rec) +
            str2bytes(B_rec) + int2bytes(S_int)))
        await websocket.send(final_msg)

        token = await websocket.recv()
        print()
        print(token)

asyncio.get_event_loop().run_until_complete(hello())