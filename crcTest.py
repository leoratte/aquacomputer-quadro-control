#!/bin/python3
from crc import CrcCalculator, Configuration
import json

import quadro

'''finds all combinations off init_value and final_xor_value'''
q = quadro.Quadro()
q.importConfigHexDump("data/data5.txt")
data1 = bytes(q.data[:-2])
print(data1)
checksum1 = 0x28e9
print(checksum1)
# q.importConfigHexDump("data/data6.txt")
# data2 = bytes(q.data[:-2])
# print(data2)
# checksum2 = 0xd8e9
# print(checksum2)
# q.importConfigHexDump("data/data7.txt")
# data3 = bytes(q.data[:-2])
# print(data3)
# checksum3 = 0xb8e8
# print(checksum3)
# q.importConfigHexDump("data/data9")
# data1 = bytes(q.data[:-2])
# print(data1)
# checksum1 = 0x3bbf
# print(checksum1)
q.importConfigHexDump("data/data10")
data2 = bytes(q.data[:-2])
print(data2)
checksum2 = 0xcb5b
print(checksum2)
q.importConfigHexDump("data/data11")
data3 = bytes(q.data[:-2])
print(data3)
checksum3 = 0x6a90
print(checksum3)


width = 16
poly=0x8005
reverse_input=True
reverse_output=True
init_value=0x0000
final_xor_value=0x426A



for init_value in range(0xffff):
    final_xor_value=0x00
    configuration = Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
    use_table = False
    crc_calculator = CrcCalculator(configuration, use_table)
    checksum = crc_calculator.calculate_checksum(data1)
    final_xor_value= checksum ^ checksum1

    configuration = Configuration(width, poly, init_value, final_xor_value, reverse_input, reverse_output)
    use_table = False
    crc_calculator = CrcCalculator(configuration, use_table)
    checksum = crc_calculator.calculate_checksum(data2)

    if checksum == checksum2:
        checksum = crc_calculator.calculate_checksum(data3)
        if checksum == checksum3:


            print(init_value, final_xor_value)

    


