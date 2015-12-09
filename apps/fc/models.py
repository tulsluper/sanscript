from django.db import models
from jsonfield import JSONField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


# ==============================================================================

def spacecheck(value):
    if ' ' in value:
        raise ValidationError('Field cannot contain spaces')

# ==============================================================================

class FabricConnection(models.Model):
    name = models.CharField(max_length=30, unique=True, validators=[spacecheck])
    address = models.CharField(max_length=256, unique=True)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'pk',]


class SwitchConnection(models.Model):
    name = models.CharField(max_length=30, unique=True, validators=[spacecheck])
    address = models.CharField(max_length=256, unique=True)
    username = models.CharField(max_length=40)
    password = models.CharField(max_length=40, null=True, blank=True)
    enabled = models.BooleanField(default=True)
    order = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['order', 'pk']

# ==============================================================================

class Serial(models.Model):
    Switch = models.CharField(max_length=30)
    Part_Num = models.CharField(max_length=13)
    Serial_Num = models.CharField(max_length=10)


class Version(models.Model):
    Switch = models.CharField(max_length=30)
    Kernel = models.CharField(max_length=8)
    Fabric_OS = models.CharField(max_length=7)
    Made_on = models.CharField(max_length=24)
    Flash = models.CharField(max_length=24)
    BootProm = models.CharField(max_length=6)


class Switch(models.Model):
    Switch = models.CharField(max_length=30)
    switchName = models.CharField(max_length=30)
    switchType = models.CharField(max_length=5)
    switchState = models.CharField(max_length=6)
    switchMode = models.CharField(max_length=19)
    switchRole = models.CharField(max_length=11)
    switchDomain = models.CharField(max_length=3)
    switchId = models.CharField(max_length=6)
    switchWwn = models.CharField(max_length=23)
    zoning = models.CharField(max_length=32)
    switchBeacon = models.CharField(max_length=3)
    FC_Router = models.CharField(max_length=3)
    FC_Router_BB_Fabric_ID = models.CharField(max_length=3)
    Address_Mode = models.CharField(max_length=1)


class SwitchCommon(models.Model):
    Switch = models.CharField(max_length=30)
    Fabric = models.CharField(max_length=30)
    switchType = models.CharField(max_length=5)
    switchMode = models.CharField(max_length=6)
    switchRole = models.CharField(max_length=11)
    Fabric_OS = models.CharField(max_length=7)
    Part_Num = models.CharField(max_length=13)
    Serial_Num = models.CharField(max_length=10)


class Port(models.Model):
    Switch = models.CharField(max_length=30)
    uPort = models.CharField(max_length=5)
    Index = models.CharField(max_length=4)
    Slot = models.CharField(max_length=2)
    Port = models.CharField(max_length=2)
    Address = models.CharField(max_length=6)
    Media = models.CharField(max_length=2)
    Speed = models.CharField(max_length=3)
    State = models.CharField(max_length=9)
    Proto = models.CharField(max_length=2)
    Type = models.CharField(max_length=6)
    Wwn = models.CharField(max_length=23)
    Comment = models.CharField(max_length=64)


class Portshow(models.Model):
    Switch = models.CharField(max_length=30)
    uPort = models.CharField(max_length=5)
    portIndex = models.CharField(max_length=4)
    portName = models.CharField(max_length=39)
    portHealth = models.CharField(max_length=100)
    Authentication = models.CharField(max_length=4)
    portDisableReason = models.CharField(max_length=26)
    portCFlags = models.CharField(max_length=3)
    portFlags = models.CharField(max_length=128)
    LocalSwcFlags = models.CharField(max_length=3)
    portType = models.CharField(max_length=4)
    POD_Port = models.CharField(max_length=32)
    portState = models.CharField(max_length=21)
    Protocol = models.CharField(max_length=2)
    portPhys = models.CharField(max_length=12)
    portScn = models.CharField(max_length=48)
    port_generation_number = models.CharField(max_length=8)
    state_transition_count = models.CharField(max_length=8)
    portId = models.CharField(max_length=6)
    portIfId = models.CharField(max_length=8)
    shareIfId = models.CharField(max_length=8)
    portWwn = models.CharField(max_length=23)
    Logical_portWwn = models.CharField(max_length=23)
    portWwn_of_devices_connected = JSONField()
    Distance = models.CharField(max_length=6)
    portSpeed = models.CharField(max_length=11)
    FEC = models.CharField(max_length=8)
    Credit_Recovery = models.CharField(max_length=8)
    Aoq = models.CharField(max_length=8)
    FAA = models.CharField(max_length=8)
    F_Trunk = models.CharField(max_length=8)
    LE_domain = models.CharField(max_length=1)
    FC_Fastwrite = models.CharField(max_length=3)


class PortCommon(models.Model):
    Switch = models.CharField(max_length=30)
    uPort = models.CharField(max_length=5)
    Index = models.CharField(max_length=4)
    Speed = models.CharField(max_length=3)
    State = models.CharField(max_length=9)
    Type = models.CharField(max_length=6)
    portWwn_of_devices_connected = JSONField()
    portName = models.CharField(max_length=39)
    Aliases = JSONField()


