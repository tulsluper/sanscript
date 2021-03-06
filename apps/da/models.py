from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User


# ==============================================================================

class StorageConnection(models.Model):
    MODELS = (
        ('3PAR', '3PAR'),
        ('EVA', 'EVA'),
        ('HDS', 'HDS'),
    )
    model = models.CharField(max_length=4, choices=MODELS)
    name = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    order = models.IntegerField(null=True, blank=True)
    class Meta:
        ordering = ['order', 'name']

# ==============================================================================

class Capacity(models.Model):
    Storage = models.CharField(max_length=30)
    RawTotal = models.DecimalField(max_digits=6, decimal_places=2)
    RawData = models.DecimalField(max_digits=6, decimal_places=2)
    RawSpare = models.DecimalField(max_digits=6, decimal_places=2)
    RawAllocated = models.DecimalField(max_digits=6, decimal_places=2)
    RawFree = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedTotal = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedUsed = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedPresented = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedNotPresented = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedAvailable = models.DecimalField(max_digits=6, decimal_places=2)


class CapacityHistory(models.Model):
    Storage = models.CharField(max_length=30)
    RawTotal = models.DecimalField(max_digits=6, decimal_places=2)
    RawData = models.DecimalField(max_digits=6, decimal_places=2)
    RawSpare = models.DecimalField(max_digits=6, decimal_places=2)
    RawAllocated = models.DecimalField(max_digits=6, decimal_places=2)
    RawFree = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedTotal = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedUsed = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedPresented = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedNotPresented = models.DecimalField(max_digits=6, decimal_places=2)
    FormattedAvailable = models.DecimalField(max_digits=6, decimal_places=2)
    Date = models.DateField(auto_now_add=True)


class TPARCapacity(models.Model):
    Storage = models.CharField(max_length=30)
    TOTAL = models.DecimalField(max_digits=6, decimal_places=2)
    USED = models.DecimalField(max_digits=6, decimal_places=2)
    FREE = models.DecimalField(max_digits=6, decimal_places=2)
    OVERPROVISIONED = models.DecimalField(max_digits=6, decimal_places=2)
    RESERVE = models.DecimalField(max_digits=6, decimal_places=2)
    RESERVE_OVERUSED = models.DecimalField(max_digits=6, decimal_places=2)
    reserve_used = models.DecimalField(max_digits=6, decimal_places=2)
    reserve_free = models.DecimalField(max_digits=6, decimal_places=2)
    full = models.DecimalField(max_digits=6, decimal_places=2)
    cpvv = models.DecimalField(max_digits=6, decimal_places=2)
    tpvv = models.DecimalField(max_digits=6, decimal_places=2)
    tpvv_used = models.DecimalField(max_digits=6, decimal_places=2)
    tpvv_free = models.DecimalField(max_digits=6, decimal_places=2)
    snp = models.DecimalField(max_digits=6, decimal_places=2)
    copy = models.DecimalField(max_digits=6, decimal_places=2)


class TPARCapacityHistory(models.Model):
    Storage = models.CharField(max_length=30)
    TOTAL = models.DecimalField(max_digits=6, decimal_places=2)
    USED = models.DecimalField(max_digits=6, decimal_places=2)
    FREE = models.DecimalField(max_digits=6, decimal_places=2)
    OVERPROVISIONED = models.DecimalField(max_digits=6, decimal_places=2)
    RESERVE = models.DecimalField(max_digits=6, decimal_places=2)
    RESERVE_OVERUSED = models.DecimalField(max_digits=6, decimal_places=2)
    reserve_used = models.DecimalField(max_digits=6, decimal_places=2)
    reserve_free = models.DecimalField(max_digits=6, decimal_places=2)
    full = models.DecimalField(max_digits=6, decimal_places=2)
    cpvv = models.DecimalField(max_digits=6, decimal_places=2)
    tpvv = models.DecimalField(max_digits=6, decimal_places=2)
    tpvv_used = models.DecimalField(max_digits=6, decimal_places=2)
    tpvv_free = models.DecimalField(max_digits=6, decimal_places=2)
    snp = models.DecimalField(max_digits=6, decimal_places=2)
    copy = models.DecimalField(max_digits=6, decimal_places=2)
    Date = models.DateField(auto_now_add=True)


