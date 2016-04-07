from django.db import models

# ==============================================================================

class Connection(models.Model):
    name = models.CharField(max_length=30, unique=True)
    address = models.CharField(max_length=255, unique=True)

class Enclosure(models.Model):
    Location = models.CharField(max_length=64)
    Enclosure_Name = models.CharField(max_length=64)
    Enclosure_SN = models.CharField(max_length=64)
    
class Server(models.Model):
    Server_Bay = models.CharField(max_length=64)
    Server_NAME = models.CharField(max_length=64)
    Enclosure_Name = models.CharField(max_length=64)
    Power_state = models.CharField(max_length=64)
    Server_SN = models.CharField(max_length=64)
    Server_iLO = models.CharField(max_length=64)
    Server_Model = models.CharField(max_length=64)
    CPU_type = models.CharField(max_length=256)
    CPU_cores = models.CharField(max_length=64)
    CPU_count =models.CharField(max_length=64)
    RAM_size = models.CharField(max_length=64)


class Mezzanine(models.Model):
    Server_Bay = models.CharField(max_length=64)
    Mezz_Name = models.CharField(max_length=64)
    Enclosure_Name = models.CharField(max_length=64)
    Ports = models.CharField(max_length=300)
    Server_SN = models.CharField(max_length=64)

#{'Location': 5, 'Enclosure Name': 11, 'Enclosure SN': 10}
#{'Server Bay': 1, 'Server NAME': 17, 'Enclosure Name': 11, 'Power state': 3, 'Server SN': 10, 'Server iLO': 11, 'Server Model': 18}
#{'Server Bay': 1, 'Mezz Name': 55, 'Enclosure Name': 11, 'Ports': 4, 'Server SN': 10}



