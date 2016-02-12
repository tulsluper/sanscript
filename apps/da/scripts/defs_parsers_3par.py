

def p_sys(systemname, lines):
    keys = lines[1].split()
    keys = [key.replace('-','') for key in keys]
    keys[keys.index('ID')] = 'SysId'
    values = lines[2].split()
    values[2] = ' '.join(values[2:4])
    del values[3]
    record = dict(zip(keys, values))
    record['Storage'] = systemname
    return [record]


def p_vv(systemname, lines):
    records = []
    keys = lines[0].split()
    keys[keys.index('Id')] = 'VVId'
    for line in lines[1:-2]:
        items = line.split()
        if items[18] != '--': # Alert_Usr_Wrn
            items[18] = ' '.join(items[18:21])
            del items[19:21]
        CreationTime = ' '.join(items[24:27])
        if items[60] != '--': # SpaceCalcTime
            items[60] = ' '.join(items[60:63])
            del items[61:63]
        Comment = ' '.join(items[78:])
        items = items[:24] + [CreationTime] + items[27:78] + [Comment]
        record = dict(zip(keys, items))
        record['Storage'] = systemname
        records.append(record)
    return records


def p_vlun(systemname, lines):
    records = []
    keys = lines[1].split()
    keys[keys.index('ID')] = 'LunId'
    for line in lines[2:]:
        if line[:2] == '--':
            break
        items = line.split()
        if items[13] == 'set':
            items[12] = 'host set'
            del items[13]
        record = dict(zip(keys, items))
        record['Storage'] = systemname
        records.append(record)
    return records


def p_host(systemname, lines):
    records = []
    keys = lines[0].split()
    keys = [key.replace('-', '') for key in keys]
    keys[keys.index('WWN/iSCSI_Name')] = 'WWN_or_Name'
    keys[keys.index('Id')] = 'HostId'
    for line in lines[1:-2]:
        items = line.split()
        record = dict(zip(keys, items))
        record['Storage'] = systemname
        records.append(record)
    return records