class TPARVV(models.Model):
    Storage = models.CharField(max_length=32)
    Adm_Free_MB = models.CharField(max_length=8)
    Adm_Free_Zn = models.CharField(max_length=8)
    Adm_RawRsvd_MB = models.CharField(max_length=8)
    Adm_Rsvd_MB = models.CharField(max_length=8)
    Adm_Used_MB = models.CharField(max_length=8)
    Adm_Zn = models.CharField(max_length=8)
    Alert_Adm_Fail = models.CharField(max_length=24)
    Alert_Adm_Fail_Y = models.CharField(max_length=8)
    Alert_Snp_Fail = models.CharField(max_length=24)
    Alert_Snp_Fail_Y = models.CharField(max_length=8)
    Alert_Snp_Lim = models.CharField(max_length=24)
    Alert_Snp_Lim_Y = models.CharField(max_length=8)
    Alert_Snp_Wrn = models.CharField(max_length=24)
    Alert_Snp_Wrn_Y = models.CharField(max_length=8)
    Alert_Usr_Fail = models.CharField(max_length=24)
    Alert_Usr_Fail_Y = models.CharField(max_length=8)
    Alert_Usr_Lim = models.CharField(max_length=24)
    Alert_Usr_Lim_Y = models.CharField(max_length=8)
    Alert_Usr_Wrn = models.CharField(max_length=24)
    Alert_Usr_Wrn_Y = models.CharField(max_length=8)
    BsId = models.CharField(max_length=8)
    Copied_MB = models.CharField(max_length=8)
    Copied_Perc = models.CharField(max_length=8)
    CopyOf = models.CharField(max_length=30)
    CreationTime = models.CharField(max_length=24)
    Detailed_State = models.CharField(max_length=8)
    Domain = models.CharField(max_length=8)
    ExpirationTime = models.CharField(max_length=24)
    Grown_Adm_MB = models.CharField(max_length=8)
    Grown_Snp_MB = models.CharField(max_length=8)
    Grown_Usr_MB = models.CharField(max_length=8)
    HPC = models.CharField(max_length=8)
    VVId = models.CharField(max_length=8)
    Limit_Snp_Perc = models.CharField(max_length=8)
    Limit_Usr_Perc = models.CharField(max_length=8)
    Mstr = models.CharField(max_length=8)
    Name = models.CharField(max_length=128)
    PBlkRemain = models.CharField(max_length=8)
    Policies = models.CharField(max_length=128)
    PPrnt = models.CharField(max_length=8)
    Prnt = models.CharField(max_length=8)
    Prov = models.CharField(max_length=8)
    Rd = models.CharField(max_length=8)
    Reclaimed_Adm_MB = models.CharField(max_length=8)
    Reclaimed_Snp_MB = models.CharField(max_length=8)
    Reclaimed_Usr_MB = models.CharField(max_length=8)
    RetentionEndTime = models.CharField(max_length=24)
    Roch = models.CharField(max_length=8)
    Rwch = models.CharField(max_length=8)
    SctSz = models.CharField(max_length=8)
    Snp_Free_MB = models.CharField(max_length=8)
    Snp_Free_Zn = models.CharField(max_length=8)
    Snp_RawRsvd_MB = models.CharField(max_length=8)
    Snp_Rsvd_MB = models.CharField(max_length=8)
    Snp_Used_MB = models.CharField(max_length=8)
    Snp_Used_Perc = models.CharField(max_length=8)
    Snp_Zn = models.CharField(max_length=8)
    SnpCPG = models.CharField(max_length=24)
    SpaceCalcTime = models.CharField(max_length=24)
    SPT = models.CharField(max_length=8)
    State = models.CharField(max_length=8)
    Tot_RawRsvd_MB = models.CharField(max_length=8)
    Tot_Rsvd_MB = models.CharField(max_length=8)
    Type = models.CharField(max_length=8)
    Usr_Free_MB = models.CharField(max_length=8)
    Usr_Free_Zn = models.CharField(max_length=8)
    Usr_RawRsvd_MB = models.CharField(max_length=8)
    Usr_Rsvd_MB = models.CharField(max_length=8)
    Usr_Used_MB = models.CharField(max_length=8)
    Usr_Used_Perc = models.CharField(max_length=8)
    Usr_Zn = models.CharField(max_length=8)
    UsrCPG = models.CharField(max_length=32)
    VSize_MB = models.CharField(max_length=8)
    VV_WWN = models.CharField(max_length=32)
    Warn_Snp_Perc = models.CharField(max_length=8)
    Warn_Usr_Perc = models.CharField(max_length=8)
    Comment = models.CharField(max_length=512)


