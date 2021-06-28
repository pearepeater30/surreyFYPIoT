# # # Code used to get the Device ID
# from network import LoRa
# import ubinascii
# import machine
#
# lora = LoRa()
# print("DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))
# #
# #
# # from network import WLAN
# # import binascii
# # wl = WLAN()
# # print(binascii.hexlify(wl.mac())[:6] + 'FFFE' + binascii.hexlify(wl.mac())[6:])
