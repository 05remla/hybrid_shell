import sys
import struct
from hybrid_shell.hs import stringx as sx
from hybrid_shell.hs import ANSI
import socket
import os
from ipaddress import IPv4Network
from ipaddress import ip_network
from ipaddress import ip_interface
from scapy.all import *
ANSI.init()
cformat = ANSI.format


def boolPing(addr):
    '''
        NEEDS WORK & DOCUMENTATION
        -add compatability for linux
    '''
    zx = sx('ping {} -n 1 -w 2'.format(addr))[0]
    for i in zx:
        if i.lower().startswith('reply from {}'.format(addr)):
            return(True)
    return(False)


def wakeonlan(mac_address, broadcast_address):
    '''
        NEEDS WORK & DOCUMENTATION
    '''
    addr_byte = mac_address.split(':')
    hw_addr = struct.pack(
        'BBBBBB', int(addr_byte[0], 16),
        int(addr_byte[1], 16),
        int(addr_byte[2], 16),
        int(addr_byte[3], 16),
        int(addr_byte[4], 16),
        int(addr_byte[5], 16))

    msg = b'\xff' * 6 + hw_addr * 16
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.sendto(msg, (broadcast_address, 9))
    s.close()


class ip_check:
    '''
            NEEDS WORK & DOCUMENTATION
    '''
    def ip_in_prefix(ip_address, net='data'):
        if (net == 'data'):
            try:
                net = netinfo.data['net']
            except:
                pass

        return(ip_address in [str(ip) for ip in IPv4Network(net)])

    def valid_ip(IP):
        '''
        '''
        def isIPv4(s):
            try: return str(int(s)) == s and 0 <= int(s) <= 255
            except: return False
        def isIPv6(s):
            if len(s) > 4:
                return False
            try:
                return int(s, 16) >= 0 and s[0] != '-'
            except:
                return False
    
        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return(True)
        if IP.count(":") == 7 and all(isIPv6(i) for i in IP.split(":")):
            return(True)
    
        return(False)

data = conf.ifaces
iface_objs = []
for i in list(data.keys()):
    iface_objs.append(data[i])


class netinfo:
    '''
        NEEDS WORK & DOCUMENTATION
        + NetTools.netinfo.config_all() is interactive
        + running NetTools.netinfo.config_all() will attempt
          to extract all (specified) iface relavent data
          and will be stored in NetTools.netinfo.data
    '''
    data = {'ip4': 0, 'snm': 0, 'net': 0, 'mac': 0, 'gw': 0}

    def config_all():
        netinfo.config_iface()
        netinfo.config_ip4_and_snm()
        netinfo.config_iface_indx()
        netinfo.config_gw()
        # del conf
        print('\n')

    def config_iface():
        for i in range(len(iface_objs)):
            print('{}. {} {}'.format(i, iface_objs[i].name, iface_objs[i].ip))

        netinfo.data['obj'] = iface_objs[int(
            input(cformat('{FG_green}enter iface number{ST_reset}: ')))]
        netinfo.data['iface'] = netinfo.data['obj'].name

    def config_ip4_and_snm():
        netinfo.data['ip4'] = netinfo.data['obj'].ip
        netinfo.data['mac'] = netinfo.data['obj'].mac
        net = 0
        if sys.platform == 'win32':
            cidr = sx('powershell (Get-NetIPAddress -IPAddress {}).PrefixLength'.format(netinfo.data['ip4']))[0][0]
            net = '{}/{}'.format(netinfo.data['ip4'], cidr)
        else:
            net_data = sx('ip route')[0]
            for i in net_data:
                if ('link' in i) and (netinfo.data['ip4'] in i):
                    net = i.split()[0]

        if not net == 0:
            netinfo.data['snm'] = str(ip_interface(net).netmask)
            netinfo.data['net'] = net
        #    try:
        #        netinfo.data['net'] = str(ip_network('{}/{}'.format(netinfo.data['ip4'], cidr), strict=False))
        #    except:
        #        pass

    def config_iface_indx():
        '''
            windows specific method
        '''
        if not sys.platform == 'win32':
            return
        netinfo.data['iface_indx'] = netinfo.data['obj'].index
        # obj = powershell Get-NetAdapter -InterfaceIndex XXX

    def config_gw():
        '''
            NEEDS WORK & DOCUMENTATION
        '''    
        # FiX NOT RELIABLE
        # pkt = IP(dst='8.8.8.8', ttl=1, id=RandShort())/TCP(flags=0x2)
        # ans = sr1(pkt, timeout=3, verbose=0)
        # host = 0
        # if not ans == None:
        #     for j in ans[IP]:
        #         host = j[IP].src
        #         break
        # netinfo.data['gw'] = host
        if sys.platform == 'win32':
            data = sx('powershell Get-NetRoute -InterfaceIndex {}'.format(netinfo.data['iface_indx']))[0]
            for i in data:
                if '0.0.0.0/0' in i:
                    netinfo.data['gw'] = i.split()[2]
        else:
            data = sx('ip route')[0]
            for i in data:
                if 'default' in i:
                    data = i.split()
                    break
            netinfo.data['gw'] = data[data.index('via') + 1]


if __name__ == '__main__':
    pass
