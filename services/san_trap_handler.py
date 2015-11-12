from san_event_client import send_event


def check_cfgenable(varBinds):
    """
    1.3.6.1.2.1.1.3.0 = 694895304
    1.3.6.1.6.3.1.1.4.1.0 = 1.3.6.1.4.1.1588.2.1.1.1.0.4
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.1.2989 = 2989
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.2.2989 = b'2015/10/23-15:22:46'
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.3.2989 = 4
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.4.2989 = 1
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.5.2989 = b'ZONE-1022 The effective configuration has changed to CONFIG1. . '
    1.3.6.1.4.1.1588.2.1.1.1.1.10.0 = b'CZC333ADUK'
    1.3.6.1.6.3.18.1.3.0 = 10.1.57.111
    1.3.6.1.4.1.11.2.17.2.2.0 = b'10.1.57.111'
    """
    brocade = False
    hit = False
    data = {}
    for name, val in varBinds:
        name, val = name.prettyPrint(), val.prettyPrint()
        if brocade is False:
            if name == '1.3.6.1.6.3.1.1.4.1.0'\
            and val == '1.3.6.1.3.94.0.4':
            #and val == '1.3.6.1.4.1.1588.2.1.1.1.0.4':
                brocade = True
        if brocade is True\
        and hit is False:
            if 'configuration has changed' in val:
                hit = True
                data['message'] = val[2:-1]
        if name == '1.3.6.1.6.3.18.1.3.0':
            data['sender'] = val
    return hit, data


def handle(varBinds):
    hit, data = check_cfgenable(varBinds)
    if hit:
        send_event('cfgenable', data)
