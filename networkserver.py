#!/usr/bin/env python

"""networkserver.py: Script to launch the network server."""

__author__      = "Konstantinos Sideris"
__copyright__   = "Copyright 2012, UCLA game lab"

from game.network.server import Server

print 'Server launched at: ','192.168.130.1:80'
Server().start('192.168.1.102','80')


