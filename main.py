from output_handler import OutputHandler
from data_handler import DataHandler
from board_handler import BoardHandler
from gui_handler import GuiHandler

def main():
	scaleModes =	{
					  "50": "Normal mode",
					  "46": "Real-time mode"
					}

	board_handler = BoardHandler()
	data_handler = DataHandler(scaleModes)
	output_handler = OutputHandler()
	gui = GuiHandler(board_handler, data_handler, output_handler)
	gui.initWindow()

if __name__ == "__main__":
	main()