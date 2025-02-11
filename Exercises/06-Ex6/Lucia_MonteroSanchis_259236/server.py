# Lucia Montero Sanchis
# 259236


#!/usr/bin/env python3

import sys
import socket
import threading
import binascii

from Crypto import Random
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

PRIMARY_SERVER_ID = 0

RSA_MODULUS_SIZE = 1024

AES_IV_SIZE = AES.block_size
AES_MODE = AES.MODE_CBC

CHAT_MSG_INDEX_SIZE = 20
CHAT_MSG_BODY_SIZE = 44

UDP_RECV_TIMEOUT = 10


class RiffleServer:

    # Server id - determines the order of onion decryption
    server_id = None

    server_ip = None
    udp_port = None
    udp_socket = None

    # Dictionary of all servers, key is server_id and value is (ip, port) pair
    all_servers = None

    # Public/Private RSA key pair
    rsa_key_pair = None

    # AES key shared with the client which will send all the chat messages
    client_shared_key = None

    # Dictionary of chat messages, key is message index and value is msg itself
    chat_messages = None

    def __init__(self, server_id, server_ip, udp_port, all_servers):

        self.server_id = server_id
        self.server_ip = server_ip
        self.udp_port = udp_port
        self.all_servers = all_servers
        self.rsa_key_pair = RSA.generate(RSA_MODULUS_SIZE)

        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((server_ip, udp_port))
        self.udp_socket.settimeout(UDP_RECV_TIMEOUT)

        self.chat_messages = dict()

    # Method expects skey_encrypted as a hex-string, which unhexlified
    # represents the RSA encryption (with our pub key) of the client shared key
    # Decrypt it and store as client_shared_key
    def recv_client_shared_key(self, skey_encrypted):
        self.client_shared_key = self.rsa_key_pair.decrypt(
            binascii.unhexlify(skey_encrypted.encode()))


    # Receive a chat message from the client, only the primary server
    # should receive this message. The message is onion-encrypted,
    # primary server should start the onion-decryption process.
    # So, primary server should decrypt the message with the client_shared_key
    # and send result to the next server in chain.
    # Method expects msg_encrypted as a hex-string, which unhexlified
    # respresents the AES onion-encrypted chat message
    def recv_chat_msg_client(self, msg_encrypted):

        # Only primary server should receive/process
        # a chat message from a client
        if self.server_id != PRIMARY_SERVER_ID:
            return

        # Remove one layer of encryption
        msg = binascii.unhexlify(msg_encrypted.encode())
        iv = msg[:AES_IV_SIZE]
        m = msg[AES_IV_SIZE:]
        cipher = AES.new(self.client_shared_key, AES_MODE, iv)
        msg = cipher.decrypt(m)

        # If there is next server send the decrypted message to it,
        # else this is the only server and just store the message
        if len(self.all_servers.keys()) == 1:
            msg = msg.decode()
            # Store the message
            msg_idx = int(msg[:CHAT_MSG_INDEX_SIZE])
            self.chat_messages[msg_idx] = msg[CHAT_MSG_INDEX_SIZE:]
            #self.chat_messages[msg_idx] = msg
        else:
            msg_to_send = binascii.hexlify(msg)
            # Send the decrypted message
            next_server_id = self.server_id + 1
            self.udp_socket.sendto((('chat_msg_server ').encode() + msg_to_send),
                self.all_servers[next_server_id])


    # Receive a chat message from another server (the previous server in the chain)
    def recv_chat_msg_server(self, msg_encrypted, sender):

        # Check if the message is sent by the previous server in the chain
        # If not, ignore the messsage
        if self.all_servers[self.server_id - 1] != sender:
            return

        # Remove one layer of encryption
        msg = binascii.unhexlify(msg_encrypted.encode())
        iv = msg[:AES_IV_SIZE]
        m = msg[AES_IV_SIZE:]
        cipher = AES.new(self.client_shared_key, AES_MODE, iv)
        msg = cipher.decrypt(m)

        # If there is next server send the decrypted message to it,
        # else this is the last server, store the message and broadcast it
        next_server_id = self.server_id + 1
        if next_server_id in self.all_servers.keys():
            msg_to_send = binascii.hexlify(msg)
            # Send the decrypted message
            self.udp_socket.sendto((('chat_msg_server ').encode() + msg_to_send),
                self.all_servers[next_server_id])

        else:
            msg = msg.decode()
            # Store the message
            msg_idx = int(msg[:CHAT_MSG_INDEX_SIZE])
            self.chat_messages[msg_idx] = msg[CHAT_MSG_INDEX_SIZE:]
            #self.chat_messages[msg_idx] = msg

            # Broadcast message
            for s_id in self.all_servers.keys():
                if s_id != self.server_id:
                    self.udp_socket.sendto((('chat_msg_plain ').encode() + msg.encode()),
                        self.all_servers[s_id])


    # Receive the plain-text chat message. This happens when the last server
    # in the chain onion-decrypts a message from a client and thus obtains
    # the plain-text message which is then broadcasted to all servers.
    # So, this method should just store the message
    def recv_chat_msg_plain(self, msg):

        # Store the message
        msg_idx = int(msg[:CHAT_MSG_INDEX_SIZE])
        self.chat_messages[msg_idx] = msg[CHAT_MSG_INDEX_SIZE:]
        #self.chat_messages[msg_idx] = msg


    # Process the PIR request from a client. Bitmask has _n_ bits,
    # where _n_ is the number of chat messages. Each bit _j_ in the bitmask
    # corresponds to the chat message with index _j_. If _j_ is set to 1,
    # the message with this index is 'selected'.
    # XOR all messages selected by the bitmask and send the result back
    def process_pir_request(self, bitmask, sender):

        result = b''
        selected_msgs = []

        mask = "{0:b}".format(bitmask)
        mask_bin = '0' * (len(self.chat_messages) - len(mask)) + mask

        #print(self.server_id, bitmask)
        #print(self.chat_messages)

        for idx, bit in enumerate(reversed(mask_bin)):
            if bit == '1':
                selected_msgs.append(self.chat_messages[idx])
            else:
                pass

        if len(selected_msgs):
            result = int(binascii.hexlify(selected_msgs[0].encode()), base=16)

            for s_m in selected_msgs[1:]:
                result = result ^ int(binascii.hexlify(s_m.encode()), base=16)

            result_hex = hex(result)[2:]
            if len(result_hex) % 2:
                result_hex = '0' + result_hex

            result = binascii.unhexlify(result_hex)

        else:
            result = b''

        # print(self.server_id, result)

        # type(result) = <class 'bytes'> in Python3
        self.udp_socket.sendto(result, sender)


    # Method which runs in a thread
    def run(self):

        print('Server', self.server_id, 'starts...')

        while(True):

            # Server will listen on the assigned port and wait for a message
            # If no message is received for more than the timeout time,
            # which is set in the init method, exception will be raised,
            # and thread will stop.
            try:
                message, sender = self.udp_socket.recvfrom(4096)
            except socket.timeout:
                print('Server %d udp-receive timedout' % self.server_id)
                break

            # Received message is of type bytes, so we decode it to get string
            message = message.decode()

            # Message format: op_code body
            op_code = message.split()[0]
            print('Server', self.server_id, 'received op_code:', op_code)

            if op_code == 'pubkey_req':
                # Request for server's RSA public key
                # Just export pubkey and send it back to the sender
                pub_key = self.rsa_key_pair.publickey().exportKey()
                self.udp_socket.sendto(pub_key, sender)

            elif op_code == 'shared_key':
                # Client sends an encrypted shared key
                shared_key = message.split(' ', 1)[1]
                self.recv_client_shared_key(shared_key)

            elif op_code == 'chat_msg_client':
                # Client sends an onion-encrypted chat message
                chat_msg = message.split(' ', 1)[1]
                self.recv_chat_msg_client(chat_msg)

            elif op_code == 'chat_msg_server':
                # Previous server sends an onion-encrypted chat message
                chat_msg = message.split(' ', 1)[1]
                self.recv_chat_msg_server(chat_msg, sender)

            elif op_code == 'chat_msg_plain':
                # Last servers server sends a plain-text chat message
                chat_msg = message.split(' ', 1)[1]
                self.recv_chat_msg_plain(chat_msg)

            elif op_code == 'pir_req':
                # Client sends PIR request
                bitmask = int(message.split(' ', 1)[1])
                self.process_pir_request(bitmask, sender)

            elif op_code == 'quit':
                print('Server', self.server_id, 'quiting...')
                break

            else:
                err_msg = 'Op_code %s not supported' % op_code
                self.udp_socket.sendto(err_msg.encode(), sender)

def read_server_data():

    # Read data about the servers from a file
    servers_filename = 'all_servers.txt'

    all_servers = dict()
    with open(servers_filename, 'r') as fp:

        for line in fp.readlines():
            server_id = int(line.split()[0])
            server_ip = line.split()[1]
            udp_port  = int(line.split()[2])

            all_servers[server_id] = (server_ip, udp_port)

    return all_servers


def main():

    all_servers = read_server_data()

    # Create RiffleServers and run each one in a separate thread
    server_threads = []
    for server_id, (server_ip, udp_port) in all_servers.items():

        ser = RiffleServer(server_id, server_ip, udp_port, all_servers)
        server_threads.append(threading.Thread(target=ser.run))
        server_threads[-1].start()

    for thr in server_threads:
        thr.join()


if __name__ == '__main__':
    main()