class Sfp(models.Model):
    Switch = models.CharField(max_length=30)
    uPort = models.CharField(max_length=5)
    Identifier = models.CharField(max_length=5)
    Connector = models.CharField(max_length=4)
    Transceiver = models.CharField(max_length=64)
    Encoding = models.CharField(max_length=8)
    Baud_Rate = models.CharField(max_length=24)
    Length_9u = models.CharField(max_length=20)
    Length_50u = models.CharField(max_length=20)
    Length_50u_OM2 = models.CharField(max_length=20)
    Length_50u_OM3 = models.CharField(max_length=20)
    Length_62u = models.CharField(max_length=20)
    Length_Cu = models.CharField(max_length=20)
    Vendor_Name = models.CharField(max_length=13)
    Vendor_OUI = models.CharField(max_length=8)
    Vendor_PN = models.CharField(max_length=16)
    Vendor_Rev = models.CharField(max_length=4)
    Wavelength = models.CharField(max_length=14)
    Options = models.CharField(max_length=64)
    BR_Max = models.CharField(max_length=1)
    BR_Min = models.CharField(max_length=1)
    Serial_No = models.CharField(max_length=15)
    Date_Code = models.CharField(max_length=8)
    DD_Type = models.CharField(max_length=4)
    Enh_Options = models.CharField(max_length=4)
    StatusCtrl = models.CharField(max_length=4)
    Pwr_On_Time = models.CharField(max_length=32)
    E_Wrap_Control = models.CharField(max_length=13)
    O_Wrap_Control = models.CharField(max_length=13)
    Temperature = models.CharField(max_length=17)
    Current = models.CharField(max_length=17)
    Voltage = models.CharField(max_length=17)
    RX_Power = models.CharField(max_length=17)
    TX_Power = models.CharField(max_length=17)
    State_transitions = models.CharField(max_length=3)
    Last_poll_time = models.CharField(max_length=28)


class Name(models.Model):
    Switch = models.CharField(max_length=30)
    Type = models.CharField(max_length=1)
    Pid = models.CharField(max_length=6)
    COS = models.CharField(max_length=3)
    PortName = models.CharField(max_length=23)
    NodeName = models.CharField(max_length=23)
    SCR = models.CharField(max_length=10)
    FC4s = models.CharField(max_length=64)
    PortSymb = models.CharField(max_length=128)
    NodeSymb = models.CharField(max_length=128)
    Fabric_Port_Name = models.CharField(max_length=23)
    Permanent_Port_Name = models.CharField(max_length=23)
    Device_type = models.CharField(max_length=34)
    Port_Index = models.CharField(max_length=4)
    Share_Area = models.CharField(max_length=3)
    Device_Shared_in_Other_AD = models.CharField(max_length=3)
    Redirect = models.CharField(max_length=3)
    Partial = models.CharField(max_length=3)
    LSAN = models.CharField(max_length=3)


class Alias(models.Model):
    Fabric = models.CharField(max_length=30)
    Name = models.CharField(max_length=30)
    Wwns = JSONField()


class Zone(models.Model):
    Fabric = models.CharField(max_length=30)
    Name = models.CharField(max_length=64)
    Aliases = JSONField()
    Wwns = JSONField()


class AliasStatus(models.Model):
    Fabric = models.CharField(max_length=30)
    Name = models.CharField(max_length=30)
    Wwns = JSONField()
    Status = models.CharField(max_length=8)


class ZoneStatus(models.Model):
    Fabric = models.CharField(max_length=30)
    Name = models.CharField(max_length=64)
    Aliases = JSONField()
    Status = models.CharField(max_length=8)


class Link(models.Model):
    Switch1 = models.CharField(max_length=30)
    Port1 = models.PositiveSmallIntegerField(blank=True, null=True)
    Switch2 = models.CharField(max_length=30)
    Port2 = models.PositiveSmallIntegerField(blank=True, null=True)
    Speed = models.PositiveSmallIntegerField(blank=True, null=True)
    TrunkId = models.PositiveSmallIntegerField(blank=True, null=True)
    Master = models.NullBooleanField()
    E_Trunk = models.NullBooleanField()
    F_Trunk = models.NullBooleanField()
    F_Link = models.NullBooleanField()
    Reverse = models.NullBooleanField()


class SwportAlias(models.Model):
    Swport = models.CharField(max_length=30)
    Aliases = JSONField()

class AliasSwport(models.Model):
    Alias = models.CharField(max_length=30)
    Swports = JSONField()

class PortRelation(models.Model):
    Port = models.CharField(max_length=30)
    Relation = JSONField()


class Path(models.Model):
    Node1 = models.CharField(max_length=30)
    Node2 = models.CharField(max_length=64)
    Treads = JSONField()
    Nodes = JSONField()
    Links = JSONField()


class Change(models.Model):
    From = models.DateTimeField()
    Till = models.DateTimeField()
    Fabric = models.CharField(max_length=30)
    Text = models.TextField()
    Data = models.TextField()
    Note = models.CharField(max_length=64)
    Acknowledged = models.BooleanField(default=False)
    User = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        ordering = ['-Till', 'Fabric',]


class Portlog(models.Model):
    switch = models.CharField(max_length=30)
    dt = models.DateTimeField()
    task = models.CharField(max_length=8)
    event = models.CharField(max_length=8)
    port = models.CharField(max_length=8)
    cmd = models.CharField(max_length=8)
    args = models.CharField(max_length=64)
#    class Meta:
#        ordering = ['-dt',]


class Fabriclog(models.Model):
    switch = models.CharField(max_length=30)
    dt = models.DateTimeField()
    action = models.CharField(max_length=64)
    S_P = models.CharField(max_length=8)
    Sn_Pn = models.CharField(max_length=8)
    Port = models.CharField(max_length=8)
    Xid = models.CharField(max_length=8)
#    class Meta:
#        ordering = ['-dt',]
