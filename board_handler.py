import bluetooth
from struct import *
import binascii
import time

class BoardHandler:
	def __init__(self):
		self.socket = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
		self.suffix = "5250".encode('utf-8')
		self.buffer = ""
		self.acquisitionStopped = False

	def connect(self):
		try : 
		    print ("connecting to the board...")
		    self.socket.connect(("94:21:97:60:14:D6", 1))
		    print ("connected!")
		except bluetooth.BluetoothError : raise
		return True

	def disconnect(self):
		self.socket.close()
		print ("disconnected")

	def startAcquisition(self):
		print ("Start acquisition...")
		self.socket.send(bytes.fromhex('52 53'))

	def stopAcquisition(self):
		print ("Stop acquisition...")
		self.socket.send(bytes.fromhex('53 50'))

	def getData(self):
		data = self.socket.recv(1024)
		hexlifyedData = binascii.hexlify(bytes(bytearray(data)))
		self.buffer += hexlifyedData.decode('utf-8')
		if hexlifyedData.endswith(self.suffix):
			self.acquisitionStopped = True

	def processTimedAcquisition(self, timeout_val):
		# self.connect()
		try:
		    self.startAcquisition()
		    timeout = time.time() + timeout_val
		    while True:
		        self.getData()
		        if self.acquisitionStopped:
		            break
		        if time.time() > timeout:
		            self.stopAcquisition()
		except IOError:
		    pass

	def processNonTimedAcquisition(self):
		try:
			self.startAcquisition()
			while True:
				self.getData()
				if self.acquisitionStopped:
					break
		except IOError:
			pass

	def getRawData(self):
		return self.buffer

	def reset(self):
		self.buffer = ""
		self.acquisitionStopped = False