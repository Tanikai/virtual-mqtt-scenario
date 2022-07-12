# MQTT Reference

## General MQTT Workflow

When a MQTT device communicates with a MQTT broker, *Control Packets* are sent
to each other. There are 15 types of Control Packets:

* CONNECT
* CONNACK
* PUBLISH
* PUBACK
* PUBREC
* PUBREL
* PUBCOMP
* SUBSCRIBE
* SUBACK
* UNSUBSCRIBE
* UNSUBACK
* PINGREQ
* PINGRESP
* DISCONNECT
* AUTH

[//]: # (Sequence Diagram of Packet Exchange between broker and device?)

## MQTT Control Packet structure

Line 390: Figure 2-1 Structure of an MQTT Control Packet

| Description                                           |
|-------------------------------------------------------|
| Fixed Header, present in all MQTT Control Packets     |
| Variable Header, present in some MQTT Control Packets |
| Payload, present in some MQTT Control Packets         |



Source: MQTT Version 5.0 OASIS Standard 07 March 2019