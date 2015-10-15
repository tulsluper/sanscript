import os
import logging
from datetime import datetime

APPNAME = 'da'
BASEDIR = os.path.join(os.path.dirname(__file__), '../../../')
TEXTDIR = os.path.join(BASEDIR, 'data/{}/plain/'.format(APPNAME))
JSONDIR = os.path.join(BASEDIR, 'data/{}/json/'.format(APPNAME))
ARCHDIR = os.path.join(BASEDIR, 'data/{}/arch/'.format(APPNAME))

EVA_CLI = os.path.join(os.path.dirname(__file__), 'cli/SSSU/linux/sssu_linux_x64')
HDS_CLI = os.path.join(os.path.dirname(__file__), 'cli/SNM2/Linux_CLI')

CONNECTIONS = os.path.join(os.path.dirname(__file__), 'StorageConnection.json')

COMMANDS_3PAR = [
    ['showsys', 'showsys'],
    ['showhost', 'showhost -d'],
    ['showvv', 'showvv -showcols Adm_Free_MB,Adm_Free_Zn,Adm_RawRsvd_MB,Adm_Rsvd_MB,Adm_Used_MB,Adm_Zn,Alert_Adm_Fail,Alert_Adm_Fail_Y,Alert_Snp_Fail,Alert_Snp_Fail_Y,Alert_Snp_Lim,Alert_Snp_Lim_Y,Alert_Snp_Wrn,Alert_Snp_Wrn_Y,Alert_Usr_Fail,Alert_Usr_Fail_Y,Alert_Usr_Lim,Alert_Usr_Lim_Y,Alert_Usr_Wrn,Alert_Usr_Wrn_Y,BsId,Copied_MB,Copied_Perc,CopyOf,CreationTime,Detailed_State,Domain,ExpirationTime,Grown_Adm_MB,Grown_Snp_MB,Grown_Usr_MB,HPC,Id,Limit_Snp_Perc,Limit_Usr_Perc,Mstr,Name,PBlkRemain,Policies,PPrnt,Prnt,Prov,Rd,Reclaimed_Adm_MB,Reclaimed_Snp_MB,Reclaimed_Usr_MB,RetentionEndTime,Roch,Rwch,SctSz,Snp_Free_MB,Snp_Free_Zn,Snp_RawRsvd_MB,Snp_Rsvd_MB,Snp_Used_MB,Snp_Used_Perc,Snp_Zn,SnpCPG,SpaceCalcTime,SPT,State,Tot_RawRsvd_MB,Tot_Rsvd_MB,Type,Usr_Free_MB,Usr_Free_Zn,Usr_RawRsvd_MB,Usr_Rsvd_MB,Usr_Used_MB,Usr_Used_Perc,Usr_Zn,UsrCPG,VSize_MB,VV_WWN,Warn_Snp_Perc,Warn_Usr_Perc,Comment'],
    ['showvlun', 'showvlun -showcols Domain,FailedPathPolicy,Host_WWN,HostDevName,HostName,ID,IsSubLUN,Lun,MonIntervalSecs,Multipathing,Port,Status,Type,VV_WWN,VVName'],
]
COMMANDS_EVA = [
    ['system', 'ls system full'],
    ['host', 'ls host full'],
    ['vdisk', 'ls vdisk full'],
]
COMMANDS_HDS = [
    ['system', 'auunitinfo'],
    ['drive_vendor', 'audrive -vendor'],
    ['drive_status', 'audrive -status'],
    ['luref', 'auluref -g'],
    ['hgwwn', 'auhgwwn -refer'],
    ['hgmap', 'auhgmap -refer'],
    ['dppool', 'audppool -g -refer'],
    ['rgref', 'aurgref -g'],
]
PARSERS_3PAR = [
    ['showsys', 'sys'],
    ['showvv', 'vv'],
    ['showvlun', 'vlun'],
    ['showhost', 'host'],
]
PARSERS_EVA = [
    ['system', 'system'],
    ['host', 'host'],
    ['vdisk', 'vdisk'],
]
PARSERS_HDS = [
    ['drive_vendor', 'drive_vendor'],
    ['drive_status', 'drive_status'],
    ['hgwwn', 'hgwwn'],
    ['luref', 'luref'],
    ['hgmap', 'hgmap'],
    ['dppool', 'dppool'],
    ['rgref','rgref'],
]
MODELS = [
    ['capacity', 'Capacity', {'before_delete_all': True}],
    ['capacity', 'CapacityHistory', {'before_delete': {'Date__contains': datetime.now().date()}}],
    ['capacity_3par', 'TPARCapacity', {'before_delete_all': True}],
    ['capacity_3par', 'TPARCapacityHistory', {'before_delete': {'Date__contains': datetime.now().date()}}],
    ['3par/host', 'TPARHost', {'before_delete_all': True}],
    ['3par/vv', 'TPARVV', {'before_delete_all': True}],
    ['3par/vlun', 'TPARVLUN', {'before_delete_all': True}],
    ['eva/vdisk', 'EVAVdisk', {'before_delete_all': True}],
    ['eva/host', 'EVAHost', {'before_delete_all': True}],
    ['hds/hgwwn', 'HDSHost', {'before_delete_all': True}],
    ['hds/luref', 'HDSLU', {'before_delete_all': True}],
    ['hds/hgmap', 'HDSMap', {'before_delete_all': True}],
    ['volumes', 'Volume', {'before_delete_all': True}],
    ['hosts', 'Host', {'before_delete_all': True}],
]

