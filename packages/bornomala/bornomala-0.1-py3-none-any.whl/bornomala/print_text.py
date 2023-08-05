from pathlib import Path

script_location = Path(__file__).absolute().parent
data_loc = script_location / "docs" / "data.txt"

def print_data(dec):
	if dec == "yes":
		with open(data_loc, encoding="utf-8") as data:
			for row in data:
				print(row)
	else:
		print("Nothing to Print")
		
