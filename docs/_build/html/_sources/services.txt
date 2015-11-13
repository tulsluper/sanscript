****************************
  Services 
****************************

There are several additional services that can be run with SANscript 


Trap Receiver
=============
| Receives SNMP traps from switches;
| sends events to Event Server.

| Default socket - 0.0.0.0:162

Event Server
============
| Receives events from Trap Receiver;
| Runs comands or perform other actions.

| Default socket - 0.0.0.0:50501


