# Lucia Montero Sanchis
# 259236

import sys

import binascii
import dpkt

#file_path = 'com402_hw6_ex3_p2.pcap'
file_path = sys.argv[1]

f = open(file_path, 'rb')
pcap = dpkt.pcap.Reader(f)

ip_sent_syn = {}
ip_received_synack = {}

# Iterate through all packets
for ts, buf in pcap:
    eth = dpkt.ethernet.Ethernet(buf)
    ip = eth.data
    tcp = ip.data

    # Get src and dst IP addresses
    ip_src = ip.src
    ip_dst = ip.dst
    eth_src = eth.src
    eth_dst = eth.dst

    # Get SYN and ACK flags
    try:
        syn_flag = (tcp.flags & dpkt.tcp.TH_SYN) != 0
        ack_flag = (tcp.flags & dpkt.tcp.TH_ACK) != 0

        if syn_flag:
            if not ack_flag:
                # Save SYN packets
                if ip_src in ip_sent_syn.keys():
                    ip_sent_syn[ip_src] += 1
                else:
                    ip_sent_syn[ip_src] = 1
            else:
                # Save SYN+ACK packets
                if ip_dst in ip_received_synack.keys():
                    ip_received_synack[ip_dst] += 1
                else:
                    ip_received_synack[ip_dst] = 1
    except AttributeError:
        pass

# Get suspicious IPs
ip_suspicious = []

for src, nb_syn in ip_sent_syn.items():
    if src in ip_received_synack.keys():
        nb_synack = ip_received_synack[src]
        if nb_syn > 3 * nb_synack:
            ip_suspicious.append(src)
    else:
        ip_suspicious.append(src)

# Print solution
for ip_add in ip_suspicious:
    ip_add = str(binascii.hexlify(ip_add))[2:-1]
    num_ip_add = [int(ip_add[i:i+2], 16) for i in range(0, len(ip_add), 2)]
    print('{}.{}.{}.{}'.format(num_ip_add[0], num_ip_add[1], num_ip_add[2], num_ip_add[3]))
