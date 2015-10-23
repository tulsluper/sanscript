#!/usr/bin/env python3

from pysnmp.entity import engine, config
from pysnmp.carrier.asynsock.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from pysnmp.proto.api import v2c

from san_trap_handler import handle

try:
    from settings import TRAP_HOST as HOST
    from settings import TRAP_PORT as PORT
except:
    HOST = '0.0.0.0'
    PORT = 162


# Create SNMP engine with autogenernated engineID and pre-bound
# to socket transport dispatcher
snmpEngine = engine.SnmpEngine()

# Transport setup

# UDP over IPv4
config.addSocketTransport(
    snmpEngine,
    udp.domainName,
    udp.UdpTransport().openServerMode((HOST, PORT))
)

# SNMPv3/USM setup

# user: usr-md5-des, auth: MD5, priv DES, contextEngineId: 8000063403005056921033
# this USM entry is used for TRAP receiving purposes
config.addV3User(
    snmpEngine, 'usr-md5-des',
    config.usmHMACMD5AuthProtocol, 'authkey1',
    config.usmDESPrivProtocol, 'privkey1',
    contextEngineId=v2c.OctetString(hexValue='8000063403005056921033')
)

# Callback function for receiving notifications
def cbFun(snmpEngine,
          stateReference,
          contextEngineId, contextName,
          varBinds,
          cbCtx):
    handle(varBinds)

# Register SNMP Application at the SNMP engine
ntfrcv.NotificationReceiver(snmpEngine, cbFun)

snmpEngine.transportDispatcher.jobStarted(1) # this job would never finish

# Run I/O dispatcher which would receive queries and send confirmations
try:
    snmpEngine.transportDispatcher.runDispatcher()
except:
    snmpEngine.transportDispatcher.closeDispatcher()
    raise
