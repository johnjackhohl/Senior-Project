class Control_Flashpoint_Map:
	def __init__(self, name):
		self.name = name
		self.sub_maps = {} # key: sub_map_name, value: SubMap object

	def add_sub_map(self, sub_map_name):
		if sub_map_name not in self.sub_maps:
			self.sub_maps[sub_map_name] = SubMap(sub_map_name)
		else:
			self.sub_maps[sub_map_name].total += 1


class SubMap:
	def __init__(self, name):
		self.name = name
		self.total = 1
		self.compositions = []

	def add_composition(self, comp):
		# Check if this exact composition already exists
		for existing_comp in self.compositions:
			if (existing_comp.tank == comp.tank and 
				existing_comp.dps == comp.dps and
				existing_comp.support == comp.support):
				existing_comp.total += comp.total
				existing_comp.wins += comp.wins
				return
		# If not found, add the new composition
		self.compositions.append(comp)
		
	def top_composition(self):
		 return max(self.compositions, key=lambda x: (x.total, x.winrate), default=None)

class Composition:
	def __init__(self, tank, dps, support):
		self.tank = tank
		self.dps = sorted(dps)  # Ensures DPS are in a consistent order
		self.support = sorted(support)  # Ensures supports are in a consistent order
		self.total = 0
		self.wins = 0

	@property
	def winrate(self):
		return (self.wins / self.total) * 100 if self.total else 0