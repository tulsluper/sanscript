

def p_system(systemname, lines):
    record = {}
    for line in lines:
        if ':' in line and line[0] == ' ' and line[2] != ' ':
            items = line.split()
            key = items[0]
            value = ' '.join(items[2:])
            record[key] = value
    if record:
        record['Storage'] = systemname
        return [record]
    else:
        return []


def p_host(systemname, lines):
    records = []
    record = {}
    keys = []
    for line in lines:
        if ':' in line and line[0] == ' ' and line[2] != ' ':  
            items = line.split()
            key = items[0]
            value = ' '.join(items[2:])
            record[key] = value
            if not key in keys:
                keys.append(key)
        elif 'portwwn' in line:
            if not 'WWNs' in record:
                record['WWNs'] = [] 
            value = ' '.join(line.split()[2:])
            record['WWNs'].append(value)
        elif line == '\n' and record:
            record['Storage'] = systemname
            if 'WWNs' in record:
                record['WWNs'] = ' '.join(record['WWNs'])
            records.append(record)         
            record = {}

#    kks = {k:0 for k in keys}
#    for r in records:
#        for k in keys:
#            if k in r:
#                if len(r[k]) > kks[k]:
#                    kks[k] = len(r[k])
#    for k in keys:
#        print(k, kks[k])

    return records


def p_vdisk(systemname, lines):
    records = []
    record = {}
    for line in lines:
        if ':' in line and line[0] == ' ' and line[2] != ' ':
            items = line.split()
            key = items[0]
            value = ' '.join(items[2:])
            record[key] = value
        elif 'hostname' in line:
            if not 'hosts' in record:
                record['hosts'] = []
            value = ' '.join(line.split()[2:])
            record['hosts'].append(value)
        elif line == '\n' and record:
            record['Storage'] = systemname
            if 'hosts' in record:
                record['hosts'] = ' '.join(record['hosts'])
            records.append(record)
            record = {}


    return records
