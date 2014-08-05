#!/usr/bin/env python
# Script to get a list of live nodes on PlanetLab.
# Root privilege is required to run ping.
#
#    sudo python hostlist.py
#
# By chenxm
# 2014-08

import sys
import xmlrpclib
import intds # https://github.com/caesar0301/intds
import ping
import socket

if len(sys.argv) < 3:
    print("Usage: hostlist.py <username> <passwd>")
    sys.exit(-1)

username = sys.argv[1]
passwd = sys.argv[2]

api_server = xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/',
                                   allow_none=True)
## print api_server.system.methodSignature('AuthCheck')

## Authentication. Create an empty XML-RPC struct
auth = {}
# Specify password authentication
auth['AuthMethod'] = 'password'
auth['Username'] = username
auth['AuthString'] = passwd
authorized = api_server.AuthCheck(auth)
if authorized:
    print('We are authorized!')
else:
    print('Authorization failed! Exit.')
    sys.exit(-1)

## Obtain a list of boot nodes
boot_state_filter = {'boot_state': 'boot'}
return_fields = ['node_id', 'hostname', 'node_type']
nodes_in_boot = api_server.GetNodes(auth, boot_state_filter, return_fields)

## Order boot list with domain suffixes
ids = intds.intds()
ofile = open('boot_nodes.txt', 'wb')
nodes_in_boot = sorted(nodes_in_boot,
                       key=lambda x: x['hostname'].rsplit('.', 1)[-1])

## Output boot list
for node in nodes_in_boot:
    nid = node['node_id']
    hostname = node['hostname']
    info = ids.host_info(hostname)
    try:
        latency = ping.do_one(hostname, 5)
    except socket.gaierror:
        latency = None
    if not latency:
        latency = "-1"
    print("%s,%s,%s" % (hostname, info['country'], str(latency)))
    ofile.write('%s,%s,%s,%s\n' % (nid, hostname,
                                   info['country'],
                                   str(latency)))
ofile.close()
