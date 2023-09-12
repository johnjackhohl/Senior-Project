def getHeros():
	with open("OverWatch_2\options\Tank.txt", "r") as tank_options:
		tanks = [line.strip() for line in tank_options]
	with open("OverWatch_2\options\DPS.txt", "r") as dps_options:
		dps = [line.strip() for line in dps_options]
	with open("OverWatch_2\options\Support.txt", "r") as support_options:
		support = [line.strip() for line in support_options]
	return [tanks, dps, support]

def getMaps(mapType):
	file_path = f"Overwatch_2/options/{mapType}_Maps.txt"
	with open(file_path, "r") as map_options:
		maps = [line.strip() for line in map_options]
	if(mapType == "Control"):
		with open("OverWatch_2\options\Control_Sub_Maps.txt", "r") as map_sub_options:
			subMaps = [line.strip() for line in map_sub_options]
		return maps, subMaps
	else:
		return maps