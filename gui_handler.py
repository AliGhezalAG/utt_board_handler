from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter.ttk import *
from tkinter import ttk
from tkinter import filedialog
import threading
from datetime import datetime

class GuiHandler:
	def __init__(self, board_handler, data_handler, output_handler):
		self.board_handler = board_handler
		self.data_handler = data_handler
		self.output_handler = output_handler

	def initWindow(self):
		# create a window
		self.window = Tk() 
		self.window.title("UTT board App")

		# set grid columns config
		self.window.grid_columnconfigure(index=0, weight=10, minsize=150)
		self.window.grid_columnconfigure(index=1, weight=10, minsize=150)
		self.window.grid_columnconfigure(index=2, weight=10, minsize=150)
		# self.window.grid_columnconfigure(index=3, weight=10, minsize=150)

		# set grid rows config
		self.window.grid_rowconfigure(index=0, weight=10, minsize=30)
		self.window.grid_rowconfigure(index=1, weight=10, minsize=30)
		self.window.grid_rowconfigure(index=2, weight=10, minsize=30)
		self.window.grid_rowconfigure(index=3, weight=10, minsize=30)
		self.window.grid_rowconfigure(index=4, weight=10, minsize=50)

		# step label
		self.step = StringVar()
		self.step.set("Board disconnected")
		step_label = Label(self.window, textvariable=self.step, font=("Arial", 10)) 
		step_label.grid(column=0, row=4, columnspan=3)

		# acquisition type selection
		# label
		acquisition_type_label = Label(self.window, text="Acquisition type", font=("Arial", 10)) 
		acquisition_type_label.grid(column=0, row=0, sticky=W) 

		# set possible values (Timed acquisition, Manual acquisition)		
		self.acquisition_type_value = StringVar()
		acquisition_type_combo = Combobox(self.window, textvariable = self.acquisition_type_value, state = 'readonly') 
		acquisition_type_combo['values']= ("Timed acquisition", "Manual acquisition")
		acquisition_type_combo.current(0) 
		acquisition_type_combo.grid(column=1, row=0, sticky=W)

		# acquisition length setting
		# label
		acquisition_length_label = Label(self.window, text="Acquisition length (s)", font=("Arial", 10)) 
		acquisition_length_label.grid(column=0, row=1, sticky=W) 

		# define entry to set value
		self.acquisition_length_value = Entry(self.window) 
		self.acquisition_length_value.grid(column=1, row=1, sticky=W)
		self.acquisition_length_value.focus()

		# output format selection
		self.output_format_value = StringVar()
		json_radio_button = Radiobutton(self.window,text = 'JSON', value = 'JSON', variable = self.output_format_value) 
		csv_radio_button = Radiobutton(self.window,text = 'CSV', value = 'CSV', variable = self.output_format_value) 
		txt_radio_button = Radiobutton(self.window,text = 'txt', value = 'TXT', variable = self.output_format_value)
		 
		json_radio_button.grid(column=0, row=2) 
		csv_radio_button.grid(column=1, row=2) 
		txt_radio_button.grid(column=2, row=2)

		# command buttons
		connect_btn = Button(self.window, text="Connect board", command = self.connect_btn_clicked)
		connect_btn.grid(column=0, row=3)

		# disconnect_btn = Button(self.window, text="Disconnect board", command = self.disconnect_btn_clicked)
		# disconnect_btn.grid(column=1, row=3)

		start_btn = Button(self.window, text="Start acquisition", command = self.start_btn_clicked)
		start_btn.grid(column=1, row=3)

		stop_btn = Button(self.window, text="Stop acquisition", command = self.stop_btn_clicked)
		stop_btn.grid(column=2, row=3, ipadx=10)

		self.window.mainloop()

	def connect_btn_clicked(self):
		self.board_handler.connect()
		self.step.set("Board connected")

	# def disconnect_btn_clicked(self):
	# 	self.board_handler.disconnect()

	def start_btn_clicked(self):
		if self.acquisition_type_value.get() == "Timed acquisition":
			self.processTimedAcquisition(float(self.acquisition_length_value.get()))
		else:
			t = threading.Thread(target=self.processNonTimedAcquisition)
			t.start()

	def processTimedAcquisition(self, timeout_val):
		self.board_handler.processTimedAcquisition(timeout_val)
		self.processRawData()
		self.step.set("Acquisition finished!")
		
	def processNonTimedAcquisition(self):
		self.step.set("Acquisition in progress... click on the stop button to finish it")
		self.board_handler.processNonTimedAcquisition()
		self.processRawData()
		self.step.set("Acquisition finished!")

	def stop_btn_clicked(self):
		self.board_handler.stopAcquisition()

	def processRawData(self):
		raw_data = self.board_handler.getRawData()
		self.data_handler.setRawData(raw_data)
		opening_packet, record_packets, closing_packet = self.data_handler.getPackets()
		self.output_handler.setPackets(opening_packet, record_packets, closing_packet)
		self.processOutput()
		self.board_handler.reset()

	def processOutput(self):
		now = datetime.now()
		dt_string = now.strftime("%Y-%m-%d-%Hh%M")

		if self.output_format_value.get() == "JSON":
			self.output_handler.getJsonOutput(dt_string)
		elif self.output_format_value.get() == "CSV":
			self.output_handler.getCsvOutput(dt_string)
		else:
			self.output_handler.getTxtOutput(dt_string)