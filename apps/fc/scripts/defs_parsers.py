

def p_alias(fabric, lines):
    prevline = ''
    aliasesD = {}
    for line in lines:
        if line[1:6] == 'alias':
            prevline = 'alias'
            items = line.replace(';', '').split()
            alias = items[1]
            wwns = items[2:] if len(items) > 2 else []
            aliasesD[alias] = wwns
            record = {'name': alias, 'wwns': wwns}
        elif line == '\n':
            break
        elif prevline == 'alias':
            wwns = line.replace(';', '').split()
            aliasesD[alias] += wwns
    records = []
    for alias, wwns in aliasesD.items():
        records.append({'Fabric': fabric, 'Name': alias, 'Wwns': wwns})
    return records


def p_zone(fabric, lines):
    zones = {}
    field = 'Aliases'
    prevline = ''
    for line in lines:
        if line[0] == 'E':
            field = 'Wwns'
        if line[1:6] == 'alias':
            prevline = ''
        if line[1:5] == 'zone':
            prevline = 'zone'
            zone = line.split(':')[1].strip()
            if not zone in zones:
                zones[zone] = {'Aliases': [], 'Wwns': []}
        elif prevline == 'zone':
            aliases = line.replace(';', '').split()
            zones[zone][field] += aliases
    records = []
    for zone, record in zones.items():
        record.update({'Fabric': fabric, 'Name': zone})
        records.append(record)
    return records


def p_fswitch(fabric, lines):
    records = []
    for line in lines[2:-3]:
        values = line.split()
        switch = values[5].replace('"','').replace('>','')
        records.append({'Fabric': fabric, 'Switch': switch})
    return records


def p_agswitch(fabric, lines):
    records = []
    for line in lines[2:]:
        values = line.split()
        switch = values[5]
        records.append({'Fabric': fabric, 'Switch': switch})
    return records


def p_switch(system, lines):
    record = {'Switch': system}
    for line in lines:
        if line == '\n':
            break
        else:
            key, value = line.split(':', 1)
            key = key.replace(' ', '_')
            value = value.strip()
            record[key] = value
    return [record,]


def p_serial(switch, lines):
    record = {'Switch': switch}
    for line in lines:
        if ':' in line:
            key, value = line.split(':', 1)
            if key in ["Part Num", "Serial Num"]:
                key = key.replace(' ', '_')
                record[key] = value.strip()
    return [record,]


def p_version(switch, lines):
    record = {'Switch': switch}
    for line in lines:
        key, value = line.split(':', 1)
        key = key.replace(' ', '_')
        value = value.strip()
        record[key] = value
    return [record,]


def p_port(system, lines):
    records = []
    keys = ['Index', 'Slot', 'Port', 'Address', 'Media', 'Speed', 'State', 'Proto', 'Type', 'Wwn', 'Comment']
    notslot = False
    portline = False
    for line in lines:
        if portline:
            values = line.split()
            if notslot:
                values.insert(1,'')
            if len(values[3]) == 2:
                values.insert(3,'')
                values.insert(7,'')
            if len(values) == 8 or not '-' in values[8]:
                values.insert(8,'')
            if len(values) == 9 or not ':' in values[9]:
                values.insert(9,'')
            if len(values) == 10:
                values.insert(10,'')
            else:
                values[10] = ' '.join(values[10:])
            record = dict(zip(keys, values))
            record['Switch'] = system
            record['uPort'] = '/'.join(values[1:3]) if values[1] else values[2]
            records.append(record)
        elif line[:5] == 'Index' and not 'Slot' in line:
            notslot = True
        elif line[:4] == 'Area':
            notslot = True
        elif line[0] == '=':
            portline = True
    return records


def p_name(switch, lines):
    records = []
    if len(lines) == 1:
        return records
    keys = lines[1].split()
    keys = [k.replace(' ', '_') for k in keys]
    record = {}
    for line in lines[2:-1]:
        if line[1] != ' ':
            if record:
                records.append(record)
            values = line.replace(';',' ').split()
            record = dict(zip(keys, values))
            record['Switch'] = switch
        else:
            key, value = [x.strip() for x in line.split(':', 1)]
            key = key.replace(' ', '_')
            record[key] = value
    records.append(record)
    return records


def p_sfp(switch, lines):
    records = []
    record = {}
    for line in lines:
        if line[:4] in ['Slot', 'Port']:
            if record and len(record) > 2:
                records.append(record)
            uPort = line.strip()
            for x in ['Slot', 'Port', ' ', ':']:
                uPort = uPort.replace(x, '')
            record = {'Switch': switch, 'uPort': uPort}
        elif ':' in line and line[:5] != 'port ':
            items = line.split(':', 1)
            key, values = items
            for word in ['(', ')', '.5', '/']:
                key = key.replace(word, '')
            key = key.strip().replace(' ', '_').replace('-', '_')
            if key in ['Temperature', 'Current', 'Voltage']:
                splvalues = values.split()
                if len(splvalues) > 2:
                    record[key] = splvalues[0]
                else:
                    record[key] = values.strip()
            elif key in ['RX_Power', 'TX_Power']:
                splvalues = values.split()
                if len(splvalues) > 2:
                    record[key] = splvalues[0]
                else:
                    record[key] = values.strip()
            else:
                record[key] = ' '.join(values.split())
    if record and len(record) > 2:
        records.append(record)
    return records


def p_portshow(switch, lines):
    parseflag = False
    records = []
    record = {}
    for line in lines:
        if line[0] == '*':
            if record:
                records.append(record)
            record = {'Switch': switch, 'uPort': line[1:].strip()}
            parseflag = True
        elif parseflag and line != '\n':
            if line[0] != '\t':
                items = line.strip().split(':', 1)
                key = items[0].replace(' ','_').replace('(','').replace(')','')
                value = ' '.join(items[1].split())
                if key == 'Interrupts':
                    parseflag = False
                else:
                    if key == 'Peer_beacon':
                        pass
                    else:
                        if 'connected' in key:
                            value = []
                        if 'portScn' in value:
                            value, value2 = value.split('portScn:')
                            record['portScn'] = value2
                        record[key] = value
            else:
                value = line.strip()
                if 'connected' in key and value == 'None':
                    pass    
                else:
                    record[key].append(value)
    records.append(record)
    return records


def p_licenseport(system, lines):

    license = {'Switch': system}

    if len(lines) == 1:
        return [license]

    assigned_flag = False
    ports_assigned = []
    not_assigned_flag = False
    not_assigned_ports = []

    reservations = ''
    assignments_offline = ''

    for line in lines:

        if assigned_flag == True:
            if not 'None' in line:
                ports_assigned += [x.strip() for x in line.split(',')]
            assigned_flag = False

        if 'Ports assigned' in line:
            assigned_flag = True

        if not_assigned_flag == True:
            if not 'None' in line:
                not_assigned_ports += [x.strip() for x in line.split(',')]
            not_assigned_flag = False

        if 'Ports not assigned' in line:
            not_assigned_flag = True

        words = line.split()
        if len(words) > 1:
            if words[1] == 'license':
                if words[2] == 'reservations':
                    reservations = words[0]
                if words[2] == 'assignments':
                    assignments_offline = words[0]

    license['ports_assigned'] = ports_assigned
    license['not_assigned_ports'] = not_assigned_ports
    license['reservations'] = reservations
    license['assignments_offline'] = assignments_offline

    return [license]
