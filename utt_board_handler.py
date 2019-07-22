import bluetooth
from struct import *
import binascii
import time
import re
import json

scaleModes =	{
  "50": "Normal mode",
  "46": "Real-time mode"
}
timeout_val = 2 # in seconds

def getData():
	socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
	suffix = "5250".encode('utf-8');

	try : 
	    print ("connecting to the board...")
	    socket.connect(("94:21:97:60:14:D6", 1))
	    print ("connected!")
	except bluetooth.BluetoothError : raise

	try:
	    print ("Start acquisition...")
	    socket.send(bytes.fromhex('52 53'));
	    buffer = ""
	    timeout = time.time() + timeout_val
	    while True:
	        data = socket.recv(32)
	        hexlifyedData = binascii.hexlify(bytes(bytearray(data)))
	        buffer += hexlifyedData.decode('utf-8')
	        if hexlifyedData.endswith(suffix):
	            break
	        if time.time() > timeout:
	            socket.send(bytes.fromhex('53 50'));
	except IOError:
	    pass

	print ("Done!")
	socket.close()
	print ("disconnected")
	return buffer

def getPackets(buffer):
	opening_packet = getOpeningPacket(buffer)
	record_packets = getRecordPackets(buffer)
	closing_packet = getClosingPacket(buffer)
	return (opening_packet, record_packets, closing_packet)

def getOpeningPacket(buffer):
	opening_packet = re.findall(r'5049.+?4950', buffer)[0]
	my_opening_packet = {
		"serial_number": int('0x'+opening_packet[4:12], 0),
		"sampling_frequency": int('0x'+opening_packet[12:14], 0),
		"scale_mode": scaleModes[opening_packet[14:16]],
		"version_number": int('0x'+opening_packet[16:18], 0),
		"battery_level": int('0x'+opening_packet[18:20], 0),
		"distance_between_X": int('0x'+opening_packet[20:24], 0),
		"distance_between_Y": int('0x'+opening_packet[24:28], 0)
	}
	return my_opening_packet

def getRecordPackets(buffer):
	record_packets = re.findall(r'504d.+?4d50', buffer)
	my_record_packets = []
	for packet in record_packets:
		my_record_packets.append(
			{
				"record_number": int('0x'+packet[4:12], 0),
				"pressure_1": int('0x'+packet[12:16], 0),
				"pressure_2": int('0x'+packet[16:20], 0),
				"pressure_3": int('0x'+packet[20:24], 0),
				"pressure_4": int('0x'+packet[24:28], 0)
			}
		)
	return my_record_packets

def getClosingPacket(buffer):
	closing_packet = re.findall(r'5052.+?5250', buffer)[0]
	my_closing_packet = {
		"records_number": int('0x'+closing_packet[4:12], 0)
	}
	return my_closing_packet

def dumpResult(opening_packet, record_packets, closing_packet):
	opening_packet["records_number"] = closing_packet["records_number"]
	acquisition_data = {
		"general_infos" : opening_packet,
		"acquisitions" : record_packets
	}
	with open('result.json', 'w') as fp:
		json.dump(acquisition_data, fp)

def main():
	buffer = getData()
	opening_packet, record_packets, closing_packet = getPackets(buffer)
	dumpResult(opening_packet, record_packets, closing_packet)

if __name__ == "__main__":
	main()