class TPARVLUN(models.Model):
    Storage = models.CharField(max_length=32)
    Domain = models.CharField(max_length=64)
    FailedPathPolicy = models.CharField(max_length=8)
    Host_WWN = models.CharField(max_length=16)
    HostDevName = models.CharField(max_length=64)
    HostName = models.CharField(max_length=64)
    LunId = models.CharField(max_length=8)
    IsSubLUN = models.CharField(max_length=8)
    Lun = models.CharField(max_length=8)
    MonIntervalSecs = models.CharField(max_length=4)
    Multipathing = models.CharField(max_length=16)
    Port = models.CharField(max_length=5)
    Status = models.CharField(max_length=8)
    Type = models.CharField(max_length=8)
    VV_WWN = models.CharField(max_length=32)
    VVName = models.CharField(max_length=64)


class TPARHost(models.Model):
    Storage = models.CharField(max_length=32)
    HostId = models.CharField(max_length=8)
    Name = models.CharField(max_length=64)
    Persona = models.CharField(max_length=64)
    WWN_or_Name = models.CharField(max_length=64)
    Port = models.CharField(max_length=5)
    IP_addr = models.CharField(max_length=16)


class EVAVdisk(models.Model):
    Storage = models.CharField(max_length=30)
    objectid = models.CharField(max_length=64)
    objectname = models.CharField(max_length=64)
    objecttype = models.CharField(max_length=64)
    objectwwn = models.CharField(max_length=64)
    objecthexuid = models.CharField(max_length=64)
    partitionname = models.CharField(max_length=64)
    uid = models.CharField(max_length=64)
    objectparentuid = models.CharField(max_length=64)
    objectparenthexuid = models.CharField(max_length=64)
    objectparentid = models.CharField(max_length=64)
    comments = models.CharField(max_length=64)
    creationdatetime = models.CharField(max_length=64)
    timestampmodify = models.CharField(max_length=64)
    previousclonesourcevdiskid = models.CharField(max_length=64)
    previousclonesourcevdiskhexuid = models.CharField(max_length=64)
    familyname = models.CharField(max_length=64)
    istpvdisk = models.CharField(max_length=64)
    wwlunid = models.CharField(max_length=64)
    dirtyblockcount = models.CharField(max_length=64)
    isvdovercommit = models.CharField(max_length=64)
    migrationinprogress = models.CharField(max_length=64)
    operationalstate = models.CharField(max_length=64)
    operationalstatedetail = models.CharField(max_length=64)
    allocatedcapacity = models.CharField(max_length=64)
    allocatedcapacityblocks = models.CharField(max_length=64)
    virtualdisktype = models.CharField(max_length=64)
    requestedcapacity = models.CharField(max_length=64)
    requestedcapacityblocks = models.CharField(max_length=64)
    sharingrelationship = models.CharField(max_length=64)
    mirrorexists = models.CharField(max_length=64)
    mirrorsuspended = models.CharField(max_length=64)
    redundancy = models.CharField(max_length=64)
    writecacheactual = models.CharField(max_length=64)
    writecache = models.CharField(max_length=64)
    vdisksecondarystate = models.CharField(max_length=64)
    mirrorcache = models.CharField(max_length=64)
    readcache = models.CharField(max_length=64)
    virtualdiskpresented = models.CharField(max_length=64)
    hosts = models.CharField(max_length=256)
    writeprotect = models.CharField(max_length=64)
    scvdenable = models.CharField(max_length=64)
    osunitid = models.CharField(max_length=64)
    diskgroupname = models.CharField(max_length=64)
    diskgroupid = models.CharField(max_length=64)
    preferredpath = models.CharField(max_length=64)
    restoreprogress = models.CharField(max_length=64)
    objectlockstate = models.CharField(max_length=64)
    hostaccess = models.CharField(max_length=64)


