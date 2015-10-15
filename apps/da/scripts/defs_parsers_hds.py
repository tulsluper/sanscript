

def p_drive_status(systemname, lines):
    records = []
    keys = ['Unit', 'HDU', 'Type', 'Status']
    for line in lines[1:]:
        record = {}
        items = line.split()
        items[3] = ' '.join(items[3:])
        del items[4:]
        for num, key in enumerate(keys):
            record[key] = items[num]
        record['Storage'] = systemname
        records.append(record)
    return records


def p_drive_vendor(systemname, lines):
    records = []
    keys = ['Unit', 'HDU', 'Capacity', 'Drive_Type', 'Rotational_Speed', 'Vendor_ID', 'Product_ID', 'Revision', 'Serial_No']
    for line in lines[1:]:
        record = {}
        items = line.split()
        for num, key in enumerate(keys):
            record[key] = items[num]
        record['Storage'] = systemname
        records.append(record)
    return records


def p_hgwwn(systemname, lines):
    records = []
    for line in lines:
        items = line.split()
        if line[:4] == 'Port':
            Storage_Port = items[1]
        if len(items) == 3 and items[0] != 'Name':
            Name, Port_Name, Host_Group = items
            record = {
                'Storage': systemname,
                'Storage_Port': Storage_Port,
                'Name': Name,
                'Port_Name': Port_Name,
                'Host_Group': Host_Group,
            }
            records.append(record)
    return records


def p_luref(systemname, lines):
    records = []
    for line in lines[2:]:
        line = line.replace('( ', '(').replace(' GB', '')
        items = line.split()
        record = {
            'Storage': systemname,
            'LU': items[0],
            'Capacity': items[1],
            'Stripe_Size': items[2],
            'RAID_Group': items[3],
            'DP_Pool': items[4],
            'RAID_Level': items[5],
            'Type': items[6],
            'Number_of_Paths': items[7],
            'Status': items[8],
        }
        records.append(record)
    return records


def p_hgmap(systemname, lines):
    records = []
    for line in lines[2:]:
        items = line.split()
        if len(items) == 4:
            record = {
                'Storage': systemname,
                'Port': items[0],
                'Group': items[1],
                'H_LUN': items[2],
                'LUN': items[3],
            }
            records.append(record)
    return records


def p_dppool(systemname, lines):
    records = []
    for line in lines[2:-1]:
        line = line.replace('( ', '(').replace(' GB', '')
        items = line.split()
        record = {
            'Storage': systemname,
            'DP_Pool': items[0],
            'RAID_Level': items[1],
            'Total_Capacity': items[2],
            'Consumed_Capacity': items[3],
            'Type': items[4],
            'Status': items[5],
            'Reconstruction_Progress': line[135:187].strip(),
            'Stripe_Size': line[187:].strip(),
        }
        records.append(record)
    return records


def p_rgref(systemname, lines):
    records = []
    for line in lines[2:]:
        line = line.replace('( ', '(').replace(' GB', '')
        items = line.split()
        record = {
            'Storage': systemname,
            'RAID_Group': items[0],
            'RAID_Level': items[1],
            'Parity_Groups': items[2],
            'Type': items[3],
            'Total_Capacity': items[4],
            'Free_Capacity': items[5],
            'Priority': line[91:113].strip(),
            'Status': line[113:158].strip(),
            'Reconstruction_Progress': line[158:].strip(),
        }
        records.append(record)
    return records

