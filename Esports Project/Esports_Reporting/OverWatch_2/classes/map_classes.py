class Control_Map:
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
		self.mount_wins = 0
		self.mount_compositions = []
		self.opponent_compositions = []

	def add_mount_composition(self, comp):
		# Check if this exact composition already exists
		for existing_comp in self.mount_compositions:
			if (existing_comp.tank == comp.tank and 
				existing_comp.dps == comp.dps and
				existing_comp.support == comp.support):
				existing_comp.total += comp.total
				existing_comp.wins += comp.wins
				return
		# If not found, add the new composition
		self.mount_compositions.append(comp)

	def add_opponent_composition(self, comp):
		# Check if this exact composition already exists
		for existing_comp in self.opponent_compositions:
			if (existing_comp.tank == comp.tank and 
				existing_comp.dps == comp.dps and
				existing_comp.support == comp.support):
				existing_comp.total += comp.total
				existing_comp.wins += comp.wins
				return
		# If not found, add the new composition
		self.opponent_compositions.append(comp)
	
	@property
	def top_mount_composition(self):
		if self.mount_compositions:
			return max(self.mount_compositions, key=lambda x: (x.total, x.winrate), default=None)
	
	def top_opponent_composition(self):
		if self.opponent_compositions:
			return max(self.opponent_compositions, key=lambda x: (x.total, x.winrate), default=None)

	@property
	def mount_winrate(self):
		return (self.mount_wins / self.total) * 100 if self.total else 0
	
	@property
	def opponent_winrate(self):
		return ((self.total - self.mount_wins) / self.total) * 100 if self.total else 0

class Clash_Map:
	def __init__(self, name):
		self.name = name
		self.total = 1
		self.mount_wins = 0
		self.mount_compositions = []
		self.opponent_compositions = []
		self.A_point_win = 0
		self.B_point_win = 0
		self.C_point_win = 0
		self.D_point_win = 0
		self.E_point_win = 0
		
	def add_mount_composition(self, comp):
		# Check if this exact composition already exists
		for existing_comp in self.mount_compositions:
			if (existing_comp.tank == comp.tank and 
				existing_comp.dps == comp.dps and
				existing_comp.support == comp.support):
				existing_comp.total += comp.total
				existing_comp.wins += comp.wins
				return
		# If not found, add the new composition
		self.mount_compositions.append(comp)

	def add_opponent_composition(self, comp):
		# Check if this exact composition already exists
		for existing_comp in self.opponent_compositions:
			if (existing_comp.tank == comp.tank and 
				existing_comp.dps == comp.dps and
				existing_comp.support == comp.support):
				existing_comp.total += comp.total
				existing_comp.wins += comp.wins
				return
		# If not found, add the new composition
		self.opponent_compositions.append(comp)
	
	@property
	def top_mount_composition(self):
		if self.mount_compositions:
			return max(self.mount_compositions, key=lambda x: (x.total, x.winrate), default=None)
	
	def top_opponent_composition(self):
		if self.opponent_compositions:
			return max(self.opponent_compositions, key=lambda x: (x.total, x.winrate), default=None)

	@property
	def mount_winrate(self):
		return (self.mount_wins / self.total) * 100 if self.total else 0
	
	@property
	def opponent_winrate(self):
		return ((self.total - self.mount_wins) / self.total) * 100 if self.total else 0

class Flashpoint_Map:
	def __init__(self, name):
		self.name = name
		self.total = 1
		self.mount_wins = 0
		self.points = {}
	
	def add_point(self, point):
		if point not in self.points:
			self.points[point] = Point(point)
		else:
			self.points[point].total += 1

class Point:
	def __init__(self, name):
		self.name = name
		self.total = 1
		self.mount_wins = 0
		self.point_number = 0
		self.mount_compositions = []
		self.opponent_compositions = []
	
	def add_mount_composition(self, comp):
		# Check if this exact composition already exists
		for existing_comp in self.mount_compositions:
			if (existing_comp.tank == comp.tank and 
				existing_comp.dps == comp.dps and
				existing_comp.support == comp.support):
				existing_comp.total += comp.total
				existing_comp.wins += comp.wins
				return
		# If not found, add the new composition
		self.mount_compositions.append(comp)
	
	def add_opponent_composition(self, comp):
		# Check if this exact composition already exists
		for existing_comp in self.opponent_compositions:
			if (existing_comp.tank == comp.tank and 
				existing_comp.dps == comp.dps and
				existing_comp.support == comp.support):
				existing_comp.total += comp.total
				existing_comp.wins += comp.wins
				return
		# If not found, add the new composition
		self.opponent_compositions.append(comp)
	
	@property
	def top_mount_composition(self):
		if self.mount_compositions:
			return max(self.mount_compositions, key=lambda x: (x.total, x.winrate), default=None)
		
	@property
	def top_opponent_composition(self):
		if self.opponent_compositions:
			return max(self.opponent_compositions, key=lambda x: (x.total, x.winrate), default=None)
	
	@property
	def mount_winrate(self):
		return (self.mount_wins / self.total) * 100 if self.total else 0
	
	@property
	def opponent_winrate(self):
		return ((self.total - self.mount_wins) / self.total) * 100 if self.total else 0
	
