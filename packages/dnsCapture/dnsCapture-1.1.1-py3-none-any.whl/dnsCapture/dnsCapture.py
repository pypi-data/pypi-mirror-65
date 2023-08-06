from scapy.all import *
import os
import sys,socket

def credits():
    creds="""Author : Vasilis Manthelas
Python version : 3.8.2(tested)
Version : 0.1"""
    return creds

def help():
    return """HELP
import dnsCapture.__main__ as dnsCapture
1](capture dns requests)
    dns=dnsCapture.DNS_TRAFFIC()
    while True:
        captured=dns.stream('interface',0)
        print(captured)
2](capture dns responses)
    dns=dnsCapture.DNS_TRAFFIC()
    while True:
        captured=dns.stream('interface',1)
        print(captured)
3](CREDITS WITH )
    print(dnsCapture.credits())
"""

class DNS_TRAFFIC(object):
    def __init__(self,display=False):
        self.display=display

    def DNS_req(self,pkt):
        #print(pkt.show())
        if IP in pkt:
            
            src=pkt[IP].src
            dst=pkt[IP].dst
        elif IPv6 in pkt:                
            src=pkt[IPv6].src
            dst=pkt[IPv6].dst
            #pkt.show()
            #pkt.show()
        if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr==0:
            DNS_request=pkt.getlayer(DNS).qd.qname
            data={'src':src,'dst':dst,'url':DNS_request}
            if self.display==False:
                return data
            else:
                print("REQUEST [SOURCE :%s DESTINATION : %s URL : %s"%(src,dst,url))

    def DNS_res(self,pkt):
        if IP in pkt:
            
            src=pkt[IP].src
            dst=pkt[IP].dst
        elif IPv6 in pkt:                
            src=pkt[IPv6].src
            dst=pkt[IPv6].dst
            #pkt.show()
            #pkt.show()
        if pkt.haslayer(DNSRR) and pkt.haslayer(DNS) and pkt.getlayer(DNS).qr==1:
            DNS_request=pkt.getlayer(DNSRR).rrname
            DNS_response=pkt.getlayer(DNSRR).rdata
            data={'src':src,'dst':dst,'url':DNS_request,'response':DNS_response}
            if self.display==False:
                return data
            else:
                print("RESPONSE [SOURCE :%s DESTINATION : %s URL : %s IP : %s"%(src,dst,DNS_request,DNS_response))



    def stream(self,IFACE,Type):
        try:
            #reqT=threading.Thread(target=req)
            #resT=threading.Thread(target=res)
            #reqT.daemon,resT.daemon=True,True
            #reqT.start()
            #resT.start()
            #pkt=sniff(iface='wlan',filter='verion 4 and port 53',prn=D)
            if Type==0:
                pkt_res = sniff(iface=IFACE,filter='port 53',prn=self.DNS_req)
            elif Type==1:
                pkt_res = sniff(iface=IFACE,filter='port 53',prn=self.DNS_res)
        except KeyboardInterrupt:
            sys.exit(1)

    #version 4 and

