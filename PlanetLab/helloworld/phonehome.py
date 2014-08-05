#!/usr/bin/python
### phonehome.py
### Hello World demonstration script

phonehome_url = "http://wpi.xunmu.pw/planetlab_demo/phonehome.php"

import sys, urllib, xmlrpclib, socket

api_server = xmlrpclib.ServerProxy('https://www.planet-lab.org/PLCAPI/')

auth = {}
auth['AuthMethod'] = "anonymous"
auth['Role'] = "user"

hostname = socket.gethostname()
query = api_server.GetNodes(auth,
             {'hostname': hostname}, ['site_id'])
site_id = query[0]['site_id']
site_info = api_server.GetSites(auth,
            {'site_id': site_id}, ['site_id', 'name', 'url',
             'latitude', 'longitude', 'login_base'])
site_info = urllib.urlencode(site_info[0])
urllib.urlopen(phonehome_url, site_info)
