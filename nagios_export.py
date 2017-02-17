#!/usr/bin/python
# https://media.readthedocs.org/pdf/pynag/latest/pynag.pdf
# first try to export hosts, will be expanded over the time.

from pynag.Model import Parsers
import os
from tempfile import mkstemp
from shutil import move
from os import remove, close
import re
import time
import pandas as pd
from pandas.io.json import json_normalize

nagios_config = '/usr/local/nagios/etc/nagios.cfg'
nagios_sock = '/usr/local/nagios/var/rw/live.sock'

# Implemented wait for nagios socket
wcount = 0
while not os.path.exists(nagios_sock):
    time.sleep(1)
    wcount +=1
    if wcount >= 60:
        raise SystemExit("Wait timeout exceed {} for socket: {}".format(wcount, nagios_sock))

p = Parsers.Livestatus(livestatus_socket_path=nagios_sock, nagios_cfg_file=nagios_config)

filename = "nagios_export.csv"

if not os.path.isfile(nagios_config):
    raise SystemExit("file: {} does not exist".format(nagios_config))


hosts = p.get_hosts()

jhosts = json_normalize(hosts)
phosts = pd.DataFrame(jhosts)
phosts.to_csv('test.csv', encoding='utf-8')
