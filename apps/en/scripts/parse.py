#!/usr/bin/env python3

import os
import json
from settings import TEXTDIR, JSONDIR
from settings import logging
from defs import dump_data, load_data
import xmltodict
import collections



def parse(data):
        
        enclosure = {
          'Enclosure_Name': data['RIMP']['INFRA2']['ENCL'],
          'Enclosure_SN': data['RIMP']['INFRA2']['ENCL_SN'],
          'Location': data['RIMP']['INFRA2']['RACK']
        }

        cod = collections.OrderedDict()
        servers = []
        mezzanines = []
  
        for blade in data['RIMP']['INFRA2']['BLADES']['BLADE']:
          servers.append({
            'Enclosure_Name': data['RIMP']['INFRA2']['ENCL'],
            'Server_Bay': blade['BAY']['CONNECTION'],
            'Server_Model': blade['SPN'],
            'Server_SN': blade['BSN'],
            'Server_iLO': blade['MGMTIPADDR']if 'MGMTIPADDR' in blade else '',
            'Server NAME': blade['NAME'] if 'NAME' in blade and blade['NAME'] != 'Status is not available' else '',
            'Power_state': blade['POWER']['POWERSTATE']
          })
  
          for mezz in blade['PORTMAP']['MEZZ']:
              if 'DEVICE' in mezz:
                  addresses = []
                  for port in mezz['DEVICE']['PORT']:
                      if 'GUIDS' in port and port['GUIDS'] != None:
                          vport = port['GUIDS']['GUID']
                          if type(vport) == list:
                              for vp in vport:
                                  addresses.append({
                                      vp['GUID_STRING']
                                  })
                          if type(vport) == type(cod):
                              addresses.append({
                                  vport['GUID_STRING']
                              })
                      else:
                          addresses.append({
                              port['WWPN']
                          })
                  addresses = '; '.join([list(a)[0] for a in addresses])

                  mezzanines.append({
                      'Enclosure_Name': data['RIMP']['INFRA2']['ENCL'],
                      'Server_Bay': blade['BAY']['CONNECTION'],
                      'Server_SN': blade['BSN'],
                      'Mezz_Name': mezz['DEVICE']['NAME'],
                      'Ports': str(addresses)
                  })
        return enclosure, servers, mezzanines



def main():
    all_enclosures = []
    all_servers = []
    all_mezzanines = []

    for filename in os.listdir(TEXTDIR):
        filepath = os.path.join(TEXTDIR, filename)
        system, command = filename.split('.')
        with open(filepath) as f:
            content = f.read()
            data = xmltodict.parse(content)
            enclosure, servers, mezzanines = parse(data)
            all_enclosures += [enclosure]
            all_servers += servers
            all_mezzanines += mezzanines

    for name, records in (
        ('enclosures', all_enclosures),
        ('servers', all_servers),
        ('mezzanines', all_mezzanines),
    ):
        filepath = os.path.join(JSONDIR, name)
        dump_data(os.path.join(JSONDIR, name), records)
        logging.info('%s | %s records' %(name, len(records)))
        ks = {}
        for record in records:
            for key, value in record.items():
                if not key in ks:
                     ks[key] = 0
                if len(value) > ks[key]:
                    ks[key] = len(value)
        print(ks)
          
 


if __name__ == '__main__':
    main()

