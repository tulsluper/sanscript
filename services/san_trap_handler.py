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

    1.3.6.1.2.1.1.3.0 = 662660321
    1.3.6.1.6.3.1.1.4.1.0 = 1.3.6.1.4.1.1588.2.1.1.42.0.4
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.1.7927 = 7927
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.2.7927 = b'2015/11/12-16:59:11'
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.3.7927 = 4
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.4.7927 = 1
    1.3.6.1.4.1.1588.2.1.1.1.8.5.1.5.7927 = b'ZONE-1022 The effective configuration has changed to DNCONFIG1.  '
    1.3.6.1.4.1.1588.2.1.1.1.1.10.0 = b'USB84140BA'
    """
    brocade = False
    hit = False
    data = {}
    for name, val in varBinds:
        name, val = name.prettyPrint(), val.prettyPrint()
        if brocade is False:
            if name == '1.3.6.1.6.3.1.1.4.1.0'\
            and '1.3.6.1.4.1.1588.2.1.1.' in val:
                brocade = True
        if brocade is True\
        and hit is False:
            if 'configuration has changed' in val:
                hit = True
                data['message'] = val[2:-1]
        if name == '1.3.6.1.6.3.18.1.3.0':
            data['sender'] = val
        if name == '1.3.6.1.4.1.1588.2.1.1.1.1.10.0':
            data['serial'] = val[2:-1]
    return hit, data


def handle(varBinds):
    hit, data = check_cfgenable(varBinds)
    if hit:
        send_event('cfgenable', data)
