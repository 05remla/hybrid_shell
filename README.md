# hybrid_shell
Python library for common system shell (cmd, powershell, bash) functions (plus extra)

Required python packages:
scapy (scapy is required for net_tools)

library utility/examples:
net_tools
+ running net_tools.netinfo.config_all() will populate/initialize net_tools.netinfo.data
+ example net_tools.netinfo.data output (once initialized):
  {'ip4': '192.168.45.185', 'snm': '255.255.255.0', 'net': '192.168.45.0/24', 'mac': 'xx:xx:xx:xx:xx:xx', 'gw': '192.168.45.190', 'obj': <NetworkInterface wlp2s0 [UP+BROADCAST+RUNNING+MULTICAST+LOWER_UP]>, 'iface': 'wlp2s0'} 