class EVAHost(models.Model):
    Storage = models.CharField(max_length=30)
    objectid = models.CharField(max_length=64)
    objectname = models.CharField(max_length=64)
    objecttype = models.CharField(max_length=64)
    objectwwn = models.CharField(max_length=64)
    objecthexuid = models.CharField(max_length=64)
    timestampmodify = models.CharField(max_length=64)
    hostname = models.CharField(max_length=64)
    uid = models.CharField(max_length=64)
    operationalstate = models.CharField(max_length=64)
    operationalstatedetail = models.CharField(max_length=64)
    objectparentuid = models.CharField(max_length=64)
    objectparenthexuid = models.CharField(max_length=64)
    comments = models.CharField(max_length=64)
    ipaddress = models.CharField(max_length=64)
    directeventing = models.CharField(max_length=64)
    osmode = models.CharField(max_length=64)
    osmodebitmask = models.CharField(max_length=64)
    hosttype = models.CharField(max_length=64)
    osmodeindex = models.CharField(max_length=64)
    presentations = models.CharField(max_length=64)
    WWNs = models.CharField(max_length=256)


class HDSHost(models.Model):
    Storage = models.CharField(max_length=30)
    Storage_Port = models.CharField(max_length=2)
    Name = models.CharField(max_length=64)
    Port_Name = models.CharField(max_length=32)
    Host_Group = models.CharField(max_length=64)


class HDSLU(models.Model):
    Storage = models.CharField(max_length=30)
    LU = models.CharField(max_length=32)
    Capacity = models.CharField(max_length=32)
    Stripe_Size = models.CharField(max_length=32)
    RAID_Group = models.CharField(max_length=32)
    DP_Pool = models.CharField(max_length=32)
    RAID_Level = models.CharField(max_length=32)
    Type = models.CharField(max_length=32)
    Number_of_Paths = models.CharField(max_length=32)
    Status = models.CharField(max_length=32)


class HDSMap(models.Model):
    Storage = models.CharField(max_length=30)
    Port = models.CharField(max_length=2)
    Group = models.CharField(max_length=32)
    H_LUN = models.CharField(max_length=3)
    LUN = models.CharField(max_length=3)


class Volume(models.Model):
    Storage = models.CharField(max_length=30)
    Uid = models.CharField(max_length=39)
    Name = models.CharField(max_length=64)
    Size = models.DecimalField(max_digits=8, decimal_places=2)
    Hosts = JSONField()


class VolumeChange(models.Model):
    From = models.DateTimeField()
    Till = models.DateTimeField()
    Storage = models.CharField(max_length=30)
    Uid = models.CharField(max_length=39)
    Name = models.CharField(max_length=64)
    Size = models.DecimalField(max_digits=8, decimal_places=2)
    Hosts = JSONField()
    Action = models.CharField(max_length=16)
    Action_Flag = models.CharField(max_length=16)
    Note = models.CharField(max_length=64)
    Acknowledged = models.BooleanField(default=False)
    User = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        ordering = ['-Till', 'Action',]


class Host(models.Model):
    Storage = models.CharField(max_length=30)
    Host = models.CharField(max_length=30)
    OS = models.CharField(max_length=30)
    WWNs = JSONField()


class HostCapacity(models.Model):
    Storage = models.CharField(max_length=30)
    Hosts = JSONField()
    Size = models.DecimalField(max_digits=8, decimal_places=2)

class HostCapacityHistory(models.Model):
    Storage = models.CharField(max_length=30)
    Hosts = JSONField()
    Size = models.DecimalField(max_digits=8, decimal_places=2)
    Date = models.DateField(auto_now_add=True)




class PDTypesCapacity(models.Model):
    Storage = models.CharField(max_length=64)
    Type = models.CharField(max_length=3)
    Size_MB = models.IntegerField()
    Volume_MB = models.IntegerField()
    Free_MB = models.IntegerField()
    Unavail_MB = models.IntegerField()
    Failed_MB = models.IntegerField()
    Spare_MB = models.IntegerField()


class PDTypesQuantity(models.Model):
    Storage = models.CharField(max_length=64)
    Type = models.CharField(max_length=3)
    MediaType = models.CharField(max_length=16)
    Capacity = models.IntegerField()
    RPM = models.IntegerField()
    Number = models.IntegerField()

