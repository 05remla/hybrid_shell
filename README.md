# hybrid_shell
**Description:**
Python library for common operating system shell (cmd, powershell, bash) functions (plus extra)

**Required python packages:** \n
scapy (scapy is required for net_tools module)

**Python packages utilized (site-packages):** \n
shutil
os
time
pathlib
math
sys
base64
struct
socket
ipaddress

**library utility/examples:** 
**hs**
- easily color output with hybrid_shell.hs.ANSI
  '{}this is blue text.{}'.format(ANSI.COLOR['FG_blue'], ANSI.COLOR['ST_reset'])
  -or-
  cformat('{BG_red}the background is red{ST_reset}')

**net_tools**
- running net_tools.netinfo.config_all() will populate/initialize net_tools.netinfo.data
- example net_tools.netinfo.data output (once initialized): {'ip4': '192.168.45.185', 'snm': '255.255.255.0', 'net': '192.168.45.0/24', 'mac': 'xx:xx:xx:xx:xx:xx', 'gw': '192.168.45.190', 'obj': <NetworkInterface wlp2s0 [UP+BROADCAST+RUNNING+MULTICAST+LOWER_UP]>, 'iface': 'wlp2s0'}