class Push_Map:
	def __init__(self, name):
		self.name = name
		self.total = 1
		self.mount_wins = 0
		self.mount_distance = []
		self.opponent_distance = []
		self.mount_compositions = []
		self.opponent_compositions = []

	def add_mount_distance(self, distance):
		self.mount_distance.append(distance)
	
	def add_opponent_distance(self, distance):
		self.opponent_distance.append(distance)
	
	def add_mount_composition(self, comp):
		# Check if this exact composition already exists
		for existing_comp in self.mount_compositions:
			if (existing_comp.tank == comp.tank and 
				existing_comp.dps == comp.dps and
				existing_comp.support == comp.support):
				existing_comp.total += comp.total
				existing_comp.wins += comp.wins
				return
		# If not found, add the new composition
		self.mount_compositions.append(comp)
	
	def add_opponent_composition(self, comp):
		# Check if this exact composition already exists
		for existing_comp in self.opponent_compositions:
			if (existing_comp.tank == comp.tank and 
				existing_comp.dps == comp.dps and
				existing_comp.support == comp.support):
				existing_comp.total += comp.total
				existing_comp.wins += comp.wins
				return
		# If not found, add the new composition
		self.opponent_compositions.append(comp)
	
	@property
	def top_mount_composition(self):
		if self.mount_compositions:
			return max(self.mount_compositions, key=lambda x: (x.total, x.winrate), default=None)
		
	@property
	def top_opponent_composition(self):
		if self.opponent_compositions:
			return max(self.opponent_compositions, key=lambda x: (x.total, x.winrate), default=None)
	
	@property
	def mount_winrate(self):
		return (self.mount_wins / self.total) * 100 if self.total else 0
	
	@property
	def opponent_winrate(self):
		return ((self.total - self.mount_wins) / self.total) * 100 if self.total else 0
	
class Escort_Hybrid_Map:
	def __init__(self, name):
		self.name = name
		self.total = 1
		self.mount_wins = 0
		self.mount_attack_compositions = []
		self.mount_defense_compositions = []
		self.opponent_attack_compositions = []
		self.opponent_defense_compositions = []
	
	def add_mount_composition(self, comp, is_attack):
		if is_attack:
			# Check if this exact composition already exists
			for existing_comp in self.mount_attack_compositions:
				if (existing_comp.tank == comp.tank and 
					existing_comp.dps == comp.dps and
					existing_comp.support == comp.support):
					existing_comp.total += comp.total
					existing_comp.wins += comp.wins
					return
			# If not found, add the new composition
			self.mount_attack_compositions.append(comp)
		else:
			# Check if this exact composition already exists
			for existing_comp in self.mount_compositions:
				if (existing_comp.tank == comp.tank and 
					existing_comp.dps == comp.dps and
					existing_comp.support == comp.support):
					existing_comp.total += comp.total
					existing_comp.wins += comp.wins
					return
			# If not found, add the new composition
			self.mount_defense_compositions.append(comp)
	
	def add_opponent_composition(self, comp, is_attack):
		if is_attack:
			# Check if this exact composition already exists
			for existing_comp in self.mount_attack_compositions:
				if (existing_comp.tank == comp.tank and 
					existing_comp.dps == comp.dps and
					existing_comp.support == comp.support):
					existing_comp.total += comp.total
					existing_comp.wins += comp.wins
					return
			# If not found, add the new composition
			self.opponent_attack_compositions.append(comp)
		else:
			# Check if this exact composition already exists
			for existing_comp in self.mount_compositions:
				if (existing_comp.tank == comp.tank and 
					existing_comp.dps == comp.dps and
					existing_comp.support == comp.support):
					existing_comp.total += comp.total
					existing_comp.wins += comp.wins
					return
			# If not found, add the new composition
			self.opponent_defense_compositions_defense_compositions.append(comp)
	
	@property
	def top_mount_composition(self):
		if self.mount_compositions:
			return max(self.mount_compositions, key=lambda x: (x.total, x.winrate), default=None)
		
	@property
	def top_opponent_composition(self):
		if self.opponent_compositions:
			return max(self.opponent_compositions, key=lambda x: (x.total, x.winrate), default=None)
	
	@property
	def mount_winrate(self):
		return (self.mount_wins / self.total) * 100 if self.total else 0
	
	@property
	def opponent_winrate(self):
		return ((self.total - self.mount_wins) / self.total) * 100 if self.total else 0

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