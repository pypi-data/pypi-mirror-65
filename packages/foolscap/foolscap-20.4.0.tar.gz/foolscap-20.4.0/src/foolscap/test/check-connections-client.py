#! /usr/bin/python
from __future__ import print_function

# This is the client side of a manual test for the socks/tor
# connection-handler code. To use it, first set up the server as described in
# the other file, then copy the hostname, tubid, and .onion address into this
# file:

HOSTNAME = "foolscap.lothar.com"
TUBID = "qy4aezcyd3mppt7arodl4mzaguls6m2o"
ONION = "kwmjlhmn5runa4bv.onion"
ONIONPORT = 16545
LOCALPORT = 7006

# Then run 'check-connections-client.py tcp', then with 'socks', then with
# 'tor'.

import os, sys, time
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.internet.endpoints import clientFromString
from foolscap.api import Referenceable, Tub


tub = Tub()

which = sys.argv[1] if len(sys.argv) > 1 else None
if which == "tcp":
    furl = "pb://%s@tcp:%s:%d/calculator" % (TUBID, HOSTNAME, LOCALPORT)
elif which in ("tor-default", "tor-socks", "tor-control", "tor-launch"):
    from foolscap.connections import tor
    if which == "tor-default":
        h = tor.default_socks()
    elif which == "tor-socks":
        h = tor.socks_port(int(sys.argv[2]))
    elif which == "tor-control":
        control_ep = clientFromString(reactor, sys.argv[2])
        h = tor.control_endpoint(control_ep)
    elif which == "tor-launch":
        data_directory = None
        if len(sys.argv) > 2:
            data_directory = os.path.abspath(sys.argv[2])
        h = tor.launch(data_directory)
    tub.removeAllConnectionHintHandlers()
    tub.addConnectionHintHandler("tor", h)
    furl = "pb://%s@tor:%s:%d/calculator" % (TUBID, ONION, ONIONPORT)
else:
    print("run as 'check-connections-client.py [tcp|tor-default|tor-socks|tor-control|tor-launch]'")
    sys.exit(1)
print("using %s: %s" % (which, furl))

class Observer(Referenceable):
    def remote_event(self, msg):
        pass

@inlineCallbacks
def go():
    tub.startService()
    start = time.time()
    rtts = []
    remote = yield tub.getReference(furl)
    t_connect = time.time() - start

    o = Observer()
    start = time.time()
    yield remote.callRemote("addObserver", observer=o)
    rtts.append(time.time() - start)

    start = time.time()
    yield remote.callRemote("removeObserver", observer=o)
    rtts.append(time.time() - start)

    start = time.time()
    yield remote.callRemote("push", num=2)
    rtts.append(time.time() - start)

    start = time.time()
    yield remote.callRemote("push", num=3)
    rtts.append(time.time() - start)

    start = time.time()
    yield remote.callRemote("add")
    rtts.append(time.time() - start)

    start = time.time()
    number = yield remote.callRemote("pop")
    rtts.append(time.time() - start)
    print("the result is", number)

    print("t_connect:", t_connect)
    print("avg rtt:", sum(rtts) / len(rtts))

d = go()
def _oops(f):
    print("error", f)
d.addErrback(_oops)
d.addCallback(lambda res: reactor.stop())

reactor.run()
