#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

from network import LoRa
from machine import Pin, I2C
import socket
import binascii
import struct
import time
import config
import CCS811

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.US915)

# create an ABP authentication params
dev_addr = struct.unpack(">l", binascii.unhexlify('26021BDB'))[0]
nwk_swkey = binascii.unhexlify('E9A03143717AD90FA10960598EE73113')
app_swkey = binascii.unhexlify('AB7E6610BA39A9A0B53FEB05460A7C12')

i2c = I2C(0)
i2c = I2C(0, I2C.MASTER)
i2c = I2C(0, pins=('P9', 'P10'))
i2c.init(I2C.MASTER, baudrate=10000)

ccs = CCS811.CCS811(i2c=i2c)

# remove all the channels
for channel in range(0, 72):
    lora.remove_channel(channel)

# set all channels to the same frequency (must be before sending the OTAA join request)
for channel in range(0, 72):
    lora.add_channel(channel, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=3)

# join a network using ABP (Activation By Personalization)
lora.join(activation=LoRa.ABP, auth=(dev_addr, nwk_swkey, app_swkey))

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket non-blocking
s.setblocking(False)


# Data sent to the
while True:
    if ccs.data_ready():
        data = ccs.eCO2
        print(data)
        pkt = str(data)
        print('Sending:', pkt)
        s.send(pkt)
        time.sleep(4)
        
