import json
import os

class OutputHandler():
	def __init__(self):
		if not os.path.exists("results\\json"):
			os.makedirs("results\\json")
		if not os.path.exists("results\\csv"):
			os.makedirs("results\\csv")
		if not os.path.exists("results\\txt"):
			os.makedirs("results\\txt")

	def setPackets(self, opening_packet, record_packets, closing_packet):
		self.opening_packet = opening_packet
		self.record_packets = record_packets
		self.closing_packet = closing_packet

	def getJsonOutput(self, dt_string):
		self.opening_packet["records_number"] = self.closing_packet["records_number"]
		acquisition_data = {
			"general_infos" : self.opening_packet,
			"acquisitions" : self.record_packets
		}
		with open("results/json/"+ dt_string + "-result.json", "w+") as fp:
			json.dump(acquisition_data, fp)

	def getCsvOutput(self, dt_string):
		file = open("results/csv/"+ dt_string + "-result.csv","w+")
		header = ["TIME_STAMP, \t", "SENSOR_1, \t", "SENSOR_2, \t", "SENSOR_3, \t", "SENSOR_4, \n"]
		file.writelines(header)

		for line in self.record_packets:
			line_values = [];
			line_values.append(str(line["time_stamp"])+ ", \t")
			for pressure_val in line["pressure"]:
				line_values.append(str(pressure_val)+ ", \t")
			line_values.append("\n")
			file.writelines(line_values)

		file.close()

	def getTxtOutput(self, dt_string):
		file = open("results/txt/"+ dt_string + "-result.txt","w+")
		header = ["TIME_STAMP \t", "SENSOR_1 \t", "SENSOR_2 \t", "SENSOR_3 \t", "SENSOR_4 \n"]
		file.writelines(header)

		for line in self.record_packets:
			line_values = [];
			line_values.append(str(line["time_stamp"])+ " \t")
			for pressure_val in line["pressure"]:
				line_values.append(str(pressure_val)+ " \t")
			line_values.append("\n")
			file.writelines(line_values)

		file.close()
