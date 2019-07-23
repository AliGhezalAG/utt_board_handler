import re

class DataHandler():
	def __init__(self, scaleModes):
		self.record_packets = []
		self.packetsProcessed = False
		self.scaleModes = scaleModes

	def setRawData(self, rawData):
		self.rawData = rawData

	def getPackets(self):
		if self.packetsProcessed == False:
			self.processPackets()
		return (self.opening_packet, self.record_packets, self.closing_packet)

	def processPackets(self):
		self.processOpeningPacket()
		self.processRecordPackets()
		self.processClosingPacket()
		self.packetsProcessed = True

	def getIntValFromHex(self, hexVal):
		return int('0x'+hexVal, 0)

	def processOpeningPacket(self):
		raw_opening_packet = re.findall(r'5049.+?4950', self.rawData)[0]
		self.opening_packet = {
			"serial_number": self.getIntValFromHex(raw_opening_packet[4:12]),
			"sampling_frequency": self.getIntValFromHex(raw_opening_packet[12:14]),
			"frequency_unit": "Hz",
			"scale_mode": self.scaleModes[raw_opening_packet[14:16]],
			"version_number": self.getIntValFromHex(raw_opening_packet[16:18]),
			"battery_level": self.getIntValFromHex(raw_opening_packet[18:20]),
			"distance_between_X": self.getIntValFromHex(raw_opening_packet[20:24]),
			"distance_between_Y": self.getIntValFromHex(raw_opening_packet[24:28]),
			"distance_unit": "millisecond",
			"pressure_order": "[sensor 1, sensor 2, sensor 3, sensor 4]",
			"pressure_unit": "Newton"
		}

	def processRecordPackets(self):
		raw_record_packets = re.findall(r'504d.+?4d50', self.rawData)
		
		for packet in raw_record_packets:
			record_number = self.getIntValFromHex(packet[4:12])
			self.record_packets.append(
				{
					"record_number": record_number,
					"time_stamp": record_number / self.opening_packet["sampling_frequency"],
					"pressure": [	self.getIntValFromHex(packet[12:16]), 
									self.getIntValFromHex(packet[16:20]), 
									self.getIntValFromHex(packet[20:24]), 
									self.getIntValFromHex(packet[24:28])
								]
				}
			)

	def processClosingPacket(self):
		raw_closing_packet = re.findall(r'5052.+?5250', self.rawData)[0]
		self.closing_packet = {
			"records_number": self.getIntValFromHex(raw_closing_packet[4:12])
		}