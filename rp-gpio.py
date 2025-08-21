class LED:
	def __init__(self, on=False, is_wall=False, is_door=False, is_key=False):
		self.light = ""

		self.on = on
		self.is_wall = is_wall
		self.is_door = is_door
		self.is_key = is_key

		if not self.is_wall and not self.is_door and not self.is_key:
			self.light = "●" if self.on else "◌"

		if not self.on:
			if self.is_wall:
				self.light = "○"
			elif self.is_door:
				self.light = "◎"
			elif self.is_key:
				self.light = "◉"

		def switch(self):
			self.on = not self.on
			self.light = "●" if self.on else "◌"

		def __str__(self):
			return self.light


class Level:
	def __init__(self):
		self.layout = [
			'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW',
			'WIIIIIIIIIIIIIIIIIIIIIIWIIIIIW',
			'WIIIIIIIIIWWWIIIIIIIIIIDIIIIIW',
			'WIIIIIIIIIIKWIIIIIIIIIIWIIIIIW',
			'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
		]

	def __str__(self):
		return "\n".join(self.layout)


wall = LED(is_wall=True)
player = LED(on=True)
inactive = LED(on=False)
key = LED(is_key=True)
door = LED(is_door=True)

level = Level()


print(level)

# print(wall, door, wall)
# print(wall, inactive, wall)
# print(wall, player, wall)
# print(wall, inactive, wall)
# print(wall, key, wall)
