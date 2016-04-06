#!/usr/bin/env python3

import os
import json
from settings import TEXTDIR, JSONDIR
from settings import logging
from defs import dump_data, load_data
import xmltodict
import collections

import requests
import xml.etree.ElementTree as ET
import datetime


dirpath = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(dirpath, 'Connection.json')
CONNECTIONS = load_data(filepath, [])


#from requests.packages.urllib3.exceptions import InsecureRequestWarning
#requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
session = requests.session()
ns = {
   'SOAP-ENV': 'http://www.w3.org/2003/05/soap-envelope',
   'hpoa': 'hpoa.xsd',
}


def get_session(enc_fqdn, username, password):
    #session = requests.session()

    oaSessionKey = ''
    url = 'https://{}/hpoa'.format(enc_fqdn.rstrip())

    # request for login
    request = """\
    <?xml version="1.0" encoding="utf-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:hpoa="hpoa.xsd">
    <SOAP-ENV:Body>
        <hpoa:userLogIn>
        <hpoa:username>{username}</hpoa:username>
        <hpoa:password>{password}</hpoa:password>
        </hpoa:userLogIn>
    </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    """.format(username=username, password=password).encode('utf-8')

    headers = {
        "Host": enc_fqdn.rstrip(),
        "Content-Type": "text/xml; charset=utf-8",
        "Content-Length": len(request),
    }

    response = session.post(
        url = url,
        headers = headers,
        data = request,
        verify = False,
    )

    content = response.content

    #print(request)
    #print(content.decode('utf-8'))

    tree = ET.fromstring(content)
    try:
        oaSessionKey = tree.find('SOAP-ENV:Body/hpoa:userLogInResponse/hpoa:HpOaSessionKeyToken/hpoa:oaSessionKey', ns).text
        #print('SessionKey: {}'.format(oaSessionKey))
    except:
        print('SessionKey: None')

    return oaSessionKey


def get_blade_info(enc_fqdn, oaSessionKey, bayNumber):

    url = 'https://{}/hpoa'.format(enc_fqdn.rstrip())

    request = """\
    <?xml version="1.0"?>
      <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://www.w3.org/2003/05/soap-envelope" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd" xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" xmlns:hpoa="hpoa.xsd">
        <SOAP-ENV:Header>
          <wsse:Security SOAP-ENV:mustUnderstand="true">
            <hpoa:HpOaSessionKeyToken>
              <hpoa:oaSessionKey>{oaSessionKey}</hpoa:oaSessionKey>
            </hpoa:HpOaSessionKeyToken>
          </wsse:Security>
        </SOAP-ENV:Header>
        <SOAP-ENV:Body>
          <hpoa:getBladeInfo>
            <hpoa:bayNumber>{bayNumber}</hpoa:bayNumber>
          </hpoa:getBladeInfo>
        </SOAP-ENV:Body>
      </SOAP-ENV:Envelope>
    """.format(oaSessionKey=oaSessionKey, bayNumber=bayNumber).encode('utf-8')

    headers = { 
        "Host": enc_fqdn.rstrip(),
        "Content-Type": "text/xml; charset=utf-8",
        "Content-Length": len(request),
    }

    response = session.post(
        url = url,
        headers = headers,
        data = request,
        verify = False,
    )
    content = response.content
    xml_tree = ET.fromstring(content)
    #blade_info = xmltodict.parse(content.decode('utf-8'))

    ram_size = xml_tree.find('SOAP-ENV:Body/hpoa:getBladeInfoResponse/hpoa:bladeInfo/hpoa:memory', ns)
    if ram_size == None:
        ram_size = ''
    else: ram_size = ram_size.text

    #os_name = xml_tree.find('SOAP-ENV:Body/hpoa:getBladeInfoResponse/hpoa:bladeInfo/hpoa:rbsuOsName', ns)

    cpu_count = xml_tree.find('SOAP-ENV:Body/hpoa:getBladeInfoResponse/hpoa:bladeInfo/hpoa:numberOfCpus', ns)
    if cpu_count == None:
        cpu_count = ''
    else: cpu_count = cpu_count.text

    cpu_type = xml_tree.find('SOAP-ENV:Body/hpoa:getBladeInfoResponse/hpoa:bladeInfo/hpoa:extraData[@hpoa:name="procVer1"]', ns)
    if cpu_type == None:
        cpu_type = xml_tree.find('SOAP-ENV:Body/hpoa:getBladeInfoResponse/hpoa:bladeInfo/hpoa:cpus/hpoa:bladeCpuInfo/hpoa:cpuType', ns)
        cpu_speed = xml_tree.find('SOAP-ENV:Body/hpoa:getBladeInfoResponse/hpoa:bladeInfo/hpoa:cpus/hpoa:bladeCpuInfo/hpoa:cpuSpeed', ns)
        if cpu_type != None:
            cpu_type = cpu_type.text
            if cpu_speed != None:
                cpu_type = cpu_type+' @ '+cpu_speed.text+'MHz'
        else: cpu_type = 'Can\'t get data'
    else: cpu_type = cpu_type.text

    cpu_cores = xml_tree.find('SOAP-ENV:Body/hpoa:getBladeInfoResponse/hpoa:bladeInfo/hpoa:extraData[@hpoa:name="procCores1"]', ns)
    if cpu_cores == None:
        cpu_cores = ''
    else: cpu_cores = cpu_cores.text

    return ram_size, cpu_count, cpu_type, cpu_cores



def main():

    username = 'encsurfer'
    password = 'Gxb3HzSqH6%'

    servers = load_data(os.path.join(JSONDIR, 'servers'))

    enc_bays = {}
    for server in servers:
        enc_name = server['Enclosure_Name']
        bay_number = server['Server_Bay']
        if not enc_name in enc_bays:
            enc_bays[enc_name] = []
        enc_bays[enc_name].append(bay_number)

    new_info = {}
    for con in CONNECTIONS[:2]:
        enc_name, enc_fqdn = con['name'], con['address']
        bays = enc_bays.get(enc_name, [])

        try:
            oaSessionKey = get_session(enc_fqdn, username, password)
            print('SessionKey: {}'.format(oaSessionKey))
        except:
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'Connection failed:', enc_fqdn)
            continue

        for bay_number in bays:
            ram_size, cpu_count, cpu_type, cpu_cores = get_blade_info(enc_fqdn, oaSessionKey, bay_number)
            new_info['{}.{}'.format(enc_name, bay_number)] = {
                'CPU_type': cpu_type,
                'CPU_cores': cpu_cores,
                'CPU_count:': cpu_count,
                'RAM_size': ram_size,
            }

    for server in servers:
        enc_name = server['Enclosure_Name']
        bay_number = server['Server_Bay']
        ext = new_info.get('{}.{}'.format(enc_name, bay_number))
        if ext:
            server.update(ext)
    dump_data(os.path.join(JSONDIR, 'servers2'), servers)

        

if __name__ == '__main__':
    main()

