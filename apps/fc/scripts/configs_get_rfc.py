#!/usr/bin/env python3

import os
import json
from datetime import datetime
import requests
import xml.etree.ElementTree as ET

try:
    from settings import CONFIGSDIR
    outpath = os.path.join(CONFIGSDIR, 'note.json')
except:
    outpath = os.path.join(os.path.dirname(__file__), 'note.json')


def itsm_request():
    #url = "http://wsdlhpdp:password@itsmtest.astelit.ukr:13777/SM/7/AstlhpdpIntegration.wsdl"
    # uncomment below if wants to use prod itsm
    url = "http://wsdlhpdp:password@itsm.astelit.ukr:13555/SM/7/AstlhpdpIntegration.wsdl"
    
    request = """\
<?xml version="1.0" encoding="UTF-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="http://schemas.hp.com/SM/7">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:RetrieveChangeListRequest>
          <ns:keys>           
            <ns:SubcategoryGroup type="String">SAN &amp; Storage</ns:SubcategoryGroup>
            <ns:Status type="String">initial</ns:Status>
            <ns:Phase type="String">Minor RFC Implementation</ns:Phase>
            <ns:ApprovalStatus type="String">approved</ns:ApprovalStatus>
            <ns:Subcategory type="String">Add/Delete/Modify SAN Zoning configuration</ns:Subcategory>
         </ns:keys>
      </ns:RetrieveChangeListRequest>
   </soapenv:Body>
</soapenv:Envelope>
"""
    request = request.encode('utf-8')
    headers = {
        "Host": "itsmtest.astelit.ukr",
        "Content-Type": "text/xml; charset=UTF-8",
        "Content-Length": len(request),
        "SOAPAction": "RetrieveList",
        "Connection": "close",
    }
    response = requests.post(
        url = url,
        headers = headers,
        data = request,
        verify = False,
        stream = False,
        timeout = 10,
    )
    content = response.content
    response.connection.close()
    return content


def find_changes(content):
    changes = []
    ns = {'ns': "http://schemas.hp.com/SM/7"}
    tree = ET.fromstring(content)
    instances = tree.findall(".//ns:instance", ns)
    for instance in instances:
        for line in instance.iter():
            tag = line.tag
            text = line.text 
            if text is not None:
                text = text.strip()
            if tag[0] == '{':
                tag = tag[1:].split('}')[1]
            if tag == 'ChangeID':
                changes.append(text)
    return changes


def main():
    content = itsm_request()
    changes = find_changes(content)

    if changes == [] and content == b'<HTML><BODY>Not Authorized</BODY></HTML>':
        changes = 'ITSM authorization failed'

    with open(outpath, 'w') as f:
        data = {str(datetime.now()): changes}
        json.dump(data, f)

    return


if __name__ == '__main__':
    main()

